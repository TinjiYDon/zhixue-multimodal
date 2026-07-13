"""LLM Agent + RAG — 负责人实现."""

from __future__ import annotations

# In-memory stub store until PG + pgvector integration (P0-5b).
_course_context: dict[str, list[str]] = {}


def set_course_context(course_id: str, chunks: list[str]) -> None:
    _course_context[course_id] = chunks


async def answer_question(course_id: str, question: str) -> tuple[str, list[str]]:
    chunks = _course_context.get(course_id, [])
    if not chunks:
        return (
            f"课程 {course_id} 暂无索引内容，请等待转写与对齐完成后再提问。",
            [],
        )

    q = question.lower()
    hits = [c for c in chunks if any(token in c.lower() for token in q.split() if len(token) > 1)]
    if not hits:
        hits = chunks[:2]

    answer = "（RAG 占位）根据课程内容：" + " ".join(hits[:3])
    return answer, hits[:3]
