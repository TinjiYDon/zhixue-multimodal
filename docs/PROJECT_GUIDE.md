# 智学多模态 · 项目指南

## 架构

```
miniapp (队友B) ──┐
web (队友A) ──────┼──► FastAPI (负责人) ──► PostgreSQL / Redis / MinIO
                  │         │
                  │    agent + alignment (负责人)
                  │         │
                  └── multimedia ASR/OCR (队友C) ◄── workers (队友D)
```

## 快速启动

```powershell
docker compose up -d          # PG 5435 / Redis / MinIO
cd backend && uvicorn app.main:app --reload
cd web && npm run dev
```

## 文档索引

| 文档 | 内容 |
|------|------|
| [COLLABORATION.md](COLLABORATION.md) | **5 人协作主手册** |
| [BACKLOG.md](BACKLOG.md) | 垂直切片任务 |
| [OWNER_VS_TEAM.md](OWNER_VS_TEAM.md) | 具体交付 |
| [TODO_OWNER.md](TODO_OWNER.md) | 负责人待办 |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | PR 规范 |

## 注意事项

- `web/node_modules/`、`backend/.venv/`、`web/dist/` 不入库  
- 队友模块只改各自 `TEAM_OWNER.md` 标注目录  
- API 契约以 `http://localhost:8000/docs` 为准

## GitHub

仓库：`TinjiYDon/zhixue-multimodal`（public）
