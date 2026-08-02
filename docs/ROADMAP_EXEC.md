# 执行路线图 ROADMAP_EXEC（人机双可读）

> 更新：2026-08-02 · **PR #12 已合**（Owner 一次修完多媒体契约）· PR #1 已关闭 · 下一步 MILE-1（D PG + 真转写）

## 人读摘要

| Wave | 含义 | 状态 |
|------|------|------|
| ICU Wave1/2 | 见 decision/scheduling 仓 | 独立 |
| **Wave3（本仓）** | job→timeline fixture 钩子 | ✅ 骨架 |
| **MILE-3** | 小程序列表/问答骨架 | ✅ PR #11 |
| **P0-3 多媒体** | schema + ffmpeg/OCR/ASR 接口 | ✅ PR #12（fixture 默认可测；真 WhisperX 可选） |
| MILE-1 | D PG + 真媒体入库 | ⏳ D 主责 |

**本仓无监督训练集划分（N/A）。** 质量靠 schema + course_id 隔离。

## Agent 上下文

```text
多媒体：transcribe_media / run_ocr → schemas/transcript.py
CI/演示：ZHIXUE_ASR_BACKEND=fixture · ZHIXUE_OCR_BACKEND=fixture
真引擎：pip install -r backend/requirements-multimedia.txt
验收：cd backend && pytest tests/ -q
禁止：自定义 raw_text OCR 契约；大媒体入仓
```

## 并行队友（一锤子）

- [ ] D：Course/Job **落 PG** + Worker 调 `transcribe_media(job_id, media_key)`（#5）
- [ ] A：Web 接真实 timeline/ask（#7）
- [ ] C：可选 — 本机装 WhisperX，用真实 sample 跑通并贴 JSON 样例到 Issue #4（**勿再开碎 PR**）
- [x] B：小程序骨架（PR #11）
