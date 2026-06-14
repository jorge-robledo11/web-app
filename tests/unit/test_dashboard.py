"""Tests de humo para GET / dashboard."""

import pytest


@pytest.mark.asyncio
async def test_dashboard_ok(async_client):
	"""Verifica que GET / retorna el dashboard con sidebar y 3 tarjetas."""
	response = await async_client.get('/')

	assert response.status_code == 200
	html = response.text

	assert 'class="sidebar"' in html or 'sidebar' in html
	assert 'class="navbar"' in html or 'navbar' in html
	assert html.count('tarjeta-metrica') >= 3
	assert 'Propiedades activas' in html
	assert '124' in html


@pytest.mark.asyncio
async def test_metricas_estado_datos(async_client):
	"""Verifica que las métricas en estado normal renderizan contenido."""
	response = await async_client.get('/')
	html = response.text

	assert 'tarjeta-metrica__valor' in html
	assert 'tarjeta-metrica__label' in html
	assert 'tarjeta-metrica__tendencia' in html


@pytest.mark.asyncio
async def test_metricas_tendencias_presentes(async_client):
	"""Verifica que las métricas incluyen tendencias con dirección y texto."""
	response = await async_client.get('/')
	html = response.text

	assert 'tarjeta-metrica__tendencia--up' in html
	assert 'tarjeta-metrica__tendencia--down' in html
	assert '+8%' in html
	assert '-5%' in html


@pytest.mark.asyncio
async def test_metricas_estado_carga_estructura(async_client):
	"""Verifica que el template incluye la estructura para estado de carga."""
	response = await async_client.get('/')
	html = response.text

	assert 'tarjeta-metrica__estado-carga' in html


@pytest.mark.asyncio
async def test_metricas_estado_error_estructura(async_client):
	"""Verifica que el template incluye la estructura para estado de error."""
	response = await async_client.get('/')
	html = response.text

	assert 'tarjeta-metrica__estado-error' in html


@pytest.mark.asyncio
async def test_accesos_rapidos_presentes(async_client):
	"""Verifica que la sección de accesos rápidos tiene 4 tarjetas cliqueables."""
	response = await async_client.get('/')
	html = response.text

	assert 'class="accesos-rapidos"' in html
	assert html.count('class="acceso-rapido"') >= 4


@pytest.mark.asyncio
async def test_accesos_rapidos_urls(async_client):
	"""Verifica que cada acceso rápido tiene icono y label."""
	response = await async_client.get('/')
	html = response.text

	assert 'Propiedades' in html
	assert 'Inquilinos' in html
	assert 'Contratos' in html
	assert 'Pagos' in html
	assert 'acceso-rapido__icono' in html


@pytest.mark.asyncio
async def test_actividad_reciente_presente(async_client):
	"""Verifica que la sección de actividad reciente tiene 3 items."""
	response = await async_client.get('/')
	html = response.text

	assert 'actividad-item' in html
	assert html.count('actividad-item') >= 3


@pytest.mark.asyncio
async def test_actividad_reciente_tipos(async_client):
	"""Verifica que los items de actividad tienen badges de tipo."""
	response = await async_client.get('/')
	html = response.text

	assert 'actividad-item__tipo' in html
	assert 'actividad-item__descripcion' in html
	assert 'actividad-item__fecha' in html
	assert 'Nueva propiedad registrada' in html
	assert 'Contrato por vencer' in html
	assert 'Pago recibido' in html


@pytest.mark.asyncio
async def test_dashboard_orden_secciones(async_client):
	"""Verifica el orden vertical fijo: Métricas → Accesos → Actividad."""
	response = await async_client.get('/')
	html = response.text

	pos_metricas = html.find('class="metricas"')
	pos_accesos = html.find('class="accesos-rapidos"')
	pos_actividad = html.find('class="actividad"')

	assert pos_metricas < pos_accesos < pos_actividad
