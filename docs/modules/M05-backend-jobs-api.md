# M05 · 业务 API：课程持久化 + 任务 Job（队友 D）

> 原 M4「纯运维」已结案；D 主责 **FastAPI 接口 + 任务域**，Worker 为实现细节。

## 目录

| 路径 | 职责 |
|------|------|
| `backend/app/api/v1/endpoints/jobs.py` | 新建：提交/查询转写任务 |
| `backend/app/api/v1/endpoints/courses.py` | 扩展：GET/PATCH/DELETE（与负责人对齐） |
| `backend/app/services/job_service.py` | 新建：Job 状态 PG/Redis |
| `backend/app/services/course_service.py` | PostgreSQL 持久化（替代内存列表） |
| `backend/app/schemas/job.py` | JobCreate / JobRead / JobStatus |
| `backend/app/workers/tasks.py` | 消费队列，调用 C 的 `transcribe_media` |

## API 契约（负责人确认后实现）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/jobs` | body: `{ course_id, media_key }` → `{ job_id, status }` |
| GET | `/api/v1/jobs/{job_id}` | `{ status, progress?, result_url?, error? }` |
| GET | `/api/v1/courses/{id}` | 课程详情（含最新 job 状态，可选） |

Job 状态枚举：`pending` · `running` · `done` · `failed`（与 COLLABORATION §4 一致）

## 边界

| D 做 | D 不做 |
|------|--------|
| Job/Course CRUD API + PG 模型 | upload 预签名（负责人） |
| Worker 调度、写 Job 状态 | alignment / RAG / agent |
| 调用 C 的转写函数 | Whisper 模型与 FFmpeg 实现（C） |
| 在 router 注册 jobs（PR 由负责人 review） | 擅自改 OpenAPI 已发布字段 |

## 依赖

- `docker compose up -d`（全员自理，D 不再维护 compose）
- C 提供 `transcribe_media(job_id)` 可调用签名
- 负责人提供 MinIO `media_key` 约定、upload 触发 job 的联调窗口

## 验收

- [ ] Course 重启后数据仍在 PG
- [ ] POST job → GET 状态从 pending → done
- [ ] done 时 result 符合 C 与负责人确认的转写 JSON schema
- [ ] `/docs` 可见 jobs 路由
