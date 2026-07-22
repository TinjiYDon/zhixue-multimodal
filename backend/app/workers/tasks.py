"""Background workers — teammate D (Redis/Celery later)."""

from __future__ import annotations

import inspect

from app.services import job_service


async def run_media_task(job_id: str) -> None:
    """Run multimedia pipeline for a job. Soft-fails if C API not ready."""
    job = await job_service.get_job(job_id)
    if not job:
        return

    await job_service.update_job(job_id, status="running", progress=0.2)

    try:
        from app.services.multimedia.transcription import transcribe_media

        # Prefer Worker contract; fall back if C still uses older signature.
        try:
            result = transcribe_media(job.job_id, job.media_key)
        except TypeError:
            result = transcribe_media(job.job_id)
        if inspect.isawaitable(result):
            result = await result
        await job_service.update_job(
            job_id,
            status="done",
            progress=1.0,
            result=str(result),
        )
    except Exception as exc:  # noqa: BLE001 — surface to job.error_msg
        await job_service.update_job(
            job_id,
            status="failed",
            error_msg=str(exc),
        )
