"""ASR pipeline — 队友 C 实现 (WhisperX + worker).

TODO:
- 从 MinIO 拉取媒体
- FFmpeg 抽音频
- WhisperX 转写 + 时间戳
- 写入 PostgreSQL / 对象存储
"""

import os
import logging
import asyncio
from pydantic import BaseModel, Field

# 对应最初负责人给出的 Pydantic 模型契约
class TranscriptSegment(BaseModel):
    text: str
    start: float = Field(..., ge=0, description="seconds")
    end: float = Field(..., ge=0, description="seconds")
    speaker: str | None = None

class TranscriptResult(BaseModel):
    job_id: str
    media_key: str
    language: str | None = None
    segments: list[TranscriptSegment]

# 导入音频抽取函数
from app.services.multimedia.ffmpeg_pipeline import extract_audio

logger = logging.getLogger(__name__)

# 全局变量，用于保存加载的 WhisperX 模型实例
_model_instance = None

def patch_faster_whisper_compatibility():
    """硬核补丁：动态兼容新版 faster-whisper 以及 pyannote 的参数删除问题"""
    # 1. 修复 faster-whisper 参数缺失
    try:
        from faster_whisper.transcribe import TranscriptionOptions
        import inspect
        
        sig = inspect.signature(TranscriptionOptions.__init__)
        if 'multilingual' in sig.parameters and 'hotwords' in sig.parameters:
            orig_init = TranscriptionOptions.__init__
            
            def new_init(self, *args, **kwargs):
                if 'multilingual' not in kwargs and len(args) < 32: 
                    kwargs['multilingual'] = False
                if 'hotwords' not in kwargs and len(args) < 33: 
                    kwargs['hotwords'] = None
                orig_init(self, *args, **kwargs)
                
            TranscriptionOptions.__init__ = new_init
            logger.info("已成功注入 faster-whisper 新版参数兼容补丁。")
    except Exception as e:
        logger.warning(f"注入 faster-whisper 补丁时发生微小异常: {e}")

    # 2. 修复 Inference 鉴权参数被废弃导致的冲突（直接剔除不兼容的入参）
    def make_clean_init(orig_init_fn):
        def clean_init(self, *args, **kwargs):
            kwargs.pop('use_auth_token', None)
            kwargs.pop('token', None)
            return orig_init_fn(self, *args, **kwargs)
        return clean_init

    try:
        from pyannote.runtime.base import Inference
        Inference.__init__ = make_clean_init(Inference.__init__)
        logger.info("已成功注入 pyannote.runtime 鉴权参数清理补丁。")
    except Exception:
        pass

    try:
        from pyannote.audio.core.inference import Inference
        Inference.__init__ = make_clean_init(Inference.__init__)
        logger.info("已成功注入 pyannote.audio 鉴权参数清理补丁。")
    except Exception as e:
        logger.warning(f"注入 token 清理补丁时遭遇微小异常: {e}")

def get_whisperx_models():
    """同步懒加载 WhisperX 模型"""
    global _model_instance
    import whisperx
    import torch
    
    # 在加载模型前，先执行动态参数修复补丁
    patch_faster_whisper_compatibility()
    
    current_device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if current_device == "cuda" else "int8"
    
    if _model_instance is None:
        logger.info(f"正在加载 WhisperX 基础模型 (Device: {current_device}, Compute Type: {compute_type})...")
        _model_instance = whisperx.load_model("base", current_device, compute_type=compute_type, language="zh")
        
    return _model_instance, current_device


async def transcribe_media(job_id: str) -> dict:
    """异步 ASR 核心流水线任务"""
    import whisperx
    
    logger.info(f"[{job_id}] 开始执行 ASR Pipeline 任务...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, "sample.mp4")
    media_key = f"minio://media/{job_id}/sample.mp4"
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"未找到本地联调视频，请确保路径正确: {input_path}")
        
    temp_wav_path = os.path.join(current_dir, f"temp_{job_id}.wav")
    
    try:
        logger.info(f"[{job_id}] 正在调用 FFmpeg 抽取 16kHz 音频...")
        await asyncio.to_thread(extract_audio, input_path, temp_wav_path, 16000)
        
        logger.info(f"[{job_id}] 正在加载 WhisperX 模型并转写...")
        model, device = await asyncio.to_thread(get_whisperx_models)
        
        audio = whisperx.load_audio(temp_wav_path)
        result = await asyncio.to_thread(model.transcribe, audio, batch_size=16)
        
        logger.info(f"[{job_id}] 进行语音时间戳精确对齐...")
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
        aligned_result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
        
        segments_list = []
        for seg in aligned_result["segments"]:
            segments_list.append(
                TranscriptSegment(
                    text=seg.get("text", "").strip(),
                    start=float(seg.get("start", 0.0)),
                    end=float(seg.get("end", 0.0)),
                    speaker=seg.get("speaker", None)
                )
            )
            
        transcript_result = TranscriptResult(
            job_id=job_id,
            media_key=media_key,
            language=result.get("language", "zh"),
            segments=segments_list
        )
        
        final_dict = transcript_result.model_dump()
        logger.info(f"[{job_id}] ASR 转写流水线成功完成。")
        return final_dict
        
    finally:
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)
            logger.info(f"[{job_id}] 临时音频缓存文件已清理。")


if __name__ == "__main__":
    import json
    logging.basicConfig(level=logging.INFO)
    
    async def main_test():
        try:
            print("\n>>> 启动异步任务测试...")
            output_dict = await transcribe_media(job_id="task_async_test_001")
            print("\n【本地测试成功！】")
            print("最终吐出符合 Schema 契约的 dict 结果:")
            print(json.dumps(output_dict, indent=2, ensure_ascii=False))
        except Exception as ex:
            print(f"\n【测试失败】: {ex}")

    asyncio.run(main_test())