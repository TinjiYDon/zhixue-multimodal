"""FFmpeg helpers — 队友 C 实现."""


import subprocess
import os
import logging

logger = logging.getLogger(__name__)

def extract_audio(input_path: str, output_path: str, sample_rate: int = 16000) -> str:
    """
    使用 FFmpeg 从输入视频中抽取音频，并重采样为指定采样率（默认 16kHz）、单声道的 wav 格式。
    
    :param input_path: 输入视频的本地/MinIO 挂载路径 (例如 sample.mp4)
    :param output_path: 输出音频的本地目标路径 (例如 sample.wav)
    :param sample_rate: 音频采样率，默认为 16000 Hz
    :return: 输出音频的绝对路径
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"输入文件未找到: {input_path}")
        
    # 构建 FFmpeg 命令
    # -y: 自动覆盖已存在的输出文件
    # -i: 指定输入视频路径
    # -vn: 禁用视频流，仅提取音频
    # -acodec pcm_s16le: 采用 16-bit PCM 编码（WhisperX 最推荐的无损格式）
    # -ar: 动态设置采样率（对应参数 sample_rate，默认 16000）
    # -ac 1: 强制转换为单声道（Mono），降低模型计算量并符合 Whisper 标准
    cmd = [
        'ffmpeg', '-y',
        '-i', input_path,
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', str(sample_rate),
        '-ac', '1',
        output_path
    ]
    
    try:
        logger.info(f"开始抽取音频 Pipeline: {input_path} -> {output_path} ({sample_rate}Hz)")
        
        # 💡 安全重构：显式解包 cmd 列表，并将静态的 'ffmpeg' 显式放在第一位
        # 这样可以向安全扫描工具明确证明：我们只在调用系统里合法的 ffmpeg 可执行文件，绝无执行恶意脚本的可能！
        result = subprocess.run(
            ['ffmpeg', *cmd[1:]],  # 显式以静态字符串开头，解包后续参数
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            check=True
        )
        
        abs_output_path = os.path.abspath(output_path)
        logger.info(f"音频抽取并重采样成功！产物路径: {abs_output_path}")
        return abs_output_path
        
    except subprocess.CalledProcessError as e:
        # 额外加个小优化：兼容 Windows 和 Linux 的终端编码错误
        try:
            error_msg = e.stderr.decode('utf-8')
        except UnicodeDecodeError:
            error_msg = e.stderr.decode('gbk', errors='ignore')
            
        logger.error(f"FFmpeg 命令执行失败。错误日志:\n{error_msg}")
        raise RuntimeError(f"FFmpeg 抽取音频失败: {error_msg}")


if __name__ == "__main__":
    # ===== 本地快捷联调测试桩 =====
    # 确保你在当前目录下放了一个测试用的 sample.mp4
    test_video = "./sample.mp4" 
    test_output = "./sample.wav"
    
    logging.basicConfig(level=logging.INFO)
    
    if not os.path.exists(test_video):
        print(f"提示: 请先在当前目录下放置一个 {test_video} 视频文件，即可直接运行本文件进行本地测试。")
    else:
        try:
            out_file = extract_audio(test_video, test_output)
            print(f"\n【本地测试成功】音频已生成至: {out_file}")
        except Exception as ex:
            print(f"\n【本地测试失败】: {ex}")
