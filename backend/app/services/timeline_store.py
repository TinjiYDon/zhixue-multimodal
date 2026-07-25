"""In-memory timeline store filled by job-done hook (fixture or real transcript)."""

from __future__ import annotations

from app.schemas.timeline import TimelineCue, TimelineResponse, TimelineSlide

_timeline_by_course: dict[str, TimelineResponse] = {}


def clear_for_tests() -> None:
    _timeline_by_course.clear()


def set_timeline(course_id: str, timeline: TimelineResponse) -> None:
    _timeline_by_course[course_id] = timeline


def get_timeline(course_id: str) -> TimelineResponse | None:
    return _timeline_by_course.get(course_id)


def timeline_from_fixture_segments(
    course_id: str,
    segments: list[dict],
    *,
    slides: list[dict] | None = None,
) -> TimelineResponse:
    """Build TimelineResponse from WhisperX-like segment dicts (Wave3 fixture path)."""
    cues = [
        TimelineCue(
            t_start=float(s.get("start", s.get("t_start", 0))),
            t_end=float(s.get("end", s.get("t_end", 0))),
            text=str(s.get("text", "")),
        )
        for s in segments
    ]
    duration = max((c.t_end for c in cues), default=0.0)
    slide_models = [
        TimelineSlide(
            page=int(sl.get("page", i + 1)),
            t_start=float(sl.get("t_start", 0)),
            title=str(sl.get("title", f"Slide {i + 1}")),
        )
        for i, sl in enumerate(slides or [])
    ]
    if not slide_models and cues:
        slide_models = [TimelineSlide(page=1, t_start=0, title="自动页（fixture）")]
    return TimelineResponse(
        course_id=course_id,
        status="ok",
        duration_sec=duration,
        cues=cues,
        slides=slide_models,
        message="timeline from fixture/job hook (Wave3)",
    )


FIXTURE_TRANSCRIPT = {
    "segments": [
        {"start": 0.0, "end": 8.0, "text": "欢迎学习本课程，今天介绍核心概念。"},
        {"start": 8.0, "end": 20.0, "text": "第一要点：理解问题定义与边界。"},
        {"start": 20.0, "end": 35.0, "text": "第二要点：用数据验证假设。"},
    ],
    "slides": [
        {"page": 1, "t_start": 0.0, "title": "封面"},
        {"page": 2, "t_start": 8.0, "title": "要点一"},
        {"page": 3, "t_start": 20.0, "title": "要点二"},
    ],
}


async def ingest_job_result_to_timeline(course_id: str, result: object | None, *, use_fixture_on_fail: bool = True) -> TimelineResponse:
    """Wave3 hook: map job result → timeline store; fall back to fixture for demo."""
    segments = None
    slides = None
    if isinstance(result, dict):
        segments = result.get("segments")
        slides = result.get("slides")
    elif isinstance(result, str) and result.strip().startswith("{"):
        import json

        try:
            parsed = json.loads(result)
            segments = parsed.get("segments")
            slides = parsed.get("slides")
        except json.JSONDecodeError:
            segments = None

    if not segments and use_fixture_on_fail:
        segments = FIXTURE_TRANSCRIPT["segments"]
        slides = FIXTURE_TRANSCRIPT["slides"]

    if not segments:
        tl = TimelineResponse(
            course_id=course_id,
            status="placeholder",
            duration_sec=0,
            cues=[],
            slides=[],
            message="no transcript segments yet",
        )
        set_timeline(course_id, tl)
        return tl

    tl = timeline_from_fixture_segments(course_id, segments, slides=slides)
    set_timeline(course_id, tl)
    # Seed RAG context from cue texts
    from app.services import agent

    agent.set_course_context(course_id, [c.text for c in tl.cues if c.text])
    return tl
