"""Tests unitarios de listar_propiedades del servicio."""

from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.propiedades.service import (
	_format_area,
	_format_precio,
	listar_propiedades,
)


class TestFormatPrecio:
	"""Pruebas de formato de precio."""

	def test_formato_entero(self) -> None:
		"""Debe formatear 1500 como $1,500.00."""
		assert _format_precio(Decimal('1500')) == '$1,500.00'

	def test_formato_decimal(self) -> None:
		"""Debe formatear 2500.50 como $2,500.50."""
		assert _format_precio(Decimal('2500.50')) == '$2,500.50'

	def test_formato_float(self) -> None:
		"""Debe aceptar float y formatearlo correctamente."""
		assert _format_precio(1000.0) == '$1,000.00'

	def test_formato_miles(self) -> None:
		"""Debe usar separador de miles."""
		assert _format_precio(Decimal('1000000')) == '$1,000,000.00'


class TestFormatArea:
	"""Pruebas de formato de área."""

	def test_formato_pequeno(self) -> None:
		"""Debe formatear 500 como 500 m²."""
		assert _format_area(500) == '500 m²'

	def test_formato_miles(self) -> None:
		"""Debe formatear 1000 como 1,000 m²."""
		assert _format_area(1000) == '1,000 m²'

	def test_formato_grande(self) -> None:
		"""Debe formatear 10000 como 10,000 m²."""
		assert _format_area(10000) == '10,000 m²'


class TestListarPropiedades:
	"""Pruebas de listar_propiedades."""

	@pytest.mark.asyncio
	async def test_retorna_dicts_con_campos(self) -> None:
		"""Verifica que retorna lista de dicts con los 8 campos esperados."""
		mock_prop = AsyncMock()
		mock_prop.id = '00000000-0000-0000-0000-000000000001'
		mock_prop.titulo = 'Casa Test'
		mock_prop.direccion = 'Calle 123'
		mock_prop.ciudad = 'Miami'
		mock_prop.precio_mensual = Decimal('1500.00')
		mock_prop.habitaciones = 3
		mock_prop.banos = 2
		mock_prop.area = 850
		mock_prop.estado = AsyncMock(value='disponible')
		mock_prop.imagen = 'https://example.com/img.jpg'
		mock_prop.created_at = '2026-01-01T00:00:00Z'

		mock_session = AsyncMock(spec=AsyncSession)

		with patch(
			'app.modules.propiedades.service.repo_listar',
			new=AsyncMock(return_value=[mock_prop]),
		):
			resultado = await listar_propiedades(mock_session)

		assert len(resultado) == 1
		prop = resultado[0]
		assert prop['id'] == '00000000-0000-0000-0000-000000000001'
		assert prop['titulo'] == 'Casa Test'
		assert prop['direccion'] == 'Calle 123'
		assert prop['ciudad'] == 'Miami'
		assert prop['precio_mensual'] == '$1,500.00'
		assert prop['habitaciones'] == 3
		assert prop['banos'] == 2
		assert prop['area'] == '850 m²'
		assert prop['estado'] == 'disponible'
		assert prop['imagen'] == 'https://example.com/img.jpg'

	@pytest.mark.asyncio
	async def test_lista_vacia_retorna_lista_vacia(self) -> None:
		"""Verifica que lista vacía del repo retorna []."""
		mock_session = AsyncMock(spec=AsyncSession)

		with patch(
			'app.modules.propiedades.service.repo_listar',
			new=AsyncMock(return_value=[]),
		):
			resultado = await listar_propiedades(mock_session)

		assert resultado == []

	@pytest.mark.asyncio
	async def test_precio_con_decimales_formato_correcto(self) -> None:
		"""Verifica formato de precio con centavos no redondos."""
		mock_prop = AsyncMock()
		mock_prop.id = 'id'
		mock_prop.titulo = 'T'
		mock_prop.direccion = 'D'
		mock_prop.ciudad = 'C'
		mock_prop.precio_mensual = Decimal('1234.50')
		mock_prop.habitaciones = 1
		mock_prop.banos = 1
		mock_prop.area = 100
		mock_prop.estado = AsyncMock(value='rentada')
		mock_prop.imagen = ''
		mock_prop.created_at = ''

		mock_session = AsyncMock(spec=AsyncSession)

		with patch(
			'app.modules.propiedades.service.repo_listar',
			new=AsyncMock(return_value=[mock_prop]),
		):
			resultado = await listar_propiedades(mock_session)

		assert resultado[0]['precio_mensual'] == '$1,234.50'
