## 负责人阶段加固（push 前）

- MinIO `object_exists` 校验；complete 未上传返回 400
- ask 合并至 `POST /courses/{id}/ask`；CJK RAG 占位
- `backend/tests/`：6 pytest passed

待联调：#P0-2a 自动触发 job（等 #5 D）
