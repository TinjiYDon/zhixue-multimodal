from app.schemas.job import JobCreate, JobRead
from typing import Optional

# 内存存储任务列表
_job_storage: list[JobRead] = []

# 创建任务
async def create_job(body: JobCreate) -> JobRead:
    job_id = f"job_{len(_job_storage) + 1}"
    new_job = JobRead(
        job_id=job_id,
        course_id=body.course_id,
        media_key=body.media_key,
        status="pending",
        progress=0.0,
        result=None,
        error_msg=None
    )
    _job_storage.append(new_job)
    return new_job

# 根据job_id查询单个任务
async def get_job(job_id: str) -> Optional[JobRead]:
    for job in _job_storage:
        if job.job_id == job_id:
            return job
    return None