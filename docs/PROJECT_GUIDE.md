# 智学多模态 · 项目指南

## 架构

```
miniapp (B) ──┐
web (A) ──────┼──► FastAPI ──► PostgreSQL / Redis / MinIO
              │      │
              │  负责人：upload / alignment / RAG
              │  D：courses / jobs API + Worker
              └── C：FFmpeg · WhisperX · OCR
```

## 文档入口

**全员先读：** [TEAM_ASSIGNMENT.md](TEAM_ASSIGNMENT.md)

## 快速启动

```powershell
docker compose up -d          # PG 5435 / Redis / MinIO
cd backend && uvicorn app.main:app --reload
cd web && npm run dev
```

## 当前 API（OpenAPI `/docs`）

| 方法 | 路径 | 状态 | 主责 |
|------|------|------|------|
| GET | `/api/v1/health` | ✅ | — |
| GET/POST | `/api/v1/courses` | ✅ 内存占位 | D → PG |
| POST | `/api/v1/upload/presign` | ✅ | 负责人 |
| POST | `/api/v1/upload/complete` | ✅ | 负责人 |
| POST | `/api/v1/courses/{id}/ask` | ✅ RAG 占位 | 负责人 |
| POST/GET | `/api/v1/jobs` | ⏳ | D |

转写/OCR 输出契约：`backend/app/schemas/transcript.py`

## 文档索引

| 文档 | 内容 |
|------|------|
| [TEAM_ASSIGNMENT.md](TEAM_ASSIGNMENT.md) | **分工总表 · 全员先读** |
| [COLLABORATION.md](COLLABORATION.md) | 联调、契约、周会 |
| [BACKLOG.md](BACKLOG.md) | 垂直切片任务 |
| [OWNER_VS_TEAM.md](OWNER_VS_TEAM.md) | 各角色交付 |

## 注意事项

- `web/node_modules/`、`backend/.venv/`、`web/dist/` 不入库  
- 队友模块只改各自 `TEAM_OWNER.md` 标注目录  
- API 契约以 `http://localhost:8000/docs` 为准

## GitHub

仓库：`TinjiYDon/zhixue-multimodal`（public）
