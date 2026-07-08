# 创新路线 — 智学多模态 Agent

> 教育域独立项目；**MinIO + CDN 边缘缓存 + ASR/RAG** 为主创新链，与 ICU 项目零代码耦合。

## 总叙事

**课程多模态理解**：上传音视频 → 对象存储 → CDN 加速 → WhisperX ASR → 时间轴对齐 → pgvector RAG → Agent 问答。

## 分步里程碑

| 阶段 | 目标 | 交付物 | 依赖 |
|------|------|--------|------|
| **P0** ✓ | 工程骨架 | FastAPI + Vue + Docker(Redis/MinIO/PG) | — |
| **P1** | 媒体管线 | 上传 → MinIO 预签名 URL → 异步转写任务 | Redis worker |
| **P2** | CDN 分发 | 静态/媒体 URL 走 CDN 缓存策略（Cache-Control、回源 MinIO） | P1 |
| **P3** | RAG 问答 | pgvector 索引 + `answer_question()` 实现 | P1 |
| **P4** | Agent 工具层（可选） | MCP Tool `search_course_knowledge(query)` | P3 |

## 后期扩展空间

- **CDN**：热门课程片段边缘缓存，降低 MinIO 回源（与 2026 边缘 AI 存储趋势一致）
- **与 ICU 叙事互补**：同为「Agent + 可解释 + 标准工具接口」，答辩时可并列展示，无需代码集成
- **小程序端**：UniApp 消费 CDN URL + `/api` 后端

## 当前 Next

1. 实现 `transcription.py`（WhisperX 占位 → 真实 ASR）
2. MinIO bucket 初始化 + 上传 API 联调
3. Redis/Celery 或 BackgroundTasks 异步任务

## Docker

```powershell
docker compose up -d
# PG 5435 · Redis 6379 · MinIO 9000/9001
```

## 关联仓库

- ICU 决策/调度：临床域，无依赖
