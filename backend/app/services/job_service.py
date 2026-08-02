from __future__ import annotations

import asyncio
import uuid

from app.db import reset_db_for_tests, session_scope
from app.models.job import JobRow
from app.schemas.job import JobCreate, JobRead, JobStatus


def _to_read(row: JobRow) -> JobRead:
    return JobRead(
        job_id=row.job_id,
        course_id=row.course_id,
        media_key=row.media_key,
        status=row.status,  # type: ignore[arg-type]
        progress=row.progress,
        result=row.result,
        error_msg=row.error_msg,
    )


async def create_job(body: JobCreate) -> JobRead:
    row = JobRow(
        job_id=f"job_{uuid.uuid4().hex[:12]}",
        course_id=body.course_id,
        media_key=body.media_key,
        status="pending",
        progress=0.0,
    )
    async with session_scope() as session:
        session.add(row)
        await session.flush()
        return _to_read(row)


async def get_job(job_id: str) -> JobRead | None:
    async with session_scope() as session:
        row = await session.get(JobRow, job_id)
        return _to_read(row) if row else None


async def update_job(
    job_id: str,
    *,
    status: JobStatus | None = None,
    progress: float | None = None,
    result: str | None = None,
    error_msg: str | None = None,
) -> JobRead | None:
    async with session_scope() as session:
        row = await session.get(JobRow, job_id)
        if not row:
            return None
        if status is not None:
            row.status = status
        if progress is not None:
            row.progress = progress
        if result is not None:
            row.result = result
        if error_msg is not None:
            row.error_msg = error_msg
        await session.flush()
        return _to_read(row)


def clear_jobs_for_tests() -> None:
    asyncio.run(reset_db_for_tests())
