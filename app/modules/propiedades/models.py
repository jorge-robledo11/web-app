"""Entidad Propiedad y catálogo cerrado de estados."""

import enum
import uuid

from sqlalchemy import (
	Enum,
	Index,
	Integer,
	Numeric,
	String,
	UniqueConstraint,
	func,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class EstadoPropiedad(enum.StrEnum):
	"""
	Catálogo cerrado de estados operativos de una propiedad.
	"""

	DISPONIBLE = 'disponible'
	RENTADA = 'rentada'
	MANTENIMIENTO = 'mantenimiento'
	INACTIVA = 'inactiva'


class Propiedad(Base):
	"""
	Propiedad inmobiliaria gestionada por el realtor.
	"""

	__tablename__ = 'propiedades'

	id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True),
		primary_key=True,
		server_default=func.gen_random_uuid(),
	)
	titulo: Mapped[str] = mapped_column(String(255), nullable=False)
	direccion: Mapped[str] = mapped_column(String(255), nullable=False)
	ciudad: Mapped[str] = mapped_column(
		String(100),
		nullable=False,
		default='Miami',
	)
	precio_mensual: Mapped[float] = mapped_column(
		Numeric(10, 2),
		nullable=False,
	)
	habitaciones: Mapped[int] = mapped_column(Integer, nullable=False)
	banos: Mapped[int] = mapped_column(Integer, nullable=False)
	area: Mapped[int] = mapped_column(Integer, nullable=False)
	estado: Mapped[EstadoPropiedad] = mapped_column(
		Enum(
			EstadoPropiedad,
			name='estado_propiedad',
			create_type=True,
			values_callable=lambda x: [e.value for e in x],
		),
		nullable=False,
	)
	imagen: Mapped[str] = mapped_column(String(512), nullable=False)
	created_at: Mapped[str] = mapped_column(
		TIMESTAMP(timezone=True),
		nullable=False,
		server_default=func.now(),
	)
	updated_at: Mapped[str] = mapped_column(
		TIMESTAMP(timezone=True),
		nullable=False,
		server_default=func.now(),
		onupdate=func.now(),
	)

	__table_args__ = (
		UniqueConstraint(
			'titulo',
			'direccion',
			'ciudad',
			name='uq_propiedades_identidad_negocio',
		),
		Index('ix_propiedades_estado', 'estado'),
		Index('ix_propiedades_ciudad', 'ciudad'),
		Index('ix_propiedades_precio_mensual', 'precio_mensual'),
		{'comment': 'Propiedades inmobiliarias del sistema Realtor'},
	)

	def __repr__(self) -> str:
		"""
		Representación legible para depuración.
		"""
		return (
			f'<Propiedad(id={self.id!r}, titulo={self.titulo!r}, '
			f'estado={self.estado!r})>'
		)
