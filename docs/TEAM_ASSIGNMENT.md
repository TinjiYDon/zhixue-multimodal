# 分工说明

> **5 人协作**：详见 [`COLLABORATION.md`](COLLABORATION.md) · 任务 [`BACKLOG.md`](BACKLOG.md) · 规范 [`CONTRIBUTING.md`](../CONTRIBUTING.md)

| 成员 | 角色 | 目录 |
|------|------|------|
| **负责人** | 后端 API + Agent/RAG + **集成** | `backend/app/api/` `services/agent.py` `alignment.py` |
| **A** | Web Vue | `web/` |
| **B** | 小程序 | `miniapp/` |
| **C** | 多媒体 ASR/OCR | `backend/app/services/multimedia/` |
| **D** | Docker + Worker | `docker-compose.yml` `backend/app/workers/` |

## 模块归属

| 模块 | 目录 | 负责人 | 状态 |
|------|------|--------|------|
| M1 前端 Vue | `web/` | **队友 A** | 骨架页，待实现时间轴/PPT/笔记 |
| M2 小程序 | `miniapp/` | **队友 B** | 仅 README，需官方脚手架初始化 |
| M3 多媒体 | `backend/app/services/multimedia/` | **队友 C** | FFmpeg/WhisperX/OCR 占位 |
| M4 数据/运维 | `docker-compose.yml` + `backend/app/workers/` | **队友 D** | Redis/MinIO/PG 已编排，Worker 待实现 |
| M5 后端+智能 | `backend/app/services/agent.py` `alignment.py` + API | **负责人** | 待你实现 |
| M6 公共 API | `backend/app/api/` | **负责人** 定义契约，队友消费 | 已有 health/courses 占位 |

## 队友必读

- 各模块详细说明见 `docs/modules/M0x-*.md`
- 禁止修改 M5 业务逻辑，API 变更需与负责人对齐 OpenAPI
- 提交前：`pytest` / `npm run build`（各自模块）

## 负责人待完成

见 [`docs/TODO_OWNER.md`](TODO_OWNER.md)
