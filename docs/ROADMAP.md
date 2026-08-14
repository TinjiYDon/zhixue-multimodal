# Roadmap · zhixue-multimodal

> 更新：2026-08-14  
> 人读：下一版本优先关 Issue / 审 PR / 正式 RAG / 彩排。  
> AI：fixture 可测优先；真 WhisperX 为本机增强，勿碎 PR。

## Agent 上下文

```text
repo: zhixue-multimodal
vnext_p0: close_or_rewrite issues #6 #7; review PR #13
vnext_p1: pgvector RAG; MILE-4 demo rehearsal
vnext_p2: real WhisperX on owner machine
ask_path: POST /api/v1/courses/{id}/ask
upload_sample: *.mp4
```

## 原则

1. 契约优先：timeline / ask / upload 路径稳定。
2. CI 与本地可用 fixture；GPU 模型可选。
3. 与 ICU 两仓无运行时耦合。

## vNext

| 优先级 | 项 | 说明 |
|--------|----|------|
| P0 | 关闭或重写 #6 / #7 | 与 MILE-2 骨架对齐验收标准 |
| P0 | 审 PR #13 | 相对 #12 / main 的增量与风险 |
| P1 | pgvector 正式 RAG | 替换 ask 占位 |
| P1 | MILE-4 | 端到端约 5 分钟答辩彩排 |
| P2 | 真 WhisperX | C 本机验证，勿再开碎 PR |
| P2 | 上传 MIME 白名单（可选） | 若产品要求「仅 mp4」再在 presign 校验 |

## 相关

- [CHANGELOG.md](CHANGELOG.md) · [PROGRESS.md](PROGRESS.md) · [ACCEPTANCE_ZHIXUE.md](ACCEPTANCE_ZHIXUE.md)
- [REPORT_OUTLINE.md](REPORT_OUTLINE.md)（结项第 2–4 部分填空框架）
