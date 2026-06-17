"""Tests unitarios de las rutas del dashboard."""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.infra.database import get_session
from app.main import app


@pytest.mark.asyncio
async def test_dashboard_route_renderiza_html_con_metricas():
	"""
	Verifica que GET / renderiza dashboard.html usando el contexto del servicio.
	"""
	mock_ctx = {
		'metricas': [
			{
				'label': 'Propiedades disponibles',
				'valor': 4,
				'icono': 'building-2',
				'estado': 'datos',
			},
			{
				'label': 'Propiedades rentadas',
				'valor': 3,
				'icono': 'check-circle-2',
				'estado': 'datos',
			},
			{
				'label': 'Ingresos',
				'valor': 0,
				'icono': 'wallet',
				'marcador': 'No disponible',
				'estado': 'datos',
			},
			{
				'label': 'Vencidos',
				'valor': 0,
				'icono': 'clock',
				'marcador': 'No disponible',
				'estado': 'datos',
			},
		],
		'accesos': [
			{'icono': 'building-2', 'label': 'Propiedades', 'url': '#'},
		],
		'actividad': [],
		'actividad_estado': 'vacio',
		'vacio': False,
	}

	mock_session = AsyncMock()
	app.dependency_overrides[get_session] = lambda: mock_session

	with patch(
		'app.modules.dashboard.routes.construir_contexto',
		new=AsyncMock(return_value=mock_ctx),
	):
		try:
			transport = ASGITransport(app=app)
			async with AsyncClient(
				transport=transport, base_url='http://test'
			) as client:
				response = await client.get('/')

			assert response.status_code == 200
			html = response.text

			assert 'Propiedades disponibles' in html
			assert 'Propiedades rentadas' in html
			assert 'No disponible' in html
			assert 'sidebar' in html
			assert 'navbar' in html
		finally:
			app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_dashboard_route_renderiza_estado_vacio():
	"""
	Verifica que GET / renderiza estado vacío cuando vacio=True.
	"""
	mock_ctx = {
		'metricas': [],
		'accesos': [],
		'actividad': [],
		'actividad_estado': 'datos',
		'vacio': True,
	}

	mock_session = AsyncMock()
	app.dependency_overrides[get_session] = lambda: mock_session

	with patch(
		'app.modules.dashboard.routes.construir_contexto',
		new=AsyncMock(return_value=mock_ctx),
	):
		try:
			transport = ASGITransport(app=app)
			async with AsyncClient(
				transport=transport, base_url='http://test'
			) as client:
				response = await client.get('/')

			assert response.status_code == 200
			html = response.text

			assert 'No hay datos disponibles' in html
			assert 'class="dashboard--empty"' in html
		finally:
			app.dependency_overrides.clear()
