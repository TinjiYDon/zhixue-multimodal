from fastapi import APIRouter

from app.schemas.course import CourseCreate, CourseRead
from app.services import course_service

router = APIRouter()


@router.get("", response_model=list[CourseRead])
async def list_courses():
    return await course_service.list_courses()


@router.post("", response_model=CourseRead)
async def create_course(body: CourseCreate):
    return await course_service.create_course(body)
