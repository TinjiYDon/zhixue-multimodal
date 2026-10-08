# 任务 Backlog（五人 · 垂直切片）

> 分工说明：[`TEAM_ASSIGNMENT.md`](TEAM_ASSIGNMENT.md) · 领任务时在 GitHub 建 Issue 并标 `#P0-x`

| 标签 | 主责 |
|------|------|
| `#P0-1`～`2` | 负责人 / D |
| `#P0-3` | C |
| `#P0-4` | D |
| `#P0-5` | 负责人 |
| `#P0-6` | A |
| `#P0-7` | B |

---

## P0-1 · 基础设施（已交付）

- [x] **#P0-1** `docker compose up -d` PG/Redis/MinIO（**全员自理**，无专岗）
- [x] ~~#P0-1b~~ 并入 **#P0-4b**（D · Worker）

---

## P0-6 · Web（A）

- [x] **#P0-6** 课程列表页（PR #9 已合并）
- [x] **#P0-6b** 时间轴播放器 + 字幕（UI/mock；待接 timeline API）
- [x] **#P0-6c** 侧边 PPT + 问答面板（UI/mock；ask 路径待改）
- [ ] **#P0-6d** 对接真实 `timeline` + `POST /courses/{id}/ask`（A follow-up）

---

## P0-5 · 智能链路（负责人）

- [x] **#P0-5** `alignment.py` 页级对齐工具函数 + 占位 API（**负责人** ✅ 骨架）
- [x] **#P0-5b** `agent.py` + `POST /courses/{id}/ask` RAG 占位 + CJK（**负责人** ✅）
- [x] **#P0-5d** `backend/tests/test_ask.py` smoke（**负责人** ✅）
- [x] **#P0-5e** `GET /courses/{id}/timeline` 占位响应（**负责人** ✅ 2026-07-22）
- [ ] **#P0-5b+** pgvector 正式 RAG + LLM（等 C/D 转写入库）
- [x] **#P0-5c** 全链路 demo 文档（**负责人** ✅ [`DEMO_E2E.md`](DEMO_E2E.md)）
- [x] **#P0-5f** Wave3：fixture timeline 钩子（`timeline_store` + `/timeline/from-fixture`）✅

---

## P0-2 · 上传与课程

- [x] **#P0-2** `endpoints/upload.py` MinIO 预签名 + complete + **对象校验**（**负责人** ✅ · Issue #2 closed）
- [x] **#P0-2d** `backend/tests/test_upload.py` smoke（**负责人** ✅）
- [x] **#P0-2a** upload complete 后自动创建 job + 后台跑 Worker（**负责人+D** ✅ 2026-07-22）
- [x] **#P0-2b** `course_service.py` **PostgreSQL** CRUD（Owner 代合 2026-08-02 · Issue #5）
- [x] **#P0-2c** `router.py` 注册 upload/ask/timeline/jobs（✅）

---

## P0-3 · 多媒体 · WhisperX（Owner 代合 · C 可选增强）

- [x] **#P0-3** `ffmpeg_pipeline.py` 抽 16kHz 音频（PR **#12** ✅）
- [x] **#P0-3b** `transcription.py` → `TranscriptResult`（fixture 默认可测；WhisperX 可选）
- [x] **#P0-3c** `ocr.py` → `OcrResult` / `OcrPageResult`（同上）

> PR #1 已关闭；由 Owner PR #12 一次落地 request-changes。真 WhisperX/GPU 样例由 C 在本机验证后贴 Issue，**勿再开碎 PR**。

---

## P0-4 · Job API + Worker（D · yucc280 + C）

- [x] **#P0-4** `endpoints/jobs.py` + `job_service.py` POST/GET（✅）
- [x] **#P0-4b** `workers/tasks.py` 调 `transcribe_media`（fixture 可 `done`）
- [x] **#P0-4c** Job/Course **落 PG**（Owner ✅；Redis/Celery 队列仍可选后续）

---

## P0-7 · 小程序（B）

- [x] **#P0-7** UniApp 初始化 + 域名白名单（PR **#11** 已合 2026-07-26 · tip `3e5f03c`）
- [x] **#P0-7b** 课程列表 + 简单问答页（同上；API 仍可指向 mock/本地）
- [x] **#P0-7c** 隐私/协议占位页 + 列表入口（合规 Z0 铺底）
- [ ] **#P0-7-ship** 微信上架：关闭 [WECHAT_COMPLIANCE.md](WECHAT_COMPLIANCE.md) Blocker（鉴权/HTTPS/注销）+ [ACCEPTANCE_MINIAPP.md](ACCEPTANCE_MINIAPP.md)

---

## 视频实测优化（C · 2026-09-16 报告）

> 详情：[VIDEO_OPTIMIZATION.md](VIDEO_OPTIMIZATION.md) · 原文：[VIDEO_TEST_REPORT_20260916.md](VIDEO_TEST_REPORT_20260916.md)

- [x] **#V-P0-1** 转写可复现（`ASR_REPRODUCIBLE` / `ASR_CPU_THREADS`；真机双跑待验）
- [x] **#V-P0-2** timeline 暴露 `data_source`（真实 vs 占位）
- [x] **#V-P0-3** 任务 `failed` 时返回空 cues（`TIMELINE_FIXTURE_ON_JOB_FAIL=false`）
- [x] **#V-P0-4** 大对象读超时可配（`S3_READ_TIMEOUT_SECONDS`）
- [x] **#V-P0-5** 默认 `UPLOAD_MAX_BYTES` 提至 512 MiB
- [x] **#V-P0-3b** Web/小程序对 `data_source=failed|placeholder` 的 UI 提示（前端）
- [ ] **#V-P0-1b** 同一 6min 素材 threads=1 连续双跑段数一致（本机实测）
- [x] **#V-P1-1** FFmpeg `highpass` + `loudnorm`（`ASR_AUDIO_PREPROCESS`）
- [x] **#V-P1-2** `ASR_INITIAL_PROMPT` 课件热词
- [x] **#V-P1-3** `quality_flags` / segment `quality_issues`
- [x] **#V-P1-4** 按时长选 `ASR_MODEL_SHORT` / `ASR_MODEL_LONG`
- [ ] **#V-P1-A/B** 固定线程下短/长素材 A/B（本机实测，对照报告基线）

---

## 联调里程碑

> 与 [`ROADMAP_EXEC.md`](ROADMAP_EXEC.md) 对齐（2026-08-14）

- [x] **#MILE-1** D+C+负责人：Course PG + jobs + upload → 转写入库（Owner 代合）
- [x] **#MILE-2** +A：Web 接真 timeline/ask 骨架（main；Issue #7 验收标准待关）
- [x] **#MILE-3** +B：小程序列表骨架（PR #11 ✅；接真 API 随 MILE-1/2）
- [ ] **#MILE-4** 答辩彩排：端到端 5 分钟 demo
