# 智学多模态 · 分工与交付清单

> 总表与上手指南：**[`TEAM_ASSIGNMENT.md`](TEAM_ASSIGNMENT.md)**（全员先读）

---

## 负责人（集成 + 智能链路）

| # | 交付物 | 路径 | 状态 |
|---|--------|------|------|
| 1 | 上传 API | `endpoints/upload.py` + `services/storage.py` | ✅ presign + complete + MinIO 校验 |
| 2 | 转写/OCR schema | `schemas/transcript.py` | ✅ 供 C 对齐 |
| 3 | 对齐服务 | `services/alignment.py` | ✅ 工具函数 + 占位 |
| 4 | RAG + Agent | `services/agent.py` + `courses/{id}/ask` | ✅ 占位 + CJK |
| 5 | 路由 + 测试 | `router.py` · `backend/tests/` | ✅ 6 pytest passed |
| 6 | OpenAPI 契约审批 | `/docs` | 进行中 |
| 7 | 联调编排 | upload → D job → alignment → RAG | ⏳ 等 D/C |

**不负责：** Course PG、Job API、Worker、Whisper（已划归 D / C）

→ [TODO_OWNER.md](TODO_OWNER.md)

---

### 队友 A · 前端 Vue（`web/`）

| 交付 | 说明 |
|------|------|
| 课堂时间轴播放器 | 同步音频/视频进度与字幕 |
| 侧边 PPT 展示 | 与 timeline API 联动 |
| 笔记页 | 可选 |
| 对接 API | `GET/POST /api/v1/courses`，后续 `/timeline` `/ask` |

文档：`web/TEAM_OWNER.md` · `docs/modules/M01-frontend-vue.md` · BACKLOG `#P0-6`

---

### 队友 B · 小程序（`miniapp/`）

| 交付 | 说明 |
|------|------|
| UniApp 项目初始化 | 官方脚手架 |
| 学生端入口 | 课程列表、进度、问答 |
| 域名白名单 | 对接后端 `/api` |

文档：`miniapp/TEAM_OWNER.md` · `docs/modules/M02-miniapp.md` · BACKLOG `#P0-7`

---

### 队友 C · 多媒体（`backend/app/services/multimedia/`）

| 交付 | 文件 | 说明 |
|------|------|------|
| FFmpeg 抽音频 | `ffmpeg_pipeline.py` | 重采样 16kHz |
| ASR 转写 | `transcription.py` | **WhisperX** + 字级时间戳 |
| OCR | `ocr.py` | PaddleOCR/RapidOCR |

输入：MinIO 路径（负责人 upload API 提供）  
输出：JSON → **必须**符合 `backend/app/schemas/transcript.py`（负责人已定义）

文档：`multimedia/OWNER.md` · `docs/modules/M03-multimedia.md` · BACKLOG `#P0-3`

---

### 队友 D · 业务 API + 任务域

| 交付 | 文件 | 说明 |
|------|------|------|
| 课程 PG 持久化 | `course_service.py` + 模型 | 替代内存列表 |
| Job REST API | `endpoints/jobs.py` `schemas/job.py` | POST/GET 任务 |
| Worker | `workers/tasks.py` | 调 C 的 `transcribe_media` |
| 课程 API 扩展 | `endpoints/courses.py` | GET `{id}` 等 |

**不再主责：** Docker 编排（M4 已交付）

文档：`workers/OWNER.md` · `docs/modules/M05-backend-jobs-api.md` · BACKLOG `#P0-2b` `#P0-4`

---

## 联调顺序

```
1. 全员     docker compose up -d
2. D        Course PG + jobs API
3. 负责人   upload API                    ← ✅ 已完成
4. C        sample 转写 JSON              ← PR #1 待重做
5. D        Worker 调度
6. 负责人   alignment + RAG 正式版        ← 骨架已完成
7. A / B    前端对接
```

---

## 答辩验收

| 角色 | 最低标准 |
|------|----------|
| 负责人 | 全链路 demo：上传 → 转写 → 问答 |
| A | Web 时间轴 + `/ask` |
| B | 小程序课程列表 |
| C | mp4 → 带时间戳 JSON |
| D | `/jobs` 可提交/查状态 + Course 落 PG |
