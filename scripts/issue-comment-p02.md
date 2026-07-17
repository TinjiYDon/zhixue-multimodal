## 进度更新（负责人 · main）

### 已完成
- [x] `POST /api/v1/upload/presign` — MinIO 预签名，返回 `media_key` + `upload_url`
- [x] `POST /api/v1/upload/complete` — 确认上传，校验 `media_key` 与 `course_id`
- [x] `services/storage.py` — MinIO bucket 自动创建
- [x] `router.py` 已挂载 upload 路由

### 待联调
- [ ] `complete` 返回 `job_id` — 需 @yucc280 实现 `POST /api/v1/jobs` 后对接
- [ ] 验证：`docker compose up -d` → `/docs` 试 presign

### 相关 commit
见 main 分支最新 push。
