"""Punto de entrada de la aplicación FastAPI — Realtor."""

import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
	directory=[
		str(BASE_DIR / 'templates'),
		str(BASE_DIR / 'static'),
	]
)


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


@app.get('/', response_class=HTMLResponse)
async def dashboard(request: Request):
	"""
	Renderiza el dashboard demo con datos hardcodeados.
	"""
	metricas = [
		{
			'label': 'Propiedades activas',
			'valor': 124,
			'icono': 'building-2',
			'tendencia': {'direccion': 'up', 'texto': '+8% vs mes anterior'},
			'estado': 'datos',
		},
		{
			'label': 'Inquilinos al día',
			'valor': 87,
			'icono': 'users',
			'tendencia': {'direccion': 'up', 'texto': '+3% vs mes anterior'},
			'estado': 'datos',
		},
		{
			'label': 'Contratos vigentes',
			'valor': 53,
			'icono': 'file-text',
			'tendencia': {'direccion': 'down', 'texto': '-5% vs mes anterior'},
			'estado': 'datos',
		},
	]
	accesos = [
		{'icono': 'building-2', 'label': 'Propiedades', 'url': '#'},
		{'icono': 'users', 'label': 'Inquilinos', 'url': '#'},
		{'icono': 'file-text', 'label': 'Contratos', 'url': '#'},
		{'icono': 'wallet', 'label': 'Pagos', 'url': '#'},
	]
	actividad = [
		{
			'tipo': 'propiedad',
			'descripcion': 'Nueva propiedad registrada: Av. Reforma 245, Col. Centro',
			'fecha': 'Hace 2 horas',
			'badge_variante': 'accent',
			'estado': 'datos',
		},
		{
			'tipo': 'contrato',
			'descripcion': 'Contrato por vencer: Depto. Condesa — vence en 3 días',
			'fecha': 'Hace 5 horas',
			'badge_variante': 'warning',
			'estado': 'datos',
		},
		{
			'tipo': 'pago',
			'descripcion': 'Pago recibido: $15,000 — Renta Depto. Polanco',
			'fecha': 'Ayer',
			'badge_variante': 'success',
			'estado': 'datos',
		},
	]
	tmpl = templates.get_template('dashboard.html')
	return tmpl.render(
		{
			'request': request,
			'metricas': metricas,
			'accesos': accesos,
			'actividad': actividad,
			'actividad_estado': 'datos',
		}
	)
