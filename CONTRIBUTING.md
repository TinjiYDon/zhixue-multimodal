# 贡献指南 · 智学多模态（5 人）

## 团队

| 成员 | 角色 | 目录 | 模块 |
|------|------|------|------|
| **负责人** | 后端集成 + Agent/RAG + API 契约 | `backend/app/api/` `services/agent.py` `alignment.py` `course_service.py` | M5/M6 |
| **A** | Web 前端 | `web/` | M1 |
| **B** | 小程序 | `miniapp/` | M2 |
| **C** | 多媒体 | `backend/app/services/multimedia/` | M3 |
| **D** | 数据/异步 | `docker-compose.yml` `backend/app/workers/` | M4 |

完整手册：[`docs/COLLABORATION.md`](docs/COLLABORATION.md)  
分工交付：[`docs/OWNER_VS_TEAM.md`](docs/OWNER_VS_TEAM.md)

## 边界规则

1. **API 契约优先**：后端 OpenAPI（`/docs`）为前后端/小程序/Worker 唯一对接标准
2. **负责人**定义/变更 API；A/B/C/D **只消费**或实现约定 schema 的输入输出
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
- 标签：`api` `web` `miniapp` `multimedia` `worker` `infra` `bug` `blocked`

## 集成负责人

**负责人**兼任：合并 PR、维护 OpenAPI、组织联调顺序（见 COLLABORATION.md §5）
