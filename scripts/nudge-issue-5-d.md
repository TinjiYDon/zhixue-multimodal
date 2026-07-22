## 催促 · D（yucc280）· #P0-4 阻塞全链路

@yucc280 你好——当前联调卡在 **Job/Course API**，请尽快推进。

### 人读摘要

| 项 | 内容 |
|----|------|
| Owner | D · `yucc280` |
| Issue | #5 · BACKLOG `#P0-2b` `#P0-4` `#P0-4b` |
| 阻塞谁 | 负责人 upload→job、C Worker 调用、A/B 真实对接 |
| 本周目标 | 至少提交 **Draft PR**（Course PG + POST/GET jobs 骨架即可） |

### Agent / 验收命令

```text
契约：docs/modules/M05-backend-jobs-api.md
目录：endpoints/jobs.py · job_service.py · course_service.py(PG) · workers/tasks.py
Worker 只调用 C 的 transcribe_media，不要自己实现 Whisper
验收：pytest + curl POST/GET /api/v1/jobs（或 PR 内说明）
```

请回复 ETA 或贴 Draft PR 链接。谢谢！
