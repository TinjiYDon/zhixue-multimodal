# Roadmap · zhixue-multimodal

> 更新：2026-09-13  
> 人读：下一版本 = 关 Issue / 审 PR / RAG / **微信上架合规 Gate** / 彩排。  
> AI：fixture 可测优先；未过 Z0 合规勿提审；飞轮默认关。

## Agent 上下文

```text
repo: zhixue-multimodal
vnext_p0: WECHAT_COMPLIANCE blockers B1 auth + B2 HTTPS; close issues #6 #7
vnext_p1: ACCEPTANCE_MINIAPP; pgvector RAG; MILE-4
vnext_p2: optional flywheel after audit pass; real WhisperX
ask_path: POST /api/v1/courses/{id}/ask
upload_sample: *.mp4
ship_gate: Z0 then Z1 then WeChat review
```

## 原则

1. 契约优先：timeline / ask / upload 路径稳定。
2. CI 与本地可用 fixture；GPU 模型可选。
3. 与 ICU 两仓无运行时耦合。
4. **上架顺序**：Z0 合规全绿 → Z1 健全性 → 提审；飞轮默认关。

## vNext

| 优先级 | 项 | 说明 |
|--------|----|------|
| **Z0** | 微信合规 | [WECHAT_COMPLIANCE.md](WECHAT_COMPLIANCE.md) · Blocker：鉴权/HTTPS/注销 |
| **Z1** | 小程序健全性 | [ACCEPTANCE_MINIAPP.md](ACCEPTANCE_MINIAPP.md) |
| P0 | 关闭或重写 #6 / #7 | 与 MILE-2 骨架对齐 |
| P0 | 审 PR #13 | 相对 main 增量与风险 |
| P1 | pgvector 正式 RAG | 替换 ask 占位 |
| P1 | 视频 ASR 准确度 | [VIDEO_OPTIMIZATION.md](VIDEO_OPTIMIZATION.md) V-P1；真机 A/B |
| P1 | MILE-4 | 端到端约 5 分钟答辩彩排 |
| P2 | 视频多模态增强 | V-P2：VAD / OCR slides / 双向对齐 |
| **Z-FLY** | 学习反馈飞轮 | [DATA_FLYWHEEL.md](DATA_FLYWHEEL.md) · **默认关** |

## 相关

- [CHANGELOG.md](CHANGELOG.md) · [PROGRESS.md](PROGRESS.md) · [ACCEPTANCE_ZHIXUE.md](ACCEPTANCE_ZHIXUE.md)
- [WECHAT_COMPLIANCE.md](WECHAT_COMPLIANCE.md) · [ACCEPTANCE_MINIAPP.md](ACCEPTANCE_MINIAPP.md) · [DATA_FLYWHEEL.md](DATA_FLYWHEEL.md)
- [VIDEO_OPTIMIZATION.md](VIDEO_OPTIMIZATION.md) · [VIDEO_TEST_REPORT_20260916.md](VIDEO_TEST_REPORT_20260916.md)
- [REPORT_OUTLINE.md](REPORT_OUTLINE.md)
