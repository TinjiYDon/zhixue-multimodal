# 智学多模态 Agent

5 人协作 · 仓库 [zhixue-multimodal](https://github.com/TinjiYDon/zhixue-multimodal)

**协作入口**：[`docs/COLLABORATION.md`](docs/COLLABORATION.md) · [`CONTRIBUTING.md`](CONTRIBUTING.md)

## 文档

**从 [`docs/TEAM_ASSIGNMENT.md`](docs/TEAM_ASSIGNMENT.md) 开始 · 分工见 [`docs/OWNER_VS_TEAM.md`](docs/OWNER_VS_TEAM.md)**

| 文档 | 说明 |
|------|------|
| [docs/TEAM_ASSIGNMENT.md](docs/TEAM_ASSIGNMENT.md) | 分工（先读） |
| [docs/PROGRESS.md](docs/PROGRESS.md) | 里程碑完成度 |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | 本仓变更 / Release |
| [docs/ROADMAP.md](docs/ROADMAP.md) | 下一版本 |
| [docs/ROADMAP_EXEC.md](docs/ROADMAP_EXEC.md) | MILE 执行记录 |
| [docs/BACKLOG.md](docs/BACKLOG.md) | P0 切片 |
| [docs/ACCEPTANCE_ZHIXUE.md](docs/ACCEPTANCE_ZHIXUE.md) | 人工验收报告 |
| [docs/REPORT_OUTLINE.md](docs/REPORT_OUTLINE.md) | 结项第 2–4 部分框架 |
| [docs/README.md](docs/README.md) | 文档索引 |

**Open**：Issues [#6](https://github.com/TinjiYDon/zhixue-multimodal/issues/6)、[#7](https://github.com/TinjiYDon/zhixue-multimodal/issues/7)；PR [#13](https://github.com/TinjiYDon/zhixue-multimodal/pull/13)。  
**上传样例格式**：联调默认 `mp4`（`video/mp4`）；API 当前无 MIME 白名单。

## 快速启动

```powershell
docker compose up -d
cd backend && uvicorn app.main:app --reload --port 8000
cd web && npm install && npm run dev
```

OpenAPI：`http://localhost:8000/docs`（含 upload / ask，详见 [`docs/PROJECT_GUIDE.md`](docs/PROJECT_GUIDE.md)）

```powershell
cd backend && .\.venv\Scripts\python.exe -m pytest tests/ -q   # 负责人 API smoke
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
