"""Text/media alignment — 负责人实现 (编辑距离 / 语义分段 / 页级对齐)."""

from __future__ import annotations

from app.schemas.transcript import OcrPageResult, TranscriptSegment


def align_segments_to_pages(
    segments: list[TranscriptSegment],
    pages: list[OcrPageResult],
) -> list[dict]:
    """Map transcript segments to slide pages by proportional timeline."""
    if not segments or not pages:
        return []

    total_duration = max(s.end for s in segments)
    page_count = len(pages)
    aligned: list[dict] = []

    for seg in segments:
        if total_duration <= 0:
            page = 1
        else:
            ratio = seg.start / total_duration
            page = min(page_count, max(1, int(ratio * page_count) + 1))
        aligned.append(
            {
                "page": page,
                "start": seg.start,
                "end": seg.end,
                "text": seg.text,
                "slide_text": pages[page - 1].blocks[0].text if pages[page - 1].blocks else "",
            }
        )
    return aligned


async def align_transcript_to_slides(course_id: str) -> dict:
    # Full pipeline loads transcript + OCR from storage/DB once C and D deliver.
    return {
        "course_id": course_id,
        "status": "pending",
        "aligned": [],
        "message": "Waiting for C transcription JSON and OCR results.",
    }
