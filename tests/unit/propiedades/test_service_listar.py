"""Tests unitarios de listar_propiedades del servicio."""

from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.propiedades.service import (
	_format_area,
	_format_precio,
	listar_propiedades,
)


def _propiedad_fake(
	*,
	id: str = '00000000-0000-0000-0000-000000000001',
	titulo: str = 'Casa Test',
	direccion: str = 'Calle 123',
	ciudad: str = 'Miami',
	precio_mensual: Decimal = Decimal('1500.00'),
	habitaciones: int = 3,
	banos: int = 2,
	area: int = 850,
	estado: str = 'disponible',
	imagen: str | None = 'https://example.com/img.jpg',
	created_at: str = '2026-01-01T00:00:00Z',
) -> SimpleNamespace:
	"""
	Construye una propiedad falsa con argumentos por keyword.

	Reemplaza los AsyncMock verbosos por SimpleNamespace explícito
	para que las aserciones sobre ``.value`` y atributos sean más legibles.
	"""
	return SimpleNamespace(
		id=id,
		titulo=titulo,
		direccion=direccion,
		ciudad=ciudad,
		precio_mensual=precio_mensual,
		habitaciones=habitaciones,
		banos=banos,
		area=area,
		estado=SimpleNamespace(value=estado),
		imagen=imagen,
		created_at=created_at,
	)


class TestFormatPrecio:
	"""
	Pruebas de formato de precio.
	"""

	def test_formato_entero(self) -> None:
		"""
		Debe formatear 1500 como $1,500.00.
		"""
		assert _format_precio(Decimal('1500')) == '$1,500.00'

	def test_formato_decimal(self) -> None:
		"""
		Debe formatear 2500.50 como $2,500.50.
		"""
		assert _format_precio(Decimal('2500.50')) == '$2,500.50'

	def test_formato_float(self) -> None:
		"""
		Debe aceptar float y formatearlo correctamente.
		"""
		assert _format_precio(1000.0) == '$1,000.00'

	def test_formato_miles(self) -> None:
		"""
		Debe usar separador de miles.
		"""
		assert _format_precio(Decimal('1000000')) == '$1,000,000.00'


class TestFormatArea:
	"""
	Pruebas de formato de área.
	"""

	def test_formato_pequeno(self) -> None:
		"""
		Debe formatear 500 como 500 m².
		"""
		assert _format_area(500) == '500 m²'

	def test_formato_miles(self) -> None:
		"""
		Debe formatear 1000 como 1,000 m².
		"""
		assert _format_area(1000) == '1,000 m²'

	def test_formato_grande(self) -> None:
		"""
		Debe formatear 10000 como 10,000 m².
		"""
		assert _format_area(10000) == '10,000 m²'


class TestListarPropiedades:
	"""
	Pruebas de listar_propiedades.
	"""

	@pytest.mark.asyncio
	async def test_retorna_dicts_con_campos_y_usa_session(self) -> None:
		"""
		Verifica el dict exacto con los 11 campos esperados y que la
		sesión se propaga al repositorio.
		"""
		mock_prop = _propiedad_fake()
		mock_session = AsyncMock(spec=AsyncSession)
		mock_listar = AsyncMock(return_value=[mock_prop])

		with patch(
			'app.modules.propiedades.service.repo_listar',
			new=mock_listar,
		):
			resultado = await listar_propiedades(mock_session)

		assert resultado == [
			{
				'id': '00000000-0000-0000-0000-000000000001',
				'titulo': 'Casa Test',
				'direccion': 'Calle 123',
				'ciudad': 'Miami',
				'precio_mensual': '$1,500.00',
				'habitaciones': 3,
				'banos': 2,
				'area': '850 m²',
				'estado': 'disponible',
				'imagen': 'https://example.com/img.jpg',
				'created_at': '2026-01-01T00:00:00Z',
			},
		]
		mock_listar.assert_awaited_once_with(mock_session)

	@pytest.mark.asyncio
	async def test_lista_vacia_retorna_lista_vacia(self) -> None:
		"""
		Verifica que lista vacía del repo retorna ``[]`` y conserva la
		propagación de la sesión.
		"""
		mock_session = AsyncMock(spec=AsyncSession)
		mock_listar = AsyncMock(return_value=[])

		with patch(
			'app.modules.propiedades.service.repo_listar',
			new=mock_listar,
		):
			resultado = await listar_propiedades(mock_session)

		assert resultado == []
		mock_listar.assert_awaited_once_with(mock_session)

	@pytest.mark.asyncio
	async def test_precio_con_decimales_formato_correcto(self) -> None:
		"""
		Verifica formato de precio con centavos no redondos.
		"""
		mock_prop = _propiedad_fake(
			id='id',
			titulo='T',
			direccion='D',
			ciudad='C',
			precio_mensual=Decimal('1234.50'),
			habitaciones=1,
			banos=1,
			area=100,
			estado='rentada',
			imagen='',
			created_at='',
		)
		mock_session = AsyncMock(spec=AsyncSession)
		mock_listar = AsyncMock(return_value=[mock_prop])

		with patch(
			'app.modules.propiedades.service.repo_listar',
			new=mock_listar,
		):
			resultado = await listar_propiedades(mock_session)

		assert resultado[0]['precio_mensual'] == '$1,234.50'
		mock_listar.assert_awaited_once_with(mock_session)

	@pytest.mark.asyncio
	async def test_imagen_none_se_normaliza_a_string_vacio(self) -> None:
		"""
		Verifica que ``imagen=None`` se transforma a ``''`` en la salida.

		El servicio usa ``p.imagen if p.imagen else ''`` para activar el
		placeholder visual cuando la imagen está ausente o es nula.
		"""
		mock_prop = _propiedad_fake(imagen=None)
		mock_session = AsyncMock(spec=AsyncSession)
		mock_listar = AsyncMock(return_value=[mock_prop])

		with patch(
			'app.modules.propiedades.service.repo_listar',
			new=mock_listar,
		):
			resultado = await listar_propiedades(mock_session)

		assert resultado[0]['imagen'] == ''
		mock_listar.assert_awaited_once_with(mock_session)
