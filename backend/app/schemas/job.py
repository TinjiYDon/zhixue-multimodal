from typing import Literal

from pydantic import BaseModel, Field

JobStatus = Literal["pending", "running", "done", "failed"]


class JobCreate(BaseModel):
    course_id: str
    media_key: str


class JobRead(BaseModel):
    job_id: str
    course_id: str
    media_key: str
    status: JobStatus = "pending"
    progress: float | None = Field(default=0.0, ge=0, le=1)
    result: str | None = None
    error_msg: str | None = None
