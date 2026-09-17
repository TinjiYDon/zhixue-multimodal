# 视频实测优化清单 · zhixue-multimodal

> 更新：2026-09-17  
> 依据：[VIDEO_TEST_REPORT_20260916.md](VIDEO_TEST_REPORT_20260916.md)  
> 性质：**P0 已落地 · P1 后端已开**；Owner：多媒体 C + 负责人联调  
> 验收基座须在 **固定 ASR 线程数（可复现=1）** 下跑，否则数字每次漂移。

## Agent 上下文

```text
repo: zhixue-multimodal
source: docs/VIDEO_TEST_REPORT_20260916.md
priority: P0-repro > P0-timeline-source > P0-failed-empty > P0-quota
code_hint:
  - backend/app/services/multimedia/transcription.py  (WhisperX 路径；报告环境曾用 faster-whisper)
  - backend/app/services/timeline_store.py            (message 文案共用)
  - backend/app/core/config.py                       (upload_max_bytes=200MiB)
  - backend/app/api/v1/endpoints/upload.py
禁区: dumps/ 大视频不入 Git；勿把 fixture 文案写成生产转写
```

## 四类 720p 基线（摘要）

| 用途 | 素材 | 预期（报告基线） |
|------|------|------------------|
| 快速回归 | 37s 短片段 | 15 段 / 164 字 · `done` |
| 主力 | 6min 正常 | 37 段 / 1384 字 · `done` |
| 压力 | 13min 正常 | 77 段 / 2764 字 · 削波/容量告警 |
| 拒绝 | 6min 数字静音轨 | `failed` · 闸门 ~0.42 s · **不应展示假内容** |

## P0 · 可信与可用（建议先做）

| ID | 项 | 问题（报告） | 建议动作 | 代码落点（当前） | 状态 |
|----|----|--------------|----------|------------------|------|
| **V-P0-1** | 转写可复现 | 同音频两次 37/41 段；多线程 int8 归约 | ASR_REPRODUCIBLE / ASR_CPU_THREADS；评测强制 1 | transcription.py · config.py | **已落地（配置）**；真机双跑待验 |
| **V-P0-2** | 区分真实/占位 | message 同为 fixture/job hook | timeline 增加 data_source | timeline_store.py · schema | **已落地** |
| **V-P0-3** | 失败空时间轴 | failed 仍返回占位 | 失败空 cues + data_source=failed | workers/tasks.py | **已落地**（含 Web/小程序 banner） |
| **V-P0-4** | 大文件超时 | 读超时过紧 | S3_READ_TIMEOUT_SECONDS | storage.py | **已落地** |
| **V-P0-5** | 容量 | 13min 占上限 94.6% | 默认 512 MiB | config.py | **已落地** |

## P1 · 准确度（P0-1 之后）

| ID | 项 | 要点 | 状态 |
|----|----|------|------|
| **V-P1-1** | 响度/削波前处理 | 13min 峰值 0 dBFS；`highpass` + EBU R128 `loudnorm` | **已落地**（`ASR_AUDIO_PREPROCESS`） |
| **V-P1-2** | 课件热词 / initial_prompt | 术语错误占比高 | **已落地**（`ASR_INITIAL_PROMPT`） |
| **V-P1-3** | compression_ratio / no_speech 质检 | 接近幻觉阈值时标记 | **已落地**（`quality_flags` / `quality_issues`） |
| **V-P1-4** | 模型档按场景 | 短用 small、长用 base；A/B 必须固定线程 | **已落地**（阈值可配） |

## P2 · 多模态增强

| ID | 项 |
|----|----|
| V-P2-1 | VAD 按有效帧占比自动开关 |
| V-P2-2 | 抽帧 OCR 填 slides（现恒 1 条占位） |
| V-P2-3 | 双向对齐（课件纠 ASR / ASR 助翻页） |
| V-P2-4 | 闸门 numpy 向量化 |

## 建议实施顺序

1. ~~**V-P0-1**~~ 配置已合；**本机**用 `ASR_REPRODUCIBLE=true` 对 6min 双跑验段数  
2. ~~**V-P0-2 + V-P0-3**~~ 后端 + Web/小程序 banner 已合  
3. ~~**V-P0-5 / V-P0-4**~~ 已合  
4. ~~**V-P1-1…4**~~ 后端已合；真机 A/B（固定线程）待验  
5. 再开 P2  

## 验收命令（实施后填写）

```powershell
cd d:\project\zhixue-multimodal\backend
.\.venv\Scripts\python.exe -m pytest tests/ -q
# 可复现回归（素材不入 Git，本地路径自备）：
# $env:ASR_REPRODUCIBLE='true'
# 同一 6min 文件连续两次转写，段数与文本须一致
```

## 相关

- [VIDEO_TEST_REPORT_20260916.md](VIDEO_TEST_REPORT_20260916.md)  
- [modules/M03-multimedia.md](modules/M03-multimedia.md)  
- Issue #6（RAG/alignment）与本清单正交；本清单优先多媒体可信度  
