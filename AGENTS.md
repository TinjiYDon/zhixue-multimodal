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
3. `docs/DEMO_E2E.md` · `docs/ROADMAP.md` · `docs/ROADMAP_EXEC.md`
4. `docs/WECHAT_COMPLIANCE.md`（**上架合规 Gate**）· `docs/ACCEPTANCE_MINIAPP.md`
5. `docs/TODO_OWNER.md`
6. `docs/BUGBOT.md`

## 上架合规 Gate（微信小程序）

- **禁止提审**直至 `docs/WECHAT_COMPLIANCE.md` Blocker（鉴权 B1、HTTPS B2、注销 B4 等）关闭。
- 健全性验收：`docs/ACCEPTANCE_MINIAPP.md`。
- 学习反馈飞轮默认关：`docs/DATA_FLYWHEEL.md`。
- 小程序隐私/协议页：`miniapp/src/pages/legal/`。

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
| POST | `/api/v1/auth/login` `/logout` · GET/DELETE `/auth/me` | ✅ 会话鉴权（上架 Gate） |
| POST | `/api/v1/upload/presign` `/complete` | ✅ **需登录** · 类型/大小限制 |
| GET/POST | `/api/v1/courses` | ✅ GET 公开 · POST 需登录 |
| GET/PATCH/DELETE | `/api/v1/courses/{id}` | ✅ 写需登录 |
| GET | `/api/v1/courses/{id}/timeline` | ✅ 占位 |
| POST | `/api/v1/courses/{id}/ask` | ✅ **需登录** |
| POST/GET | `/api/v1/jobs` | ✅ 创建需登录 |

**禁止**：自造 `POST /api/v1/ask`（错误路径）。  
**上架**：见 `docs/WECHAT_COMPLIANCE.md`；生产关闭 `AUTH_DEV_LOGIN`，配置微信 AppId/Secret 与 HTTPS 域名。

## 禁改（非负责人）

- `agent.py` / `alignment.py` / upload 契约未经 Issue 批准

## PR 规则

- 用 PR 模板；写验收命令；`Closes #n`
- 多媒体必须对齐 `backend/app/schemas/transcript.py`
