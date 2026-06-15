"""Fixtures de integración con PostgreSQL vía Testcontainers."""

import os
import subprocess
import sys
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer

from app.database import Base
from app.modules.propiedades import models  # noqa: F401 - registrar modelo

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


@pytest.fixture(scope='session')
def postgres_url() -> str:
	"""
	Levanta PostgreSQL efímero una vez por sesión y retorna la URL asyncpg.
	"""
	postgres = PostgresContainer('postgres:16-alpine')
	postgres.start()
	raw = postgres.get_connection_url()
	url = raw.replace('postgresql://', 'postgresql+asyncpg://', 1)
	url = url.replace('postgresql+psycopg2://', 'postgresql+asyncpg://', 1)
	yield url
	postgres.stop()


@pytest_asyncio.fixture
async def async_session(
	postgres_url: str,
) -> AsyncGenerator[AsyncSession]:
	"""
	Sesión de BD contra el contenedor efímero, rollback por test.
	"""
	engine = create_async_engine(postgres_url, echo=False)
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
	session_factory = async_sessionmaker(engine, expire_on_commit=False)
	async with session_factory() as session:
		yield session
		await session.rollback()
	await engine.dispose()


def _alembic(url: str, *args: str) -> subprocess.CompletedProcess[str]:
	"""
	Ejecuta alembic apuntando a la URL del contenedor.
	"""
	env = os.environ | {'DATABASE_URL': url}
	return subprocess.run(
		[sys.executable, '-m', 'alembic', *args],
		capture_output=True,
		text=True,
		cwd=REPO_ROOT,
		env=env,
	)


def _seed(url: str) -> subprocess.CompletedProcess[str]:
	"""
	Ejecuta el seed apuntando a la URL del contenedor.
	"""
	env = os.environ | {'DATABASE_URL': url}
	return subprocess.run(
		[sys.executable, str(REPO_ROOT / 'scripts' / 'dev' / 'seed_propiedades.py')],
		capture_output=True,
		text=True,
		cwd=REPO_ROOT,
		env=env,
	)
