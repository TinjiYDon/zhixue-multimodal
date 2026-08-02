# zhixue · PR 审阅清单（契约守卫）

> 2026-08-02 · ICU 忙时并行最低保障：审 PR + 契约，不深挖 RAG

## 必须对齐

| 项 | 期望 |
|----|------|
| Ask 路径 | `POST /api/v1/courses/{id}/ask`（禁止 `/api/v1/ask`） |
| Timeline | `GET /api/v1/courses/{id}/timeline` |
| Fixture | `POST /api/v1/courses/{id}/timeline/from-fixture` |
| 转写契约 | `schemas/transcript.py` / 仓库约定 schema，勿另起字段名 |
| 依赖位置 | 后端依赖在 `backend/`；勿把巨型 sample 媒体提交进 Git |
| 测试 | `cd backend && pytest tests/ -q` 绿；缺外服时用 fixture fallback |

## 多媒体 PR 红线（对照 PR #12）

- [ ] 无超大二进制 / 课堂录像进库  
- [ ] request schema 与 OpenAPI 一致  
- [ ] job 状态机不破坏 Course/Job PG（MILE-1）  
- [ ] Web/小程序若改 API，同步 `web/src/api/client.ts` 与 miniapp api  

## Owner 并行节奏

| 带宽 | 动作 |
|------|------|
| ICU 平台占满 | 只做本清单 + 评论 PR |
| 有空档 | Web `CourseView` 接真 timeline/ask（#7） |
| 转写入库后 | #6 pgvector 正式 RAG |
