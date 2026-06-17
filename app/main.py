"""Punto de entrada de la aplicación FastAPI — Realtor."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import get_paths, get_settings
from app.infra.database import engine
from app.modules.dashboard.routes import router as dashboard_router
from app.modules.health.routes import router as health_router
from app.modules.propiedades.routes import router as propiedades_router

logger = logging.getLogger(__name__)

settings = get_settings()
paths = get_paths(settings)


@asynccontextmanager
async def lifespan(app: FastAPI):
	"""
	Inicializa y libera recursos al arrancar y apagar la aplicación.
	"""
	yield
	await engine.dispose()


app = FastAPI(
	title=settings.app_name,
	description='Sistema de gestión inmobiliaria',
	version='0.1.0',
	debug=settings.debug,
	lifespan=lifespan,
)

app.mount(
	settings.static_url,
	StaticFiles(directory=paths.static_dir),
	name='static',
)

app.include_router(health_router)
app.include_router(dashboard_router)
app.include_router(propiedades_router)
