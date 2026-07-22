from fastapi import APIRouter, HTTPException

from app.schemas.ask import AskRequest, AskResponse
from app.schemas.course import CourseCreate, CourseRead
from app.schemas.timeline import TimelineCue, TimelineResponse, TimelineSlide
from app.services import agent, course_service

router = APIRouter()


@router.get("", response_model=list[CourseRead])
async def list_courses():
    return await course_service.list_courses()


@router.post("", response_model=CourseRead)
async def create_course(body: CourseCreate):
    return await course_service.create_course(body)


@router.get("/{course_id}/timeline", response_model=TimelineResponse, tags=["timeline"])
async def get_course_timeline(course_id: str):
    """Structured timeline for web/miniapp. Placeholder until jobs persist transcripts."""
    return TimelineResponse(
        course_id=course_id,
        status="placeholder",
        duration_sec=120,
        cues=[
            TimelineCue(t_start=0, t_end=30, text="（占位）课程开场与学习目标"),
            TimelineCue(t_start=30, t_end=90, text="（占位）等待转写入库后替换为真实字幕"),
        ],
        slides=[
            TimelineSlide(page=1, t_start=0, title="封面（占位）"),
            TimelineSlide(page=2, t_start=30, title="要点（占位）"),
        ],
        message="等待 D jobs + C multimedia 写入后由 alignment 聚合真实 timeline",
    )


@router.get("/{course_id}", response_model=CourseRead)
async def get_single_course(course_id: str):
    course = await course_service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    return course


@router.patch("/{course_id}", response_model=CourseRead)
async def patch_course(course_id: str, body: CourseCreate):
    updated = await course_service.update_course(course_id, body.title)
    if not updated:
        raise HTTPException(status_code=404, detail="课程不存在")
    return updated


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
