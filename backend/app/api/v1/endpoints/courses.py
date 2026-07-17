from fastapi import APIRouter, HTTPException
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

# 新增：获取单条课程
@router.get("/{course_id}", response_model=CourseRead)
async def get_single_course(course_id: str):
    course = await course_service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    return course

# 新增：修改课程
@router.patch("/{course_id}", response_model=CourseRead)
async def patch_course(course_id: str, body: CourseCreate):
    updated = await course_service.update_course(course_id, body.title)
    if not updated:
        raise HTTPException(status_code=404, detail="课程不存在")
    return updated

# 新增：删除课程
@router.delete("/{course_id}")
async def remove_course(course_id: str):
    ok = await course_service.delete_course(course_id)
    if not ok:
        raise HTTPException(status_code=404, detail="课程不存在")
    return {"msg": "删除成功"}

@router.post("/{course_id}/ask", response_model=AskResponse, tags=["ask"])
async def ask_course(course_id: str, body: AskRequest):
    answer, sources = await agent.answer_question(course_id, body.question)
    return AskResponse(course_id=course_id, answer=answer, sources=sources)
