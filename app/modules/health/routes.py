"""
Rutas HTTP del módulo de health.

GET /health verifica conectividad de la aplicación y la base de datos.
"""

import asyncio
import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/health', tags=['health'])


@router.get('', response_model=None)
async def health(session: SessionDep) -> dict[str, str] | JSONResponse:
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
