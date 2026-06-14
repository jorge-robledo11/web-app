"""Lógica de negocio del módulo de propiedades."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.propiedades.models import EstadoPropiedad
from app.modules.propiedades.repository import crear as repo_crear
from app.modules.propiedades.schemas import PropiedadIn, PropiedadOut

logger = logging.getLogger(__name__)


def validar_estado(valor: str) -> EstadoPropiedad:
	"""Valida que un string corresponda a un estado del catálogo.

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
	"""Crea una propiedad aplicando reglas de negocio."""
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
