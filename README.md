# 智学多模态 Agent

5 人协作 · 仓库 [zhixue-multimodal](https://github.com/TinjiYDon/zhixue-multimodal)

**协作入口**：[`docs/COLLABORATION.md`](docs/COLLABORATION.md) · [`CONTRIBUTING.md`](CONTRIBUTING.md)

## 文档

**从 [`docs/PROJECT_GUIDE.md`](docs/PROJECT_GUIDE.md) 开始 · 分工见 [`docs/OWNER_VS_TEAM.md`](docs/OWNER_VS_TEAM.md)**

## 快速启动

```powershell
docker compose up -d
cd backend && uvicorn app.main:app --reload --port 8000
cd web && npm install && npm run dev
```

## 目录

```
backend/     # FastAPI（负责人：API + Agent/RAG）
web/         # Vue 3（队友 A）
miniapp/     # UniApp（队友 B）
docker-compose.yml
docs/
```

## 技术栈

FastAPI · Vue 3 · UniApp · PostgreSQL · Redis · MinIO · WhisperX/RAG（规划）
