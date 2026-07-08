# M04 · 数据与异步（队友 D）

## 目标

Redis 任务队列 + Worker 调度长任务。

## 目录

- `docker-compose.yml` — PG/Redis/MinIO
- `backend/app/workers/tasks.py` — Celery/RQ 入口

## 验收

- `docker compose up -d` 健康
- 提交转写任务后可查状态
