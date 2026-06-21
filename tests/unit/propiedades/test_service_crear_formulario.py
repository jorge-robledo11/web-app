"""Tests unitarios del servicio de creación desde formulario y de creación directa."""

from datetime import datetime
from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest
from sqlalchemy.exc import IntegrityError

from app.modules.propiedades.models import EstadoPropiedad, Propiedad
from app.modules.propiedades.schemas import (
	PropiedadFormIn,
	PropiedadIn,
	PropiedadOut,
)
from app.modules.propiedades.service import (
	_generar_url_imagen,
	crear_propiedad,
	crear_propiedad_desde_formulario,
)


def _entidad_fake(
	payload: PropiedadIn,
	id: str = '00000000-0000-0000-0000-000000000001',
) -> AsyncMock:
	"""
	Construye una entidad ``Propiedad`` falsa para inyectar como retorno
	de ``repo_crear``. Usa ``AsyncMock`` con ``spec=Propiedad`` para que
	``PropiedadOut.model_validate`` funcione correctamente.
	"""
	entidad = AsyncMock(spec=Propiedad)
	entidad.id = id
	entidad.titulo = payload.titulo
	entidad.direccion = payload.direccion
	entidad.ciudad = payload.ciudad
	entidad.precio_mensual = payload.precio_mensual
	entidad.habitaciones = payload.habitaciones
	entidad.banos = payload.banos
	entidad.area = payload.area
	entidad.estado = payload.estado
	entidad.imagen = payload.imagen
	entidad.created_at = '2026-06-20T00:00:00Z'
	entidad.updated_at = '2026-06-20T00:00:00Z'
	return entidad


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


class TestCrearPropiedad:
	"""
	Pruebas de ``crear_propiedad``: variante API directa con ``PropiedadIn``.

	Cubre los 10 mutantes ``no_tests`` que mutmut reportó porque ninguna
	suite atacaba directamente la función pública de creación (solo se
	probaba ``crear_propiedad_desde_formulario``).
	"""

	@pytest.mark.asyncio
	async def test_crear_propiedad_pasa_session_y_payload_a_repo_crear(self) -> None:
		"""
		Verifica que ``crear_propiedad`` propaga ``session`` y ``payload``
		intactos a ``repo_crear`` y retorna ``PropiedadOut`` con los mismos
		campos que la entidad persistida.

		Nota: ``precio_mensual`` se pasa como ``float`` para evitar el bug
		conocido de mutmut 3.x + Pydantic v2 + ``Decimal`` documentado en
		``docs/testing/test-value-audit.md``. El campo se serializa a
		``Decimal`` internamente durante la validación.
		"""
		mock_session = AsyncMock()
		payload = PropiedadIn(
			titulo='Casa Test',
			direccion='Calle 123',
			ciudad='Miami',
			precio_mensual=1500.00,
			habitaciones=2,
			banos=1,
			area=80,
			estado=EstadoPropiedad.DISPONIBLE,
			imagen='https://example.com/img.jpg',
		)
		mock_entidad = _entidad_fake(payload)
		mock_repo_crear = AsyncMock(return_value=mock_entidad)

		with patch(
			'app.modules.propiedades.service.repo_crear',
			new=mock_repo_crear,
		):
			resultado = await crear_propiedad(mock_session, payload)

		mock_repo_crear.assert_awaited_once_with(mock_session, payload)
		assert isinstance(resultado, PropiedadOut)
		assert resultado.id == UUID('00000000-0000-0000-0000-000000000001')
		assert resultado.titulo == payload.titulo
		assert resultado.direccion == payload.direccion
		assert resultado.ciudad == payload.ciudad
		assert resultado.precio_mensual == payload.precio_mensual
		assert resultado.habitaciones == payload.habitaciones
		assert resultado.banos == payload.banos
		assert resultado.area == payload.area
		assert resultado.estado == payload.estado
		assert resultado.imagen == payload.imagen

	@pytest.mark.asyncio
	async def test_crear_propiedad_retorna_dto_con_todos_los_campos(self) -> None:
		"""
		Verifica que el DTO retornado contiene todos los campos esperados
		(``model_validate`` sobre la entidad), comparando campo a campo
		para evitar diferencias de canonicalización entre Decimal y
		datetime en entornos pytest vs mutmut.

		Nota: ``precio_mensual`` se pasa como ``float`` para evitar el bug
		conocido de mutmut 3.x + Pydantic v2 + ``Decimal`` documentado en
		``docs/testing/test-value-audit.md``.
		"""
		mock_session = AsyncMock()
		payload = PropiedadIn(
			titulo='Depto Polanco',
			direccion='Av. Presidente Masaryk 111',
			ciudad='CDMX',
			precio_mensual=3500.00,
			habitaciones=3,
			banos=2,
			area=180,
			estado=EstadoPropiedad.RENTADA,
			imagen='https://example.com/polanco.jpg',
		)
		mock_entidad = _entidad_fake(payload, id='aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee')
		mock_repo_crear = AsyncMock(return_value=mock_entidad)

		with patch(
			'app.modules.propiedades.service.repo_crear',
			new=mock_repo_crear,
		):
			resultado = await crear_propiedad(mock_session, payload)

		dumped = resultado.model_dump()
		assert dumped['id'] == UUID('aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee')
		assert dumped['titulo'] == 'Depto Polanco'
		assert dumped['direccion'] == 'Av. Presidente Masaryk 111'
		assert dumped['ciudad'] == 'CDMX'
		# Comparación numérica para evitar diferencias de canonicalización
		# Decimal entre pytest y mutmut.
		assert float(dumped['precio_mensual']) == 3500.00
		assert dumped['habitaciones'] == 3
		assert dumped['banos'] == 2
		assert dumped['area'] == 180
		assert dumped['estado'] == EstadoPropiedad.RENTADA
		assert dumped['imagen'] == 'https://example.com/polanco.jpg'
		# Comparación de fecha/hora naive para evitar diferencias de tzinfo
		# entre pytest y mutmut (Pydantic puede devolver naive o aware UTC
		# según el contexto de validación).
		assert dumped['created_at'].replace(tzinfo=None) == datetime(2026, 6, 20, 0, 0)
		assert dumped['updated_at'].replace(tzinfo=None) == datetime(2026, 6, 20, 0, 0)
		assert set(dumped.keys()) == {
			'id',
			'titulo',
			'direccion',
			'ciudad',
			'precio_mensual',
			'habitaciones',
			'banos',
			'area',
			'estado',
			'imagen',
			'created_at',
			'updated_at',
		}


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
			precio_mensual='1800.00',
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
			mock_crear.return_value = _entidad_fake(
				PropiedadIn(
					titulo=form_valido.titulo,
					direccion=form_valido.direccion,
					ciudad='Miami',
					precio_mensual=form_valido.precio_mensual,
					habitaciones=form_valido.habitaciones,
					banos=form_valido.banos,
					area=form_valido.area,
					estado=EstadoPropiedad.DISPONIBLE,
					imagen='https://picsum.photos/800/600',
				),
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
			mock_crear.return_value = _entidad_fake(
				PropiedadIn(
					titulo=form_valido.titulo,
					direccion=form_valido.direccion,
					ciudad='Miami',
					precio_mensual=form_valido.precio_mensual,
					habitaciones=form_valido.habitaciones,
					banos=form_valido.banos,
					area=form_valido.area,
					estado=EstadoPropiedad.DISPONIBLE,
					imagen='https://picsum.photos/800/600',
				),
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
		Debe generar una imagen no vacía vía ``_generar_url_imagen``.
		"""
		with patch(
			'app.modules.propiedades.service.repo_crear',
			new=AsyncMock(),
		) as mock_crear:
			mock_crear.return_value = _entidad_fake(
				PropiedadIn(
					titulo=form_valido.titulo,
					direccion=form_valido.direccion,
					ciudad='Miami',
					precio_mensual=form_valido.precio_mensual,
					habitaciones=form_valido.habitaciones,
					banos=form_valido.banos,
					area=form_valido.area,
					estado=EstadoPropiedad.DISPONIBLE,
					imagen='https://picsum.photos/800/600',
				),
			)
			await crear_propiedad_desde_formulario(AsyncMock(), form_valido)
			llamada = mock_crear.call_args
			payload: PropiedadIn = llamada[0][1]
			assert payload.imagen != ''
			assert payload.imagen.startswith('https://')

	@pytest.mark.asyncio
	async def test_propag_area_cero(self) -> None:
		"""
		``form.area=0`` debe propagarse a ``PropiedadIn.area=0``.
		"""
		form = PropiedadFormIn(
			titulo='Sin Area',
			direccion='Calle Sin Area 1',
			precio_mensual='1000.00',
			habitaciones=1,
			banos=1,
			area=0,
		)
		with patch(
			'app.modules.propiedades.service.repo_crear',
			new=AsyncMock(),
		) as mock_crear:
			mock_crear.return_value = _entidad_fake(
				PropiedadIn(
					titulo=form.titulo,
					direccion=form.direccion,
					ciudad='Miami',
					precio_mensual=form.precio_mensual,
					habitaciones=form.habitaciones,
					banos=form.banos,
					area=0,
					estado=EstadoPropiedad.DISPONIBLE,
					imagen='https://picsum.photos/800/600',
				),
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
		Debe retornar ``None`` y hacer ``rollback`` cuando hay ``IntegrityError``.
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
		Debe retornar ``PropiedadOut`` con id y estado en éxito.
		"""
		mock_entidad = _entidad_fake(
			PropiedadIn(
				titulo=form_valido.titulo,
				direccion=form_valido.direccion,
				ciudad='Miami',
				precio_mensual=form_valido.precio_mensual,
				habitaciones=form_valido.habitaciones,
				banos=form_valido.banos,
				area=form_valido.area,
				estado=EstadoPropiedad.DISPONIBLE,
				imagen='https://picsum.photos/800/600',
			),
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

	@pytest.mark.asyncio
	async def test_construye_payload_completo_y_usa_session(
		self,
		form_valido: PropiedadFormIn,
	) -> None:
		"""
		Verifica que ``crear_propiedad_desde_formulario`` construye el
		``PropiedadIn`` completo (defaults aplicados) y propaga la sesión
		al ``repo_crear`` con ``assert_awaited_once`` y verificación de
		identidad de la sesión.
		"""
		mock_session = AsyncMock()
		mock_crear = AsyncMock()
		mock_crear.return_value = _entidad_fake(
			PropiedadIn(
				titulo=form_valido.titulo,
				direccion=form_valido.direccion,
				ciudad='Miami',
				precio_mensual=form_valido.precio_mensual,
				habitaciones=form_valido.habitaciones,
				banos=form_valido.banos,
				area=form_valido.area,
				estado=EstadoPropiedad.DISPONIBLE,
				imagen='https://picsum.photos/800/600',
			),
		)

		with patch(
			'app.modules.propiedades.service.repo_crear',
			new=mock_crear,
		):
			await crear_propiedad_desde_formulario(mock_session, form_valido)

		mock_crear.assert_awaited_once()
		assert mock_crear.await_args.args[0] is mock_session
		payload: PropiedadIn = mock_crear.await_args.args[1]
		assert payload.titulo == form_valido.titulo
		assert payload.direccion == form_valido.direccion
		assert payload.ciudad == 'Miami'
		assert payload.precio_mensual == form_valido.precio_mensual
		assert payload.habitaciones == form_valido.habitaciones
		assert payload.banos == form_valido.banos
		assert payload.area == form_valido.area
		assert payload.estado == EstadoPropiedad.DISPONIBLE
		assert payload.imagen != ''
		assert payload.imagen.startswith('https://')
