"""Tests unitarios del servicio de dashboard."""

from unittest.mock import AsyncMock, patch

import pytest

from app.modules.dashboard.service import construir_contexto


@pytest.mark.asyncio
async def test_construir_contexto_con_datos():
	"""
	Verifica que el contexto refleja disponibles y rentadas desde el repo.
	"""
	with patch(
		'app.modules.dashboard.service.obtener_metricas',
		new=AsyncMock(return_value={'disponibles': 4, 'rentadas': 3, 'total': 7}),
	):
		ctx = await construir_contexto(session=AsyncMock())

	assert ctx['vacio'] is False
	assert ctx['actividad_estado'] == 'datos'
	assert ctx['metricas'][0]['label'] == 'Propiedades disponibles'
	assert ctx['metricas'][0]['valor'] == 4
	assert ctx['metricas'][0]['icono'] == 'building-2'
	assert ctx['metricas'][1]['label'] == 'Propiedades rentadas'
	assert ctx['metricas'][1]['valor'] == 3
	assert ctx['metricas'][1]['icono'] == 'check-circle-2'


@pytest.mark.asyncio
async def test_construir_contexto_sin_propiedades():
	"""
	Verifica que vacio es True cuando no hay propiedades.
	"""
	with patch(
		'app.modules.dashboard.service.obtener_metricas',
		new=AsyncMock(return_value={'disponibles': 0, 'rentadas': 0, 'total': 0}),
	):
		ctx = await construir_contexto(session=AsyncMock())

	assert ctx['vacio'] is True
	assert ctx['metricas'][0]['valor'] == 0
	assert ctx['metricas'][1]['valor'] == 0


@pytest.mark.asyncio
async def test_construir_contexto_solo_disponibles():
	"""
	Verifica que con solo disponibles no se activa estado vacío.
	"""
	with patch(
		'app.modules.dashboard.service.obtener_metricas',
		new=AsyncMock(return_value={'disponibles': 4, 'rentadas': 0, 'total': 4}),
	):
		ctx = await construir_contexto(session=AsyncMock())

	assert ctx['vacio'] is False
	assert ctx['metricas'][0]['valor'] == 4
	assert ctx['metricas'][1]['valor'] == 0


@pytest.mark.asyncio
async def test_construir_contexto_solo_rentadas():
	"""
	Verifica que con solo rentadas no se activa estado vacío.
	"""
	with patch(
		'app.modules.dashboard.service.obtener_metricas',
		new=AsyncMock(return_value={'disponibles': 0, 'rentadas': 3, 'total': 3}),
	):
		ctx = await construir_contexto(session=AsyncMock())

	assert ctx['vacio'] is False
	assert ctx['metricas'][1]['valor'] == 3


@pytest.mark.asyncio
async def test_metricas_no_operativas():
	"""
	Verifica que ingresos y vencidos tienen valor 0 y marcador 'No disponible'.
	"""
	with patch(
		'app.modules.dashboard.service.obtener_metricas',
		new=AsyncMock(return_value={'disponibles': 2, 'rentadas': 1, 'total': 3}),
	):
		ctx = await construir_contexto(session=AsyncMock())

	assert ctx['metricas'][2]['label'] == 'Ingresos'
	assert ctx['metricas'][2]['valor'] == 0
	assert ctx['metricas'][2]['marcador'] == 'No disponible'
	assert ctx['metricas'][2]['icono'] == 'wallet'

	assert ctx['metricas'][3]['label'] == 'Vencidos'
	assert ctx['metricas'][3]['valor'] == 0
	assert ctx['metricas'][3]['marcador'] == 'No disponible'
	assert ctx['metricas'][3]['icono'] == 'clock'


@pytest.mark.asyncio
async def test_orden_metricas():
	"""
	Verifica el orden fijo de las métricas.
	"""
	with patch(
		'app.modules.dashboard.service.obtener_metricas',
		new=AsyncMock(return_value={'disponibles': 1, 'rentadas': 1, 'total': 2}),
	):
		ctx = await construir_contexto(session=AsyncMock())

	labels = [m['label'] for m in ctx['metricas']]
	assert labels == [
		'Propiedades disponibles',
		'Propiedades rentadas',
		'Ingresos',
		'Vencidos',
	]


@pytest.mark.asyncio
async def test_metricas_reales_sin_tendencia():
	"""
	Verifica que las métricas reales no incluyen el campo tendencia.
	"""
	with patch(
		'app.modules.dashboard.service.obtener_metricas',
		new=AsyncMock(return_value={'disponibles': 4, 'rentadas': 2, 'total': 6}),
	):
		ctx = await construir_contexto(session=AsyncMock())

	assert 'tendencia' not in ctx['metricas'][0]
	assert 'tendencia' not in ctx['metricas'][1]


@pytest.mark.asyncio
async def test_contexto_accesos():
	"""
	Verifica que los accesos rápidos tienen la estructura esperada.
	"""
	with patch(
		'app.modules.dashboard.service.obtener_metricas',
		new=AsyncMock(return_value={'disponibles': 0, 'rentadas': 0, 'total': 0}),
	):
		ctx = await construir_contexto(session=AsyncMock())

	assert len(ctx['accesos']) == 4
	assert ctx['accesos'][0]['label'] == 'Propiedades'
	assert ctx['accesos'][3]['label'] == 'Pagos'


@pytest.mark.asyncio
async def test_contexto_actividad():
	"""
	Verifica que la actividad demo tiene 3 items.
	"""
	with patch(
		'app.modules.dashboard.service.obtener_metricas',
		new=AsyncMock(return_value={'disponibles': 0, 'rentadas': 0, 'total': 0}),
	):
		ctx = await construir_contexto(session=AsyncMock())

	assert len(ctx['actividad']) == 3
	assert ctx['actividad_estado'] == 'datos'
