"""Background workers — 队友 D 实现 (Redis/Celery)."""

# TODO: Celery app / RQ worker 入口
# TODO: 调用 multimedia.transcription / agent 任务

import asyncio
from app.services import job_service
# C负责的多媒体转写函数
from app.services.multimedia.transcription import transcribe_media

async def run_media_task(job_id: str):
    # 1. 获取任务
    job = await job_service.get_job(job_id)
    if not job:
        return
    
    # 模拟修改状态为running
    job.status = "running"
    job.progress = 0.2

    try:
        # 调用C的转写函数
        transcript_result = await transcribe_media(job_id)
        # 转写成功，更新状态
        job.status = "done"
        job.progress = 1.0
        job.result = str(transcript_result)
    except Exception as e:
        # 异常标记失败
        job.status = "failed"
        job.error_msg = str(e)