# 任务 Backlog（五人 · 垂直切片）

---

## P0-1 · 基础设施（D）

- [ ] **#P0-1** `docker compose up -d` PG/Redis/MinIO 健康  
- [ ] **#P0-1b** `workers/tasks.py` 骨架：接收 job_id，可 mock 完成

---

## P0-2 · 上传与课程（负责人）

- [ ] **#P0-2** `endpoints/upload.py` MinIO 预签名 + job_id  
- [ ] **#P0-2b** `course_service.py` PostgreSQL CRUD  
- [ ] **#P0-2c** `router.py` 挂载 routes，OpenAPI 可见

---

## P0-3 · 多媒体（C）

- [ ] **#P0-3** `ffmpeg_pipeline.py` 抽 16kHz 音频  
- [ ] **#P0-3b** `transcription.py` sample mp4 → JSON（时间戳）  
- [ ] **#P0-3c** `ocr.py` sample 图片 → 文本

---

## P0-4 · Worker（D + C）

- [ ] **#P0-4** 队列消费转写任务，写 PG 或 MinIO（schema 与负责人对齐）  
- [ ] **#P0-4b** GET `/jobs/{id}` 查状态（负责人定义 API，D 实现）

---

## P0-5 · 智能链路（负责人）

- [ ] **#P0-5** `alignment.py` 转写 ↔ PPT 页对齐  
- [ ] **#P0-5b** `agent.py` pgvector RAG + `/ask`  
- [ ] **#P0-5c** 全链路 demo 文档（upload→worker→align→ask）

---

## P0-6 · Web（A）

- [ ] **#P0-6** 课程列表页  
- [ ] **#P0-6b** 时间轴播放器 + 字幕  
- [ ] **#P0-6c** 侧边 PPT + 问答面板

---

## P0-7 · 小程序（B）

- [ ] **#P0-7** UniApp 初始化 + 域名白名单  
- [ ] **#P0-7b** 课程列表 + 简单问答页

---

## 联调里程碑

- [ ] **#MILE-1** 负责人+C+D：上传 → worker → 转写入库  
- [ ] **#MILE-2** +A：Web 播放时间轴  
- [ ] **#MILE-3** +B：小程序列表  
- [ ] **#MILE-4** 答辩彩排：端到端 5 分钟 demo
