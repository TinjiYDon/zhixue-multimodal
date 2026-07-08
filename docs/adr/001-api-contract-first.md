# ADR-001：API 契约优先的多端协作

- **状态**：已采纳  
- **日期**：2026-07-08

## 背景

5 人跨 Web、小程序、Worker、多媒体，需避免「口头约定接口」导致联调失败。

## 决策

1. OpenAPI（FastAPI `/docs`）为 **唯一** 前后端/Worker 对接标准
2. 负责人维护 API；A/B/C/D 变更消费方前先确认 schema
3. 多媒体输出 JSON schema 由 C 起草、负责人批准后再实现 Worker 写库

## 后果

- 模块可并行开发，联调窗口缩短
- API 变更必须可追溯（issue + PR）
