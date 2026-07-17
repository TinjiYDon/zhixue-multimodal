"""LLM Agent + RAG — 负责人实现."""

from __future__ import annotations

# In-memory stub store until PG + pgvector integration (P0-5b).
_course_context: dict[str, list[str]] = {}


def set_course_context(course_id: str, chunks: list[str]) -> None:
    _course_context[course_id] = chunks


def _match_chunks(chunks: list[str], question: str) -> list[str]:
    q = question.strip()
    if not q:
        return chunks[:2]

    hits = [c for c in chunks if q in c]
    if hits:
        return hits

    for token in q.split():
        if len(token) < 2:
            continue
        hits = [c for c in chunks if token.lower() in c.lower()]
        if hits:
            return hits

    # CJK: any multi-char substring of length >= 2
    if len(q) >= 2:
        for size in range(min(len(q), 8), 1, -1):
            for i in range(len(q) - size + 1):
                part = q[i : i + size]
                hits = [c for c in chunks if part in c]
                if hits:
                    return hits

    return chunks[:2]


async def answer_question(course_id: str, question: str) -> tuple[str, list[str]]:
    chunks = _course_context.get(course_id, [])
    if not chunks:
        return (
            f"课程 {course_id} 暂无索引内容，请等待转写与对齐完成后再提问。",
            [],
        )

    hits = _match_chunks(chunks, question)
    answer = "（RAG 占位）根据课程内容：" + " ".join(hits[:3])
    return answer, hits[:3]
