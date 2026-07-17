# 五人协作手册 · zhixue-multimodal

> **分工总表（全员先读）：** [`TEAM_ASSIGNMENT.md`](TEAM_ASSIGNMENT.md)

## 1. 角色总览

```
miniapp (B) ──┐
web (A) ──────┼──► FastAPI + Agent (负责人) ──► PG / Redis / MinIO
              │              │
              │         alignment / RAG
              │              │
              └── multimedia (C) ◄── workers (D)
```

| 成员 | 读文档 | 交付核心 |
|------|--------|----------|
| **负责人** | TODO_OWNER.md | upload API、alignment、RAG、OpenAPI 审批 |
| **A** | M01 · web/TEAM_OWNER.md | 时间轴 + PPT + `/ask` |
| **B** | M02 · miniapp/TEAM_OWNER.md | 课程列表 + 问答入口 |
| **C** | M03 | FFmpeg + WhisperX + OCR JSON |
| **D** | M6 · [M05-backend-jobs-api.md](modules/M05-backend-jobs-api.md) | Job/Course API + PG + Worker |

## 2. 集成负责人（负责人）职责

- 维护 **OpenAPI** 为唯一契约（`http://localhost:8000/docs`）
- 合并跨模块 PR 前确认 schema 已通知 A/B/D
- 维护联调里程碑（见 BACKLOG）

## 3. 垂直切片（联调顺序）

| 阶段 | 切片 | 主责 | 协作者 | 验收 |
|------|------|------|--------|------|
| P0-1 | 基础设施 | ~~D~~ **已交付** | — | `docker compose up -d` 绿 |
| P0-2 | 上传 + 课程 CRUD | 负责人 + **D** | D | POST upload ✅；Course PG/API（D） |
| P0-3 | 转写 sample | C | D | mp4 → 带时间戳 JSON（WhisperX） |
| P0-4 | Job API + Worker | **D** | C | POST/GET `/jobs` + 队列调度 |
| P0-5 | 对齐 + RAG | 负责人 | C | 转写+OCR → 问答 API |
| P0-6 | Web 时间轴 | A | 负责人 | 播放 + 调 API |
| P0-7 | 小程序列表 | B | 负责人 | 列表 + 问答 |

任务 issue 化：[`BACKLOG.md`](BACKLOG.md)

## 4. 对接契约（比口头分工更重要）

| 契约 |  Owner | 说明 |
|------|--------|------|
| REST API | 负责人 | 路径、请求/响应 JSON |
| 转写结果 schema | 负责人 | `schemas/transcript.py` 已发布 |
| OCR 结果 schema | C 提议，负责人确认 | page, text, bbox |
| Job 状态 | D | pending / running / done / failed |
| MinIO 路径约定 | 负责人 | bucket/key 命名 |

**变更流程**：issue → 负责人更新 OpenAPI → @A @B @D 确认 → 再改代码

## 5. 周会（20 分钟）

1. D：Job API / Worker 进度  
2. C：WhisperX / 转写 blocker  
3. 负责人：API 变更、联调窗口  
4. A/B：前端对接进度  
5. 定 1 条「全链路可演示」切片

## 6. 调试分工

| 现象 | 先找 |
|------|------|
| 502 / 连不上 API | 全员查 docker compose → 负责人 |
| Course 重启丢数据 | D · course PG |
| POST /jobs 失败 | D |
| upload 失败 | 负责人 |
| 转写空/慢 | C → D 看 worker |
| 对齐/RAG 胡答 | 负责人 |
| 前端 CORS/代理 | A/B 看 vite 配置 + 负责人 API |

## 7. 答辩最低标准

见 [`OWNER_VS_TEAM.md`](OWNER_VS_TEAM.md) 验收表。

## 8. 相关

- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [TEAM_ASSIGNMENT.md](TEAM_ASSIGNMENT.md)
- [adr/001-api-contract-first.md](adr/001-api-contract-first.md)
