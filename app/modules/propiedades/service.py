"""Lógica de negocio del módulo de propiedades."""

import logging
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.propiedades.models import EstadoPropiedad
from app.modules.propiedades.repository import crear as repo_crear
from app.modules.propiedades.repository import listar as repo_listar
from app.modules.propiedades.schemas import PropiedadIn, PropiedadOut

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
