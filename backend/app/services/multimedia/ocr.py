"""OCR pipeline — 队友 C 实现 (PaddleOCR / RapidOCR).



TODO:

- PPT/板书图片 → 文本

- 参与 alignment 页级对齐

"""
import os
import logging
import asyncio
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# 定义符合团队规范的 OCR 输出 Schema 契约
class OCRResult(BaseModel):
    asset_id: str
    raw_text: str = Field(..., description="合并后的完整文本")
    blocks: list[dict] = Field(..., description="包含坐标和置信度的原始文本块")

# 全局初始化 RapidOCR 实例（懒加载）
_engine_instance = None

def get_ocr_engine():
    """获取或初始化 RapidOCR 引擎"""
    global _engine_instance
    if _engine_instance is None:
        from rapidocr_onnxruntime import RapidOCR
        logger.info("正在初始化 RapidOCR (ONNXRuntime) 引擎...")
        _engine_instance = RapidOCR()
    return _engine_instance

async def run_ocr(asset_id: str) -> dict:
    """异步 OCR 核心流水线任务
    
    Args:
        asset_id: 图片资源的 ID
    Returns:
        符合 OCRResult Schema 的字典结果
    """
    logger.info(f"[{asset_id}] 开始执行 OCR Pipeline 任务...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 假定本地联调有一张 sample.png 或 sample.jpg
    input_path = os.path.join(current_dir, "sample.png")
    
    # 兼容处理兼容 png/jpg 命名
    if not os.path.exists(input_path):
        input_path = os.path.join(current_dir, "sample.jpg")
        
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"未找到本地联调图片，请在当前目录放一张 sample.png 或 sample.jpg")
        
    try:
        # 1. 动态获取引擎
        engine = get_ocr_engine()
        
        # 2. 在线程池中跑密集的 CPU 推理，避免阻塞 asyncio 事件循环
        logger.info(f"[{asset_id}] 正在调用 RapidOCR 识别图像文本...")
        result, elapse = await asyncio.to_thread(engine, input_path)
        
        blocks_list = []
        text_lines = []
        
        if result:
            for box, text, score in result:
                text_lines.append(text)
                blocks_list.append({
                    "box": box,         # 四点坐标 [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                    "text": text,       # 识别文本
                    "confidence": float(score)  # 置信度
                })
        
        # 3. 拼接得到完整文本，并包装成契约格式
        full_text = "\n".join(text_lines)
        ocr_result = OCRResult(
            asset_id=asset_id,
            raw_text=full_text,
            blocks=blocks_list
        )
        
        logger.info(f"[{asset_id}] OCR 推理成功完成，耗时: {elapse}s")
        return ocr_result.model_dump()
        
    except Exception as e:
        logger.error(f"[{asset_id}] OCR 任务执行失败: {e}")
        raise e

if __name__ == "__main__":
    import json
    logging.basicConfig(level=logging.INFO)
    
    async def main_test():
        try:
            print("\n>>> 启动异步 OCR 任务测试...")
            output_dict = await run_ocr(asset_id="asset_ocr_test_001")
            print("\n【本地 OCR 测试成功！】")
            print("最终吐出符合 Schema 契约的 dict 结果:")
            print(json.dumps(output_dict, indent=2, ensure_ascii=False))
        except Exception as ex:
            print(f"\n【测试失败】: {ex}")

    asyncio.run(main_test())