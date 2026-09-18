# Progress · zhixue-multimodal

> 更新：2026-08-14  
> 人读：MILE 完成度与开放 Issue。  
> AI：以 [ROADMAP_EXEC.md](ROADMAP_EXEC.md) 与本文件为准；BACKLOG 勾选已对齐。

## Agent 上下文

```text
repo: zhixue-multimodal
product: classroom multimodal realtime Agent (timeline + ask)
stack: FastAPI + Vue3 + UniApp + PG/Redis/MinIO
mile1: done (Course/Job PG)
mile2: skeleton done (Web real API)
mile4: pending
acceptance: conditional_pass 2026-08-14
```

## 里程碑

| 里程碑 | 状态 | 证据 |
|--------|------|------|
| P0 多媒体 fixture | 完成 | PR #12 |
| MILE-1 Course/Job PG | 完成 | main · ROADMAP_EXEC |
| MILE-2 Web 真 API 骨架 | 完成（骨架） | main；Issue #7 未关 |
| MILE-3 miniapp 骨架 | 完成 | PR #11 |
| 正式 pgvector RAG | 未做 | Issue #6 |
| MILE-4 答辩彩排 | 未做 | BACKLOG |
| 人工验收 Step 3 | 有条件通过 | [ACCEPTANCE_ZHIXUE.md](ACCEPTANCE_ZHIXUE.md) |

## Issue / PR

- Open Issues：**#6**（alignment + RAG + ask）、**#7**（Web timeline + Q&A）。
- Open PR：**#13** `multimedia_new`。
- 上传格式：API **无白名单**；联调默认 **`mp4` / `video/mp4`**；下游依赖本机 ffmpeg。

## 下一冲刺

见 [ROADMAP.md](ROADMAP.md)。
