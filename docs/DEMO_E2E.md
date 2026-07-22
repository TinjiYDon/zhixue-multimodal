# 全链路 Demo 说明（#P0-5c）

> 更新：2026-07-22 · 负责人

## 人读摘要

| 项 | 内容 |
|----|------|
| Owner | 负责人 TinjiYDon |
| 目标 | 说明当前可演示边界与联调缺口 |
| 依赖 | D PG · C 多媒体 · A 接 API |
| 里程碑 | `#MILE-1` 未达成 |

## 当前可跑

| 步骤 | 命令 / 路径 | 预期 |
|------|-------------|------|
| 基建 | `docker compose up -d` | PG:5435 Redis MinIO |
| 测试 | `cd backend` → `.\.venv\Scripts\python.exe -m pytest tests/ -q` | ≥10 passed |
| 健康 | `GET /api/v1/health` | ok |
| 课程 | `POST/GET /api/v1/courses` | **内存**（重启丢失） |
| 上传 | `POST /upload/presign` + PUT + `/complete` | complete 会 **自动建 job** |
| Job | `POST/GET /api/v1/jobs` | 内存；Worker 调转写 |
| Timeline | `GET /courses/{id}/timeline` | **占位**字幕/PPT |
| Ask | `POST /courses/{id}/ask` | 内存 RAG + CJK 占位 |
| Web | `cd web && npm run dev` | UI 已合（PR #9）；数据仍 **mock** |

## 已知缺口（答辩前须清）

| 缺口 | Owner | Issue |
|------|-------|-------|
| WhisperX/OCR 对齐 schema | C | #4 · PR #1 request-changes |
| Course/Job **PostgreSQL** + 队列 | D | #5 · `#P0-2b` `#P0-4c` |
| 真实 timeline / RAG 灌库 | 负责人 | 等 C/D · `#P0-5b+` |
| Web 接真实 API | A | #7 · `#P0-6d` |
| 小程序 | B | #8 |

C 未实现时：Worker 将 job 标为 `failed`（`NotImplementedError`）——**属预期**，不是 upload 坏了。

## 联调顺序

见 [`TEAM_ASSIGNMENT.md`](TEAM_ASSIGNMENT.md) §五 → `#MILE-1`：D PG + C 转写 + 负责人 alignment/RAG。

## Agent 上下文

```text
验收：d:\project\scripts\py.ps1 zhixue -m pytest tests/ -q
契约：ask = POST /api/v1/courses/{id}/ask（禁止 /api/v1/ask）
timeline = GET /api/v1/courses/{id}/timeline
jobs = POST/GET /api/v1/jobs；upload/complete 自动 create_job
禁改：agent/alignment/upload 契约未经 Issue
Bugbot：docs/BUGBOT.md
```
