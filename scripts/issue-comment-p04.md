## upload API 已就绪（供 D 联调）

负责人已完成 upload 端点，D 实现 Job API 时可对接：

1. 前端/负责人：`POST /api/v1/upload/presign` → 客户端 PUT 到 MinIO
2. `POST /api/v1/upload/complete` → 得到 `media_key`
3. D：`POST /api/v1/jobs` body `{ course_id, media_key }` → 返回 `job_id`

`upload/complete` 暂返回 `job_id: null`，等本 Issue 的 jobs API 合并后串联。

契约：`docs/modules/M05-backend-jobs-api.md`
