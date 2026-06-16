"""Punto de entrada de la aplicación FastAPI — Realtor."""

import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, get_session
from app.modules.dashboard.routes import router as dashboard_router

SessionDep = Annotated[AsyncSession, Depends(get_session)]

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
	"""
	Inicializa y libera recursos al arrancar y apagar la aplicación.
	"""
	yield
	await engine.dispose()


app = FastAPI(
	title='Realtor',
	description='Sistema de gestión inmobiliaria',
	version='0.1.0',
	lifespan=lifespan,
)

app.mount(
	'/static',
	StaticFiles(directory=str(BASE_DIR / 'static')),
	name='static',
)

app.include_router(dashboard_router)


@app.get('/health')
async def health(session: SessionDep):
	"""
	Verifica conectividad de la aplicación y la base de datos.
	"""
	try:
		async with asyncio.timeout(2):
			await session.execute(text('SELECT 1'))
	except (TimeoutError, SQLAlchemyError) as exc:
		logger.warning('health.database_unavailable', extra={'detail': str(exc)})
		return JSONResponse(
			status_code=503,
			content={
				'status': 'error',
				'database': 'unavailable',
				'detail': 'timeout after 2s',
			},
		)

	return {'status': 'ok', 'database': 'ok'}
