"""Pruebas del servicio de propiedades."""

from decimal import Decimal

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.propiedades.models import EstadoPropiedad
from app.modules.propiedades.schemas import PropiedadIn
from app.modules.propiedades.service import crear_propiedad, validar_estado


class TestServicioPropiedades:
	"""Pruebas de lógica de negocio."""

	@pytest_asyncio.fixture
	async def datos_validos(self) -> dict[str, object]:
		"""Fixture con datos de entrada válidos."""
		return {
			'titulo': 'Test Service',
			'direccion': 'Calle Service 123',
			'ciudad': 'Miami',
			'precio_mensual': Decimal('1500.00'),
			'habitaciones': 2,
			'banos': 1,
			'area': 800,
			'estado': 'disponible',
			'imagen': 'https://example.com/service.jpg',
		}

	@pytest.mark.asyncio
	async def test_crear_propiedad_retorna_dto(
		self,
		async_session: AsyncSession,
		datos_validos: dict[str, object],
	) -> None:
		"""crear_propiedad debe retornar PropiedadOut."""
		dto = PropiedadIn(**datos_validos)
		resultado = await crear_propiedad(async_session, dto)
		assert resultado.titulo == 'Test Service'
		assert resultado.id is not None
		assert resultado.estado == EstadoPropiedad.DISPONIBLE

	async def test_validar_estado_valido(self) -> None:
		"""validar_estado debe aceptar estados del catálogo."""
		for estado in ('disponible', 'rentada', 'mantenimiento', 'inactiva'):
			result = validar_estado(estado)
			assert isinstance(result, EstadoPropiedad)

	def test_validar_estado_invalido_rechaza(self) -> None:
		"""validar_estado debe rechazar estados fuera del catálogo."""
		with pytest.raises(ValueError, match='Estado .* no válido'):
			validar_estado('vendida')

	@pytest.mark.asyncio
	async def test_crear_propiedad_rechaza_duplicado(
		self,
		async_session: AsyncSession,
		datos_validos: dict[str, object],
	) -> None:
		"""Crear duplicado por clave de negocio debe lanzar IntegrityError."""
		from sqlalchemy.exc import IntegrityError

		dto = PropiedadIn(**datos_validos)
		await crear_propiedad(async_session, dto)
		with pytest.raises(IntegrityError):
			await crear_propiedad(async_session, dto)
