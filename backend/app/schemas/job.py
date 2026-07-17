from pydantic import BaseModel
from typing import Optional

# 创建任务传入参数
class JobCreate(BaseModel):
    course_id: str
    media_key: str

# 任务完整返回结构
class JobRead(BaseModel):
    job_id: str
    course_id: str
    media_key: str
    status: str  # pending / running / done / failed
    progress: Optional[float] = None
    result: Optional[str] = None
    error_msg: Optional[str] = None