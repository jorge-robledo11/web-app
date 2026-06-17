"""
Rutas HTTP del módulo de propiedades.

GET /propiedades renderiza la página de propiedades con grid de cards.
"""

import logging
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_paths
from app.infra.database import get_session
from app.modules.propiedades.service import listar_propiedades

SessionDep = Annotated[AsyncSession, Depends(get_session)]

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent

paths = get_paths()

templates = Jinja2Templates(
	directory=[
		paths.templates_dir,
		paths.static_dir,
		BASE_DIR / 'templates',
	]
)

router = APIRouter(prefix='/propiedades', tags=['propiedades'])


@router.get('', response_class=HTMLResponse)
async def propiedades(
	request: Request,
	session: SessionDep,
) -> HTMLResponse:
	"""
	Renderiza la página de propiedades con grid de cards responsive.
	"""
	logger.info('propiedades.listar.inicio')
	lista = await listar_propiedades(session)
	ctx: dict[str, object] = {
		'request': request,
		'propiedades': lista,
		'vacio': len(lista) == 0,
	}
	tmpl = templates.get_template('propiedades.html')
	logger.info(
		'propiedades.listar.fin',
		extra={'total': len(lista), 'vacio': ctx['vacio']},
	)
	return HTMLResponse(tmpl.render(ctx))
