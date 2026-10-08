"""Background workers — teammate D (Redis/Celery later)."""

from __future__ import annotations

import inspect

from app.core.config import settings
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
        try:
            from app.services import timeline_store

            # Real ASR dict → asr; fixture backend stays fixture. Do not invent content.
            await timeline_store.ingest_job_result_to_timeline(
                job.course_id,
                result,
                use_fixture_on_fail=False,
            )
        except Exception:
            pass
    except Exception as exc:  # noqa: BLE001 — surface to job.error_msg
        await job_service.update_job(
            job_id,
            status="failed",
            error_msg=str(exc),
        )
        try:
            from app.services import timeline_store

            if settings.timeline_fixture_on_job_fail:
                await timeline_store.ingest_job_result_to_timeline(
                    job.course_id, None, use_fixture_on_fail=True
                )
            else:
                # V-P0-3: failed job → empty timeline, not fake cues
                await timeline_store.ingest_job_result_to_timeline(
                    job.course_id,
                    None,
                    use_fixture_on_fail=False,
                    job_failed=True,
                    error_msg=str(exc),
                )
        except Exception:
            pass
