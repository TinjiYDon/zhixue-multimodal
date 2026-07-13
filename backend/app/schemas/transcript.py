"""Multimedia output schemas — C implements against these models."""

from pydantic import BaseModel, Field


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
