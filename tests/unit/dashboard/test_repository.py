"""Tests unitarios del repositorio de dashboard."""

from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.dashboard.repository import obtener_metricas


@pytest.mark.asyncio
async def test_obtener_metricas_con_datos():
	"""
	Verifica que obtener_metricas retorna conteos desde el repo de propiedades.
	"""
	mock_session = AsyncMock(spec=AsyncSession)
	with (
		patch(
			'app.modules.dashboard.repository.contar_por_estado',
			new=AsyncMock(side_effect=[5, 2]),
		),
		patch(
			'app.modules.dashboard.repository.contar_total',
			new=AsyncMock(return_value=10),
		),
	):
		result = await obtener_metricas(mock_session)

	assert result['disponibles'] == 5
	assert result['rentadas'] == 2
	assert result['total'] == 10


@pytest.mark.asyncio
async def test_obtener_metricas_sin_datos():
	"""
	Verifica que obtener_metricas retorna ceros cuando no hay propiedades.
	"""
	mock_session = AsyncMock(spec=AsyncSession)
	with (
		patch(
			'app.modules.dashboard.repository.contar_por_estado',
			new=AsyncMock(side_effect=[0, 0]),
		),
		patch(
			'app.modules.dashboard.repository.contar_total',
			new=AsyncMock(return_value=0),
		),
	):
		result = await obtener_metricas(mock_session)

	assert result['disponibles'] == 0
	assert result['rentadas'] == 0
	assert result['total'] == 0
