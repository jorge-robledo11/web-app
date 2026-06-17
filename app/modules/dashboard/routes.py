"""
Rutas HTTP del módulo de dashboard.

El endpoint GET / sirve la página principal con métricas reales
desde base de datos.
"""

import logging
from typing import Annotated, cast

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_paths
from app.infra.database import get_session
from app.modules.dashboard.service import construir_contexto

SessionDep = Annotated[AsyncSession, Depends(get_session)]

logger = logging.getLogger(__name__)

paths = get_paths()

templates = Jinja2Templates(directory=[paths.templates_dir, paths.static_dir])

router = APIRouter(tags=['dashboard'])


@router.get('/', response_class=HTMLResponse)
async def dashboard(
	request: Request,
	session: SessionDep,
) -> HTMLResponse:
	"""
	Renderiza el dashboard principal con métricas reales desde base de datos.
	"""
	logger.info('dashboard.render.inicio')
	ctx: dict[str, object] = cast(dict[str, object], await construir_contexto(session))
	ctx['request'] = request
	tmpl = templates.get_template('dashboard.html')
	logger.info('dashboard.render.fin', extra={'vacio': ctx['vacio']})
	return HTMLResponse(tmpl.render(ctx))
