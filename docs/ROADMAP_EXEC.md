# 执行路线图 ROADMAP_EXEC

> 更新：2026-08-02 · 课堂实时多模态 Agent · 与 ICU 零耦合

## 人读摘要

| Wave | 含义 | 状态 |
|------|------|------|
| Wave3 / MILE-3 | fixture timeline + miniapp | ✅ |
| P0-3 多媒体 | schema + ffmpeg/OCR/ASR 接口 | ✅ PR #12 |
| MILE-1 | Course/Job PG | ⏳ D（#5） |

## Agent 上下文

```text
实时：媒体/字幕/任务流；非 ICU
验收：cd backend && pytest tests/ -q
ZHIXUE_ASR_BACKEND=fixture 用于 CI
下一步：D 一次 PR 落 PG（见 Issue #5）
```
