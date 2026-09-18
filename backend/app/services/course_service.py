from __future__ import annotations

import asyncio
import uuid

from sqlalchemy import select

from app.db import reset_db_for_tests, session_scope
from app.models.course import CourseRow
from app.schemas.course import CourseCreate, CourseRead


def _to_read(row: CourseRow) -> CourseRead:
    return CourseRead(id=row.id, title=row.title)


async def list_courses() -> list[CourseRead]:
    async with session_scope() as session:
        rows = (await session.execute(select(CourseRow).order_by(CourseRow.created_at))).scalars().all()
        return [_to_read(r) for r in rows]


async def create_course(body: CourseCreate) -> CourseRead:
    row = CourseRow(id=str(uuid.uuid4()), title=body.title)
    async with session_scope() as session:
        session.add(row)
        await session.flush()
        return _to_read(row)


async def get_course(course_id: str) -> CourseRead | None:
    async with session_scope() as session:
        row = await session.get(CourseRow, course_id)
        return _to_read(row) if row else None


async def update_course(course_id: str, new_title: str) -> CourseRead | None:
    async with session_scope() as session:
        row = await session.get(CourseRow, course_id)
        if not row:
            return None
        row.title = new_title
        await session.flush()
        return _to_read(row)


async def delete_course(course_id: str) -> bool:
    async with session_scope() as session:
        row = await session.get(CourseRow, course_id)
        if not row:
            return False
        await session.delete(row)
        return True


def clear_courses_for_tests() -> None:
    asyncio.run(reset_db_for_tests())
