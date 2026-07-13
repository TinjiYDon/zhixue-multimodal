# 负责人待办

## P0（你完成）

| 任务 | 文件 | 状态 |
|------|------|------|
| 上传 API | `endpoints/upload.py` + `services/storage.py` | ✅ presign + complete |
| 转写 schema | `schemas/transcript.py` | ✅ 供 C 对齐 |
| 问答 API | `endpoints/ask.py` + `services/agent.py` | ✅ RAG 占位 |
| 对齐服务 | `services/alignment.py` | ✅ 工具函数 + 占位 |
| API 路由注册 | `router.py` | ✅ upload + ask |
| RAG 正式版 | `agent.py` pgvector | ⏳ 等 C/D 转写入库 |
| review D PR | jobs/courses | ⏳ 待 D 提交 |

## 队友 D（业务 API，不再做 Docker 运维）

- `course_service.py` PostgreSQL 持久化  
- `endpoints/jobs.py` + `job_service.py`  
- `workers/tasks.py` 异步调度（调用 C 转写）  

## 联调顺序

1. Docker `docker compose up -d`  
2. 负责人：上传 → 触发 worker → 转写结果可查  
3. 负责人：alignment + RAG  
4. 队友：前端/小程序对接 API
