from __future__ import annotations

from app.schemas.job import JobCreate, JobRead, JobStatus

_job_storage: list[JobRead] = []


async def create_job(body: JobCreate) -> JobRead:
    job_id = f"job_{len(_job_storage) + 1}"
    new_job = JobRead(
        job_id=job_id,
        course_id=body.course_id,
        media_key=body.media_key,
        status="pending",
        progress=0.0,
        result=None,
        error_msg=None,
    )
    _job_storage.append(new_job)
    return new_job


async def get_job(job_id: str) -> JobRead | None:
    for job in _job_storage:
        if job.job_id == job_id:
            return job
    return None


async def update_job(
    job_id: str,
    *,
    status: JobStatus | None = None,
    progress: float | None = None,
    result: str | None = None,
    error_msg: str | None = None,
) -> JobRead | None:
    for idx, job in enumerate(_job_storage):
        if job.job_id != job_id:
            continue
        updated = job.model_copy(
            update={
                k: v
                for k, v in {
                    "status": status,
                    "progress": progress,
                    "result": result,
                    "error_msg": error_msg,
                }.items()
                if v is not None
            }
        )
        _job_storage[idx] = updated
        return updated
    return None


def clear_jobs_for_tests() -> None:
    _job_storage.clear()
