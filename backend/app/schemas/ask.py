from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


class AskResponse(BaseModel):
    course_id: str
    answer: str
    sources: list[str] = Field(default_factory=list)
