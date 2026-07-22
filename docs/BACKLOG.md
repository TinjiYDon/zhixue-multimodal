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
- [ ] **#P0-5c** 全链路 demo 文档

---

## P0-2 · 上传与课程

- [x] **#P0-2** `endpoints/upload.py` MinIO 预签名 + complete + **对象校验**（**负责人** ✅ · Issue #2 closed）
- [x] **#P0-2d** `backend/tests/test_upload.py` smoke（**负责人** ✅）
- [x] **#P0-2a** upload complete 后自动创建 job + 后台跑 Worker（**负责人+D** ✅ 2026-07-22）
- [ ] **#P0-2b** `course_service.py` **PostgreSQL** CRUD（**D** 续作；当前为内存 CRUD 骨架）
- [x] **#P0-2c** `router.py` 注册 upload/ask/timeline/jobs（✅）

---

## P0-3 · 多媒体 · WhisperX（C · whq6830-arch）

- [ ] **#P0-3** `ffmpeg_pipeline.py` 抽 16kHz 音频
- [ ] **#P0-3b** `transcription.py` sample mp4 → JSON（时间戳，对齐 `schemas/transcript.py`）
- [ ] **#P0-3c** `ocr.py` sample 图片 → 文本

> PR #1 request changes（2026-07-22），见 Issue #4 / PR 评论。

---

## P0-4 · Job API + Worker（D · yucc280 + C）

- [x] **#P0-4** `endpoints/jobs.py` + `job_service.py` POST/GET（内存骨架 · 分支 `course-job-zyc` 已合入）
- [x] **#P0-4b** `workers/tasks.py` 调 `transcribe_media`（C 未就绪 → job=`failed` 可接受）
- [ ] **#P0-4c** Job/Course **落 PG** + 队列（Redis/Celery）正式化（D）

---

## P0-7 · 小程序（B）

- [ ] **#P0-7** UniApp 初始化 + 域名白名单
- [ ] **#P0-7b** 课程列表 + 简单问答页

---

## 联调里程碑

- [ ] **#MILE-1** D+C+负责人：Course PG + jobs + upload → 转写入库
- [ ] **#MILE-2** +A：Web 播放时间轴
- [ ] **#MILE-3** +B：小程序列表
- [ ] **#MILE-4** 答辩彩排：端到端 5 分钟 demo
