from fastapi import APIRouter, HTTPException
from app.schemas.job import JobCreate, JobRead
from app.services import job_service

router = APIRouter(prefix="/jobs", tags=["jobs"])

# 创建任务 POST /api/v1/jobs
@router.post("", response_model=JobRead)
async def create_job(body: JobCreate):
    return await job_service.create_job(body)

# 查询单个任务 GET /api/v1/jobs/{job_id}
@router.get("/{job_id}", response_model=JobRead)
async def get_single_job(job_id: str):
    job = await job_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="任务不存在")
    return job