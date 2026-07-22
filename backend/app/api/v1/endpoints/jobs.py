from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.schemas.job import JobCreate, JobRead
from app.services import job_service
from app.workers.tasks import run_media_task

router = APIRouter()


@router.post("", response_model=JobRead)
async def create_job(body: JobCreate, background_tasks: BackgroundTasks):
    job = await job_service.create_job(body)
    background_tasks.add_task(run_media_task, job.job_id)
    return job


@router.get("/{job_id}", response_model=JobRead)
async def get_single_job(job_id: str):
    job = await job_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="任务不存在")
    return job
