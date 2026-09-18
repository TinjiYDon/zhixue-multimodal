"""Async SQLAlchemy engine / session (Postgres prod, SQLite for pytest)."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def _normalize_url(url: str) -> str:
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


engine: AsyncEngine | None = None
SessionLocal: async_sessionmaker[AsyncSession] | None = None


def configure_engine(url: str | None = None) -> AsyncEngine:
    global engine, SessionLocal
    raw = url or settings.database_url
    db_url = _normalize_url(raw)
    kwargs: dict = {"echo": bool(settings.debug)}
    if db_url.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
    engine = create_async_engine(db_url, **kwargs)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return engine


configure_engine()


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    if SessionLocal is None:
        configure_engine()
    assert SessionLocal is not None
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db() -> None:
    from app import models  # noqa: F401

    if engine is None:
        configure_engine()
    assert engine is not None
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def reset_db_for_tests() -> None:
    from app import models  # noqa: F401

    if engine is None:
        configure_engine()
    assert engine is not None
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
