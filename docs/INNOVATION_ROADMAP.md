# 创新路线 — 智学多模态 Agent

> 教育域独立项目；**实时课堂管线**（上传→ASR/OCR→时间轴→RAG）为主创新链，与 ICU 项目**零代码耦合**。

## 总叙事

**课程多模态实时理解**：媒体流/任务流 → MinIO → WhisperX/OCR（契约 `schemas/transcript.py`）→ timeline → RAG 问答。

「实时」指课堂音视频与字幕/任务进度，**不接入 ICU 风险或床位模型**。投刊时可与 ICU Agent 并列展示同构工程方法。

## 分步里程碑

| 阶段 | 目标 | 交付物 |
|------|------|--------|
| **P0** ✓ | 工程骨架 | FastAPI + Vue + Docker |
| **P0-3** ✓ | 多媒体契约 | PR #12 · fixture 默认可测 |
| **MILE-3** ✓ | 小程序骨架 | PR #11 |
| **MILE-1** | Course/Job PG | D 一锤子（Issue #5） |
| **P3** | 正式 RAG | pgvector + LLM |

## 评测

schema/`course_id` 隔离；pytest；fixture ≠ 宣称真 Whisper 已上线。

## Docker（省盘）

```powershell
docker compose up -d
# PG 5435 · Redis 6379 · MinIO 9000；不用则 compose stop
```
