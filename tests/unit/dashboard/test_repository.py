"""Tests unitarios del repositorio de dashboard."""

from unittest.mock import AsyncMock, call, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.dashboard.repository import obtener_metricas
from app.modules.propiedades.models import EstadoPropiedad


@pytest.mark.asyncio
async def test_obtener_metricas_con_datos():
	"""
	Verifica conteos y que se delega al repositorio usando la sesión recibida.

	Caza mutantes sobre la firma de las llamadas (sesión, enum de estado,
	orden de invocación) comparando el dict completo y los argumentos
	await explícitos.
	"""
	mock_session = AsyncMock(spec=AsyncSession)
	mock_contar_por_estado = AsyncMock(side_effect=[5, 2])
	mock_contar_total = AsyncMock(return_value=10)

	with (
		patch(
			'app.modules.dashboard.repository.contar_por_estado',
			new=mock_contar_por_estado,
		),
		patch(
			'app.modules.dashboard.repository.contar_total',
			new=mock_contar_total,
		),
	):
		result = await obtener_metricas(mock_session)

	assert result == {'disponibles': 5, 'rentadas': 2, 'total': 10}
	assert mock_contar_por_estado.await_args_list == [
		call(mock_session, EstadoPropiedad.DISPONIBLE),
		call(mock_session, EstadoPropiedad.RENTADA),
	]
	mock_contar_total.assert_awaited_once_with(mock_session)


@pytest.mark.asyncio
async def test_obtener_metricas_sin_datos():
	"""
	Verifica ceros y conserva el contrato de llamadas al repositorio.
	"""
	mock_session = AsyncMock(spec=AsyncSession)
	mock_contar_por_estado = AsyncMock(side_effect=[0, 0])
	mock_contar_total = AsyncMock(return_value=0)

	with (
		patch(
			'app.modules.dashboard.repository.contar_por_estado',
			new=mock_contar_por_estado,
		),
		patch(
			'app.modules.dashboard.repository.contar_total',
			new=mock_contar_total,
		),
	):
		result = await obtener_metricas(mock_session)

	assert result == {'disponibles': 0, 'rentadas': 0, 'total': 0}
	assert mock_contar_por_estado.await_args_list == [
		call(mock_session, EstadoPropiedad.DISPONIBLE),
		call(mock_session, EstadoPropiedad.RENTADA),
	]
	mock_contar_total.assert_awaited_once_with(mock_session)
