# 贡献指南 · 智学多模态（5 人）

## 团队

| 成员 | 角色 | 目录 | 模块 |
|------|------|------|------|
| **负责人** | 上传 + alignment + RAG + OpenAPI 审批 | `upload.py` `agent.py` `alignment.py` | M5 |
| **A** | Web 前端 | `web/` | M1 |
| **B** | 小程序 | `miniapp/` | M2 |
| **C** | 多媒体 WhisperX/OCR | `backend/app/services/multimedia/` | M3 |
| **D** | Job/Course API + Worker + PG | `jobs.py` `job_service.py` `course_service.py` `workers/` | M6 |

**全员先读：** [`docs/TEAM_ASSIGNMENT.md`](docs/TEAM_ASSIGNMENT.md)

## 边界规则

1. **API 契约优先**：后端 OpenAPI（`/docs`）为前后端/小程序/Worker 唯一对接标准
2. **负责人**定义/审批 API；A/B 消费 REST；C 产出 JSON schema；D 实现 jobs/courses
3. **禁止**队友修改 `agent.py` / `alignment.py` 核心逻辑（需求开 issue @负责人）
4. 各模块只改各自 `OWNER.md` / `TEAM_OWNER.md` 标注目录

## 合并门槛

| 模块 | 验证 |
|------|------|
| backend | `cd backend && pytest` |
| web | `cd web && npm run build` |
| worker/multimedia | 模块 README 中命令 |
| docker | `docker compose config` |

## PR / Issue

- [PR 模板](.github/pull_request_template.md)
- 任务：[`docs/BACKLOG.md`](docs/BACKLOG.md)
- 标签：`api` `web` `miniapp` `multimedia` `jobs` `worker` `bug` `blocked`

## 集成负责人

**负责人**兼任：合并 PR、维护 OpenAPI、组织联调顺序（见 COLLABORATION.md §5）
