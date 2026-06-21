"""Lógica de negocio del módulo de propiedades."""

import logging
from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.propiedades.models import EstadoPropiedad
from app.modules.propiedades.repository import crear as repo_crear
from app.modules.propiedades.repository import listar as repo_listar
from app.modules.propiedades.schemas import (
	PropiedadFormIn,
	PropiedadIn,
	PropiedadOut,
)

logger = logging.getLogger(__name__)


def validar_estado(valor: str) -> EstadoPropiedad:
	"""
	Valida que un string corresponda a un estado del catálogo.

	Lanza ValueError si el estado no es válido.
	"""
	try:
		return EstadoPropiedad(valor)
	except ValueError:
		raise ValueError(
			f"Estado '{valor}' no válido. Debe ser uno de: "
			f'{[e.value for e in EstadoPropiedad]}'
		) from None


def _formatear_url_picsum(ancho: int, alto: int) -> str:
	"""
	Construye la URL de picsum.photos con las dimensiones dadas.

	Función helper aislada para facilitar el mocking del path defensivo
	de ``_generar_url_imagen``.
	"""
	return f'https://picsum.photos/{ancho}/{alto}'


def _generar_url_imagen(ancho: int = 800, alto: int = 600) -> str:
	"""
	Genera una URL de imagen determinista vía picsum.photos.

	Si el formato falla por motivos excepcionales, retorna cadena vacía
	para activar el placeholder visual del listado.
	"""
	try:
		return _formatear_url_picsum(ancho, alto)
	except Exception:
		logger.exception('imagen.generar.fallo')
		return ''


async def crear_propiedad(
	session: AsyncSession,
	payload: PropiedadIn,
) -> PropiedadOut:
	"""
	Crea una propiedad aplicando reglas de negocio.
	"""
	logger.info(
		'propiedad.crear.inicio',
		extra={'titulo': payload.titulo},
	)
	entidad = await repo_crear(session, payload)
	logger.info(
		'propiedad.crear.ok',
		extra={'propiedad_id': str(entidad.id)},
	)
	return PropiedadOut.model_validate(entidad)


async def crear_propiedad_desde_formulario(
	session: AsyncSession,
	form: PropiedadFormIn,
) -> PropiedadOut | None:
	"""
	Crea una propiedad a partir de un formulario HTTP.

	Aplica los defaults que el usuario no completa en el form:
	- ``ciudad = "Miami"`` (FR-007).
	- ``estado = EstadoPropiedad.DISPONIBLE`` (FR-006).
	- ``imagen = _generar_url_imagen()`` (FR-008, FR-009).
	- ``area = form.area`` (default 0, FR-020).

	Retorna ``None`` cuando el repositorio lanza ``IntegrityError`` por
	duplicado de la constraint única (titulo, direccion, ciudad). En ese
	caso la sesión hace rollback y el caller debe interpretar ``None`` como
	"mostrar error global de duplicado al usuario".
	"""
	imagen = _generar_url_imagen()
	payload = PropiedadIn(
		titulo=form.titulo,
		direccion=form.direccion,
		ciudad='Miami',
		precio_mensual=form.precio_mensual,
		habitaciones=form.habitaciones,
		banos=form.banos,
		area=form.area,
		estado=EstadoPropiedad.DISPONIBLE,
		imagen=imagen,
	)
	logger.info(
		'propiedad.crear_formulario.inicio',
		extra={'titulo': form.titulo},
	)
	try:
		entidad = await repo_crear(session, payload)
	except IntegrityError:
		await session.rollback()
		logger.warning(
			'propiedad.crear_formulario.duplicado',
			extra={'titulo': form.titulo, 'direccion': form.direccion},
		)
		return None
	logger.info(
		'propiedad.crear_formulario.ok',
		extra={'propiedad_id': str(entidad.id)},
	)
	return PropiedadOut.model_validate(entidad)


def _format_precio(valor: Decimal | float) -> str:
	"""
	Formatea un Decimal o float como moneda: $X,XXX.00.
	"""
	if isinstance(valor, float):
		valor = Decimal(str(valor))
	quantized = valor.quantize(Decimal('0.01'))
	parte_entera, parte_decimal = str(quantized).split('.')
	entera_formateada = f'{int(parte_entera):,}'
	return f'${entera_formateada}.{parte_decimal:0<2}'


def _format_area(valor: int) -> str:
	"""
	Formatea un entero como área: X,XXX m².
	"""
	return f'{valor:,} m²'


async def listar_propiedades(
	session: AsyncSession,
) -> list[dict[str, object]]:
	"""
	Obtiene y formatea todas las propiedades para el template del grid.
	"""
	propiedades = await repo_listar(session)
	return [
		{
			'id': str(p.id),
			'titulo': p.titulo,
			'direccion': p.direccion,
			'ciudad': p.ciudad,
			'precio_mensual': _format_precio(p.precio_mensual),
			'habitaciones': p.habitaciones,
			'banos': p.banos,
			'area': _format_area(p.area),
			'estado': p.estado.value,
			'imagen': p.imagen if p.imagen else '',
			'created_at': str(p.created_at),
		}
		for p in propiedades
	]
