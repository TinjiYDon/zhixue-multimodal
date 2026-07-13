from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.schemas.upload import (
    UploadCompleteRequest,
    UploadCompleteResponse,
    UploadPresignRequest,
    UploadPresignResponse,
)
from app.services import storage

router = APIRouter()


@router.post("/presign", response_model=UploadPresignResponse)
async def create_upload_presign(body: UploadPresignRequest):
    media_key = storage.build_media_key(body.course_id, body.filename)
    try:
        upload_url = storage.presign_put_object(media_key)
    except Exception as exc:  # noqa: BLE001 — surface MinIO connectivity to client
        raise HTTPException(status_code=503, detail=f"MinIO unavailable: {exc}") from exc

    return UploadPresignResponse(
        media_key=media_key,
        upload_url=upload_url,
        bucket=settings.s3_bucket,
        expires_in=3600,
    )


@router.post("/complete", response_model=UploadCompleteResponse)
async def complete_upload(body: UploadCompleteRequest):
    expected_prefix = f"courses/{body.course_id}/"
    if not body.media_key.startswith(expected_prefix):
        raise HTTPException(status_code=400, detail="media_key does not match course_id")

    # Job creation stays in D's POST /jobs — upload only confirms object key for now.
    return UploadCompleteResponse(
        course_id=body.course_id,
        media_key=body.media_key,
        job_id=None,
        message="Upload registered. Teammate D: POST /api/v1/jobs with this media_key to start transcription.",
    )
