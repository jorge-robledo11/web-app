"""DTOs Pydantic v2 para el módulo de propiedades."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.propiedades.models import EstadoPropiedad


class PropiedadFormIn(BaseModel):
	"""
	DTO de entrada específico del formulario de creación HTTP.

	Contiene solo los campos que el usuario completa en el formulario.
	Los defaults de ``ciudad``, ``estado`` e ``imagen`` se aplican en
	``service.crear_propiedad_desde_formulario``.
	"""

	model_config = ConfigDict(frozen=True, extra='forbid')

	titulo: str = Field(min_length=1, max_length=255)
	direccion: str = Field(min_length=1, max_length=255)
	precio_mensual: Decimal = Field(gt=0)
	habitaciones: int = Field(ge=1, le=20)
	banos: int = Field(ge=1, le=10)
	area: int = Field(ge=0, default=0)

	@field_validator('titulo', 'direccion', mode='before')
	@classmethod
	def _strip_whitespace(cls, v: object) -> object:
		"""
		Elimina espacios en blanco al inicio y final de strings.
		"""
		if isinstance(v, str):
			return v.strip()
		return v


class PropiedadIn(BaseModel):
	"""
	DTO de entrada para crear o actualizar una propiedad.
	"""

	model_config = ConfigDict(frozen=True, extra='forbid')

	titulo: str
	direccion: str
	ciudad: str = 'Miami'
	precio_mensual: Decimal = Field(gt=0)
	habitaciones: int = Field(ge=1)
	banos: int = Field(ge=1)
	area: int = Field(ge=0, default=0)
	estado: EstadoPropiedad
	imagen: str

	@field_validator('estado', mode='before')
	@classmethod
	def validar_estado(cls, v: object) -> EstadoPropiedad:
		"""
		Valida que el estado pertenezca al catálogo cerrado.
		"""
		if isinstance(v, EstadoPropiedad):
			return v
		if isinstance(v, str):
			try:
				return EstadoPropiedad(v)
			except ValueError:
				raise ValueError(
					f"Estado '{v}' no válido. Debe ser uno de: "
					f'{[e.value for e in EstadoPropiedad]}'
				) from None
		raise ValueError(f'Tipo de estado no soportado: {type(v)}')


class PropiedadOut(BaseModel):
	"""
	DTO de salida con todos los campos, incluyendo id y timestamps.
	"""

	model_config = ConfigDict(frozen=True, from_attributes=True)

	id: UUID
	titulo: str
	direccion: str
	ciudad: str
	precio_mensual: Decimal
	habitaciones: int
	banos: int
	area: int
	estado: EstadoPropiedad
	imagen: str
	created_at: datetime
	updated_at: datetime
