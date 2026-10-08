# 给老师的创新口径 · zhixue-multimodal

> 2026-10-08 · 大创结项口径 · 每条都有实测或代码证据，不做无证据宣称
>
> 本仓与 icu-decision / icu-scheduling **零代码耦合**（见 `INNOVATION_ROADMAP.md`），
> 是教育域独立项目，可与 ICU 项目并列展示同构工程方法。

## 一句话

**把课堂音视频变成可检索、可追溯的时间轴知识，并且把「模型到底靠不靠谱」这件容易被糊过去的事，用实测数据讲清楚。**

## 不要这样讲

- 「RAG 已上线」——`/ask` 目前是**占位 RAG + sources**，`ACCEPTANCE_ZHIXUE.md` 自己记为「占位」。
- 「多模态优势已发挥」——课件侧 slides 目前**恒为 1 条占位**，PPT 图像尚未进入时间轴。
- 「转写准确率很高」——在没有基准集之前不要报百分比。`VIDEO_TEST_REPORT` 报的是段数、耗时、削波、术语错误**计数**，不是准确率。
- 把fixture 结果说成真实模型上线。

## 要这样讲

| 主张 | 证据 | 在哪 |
|---|---|---|
| 真实 CPU 可跑通音视频管线 | faster-whisper + CTranslate2 int8 通路，阻塞调用全走 `asyncio.to_thread` | `app/services/multimedia/transcription.py` |
| 结果可复现 | 线程数固定为 1 时段数与逐段文本完全一致，代价约慢 1.6 倍 | `VIDEO_TEST_REPORT` §对照实验 |
| 选型按证据不靠默认值 | base/small 分素材对照；升档不能默认更大 | `VIDEO_TEST_REPORT` §模型选型 |
| VAD 收益分场景 | 静音省 99.4%，语音密集反慢 11%，一刀切不可行 | 同上 |
| 工程边界有测试兜底 | `backend/tests` 30 passed | CI / 本地 |

## 底座 vs 深化（答辩一页）

| 层 | 是什么 | 对老师怎么说 |
|---|---|---|
| 底座 | FastAPI + Vue + UniApp + PG/Redis/MinIO | 可复现工程底座，不是卖点 |
| 深化 | 音视频转写 + 时间轴对齐 + 可复现性验证 | **可复现性**是本仓最硬的一条 |
| 尚未完成 | 正式 RAG、PPT 侧多模态、真人视频流 | 主动说清边界，不含糊 |

## 这份报告本身就是产出

`VIDEO_TEST_REPORT_20260916.md` 列出 8 条实测问题，其中第 1 条被标为**优先级最高**：

> 转写结果的随机性不会表现为报错，也不会立刻被察觉，但会让后续所有准确度评测与模型对比失去基准。

**这条判断本身就是可展示的方法论** —— 一个多媒体系统先证明自己「测得准」，再谈「做得好」。多数同类项目跳过了这一步。

## 演示台

```powershell
docker compose up -d
cd backend && .\.venv\Scripts\python.exe -m pytest tests/ -q   # 30 passed
```

ASR 复现实验见 `VIDEO_OPTIMIZATION.md`；视频侧结论见 `VIDEO_TEST_REPORT_20260916.md`。

## 交稿前要做的两件事

1. 把「转写不可复现」这条从「已知问题」升级为「已解决」并给出前后对比数据 —— 这是本仓最强的单点。
2. 小程序上架前走完 `WECHAT_COMPLIANCE.md` 的 Gate（域名白名单、隐私政策、类目审核）。