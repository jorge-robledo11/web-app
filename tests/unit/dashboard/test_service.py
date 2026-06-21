"""Tests unitarios del servicio de dashboard."""

from unittest.mock import AsyncMock, patch

import pytest

from app.modules.dashboard.service import construir_contexto


async def _construir_contexto_con_metricas(
	metricas: dict[str, int],
	mock_session: AsyncMock | None = None,
) -> dict[str, object]:
	"""
	Helper que mockea ``obtener_metricas`` y devuelve el contexto completo.

	Permite que cada test verifique el contrato observable completo
	(metricas, accesos, actividad, actividad_estado, vacio) sin repetir
	el boilerplate de patch/AsyncMock en cada test.
	"""
	if mock_session is None:
		mock_session = AsyncMock()

	with patch(
		'app.modules.dashboard.service.obtener_metricas',
		new=AsyncMock(return_value=metricas),
	):
		return await construir_contexto(session=mock_session)


@pytest.mark.asyncio
async def test_construir_contexto_con_datos():
	"""
	Verifica el contrato observable completo con datos: dict de metricas
	exacto (orden y campos), ``actividad_estado='datos'``, ``vacio=False``
	y propagación de la sesión al repositorio de metricas.
	"""
	mock_session = AsyncMock()
	ctx = await _construir_contexto_con_metricas(
		{'disponibles': 4, 'rentadas': 3, 'total': 7},
		mock_session=mock_session,
	)

	assert ctx['vacio'] is False
	assert ctx['actividad_estado'] == 'datos'
	assert ctx['metricas'] == [
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
	]

	with patch(
		'app.modules.dashboard.service.obtener_metricas',
		new=AsyncMock(return_value={'disponibles': 0, 'rentadas': 0, 'total': 0}),
	) as mock_obtener:
		await construir_contexto(session=mock_session)
		mock_obtener.assert_awaited_once_with(mock_session)


@pytest.mark.asyncio
async def test_construir_contexto_sin_propiedades():
	"""
	Verifica que ``vacio=True`` cuando no hay propiedades y que los
	valores de las métricas reales se propagan en cero.
	"""
	ctx = await _construir_contexto_con_metricas(
		{'disponibles': 0, 'rentadas': 0, 'total': 0},
	)

	assert ctx['vacio'] is True
	assert ctx['metricas'][0]['valor'] == 0
	assert ctx['metricas'][1]['valor'] == 0
	assert ctx['metricas'][2]['valor'] == 0
	assert ctx['metricas'][3]['valor'] == 0


@pytest.mark.asyncio
async def test_construir_contexto_solo_disponibles():
	"""
	Verifica que con solo disponibles no se activa estado vacío.
	"""
	ctx = await _construir_contexto_con_metricas(
		{'disponibles': 4, 'rentadas': 0, 'total': 4},
	)

	assert ctx['vacio'] is False
	assert ctx['metricas'][0]['valor'] == 4
	assert ctx['metricas'][1]['valor'] == 0


@pytest.mark.asyncio
async def test_construir_contexto_solo_rentadas():
	"""
	Verifica que con solo rentadas no se activa estado vacío.
	"""
	ctx = await _construir_contexto_con_metricas(
		{'disponibles': 0, 'rentadas': 3, 'total': 3},
	)

	assert ctx['vacio'] is False
	assert ctx['metricas'][1]['valor'] == 3


@pytest.mark.asyncio
async def test_contexto_accesos_conserva_contrato():
	"""
	Verifica el contrato observable completo de la lista de accesos
	rápidos: dict exacto con los 4 items hardcodeados.

	Caza mutantes sobre el orden, etiquetas, iconos y URLs de los
	accesos rápidos devueltos por ``_accesos()``.
	"""
	ctx = await _construir_contexto_con_metricas(
		{'disponibles': 1, 'rentadas': 1, 'total': 2},
	)

	assert ctx['accesos'] == [
		{'icono': 'building-2', 'label': 'Propiedades', 'url': '#'},
		{'icono': 'users', 'label': 'Inquilinos', 'url': '#'},
		{'icono': 'file-text', 'label': 'Contratos', 'url': '#'},
		{'icono': 'wallet', 'label': 'Pagos', 'url': '#'},
	]


@pytest.mark.asyncio
async def test_contexto_actividad_conserva_contrato():
	"""
	Verifica el contrato observable completo de la lista de actividad
	reciente: dict exacto con los 3 items hardcodeados.

	Caza mutantes sobre el orden, tipo, descripcion, fecha y
	badge_variante de cada item de actividad devuelto por ``_actividad()``.
	"""
	ctx = await _construir_contexto_con_metricas(
		{'disponibles': 1, 'rentadas': 1, 'total': 2},
	)

	assert ctx['actividad'] == [
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


@pytest.mark.asyncio
async def test_actividad_estado_siempre_datos_con_datos():
	"""
	Verifica que ``actividad_estado`` se mantiene en ``'datos'``
	incluso cuando las métricas reales son cero (la actividad demo no
	depende del estado de propiedades).
	"""
	ctx = await _construir_contexto_con_metricas(
		{'disponibles': 0, 'rentadas': 0, 'total': 0},
	)

	assert ctx['actividad_estado'] == 'datos'
