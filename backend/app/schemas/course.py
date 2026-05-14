from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)


class CourseCreate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: str
