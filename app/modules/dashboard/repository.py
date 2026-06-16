"""Acceso a datos del módulo de dashboard."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.propiedades.models import EstadoPropiedad
from app.modules.propiedades.repository import contar_por_estado, contar_total


async def obtener_metricas(session: AsyncSession) -> dict[str, int]:
	"""
	Obtiene los conteos de propiedades por estado y total.

	Invoca funciones públicas del repositorio de propiedades sin
	importar la entidad Propiedad directamente.
	"""
	disponibles = await contar_por_estado(session, EstadoPropiedad.DISPONIBLE)
	rentadas = await contar_por_estado(session, EstadoPropiedad.RENTADA)
	total = await contar_total(session)
	return {'disponibles': disponibles, 'rentadas': rentadas, 'total': total}
