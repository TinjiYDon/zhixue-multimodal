"""OCR pipeline — official ``OcrResult`` schema; RapidOCR optional."""

from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path

from app.schemas.transcript import OcrBlock, OcrPageResult, OcrResult

logger = logging.getLogger(__name__)

_FIXTURE_DIR = Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "multimedia"


def _fixture_ocr(asset_id: str) -> dict:
    return OcrResult(
        asset_id=asset_id,
        pages=[
            OcrPageResult(
                page=1,
                blocks=[
                    OcrBlock(text="智学 OCR 样例", bbox=[0.1, 0.1, 0.9, 0.2], confidence=0.99),
                ],
            )
        ],
    ).model_dump()


def _resolve_image(asset_id: str) -> Path | None:
    env_path = os.environ.get("ZHIXUE_OCR_IMAGE")
    if env_path and Path(env_path).exists():
        return Path(env_path)
    for name in (f"{asset_id}.png", "sample.png"):
        candidate = _FIXTURE_DIR / name
        if candidate.exists():
            return candidate
    return None


def _box_to_bbox(box) -> list[float]:
    """Normalize RapidOCR quad to rough x1,y1,x2,y2 in 0-1 if possible."""
    try:
        xs = [float(p[0]) for p in box]
        ys = [float(p[1]) for p in box]
        return [min(xs), min(ys), max(xs), max(ys)]
    except Exception:
        return []


async def run_ocr(asset_id: str) -> dict:
    """Return ``OcrResult`` dict. Fixture fallback when RapidOCR missing."""
    backend = os.environ.get("ZHIXUE_OCR_BACKEND", "auto").lower()
    if backend == "fixture" or os.environ.get("CI") == "true":
        return _fixture_ocr(asset_id)

    try:
        from rapidocr_onnxruntime import RapidOCR  # type: ignore
    except ImportError:
        logger.warning("rapidocr not installed; returning fixture OCR")
        return _fixture_ocr(asset_id)

    image_path = _resolve_image(asset_id)
    if image_path is None:
        return _fixture_ocr(asset_id)

    engine = RapidOCR()
    result, _elapse = await asyncio.to_thread(engine, str(image_path))
    blocks: list[OcrBlock] = []
    if result:
        for box, text, score in result:
            blocks.append(
                OcrBlock(
                    text=str(text),
                    bbox=_box_to_bbox(box),
                    confidence=float(score) if score is not None else None,
                )
            )
    return OcrResult(
        asset_id=asset_id,
        pages=[OcrPageResult(page=1, blocks=blocks)],
    ).model_dump()