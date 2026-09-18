# M03 · 多媒体处理（队友 C）

## 目录

`backend/app/services/multimedia/`

| 文件 | 职责 |
|------|------|
| `ffmpeg_pipeline.py` | 抽音频、重采样 |
| `transcription.py` | WhisperX ASR |
| `ocr.py` | PPT/板书 OCR |

## 依赖

- FFmpeg 系统安装
- MinIO 对象路径由负责人 upload API 提供（`POST /api/v1/upload/presign`）

## 输出契约

实现结果须符合 `backend/app/schemas/transcript.py`：

- `TranscriptResult` / `TranscriptSegment` — ASR
- `OcrResult` / `OcrPageResult` — OCR

## 验收

- 单测或脚本：给定 sample.mp4 → 返回带时间戳 JSON




---

### 📝 7.17第一次任务 · 多媒体模块（ASR & OCR）本地联调交付报告

#### 1. 🛠️ 本次改动的内容（Code Changes）

* **`ffmpeg_pipeline.py` (#P0-3)**：完成了音视频资源的预处理逻辑，实现了高效提取 `16kHz` 标准音频流，为后续 ASR 提供干净的输入。
* **`transcription.py` (#P0-3b)**：
* 本地成功跑通 `faster-whisper` + `WhisperX` (Wav2Vec2 强制对齐) 核心双模型流水线。
* 针对 **Python 3.14 高版本** 导致的底层库不兼容问题，成功编写并植入了**动态参数兼容补丁（Monkey Patch）**，解决了旧版参数引发的 `TypeError`。
* 本地测试（sample.mp4）验证成功，输出数据完全符合团队约定的 `TranscriptResult` 契约，输出包含毫秒级精确时间戳（`text`/`start`/`end`）。


* **`ocr.py` (#P0-3c)**：
* 本地成功跑通基于 ONNXRuntime 的 `RapidOCR` 异步流水线，避免了本地编译复杂 C++ 环境的问题。
* 修复了新版引擎 `elapse` 耗时返回类型导致的格式化崩溃问题。
* 本地测试（sample.png）验证成功，完整吐出符合契约的 `OCRResult` 结构（包含合并文本与各文本块的四点 `box` 坐标）。


* **接口封装**：核心函数已全部封装为 `async def transcribe_media(job_id)` 和 `async def run_ocr(asset_id)`，具备随时供 **成员 D** 接入异步任务队列（Worker）调用的标准。

---

#### 2. 💻 所需的运行环境与系统依赖

除了 Python 基础环境外，由于涉及音视频的解封装与抽流，**系统必须安装 FFmpeg 工具**：

* **工具包名称**：`FFmpeg`
* **安装及配置要求**：
* **Windows**：需下载并解压 FFmpeg 二进制文件，并将包含 `ffmpeg.exe` 的 `bin` 目录路径手动添加至系统的**环境变量 `Path**` 中。
* **验证方式**：在终端运行 `ffmpeg -version` 有正确输出即可。如果不配置，`transcription.py` 在执行抽流时会直接报错。



---

#### 3. 📦 需要安装的 Python 第三方依赖包

已将本次改动引入的核心依赖包及兼容版本追加至组长建立的 `requirements.txt` 中。团队成员在运行前需更新环境：

* **核心工具包清单**：
1. `whisperx` —— 负责语音识别与字词级时间戳高精度对齐。
2. `rapidocr_onnxruntime` —— 负责轻量化、免编译的本地图片文本与坐标提取。
3. `pyannote.audio` / `torchaudio` —— 语音处理与声学对齐模型底层支撑库。
4. `pillow` —— OCR 图像读取基础库。


* **团队一键安装命令**：`pip install -r requirements.txt`

---

#### 4. 🧠 首次运行需要下载的 AI 模型权重（队友避坑指南）

由于模型权重文件体积较大，未提交至 Git，初次运行时程序会自动触发云端下载：

1. **ASR 文本识别模型**：`faster-whisper` 相关规格权重。
2. **ASR 毫秒级对齐模型**：`Wav2Vec2` 强对齐模型（大小约 `1.28GB`）。
3. **💡 团队加速下载技巧**：为防止 Hugging Face 连通性限制导致下载卡死，强烈建议其他队友在**第一次运行脚本前**，先在 PowerShell 终端执行以下命令挂载国内镜像源，即可实现秒级高速下载：
```powershell
$env:HF_ENDPOINT="https://hf-mirror.com"

```



---
