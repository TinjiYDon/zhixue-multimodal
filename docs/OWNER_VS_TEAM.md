# 智学多模态 · 你 vs 队友分工（具体交付）

> 来源：`_local-data/team-docs/分工/大二项目学习内容整理.docx`  
> 仓库：`zhixue-multimodal` · GitHub public

---

## 你要完成的（负责人）

| # | 交付物 | 路径 | 具体做什么 |
|---|--------|------|------------|
| 1 | **上传 API** | `backend/app/api/v1/endpoints/upload.py`（新建） | 接收课程音视频/PPT；MinIO 预签名 URL；返回 `job_id` |
| 2 | **课程持久化** | `backend/app/services/course_service.py` | PostgreSQL 替代内存列表；课程 CRUD |
| 3 | **对齐服务** | `backend/app/services/alignment.py` | 转写文本 ↔ PPT/OCR 页级对齐（编辑距离/语义分段） |
| 4 | **RAG + Agent** | `backend/app/services/agent.py` | pgvector 入库检索；LLM 问答/摘要/大纲 JSON 输出 |
| 5 | **API 路由** | `backend/app/api/v1/router.py` | 挂载 upload / timeline / ask 等 endpoint |
| 6 | **OpenAPI 契约** | `/docs` | 定义请求/响应，队友前端/小程序按此联调 |
| 7 | **联调编排** | 文档 + 本地 demo | 上传 → 调队友 worker → 拿转写结果 → alignment → RAG |

**你不负责：** Vue 页面 UI、小程序页面、FFmpeg/WhisperX 底层、Celery worker 实现（但要定义调用接口）。

---

## 队友要完成的

### 队友 A · 前端 Vue（`web/`）

| 交付 | 说明 |
|------|------|
| 课堂时间轴播放器 | 同步音频/视频进度与字幕 |
| 侧边 PPT 展示 | 与 timeline API 联动 |
| 笔记页 | 可选 |
| 对接 API | `GET/POST /api/v1/courses`，后续 `/timeline` `/ask` |

文档：`web/TEAM_OWNER.md` · `docs/modules/M01-frontend-vue.md`

---

### 队友 B · 小程序（`miniapp/`）

| 交付 | 说明 |
|------|------|
| UniApp 项目初始化 | 官方脚手架 |
| 学生端入口 | 课程列表、进度、问答 |
| 域名白名单 | 对接后端 `/api` |

文档：`miniapp/TEAM_OWNER.md` · `docs/modules/M02-miniapp.md`

---

### 队友 C · 多媒体（`backend/app/services/multimedia/`）

| 交付 | 文件 | 说明 |
|------|------|------|
| FFmpeg 抽音频 | `ffmpeg_pipeline.py` | 重采样 16kHz |
| ASR 转写 | `transcription.py` | WhisperX + 字级时间戳 |
| OCR | `ocr.py` | PaddleOCR/RapidOCR，PPT/板书 |

输入：MinIO 路径（你 upload API 提供）  
输出：JSON 转写/OCR 结果（写 PG 或 MinIO，与你对齐 schema）

文档：`docs/modules/M03-multimedia.md`

---

### 队友 D · 数据与异步（`docker-compose.yml` + `workers/`）

| 交付 | 说明 |
|------|------|
| Docker 环境 | PG 5435 / Redis / MinIO 可启动 |
| 任务队列 | `backend/app/workers/tasks.py` — Celery 或 RQ |
| 异步任务 | 消费转写/OCR job，回调或写库 |

文档：`docs/modules/M04-data-infra.md`

---

## 联调顺序（建议）

```
1. 队友 D：docker compose up
2. 你：upload API + course PG
3. 队友 C：transcription 跑通 sample 文件
4. 队友 D：worker 调度 C 的任务
5. 你：alignment + agent/RAG
6. 队友 A/B：前端/小程序对接
```

---

## 验收标准（答辩前）

| 角色 | 最低标准 |
|------|----------|
| 你 | 上传 → worker 转写 → 对齐 → 问答 API 全链路 demo |
| A | Web 能播放时间轴 + 调 `/ask` |
| B | 小程序能看课程列表 |
| C | 给定 mp4 输出带时间戳 JSON |
| D | 异步任务可提交/查状态 |

详细待办：`docs/TODO_OWNER.md`
