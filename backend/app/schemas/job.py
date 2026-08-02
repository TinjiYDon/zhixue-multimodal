from typing import Literal, Optional

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
    progress: Optional[float] = Field(default=0.0, ge=0, le=1)
    result: Optional[str] = None
    error_msg: Optional[str] = None
