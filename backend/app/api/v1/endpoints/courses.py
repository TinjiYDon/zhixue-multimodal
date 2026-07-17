from fastapi import APIRouter

from app.schemas.ask import AskRequest, AskResponse
from app.schemas.course import CourseCreate, CourseRead
from app.services import agent, course_service

router = APIRouter()


@router.get("", response_model=list[CourseRead])
async def list_courses():
    return await course_service.list_courses()


@router.post("", response_model=CourseRead)
async def create_course(body: CourseCreate):
    return await course_service.create_course(body)


@router.post("/{course_id}/ask", response_model=AskResponse, tags=["ask"])
async def ask_course(course_id: str, body: AskRequest):
    answer, sources = await agent.answer_question(course_id, body.question)
    return AskResponse(course_id=course_id, answer=answer, sources=sources)
