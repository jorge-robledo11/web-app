"""Capa de base de datos asíncrona con SQLAlchemy 2.x y asyncpg."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Clase base declarativa para todos los modelos SQLAlchemy."""


async def get_session() -> AsyncGenerator[AsyncSession]:
    """Provee una AsyncSession por request. Usar con Depends(get_session)."""
    async with AsyncSessionLocal() as session:
        yield session
