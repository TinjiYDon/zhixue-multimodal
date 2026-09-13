from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.api.deps import CurrentUser
from app.core.config import allowed_upload_content_types, settings
from app.schemas.job import JobCreate
from app.schemas.upload import (
    UploadCompleteRequest,
    UploadCompleteResponse,
    UploadPresignRequest,
    UploadPresignResponse,
)
from app.services import job_service, storage
from app.workers.tasks import run_media_task

router = APIRouter()


def _validate_upload_meta(content_type: str, size_bytes: int | None) -> None:
    allowed = allowed_upload_content_types()
    ct = (content_type or "").strip().lower()
    if ct not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的 content_type: {content_type}；允许: {sorted(allowed)}",
        )
    if size_bytes is not None and size_bytes > settings.upload_max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"文件过大: {size_bytes} > max {settings.upload_max_bytes} bytes",
        )


@router.post("/presign", response_model=UploadPresignResponse)
async def create_upload_presign(body: UploadPresignRequest, _user: CurrentUser):
    _validate_upload_meta(body.content_type, body.size_bytes)
    media_key = storage.build_media_key(body.course_id, body.filename)
    try:
        upload_url = storage.presign_put_object(media_key, content_type=body.content_type)
    except Exception as exc:  # noqa: BLE001 — surface MinIO connectivity to client
        raise HTTPException(status_code=503, detail=f"MinIO 不可用: {exc}") from exc

    return UploadPresignResponse(
        media_key=media_key,
        upload_url=upload_url,
        bucket=settings.s3_bucket,
        expires_in=3600,
        content_type=body.content_type,
        max_bytes=settings.upload_max_bytes,
    )


@router.post("/complete", response_model=UploadCompleteResponse)
async def complete_upload(
    body: UploadCompleteRequest,
    background_tasks: BackgroundTasks,
    _user: CurrentUser,
):
    expected_prefix = f"courses/{body.course_id}/"
    if not body.media_key.startswith(expected_prefix):
        raise HTTPException(status_code=400, detail="media_key 与 course_id 不匹配")

    try:
        exists = storage.object_exists(body.media_key)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"MinIO 不可用: {exc}") from exc

    if not exists:
        raise HTTPException(
            status_code=400,
            detail="对象尚未上传到 MinIO，请先 PUT 到 presign 返回的 upload_url",
        )

    job = await job_service.create_job(
        JobCreate(course_id=body.course_id, media_key=body.media_key)
    )
    background_tasks.add_task(run_media_task, job.job_id)

    return UploadCompleteResponse(
        course_id=body.course_id,
        media_key=body.media_key,
        job_id=job.job_id,
        message="上传已确认，已创建转写任务（C 未就绪时 job 可能为 failed）。",
    )
