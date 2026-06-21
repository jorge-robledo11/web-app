"""Tests unitarios del servicio de creación desde formulario."""

from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.exc import IntegrityError

from app.modules.propiedades.models import EstadoPropiedad
from app.modules.propiedades.schemas import PropiedadFormIn, PropiedadIn
from app.modules.propiedades.service import (
	_generar_url_imagen,
	crear_propiedad_desde_formulario,
)


class TestGenerarUrlImagen:
	"""
	Pruebas del helper de generación de URL de imagen.
	"""

	def test_retorna_url_picsum_formato_esperado(self) -> None:
		"""
		Debe retornar URL con formato https://picsum.photos/800/600.
		"""
		url = _generar_url_imagen()
		assert url == 'https://picsum.photos/800/600'

	def test_acepta_dimensiones_custom(self) -> None:
		"""
		Debe aceptar ancho y alto personalizados.
		"""
		url = _generar_url_imagen(ancho=400, alto=300)
		assert url == 'https://picsum.photos/400/300'

	def test_retorna_vacio_si_falla_formato(self) -> None:
		"""
		Debe retornar string vacío si el formato falla.
		"""
		with patch(
			'app.modules.propiedades.service._formatear_url_picsum',
			side_effect=Exception('formato falla'),
		):
			url = _generar_url_imagen()
		assert url == ''


class TestCrearPropiedadDesdeFormulario:
	"""
	Pruebas de la lógica de creación desde formulario.
	"""

	@pytest.fixture
	def form_valido(self) -> PropiedadFormIn:
		"""
		Fixture con un formulario válido.
		"""
		return PropiedadFormIn(
			titulo='Casa Form',
			direccion='Calle Form 100',
			precio_mensual=Decimal('1800.00'),
			habitaciones=2,
			banos=1,
			area=70,
		)

	@pytest.mark.asyncio
	async def test_aplica_defaults_ciudad_miami(
		self,
		form_valido: PropiedadFormIn,
	) -> None:
		"""
		Debe aplicar ciudad='Miami' por defecto.
		"""
		with patch(
			'app.modules.propiedades.service.repo_crear',
			new=AsyncMock(),
		) as mock_crear:
			mock_crear.return_value = AsyncMock(
				id='00000000-0000-0000-0000-000000000001',
				titulo=form_valido.titulo,
				direccion=form_valido.direccion,
				ciudad='Miami',
				precio_mensual=form_valido.precio_mensual,
				habitaciones=form_valido.habitaciones,
				banos=form_valido.banos,
				area=form_valido.area,
				estado=EstadoPropiedad.DISPONIBLE,
				imagen='https://picsum.photos/800/600',
				created_at='2026-06-20T00:00:00Z',
				updated_at='2026-06-20T00:00:00Z',
			)
			await crear_propiedad_desde_formulario(AsyncMock(), form_valido)
			llamada = mock_crear.call_args
			payload: PropiedadIn = llamada[0][1]
			assert payload.ciudad == 'Miami'

	@pytest.mark.asyncio
	async def test_aplica_default_estado_disponible(
		self,
		form_valido: PropiedadFormIn,
	) -> None:
		"""
		Debe aplicar estado=EstadoPropiedad.DISPONIBLE por defecto.
		"""
		with patch(
			'app.modules.propiedades.service.repo_crear',
			new=AsyncMock(),
		) as mock_crear:
			mock_crear.return_value = AsyncMock(
				id='00000000-0000-0000-0000-000000000001',
				titulo=form_valido.titulo,
				direccion=form_valido.direccion,
				ciudad='Miami',
				precio_mensual=form_valido.precio_mensual,
				habitaciones=form_valido.habitaciones,
				banos=form_valido.banos,
				area=form_valido.area,
				estado=EstadoPropiedad.DISPONIBLE,
				imagen='https://picsum.photos/800/600',
				created_at='2026-06-20T00:00:00Z',
				updated_at='2026-06-20T00:00:00Z',
			)
			await crear_propiedad_desde_formulario(AsyncMock(), form_valido)
			llamada = mock_crear.call_args
			payload: PropiedadIn = llamada[0][1]
			assert payload.estado == EstadoPropiedad.DISPONIBLE

	@pytest.mark.asyncio
	async def test_genera_imagen_no_vacia(
		self,
		form_valido: PropiedadFormIn,
	) -> None:
		"""
		Debe generar una imagen no vacía vía _generar_url_imagen.
		"""
		with patch(
			'app.modules.propiedades.service.repo_crear',
			new=AsyncMock(),
		) as mock_crear:
			mock_crear.return_value = AsyncMock(
				id='00000000-0000-0000-0000-000000000001',
				titulo=form_valido.titulo,
				direccion=form_valido.direccion,
				ciudad='Miami',
				precio_mensual=form_valido.precio_mensual,
				habitaciones=form_valido.habitaciones,
				banos=form_valido.banos,
				area=form_valido.area,
				estado=EstadoPropiedad.DISPONIBLE,
				imagen='https://picsum.photos/800/600',
				created_at='2026-06-20T00:00:00Z',
				updated_at='2026-06-20T00:00:00Z',
			)
			await crear_propiedad_desde_formulario(AsyncMock(), form_valido)
			llamada = mock_crear.call_args
			payload: PropiedadIn = llamada[0][1]
			assert payload.imagen != ''
			assert payload.imagen.startswith('https://')

	@pytest.mark.asyncio
	async def test_propag_area_cero(self) -> None:
		"""
		form.area=0 debe propagarse a PropiedadIn.area=0.
		"""
		form = PropiedadFormIn(
			titulo='Sin Area',
			direccion='Calle Sin Area 1',
			precio_mensual=Decimal('1000.00'),
			habitaciones=1,
			banos=1,
			area=0,
		)
		with patch(
			'app.modules.propiedades.service.repo_crear',
			new=AsyncMock(),
		) as mock_crear:
			mock_crear.return_value = AsyncMock(
				id='00000000-0000-0000-0000-000000000001',
				titulo=form.titulo,
				direccion=form.direccion,
				ciudad='Miami',
				precio_mensual=form.precio_mensual,
				habitaciones=form.habitaciones,
				banos=form.banos,
				area=0,
				estado=EstadoPropiedad.DISPONIBLE,
				imagen='https://picsum.photos/800/600',
				created_at='2026-06-20T00:00:00Z',
				updated_at='2026-06-20T00:00:00Z',
			)
			await crear_propiedad_desde_formulario(AsyncMock(), form)
			llamada = mock_crear.call_args
			payload: PropiedadIn = llamada[0][1]
			assert payload.area == 0

	@pytest.mark.asyncio
	async def test_retorna_none_en_duplicado(
		self,
		form_valido: PropiedadFormIn,
	) -> None:
		"""
		Debe retornar None y hacer rollback cuando hay IntegrityError.
		"""
		mock_session = AsyncMock()
		with patch(
			'app.modules.propiedades.service.repo_crear',
			new=AsyncMock(side_effect=IntegrityError('dup', {}, Exception())),
		):
			resultado = await crear_propiedad_desde_formulario(
				mock_session,
				form_valido,
			)
		assert resultado is None
		mock_session.rollback.assert_awaited_once()

	@pytest.mark.asyncio
	async def test_retorna_dto_en_exito(
		self,
		form_valido: PropiedadFormIn,
	) -> None:
		"""
		Debe retornar PropiedadOut con id y estado en éxito.
		"""
		mock_entidad = AsyncMock(
			id='00000000-0000-0000-0000-000000000001',
			titulo=form_valido.titulo,
			direccion=form_valido.direccion,
			ciudad='Miami',
			precio_mensual=form_valido.precio_mensual,
			habitaciones=form_valido.habitaciones,
			banos=form_valido.banos,
			area=form_valido.area,
			estado=EstadoPropiedad.DISPONIBLE,
			imagen='https://picsum.photos/800/600',
			created_at='2026-06-20T00:00:00Z',
			updated_at='2026-06-20T00:00:00Z',
		)
		with patch(
			'app.modules.propiedades.service.repo_crear',
			new=AsyncMock(return_value=mock_entidad),
		):
			resultado = await crear_propiedad_desde_formulario(
				AsyncMock(),
				form_valido,
			)
		assert resultado is not None
		assert str(resultado.id) == '00000000-0000-0000-0000-000000000001'
		assert resultado.estado == EstadoPropiedad.DISPONIBLE
		assert resultado.titulo == 'Casa Form'
