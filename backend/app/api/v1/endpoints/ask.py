from fastapi import APIRouter

from app.schemas.ask import AskRequest, AskResponse
from app.services import agent

router = APIRouter()


@router.post("/{course_id}/ask", response_model=AskResponse)
async def ask_course(course_id: str, body: AskRequest):
    answer, sources = await agent.answer_question(course_id, body.question)
    return AskResponse(course_id=course_id, answer=answer, sources=sources)
