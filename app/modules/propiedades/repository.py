"""Acceso a datos del módulo de propiedades."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.propiedades.models import EstadoPropiedad, Propiedad
from app.modules.propiedades.schemas import PropiedadIn


async def crear(session: AsyncSession, payload: PropiedadIn) -> Propiedad:
	"""
	Crea una nueva propiedad y la persiste.
	"""
	prop = Propiedad(
		titulo=payload.titulo,
		direccion=payload.direccion,
		ciudad=payload.ciudad,
		precio_mensual=payload.precio_mensual,
		habitaciones=payload.habitaciones,
		banos=payload.banos,
		area=payload.area,
		estado=payload.estado,
		imagen=payload.imagen,
	)
	session.add(prop)
	await session.flush()
	return prop


async def obtener_por_id(
	session: AsyncSession,
	prop_id: uuid.UUID,
) -> Propiedad | None:
	"""
	Obtiene una propiedad por su id o None.
	"""
	stmt = select(Propiedad).where(Propiedad.id == prop_id)
	result = await session.execute(stmt)
	return result.scalar_one_or_none()


async def listar(session: AsyncSession) -> list[Propiedad]:
	"""
	Lista todas las propiedades.
	"""
	stmt = select(Propiedad).order_by(Propiedad.created_at.desc())
	result = await session.execute(stmt)
	return list(result.scalars().all())


async def eliminar(session: AsyncSession, prop_id: uuid.UUID) -> bool:
	"""
	Elimina una propiedad por id. Retorna True si existía.
	"""
	prop = await obtener_por_id(session, prop_id)
	if prop is None:
		return False
	await session.delete(prop)
	await session.flush()
	return True


async def contar_por_estado(
	session: AsyncSession,
	estado: EstadoPropiedad,
) -> int:
	"""
	Cuenta propiedades por estado del catálogo.
	"""
	stmt = select(func.count(Propiedad.id)).where(Propiedad.estado == estado)
	result = await session.execute(stmt)
	return result.scalar_one()


async def contar_total(session: AsyncSession) -> int:
	"""
	Cuenta el total de propiedades persistidas.
	"""
	stmt = select(func.count(Propiedad.id))
	result = await session.execute(stmt)
	return result.scalar_one()
