# zhixue-multimodal — AGENTS.md

> 给人 + AI Agent 的短 SSOT（≤150 行）。细节见 `docs/`。

## 一句话

多模态智学：上传课件 → Job/转写 → timeline/问答；栈 FastAPI + Vue + UniApp。

## 角色

| 角色 | GitHub | 目录 |
|------|--------|------|
| 负责人 | TinjiYDon | upload / alignment / agent / timeline |
| A 前端 | RynnYuan | `web/` |
| B 小程序 | oceancat91 | `miniapp/` |
| C 多媒体 | whq6830-arch | `backend/app/services/multimedia/` |
| D Job/Course | yucc280 | jobs / course_service PG / workers |

## 先读

1. `docs/TEAM_ASSIGNMENT.md`
2. `docs/BACKLOG.md`
3. `docs/STATUS` 类 / `TODO_OWNER.md`

## 命令

```powershell
docker compose up -d
cd backend
.\.venv\Scripts\python.exe -m pytest tests/ -q
# 或仓库外：d:\project\scripts\py.ps1 zhixue -m pytest tests/ -q
cd ..\web
npm install
npm run build
```

## API 契约（当前）

| 方法 | 路径 | 状态 |
|------|------|------|
| POST | `/api/v1/upload/presign` `/complete` | ✅ |
| GET/POST | `/api/v1/courses` | ✅ 内存 |
| GET/PATCH/DELETE | `/api/v1/courses/{id}` | ✅ 内存 CRUD |
| GET | `/api/v1/courses/{id}/timeline` | ✅ 占位 |
| POST | `/api/v1/courses/{id}/ask` | ✅ 占位 RAG |
| POST/GET | `/api/v1/jobs` | ✅ 内存骨架（D）；upload/complete 会自动建 job |

**禁止**：自造 `POST /api/v1/ask`（错误路径）。

## 禁改（非负责人）

- `agent.py` / `alignment.py` / upload 契约未经 Issue 批准

## PR 规则

- 用 PR 模板；写验收命令；`Closes #n`
- 多媒体必须对齐 `backend/app/schemas/transcript.py`
