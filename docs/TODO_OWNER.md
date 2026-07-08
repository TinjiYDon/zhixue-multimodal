# 负责人待办

## P0（你完成）

| 任务 | 文件 | 说明 |
|------|------|------|
| 上传 API | `backend/app/api/v1/endpoints/upload.py` | 新建，MinIO 预签名 |
| 对齐服务 | `backend/app/services/alignment.py` | 转写 ↔ PPT 页级对齐 |
| RAG/Agent | `backend/app/services/agent.py` | pgvector + LLM 问答 |
| 课程域扩展 | `backend/app/services/course_service.py` | 持久化 PG，替代内存 |
| API 路由注册 | `backend/app/api/v1/router.py` | 挂载新 endpoints |

## 队友模块（仅验收）

- `web/` — 时间轴 UI  
- `miniapp/` — 小程序  
- `backend/app/services/multimedia/` — ASR/OCR/FFmpeg  
- `backend/app/workers/` — 异步任务  

## 联调顺序

1. Docker `docker compose up -d`  
2. 负责人：上传 → 触发 worker → 转写结果可查  
3. 负责人：alignment + RAG  
4. 队友：前端/小程序对接 API
