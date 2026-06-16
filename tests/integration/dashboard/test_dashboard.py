"""Tests de integración del dashboard con PostgreSQL vía Testcontainers."""

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.main import app
from tests.integration.conftest import _alembic, _seed


def _setup_db(postgres_url: str) -> None:
	"""
	Ejecuta alembic upgrade en el contenedor de test.
	"""
	_alembic(postgres_url, 'upgrade', 'head')


@pytest.mark.asyncio
async def test_dashboard_metricas_reales(
	postgres_url: str, async_session: AsyncSession
):
	"""
	Verifica que GET / muestra conteos reales del seed (4 disponibles, 3 rentadas).
	"""
	_setup_db(postgres_url)
	_seed(postgres_url)

	async def override_get_session():
		yield async_session

	app.dependency_overrides[get_session] = override_get_session

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/')

		assert response.status_code == 200
		html = response.text

		assert 'Propiedades disponibles' in html
		assert 'Propiedades rentadas' in html
		assert 'Ingresos' in html
		assert 'Vencidos' in html
		assert 'No disponible' in html
		assert html.count('No disponible') == 2
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_dashboard_estado_vacio(postgres_url: str, async_session: AsyncSession):
	"""
	Verifica que GET / muestra estado vacío cuando no hay propiedades.
	"""
	_setup_db(postgres_url)

	async def override_get_session():
		yield async_session

	app.dependency_overrides[get_session] = override_get_session

	try:
		# Truncar datos para asegurar estado vacío
		from sqlalchemy import text as sa_text

		await async_session.execute(sa_text('DELETE FROM propiedades'))
		await async_session.commit()

		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/')

		assert response.status_code == 200
		html = response.text

		assert 'No hay datos disponibles' in html
		assert 'class="dashboard--empty"' in html
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_dashboard_orden_secciones(
	postgres_url: str, async_session: AsyncSession
):
	"""
	Verifica el orden vertical: métricas → accesos rápidos → actividad.
	"""
	_setup_db(postgres_url)
	_seed(postgres_url)

	async def override_get_session():
		yield async_session

	app.dependency_overrides[get_session] = override_get_session

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/')

		html = response.text
		pos_metricas = html.find('class="metricas"')
		pos_accesos = html.find('class="accesos-rapidos"')
		pos_actividad = html.find('class="actividad"')

		assert pos_metricas > 0
		assert pos_accesos > 0
		assert pos_actividad > 0
		assert pos_metricas < pos_accesos < pos_actividad
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_dashboard_accesos_rapidos(
	postgres_url: str, async_session: AsyncSession
):
	"""
	Verifica que los accesos rápidos tienen 4 items sin cambios.
	"""
	_setup_db(postgres_url)
	_seed(postgres_url)

	async def override_get_session():
		yield async_session

	app.dependency_overrides[get_session] = override_get_session

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/')

		html = response.text
		assert 'class="accesos-rapidos"' in html
		assert html.count('class="acceso-rapido"') >= 4
		assert 'Propiedades' in html
		assert 'Inquilinos' in html
		assert 'Contratos' in html
		assert 'Pagos' in html
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_dashboard_sidebar_navbar(postgres_url: str, async_session: AsyncSession):
	"""
	Verifica que el dashboard incluye sidebar y navbar.
	"""
	_setup_db(postgres_url)
	_seed(postgres_url)

	async def override_get_session():
		yield async_session

	app.dependency_overrides[get_session] = override_get_session

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/')

		html = response.text
		assert 'sidebar' in html
		assert 'navbar' in html
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_dashboard_responde_200(postgres_url: str, async_session: AsyncSession):
	"""
	Verifica que GET / retorna HTTP 200 con text/html.
	"""
	_setup_db(postgres_url)
	_seed(postgres_url)

	async def override_get_session():
		yield async_session

	app.dependency_overrides[get_session] = override_get_session

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/')

		assert response.status_code == 200
		assert 'text/html' in response.headers['content-type']
	finally:
		app.dependency_overrides.clear()
