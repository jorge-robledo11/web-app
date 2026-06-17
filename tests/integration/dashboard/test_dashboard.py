"""Tests de integración del dashboard con PostgreSQL vía Testcontainers."""

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database import get_session
from app.main import app
from tests.integration.conftest import seed_ok, setup_db


def _setup(postgres_url: str) -> None:
	"""
	Aplica alembic y seed validando returncode.
	"""
	setup_db(postgres_url)
	seed_ok(postgres_url)


@pytest.mark.asyncio
async def test_dashboard_metricas_reales(
	postgres_url: str, async_session: AsyncSession
):
	"""
	Verifica que GET / muestra conteos reales del seed (4 disponibles, 3 rentadas).
	"""
	_setup(postgres_url)

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
		# Verifica valores reales del seed
		assert '>4<' in html or '>4</div>' in html
		assert '>3<' in html or '>3</div>' in html
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_dashboard_estado_vacio(postgres_url: str, async_session: AsyncSession):
	"""
	Verifica que GET / muestra estado vacío cuando no hay propiedades.
	"""
	setup_db(postgres_url)

	# Limpiar datos residuales de otros tests (el seed escribe en su propia
	# conexión y commitea, así que el rollback de async_session no lo revierte).
	from sqlalchemy import text as sa_text

	await async_session.execute(sa_text('DELETE FROM propiedades'))
	await async_session.commit()

	async def override_get_session():
		yield async_session

	app.dependency_overrides[get_session] = override_get_session

	try:
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
	_setup(postgres_url)

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
	_setup(postgres_url)

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
	_setup(postgres_url)

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
	_setup(postgres_url)

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


@pytest.mark.asyncio
async def test_marcador_dentro_de_tarjeta(
	postgres_url: str, async_session: AsyncSession
):
	"""
	Verifica que 'No disponible' se renderiza DENTRO de la tarjeta métrica
	y no como hermano directo del grid .metricas.
	"""
	_setup(postgres_url)

	async def override_get_session():
		yield async_session

	app.dependency_overrides[get_session] = override_get_session

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/')

		html = response.text

		# El marcador NO debe ser hijo directo de .metricas
		assert '<small class="tarjeta-metrica__marcador">' not in html, (
			'El marcador se renderiza fuera de la tarjeta métrica'
		)
		assert html.count('tarjeta-metrica') >= 16, (
			'Debe haber al menos 4 tarjetas métricas (4 ocurrencias de '
			'tarjeta-metrica × 4: div + 3 sub-elementos cada una)'
		)
		assert 'No disponible' in html
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_metricas_valores_reales_4_y_3(
	postgres_url: str, async_session: AsyncSession
):
	"""
	Verifica que los valores 4 (disponibles) y 3 (rentadas) aparecen en el HTML.
	"""
	_setup(postgres_url)

	async def override_get_session():
		yield async_session

	app.dependency_overrides[get_session] = override_get_session

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/')

		html = response.text

		# Valor 4 debe aparecer antes de "Propiedades disponibles"
		idx_disponibles = html.find('Propiedades disponibles')
		assert idx_disponibles > 0
		contexto_antes = html[max(0, idx_disponibles - 300) : idx_disponibles]
		assert '4' in contexto_antes, (
			'El valor 4 no aparece cerca de Propiedades disponibles'
		)

		# Valor 3 debe aparecer antes de "Propiedades rentadas"
		idx_rentadas = html.find('Propiedades rentadas')
		assert idx_rentadas > 0
		contexto_antes = html[max(0, idx_rentadas - 300) : idx_rentadas]
		assert '3' in contexto_antes, (
			'El valor 3 no aparece cerca de Propiedades rentadas'
		)
	finally:
		app.dependency_overrides.clear()
