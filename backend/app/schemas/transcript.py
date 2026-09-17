"""Multimedia output schemas — C implements against these models."""

from pydantic import BaseModel, Field


class TranscriptSegment(BaseModel):
    text: str
    start: float = Field(..., ge=0, description="seconds")
    end: float = Field(..., ge=0, description="seconds")
    speaker: str | None = None
    quality_issues: list[str] = Field(
        default_factory=list,
        description="e.g. high_compression_ratio, high_no_speech_prob",
    )


class TranscriptResult(BaseModel):
    job_id: str
    media_key: str
    language: str | None = None
    segments: list[TranscriptSegment]
    backend: str | None = Field(
        default=None,
        description="fixture | whisperx | … — 供 timeline data_source 区分",
    )
    asr_model: str | None = None
    duration_sec: float | None = None
    quality_flags: list[dict] = Field(
        default_factory=list,
        description="segment-level ASR quality warnings (V-P1-3)",
    )


class OcrBlock(BaseModel):
    text: str
    bbox: list[float] = Field(default_factory=list, description="x1,y1,x2,y2 normalized 0-1")
    confidence: float | None = Field(default=None, ge=0, le=1)


class OcrPageResult(BaseModel):
    page: int = Field(..., ge=1)
    blocks: list[OcrBlock]


class OcrResult(BaseModel):
    asset_id: str
    pages: list[OcrPageResult]
