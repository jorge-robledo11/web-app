"""Capa de base de datos asíncrona con SQLAlchemy 2.x y asyncpg."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

settings = get_settings()
engine = create_async_engine(settings.database_url, echo=False)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
	"""
	Clase base declarativa para todos los modelos SQLAlchemy.
	"""


async def get_session() -> AsyncGenerator[AsyncSession]:
	"""
	Provee una AsyncSession por request. Usar con Depends(get_session).

	El cuerpo (yield) solo se ejerce vía FastAPI dependency injection;
	los tests unitarios usan dependency_overrides.
	"""
	async with AsyncSessionLocal() as session:
		yield session  # pragma: no cover
