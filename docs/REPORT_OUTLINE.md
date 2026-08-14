# 结项报告辅助材料（第 2 / 3 / 4 部分框架）

> 供组员填充。**第 1 部分「模型架构、算法」由负责人本人撰写，本文不展开。**  
> 本文件在 **zhixue-multimodal** 仓；ICU 两仓工程细节请各仓组员对照各自 `docs/PROGRESS.md` / `STATUS.md` 填写，避免跨仓路径依赖。

## Agent 上下文

```text
repo: zhixue-multimodal
doc_role: report_outline_parts_2_3_4
part1: written_by_owner_elsewhere
fill_in: teammates
icu_refs: use each ICU repo docs on GitHub, not monorepo root
```

---

## 第 1 部分（占位）

**标题建议：** 模型架构与算法  

范围按分工：decision 预警、scheduling 优化、zhixue RAG/对齐。  
**本文不提供正文。**

---

## 第 2 部分 · 系统实现与工程交付

**标题建议：** 系统架构、工程实现与可复现交付  

### 2.1 核心关键词

- 仓独立 / 独立数据库 / 零运行时硬耦合  
- FastAPI + Vue3 + UniApp（本仓）  
- Docker Compose（PG / Redis / MinIO）  
- upload presign → complete → job → worker  
- timeline / ask 契约；fixture 降级  
- （对照填写）ICU：LightGBM+SHAP；CP-SAT；dump 复现  

### 2.2 章节骨架

1. 本仓总体架构（backend / web / miniapp / worker）  
2. 上传与多媒体链路（默认样例 mp4；ffmpeg 抽音）  
3. 课程 / Job / timeline / ask  
4. 协作与质量（Issue/PR、pytest、fixture）  
5. 已知限制（无登录、占位 RAG、模拟视频区）  

### 2.3 本仓证据

- [PROGRESS.md](PROGRESS.md) · [CHANGELOG.md](CHANGELOG.md) · [ACCEPTANCE_ZHIXUE.md](ACCEPTANCE_ZHIXUE.md)  
- Release：`zhixue-mile2`  

---

## 第 3 部分 · 实验评测与验收结果

**标题建议：** 实验设计、指标与验收结论  

### 3.1 核心关键词

- pytest 契约（schema / upload / ask / jobs）  
- fixture timeline；冒烟 API 200  
- 人工视觉验收（有条件通过）  
- （ICU 对照）PR-AUC / Brier；CP-SAT 利用率与 λ  

### 3.2 章节骨架

1. 本仓测试与验收协议  
2. 摘录 [ACCEPTANCE_ZHIXUE.md](ACCEPTANCE_ZHIXUE.md)  
3. 失败与边界（无 auth、占位多媒体）  
4. ICU 定量结果由对应仓 STATUS 粘贴（勿写死在本仓）  

### 3.3 本仓数字锚点

| 项 | 值 |
|----|-----|
| pytest | 14 passed（2026-08-14） |
| 验收结论 | 有条件通过 |
| 截图 | `docs/acceptance-screens/` |

---

## 第 4 部分 · 总结、创新点与展望

**标题建议：** 工作总结、创新点、不足与下一步  

### 4.1 核心关键词

- 课堂多模态实时 Agent（时间轴 + 问答）  
- fixture 可演示 / 真模型可选  
- MILE-4 彩排；正式 RAG  
- （对照）ICU 双轨可讲解、预测–优化、不硬耦合  

### 4.2 章节骨架

1. 本仓已完成一句话  
2. 创新点（工程方法，勿夸大 WhisperX 已生产）  
3. 不足（#6/#7、PR#13、无登录）  
4. 下一步对齐 [ROADMAP.md](ROADMAP.md)  

### 4.3 禁止表述

- 「已具备完整账号登录」  
- 「生产级 WhisperX 已默认上线」  
- 「与 ICU 运行时已打通风险/床位」  

---

## 附录

| 文件 | 用途 |
|------|------|
| [ROADMAP.md](ROADMAP.md) | 下一版本 |
| [ROADMAP_EXEC.md](ROADMAP_EXEC.md) | MILE 执行 |
| [BACKLOG.md](BACKLOG.md) | P0 切片 |
