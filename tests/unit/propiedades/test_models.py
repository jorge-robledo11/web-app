"""Pruebas unitarias del modelo Propiedad y enum EstadoPropiedad."""

import enum

from sqlalchemy import Enum, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from app.modules.propiedades.models import EstadoPropiedad, Propiedad


class TestEstadoPropiedad:
	"""Pruebas del catálogo cerrado de estados."""

	def test_es_str_enum(self) -> None:
		"""EstadoPropiedad debe ser un StrEnum."""
		assert issubclass(EstadoPropiedad, enum.StrEnum)

	def test_cuatro_valores(self) -> None:
		"""Debe tener exactamente 4 valores."""
		assert len(EstadoPropiedad) == 4

	def test_valores_esperados(self) -> None:
		"""Debe contener los 4 estados del catálogo."""
		valores = {e.value for e in EstadoPropiedad}
		assert valores == {'disponible', 'rentada', 'mantenimiento', 'inactiva'}


class TestPropiedad:
	"""Pruebas de la entidad Propiedad."""

	def test_tabla_es_propiedades(self) -> None:
		"""El __tablename__ debe ser 'propiedades'."""
		assert Propiedad.__tablename__ == 'propiedades'

	def test_once_atributos_minimos(self) -> None:
		"""Debe tener al menos 11 columnas mapeadas (FR-001)."""
		columnas = [c.name for c in Propiedad.__table__.columns]
		esperadas = {
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
		assert esperadas.issubset(set(columnas))

	def test_pk_es_uuid(self) -> None:
		"""La clave primaria debe ser UUID con server_default."""
		col = Propiedad.__table__.columns['id']
		assert isinstance(col.type, UUID)
		assert col.primary_key
		assert col.server_default is not None

	def test_tipo_columnas_obligatorias(self) -> None:
		"""Las columnas deben tener los tipos correctos."""
		cols = Propiedad.__table__.columns

		assert isinstance(cols['titulo'].type, String)
		assert isinstance(cols['direccion'].type, String)
		assert isinstance(cols['ciudad'].type, String)
		assert isinstance(cols['precio_mensual'].type, Numeric)
		assert isinstance(cols['habitaciones'].type, Integer)
		assert isinstance(cols['banos'].type, Integer)
		assert isinstance(cols['area'].type, Integer)
		assert isinstance(cols['imagen'].type, String)

	def test_columna_estado_es_enum(self) -> None:
		"""La columna estado debe ser un sa.Enum de EstadoPropiedad."""
		col = Propiedad.__table__.columns['estado']
		assert isinstance(col.type, Enum)
		assert col.type.enum_class is EstadoPropiedad

	def test_timestamps_server_default(self) -> None:
		"""created_at y updated_at deben tener server_default."""
		assert Propiedad.__table__.columns['created_at'].server_default is not None
		assert Propiedad.__table__.columns['updated_at'].server_default is not None
		assert isinstance(Propiedad.__table__.columns['created_at'].type, TIMESTAMP)
		assert isinstance(Propiedad.__table__.columns['updated_at'].type, TIMESTAMP)

	def test_unique_constraint_negocio(self) -> None:
		"""Debe existir UniqueConstraint sobre (titulo, direccion, ciudad)."""
		constraints = Propiedad.__table__.constraints  # type: ignore[attr-defined]
		uc = next(
			(c for c in constraints if isinstance(c, UniqueConstraint)),
			None,
		)
		assert uc is not None
		columnas_uc = {c.name for c in uc.columns}
		assert columnas_uc == {'titulo', 'direccion', 'ciudad'}

	def test_indices_declarados(self) -> None:
		"""Debe tener índices sobre estado, ciudad y precio_mensual."""
		nombres = {idx.name for idx in Propiedad.__table__.indexes}  # type: ignore[attr-defined]
		assert 'ix_propiedades_estado' in nombres
		assert 'ix_propiedades_ciudad' in nombres
		assert 'ix_propiedades_precio_mensual' in nombres

	def test_columnas_not_null(self) -> None:
		"""Las columnas de negocio deben ser NOT NULL."""
		columnas_requeridas = {
			'titulo',
			'direccion',
			'ciudad',
			'precio_mensual',
			'habitaciones',
			'banos',
			'area',
			'estado',
			'imagen',
		}
		for nombre in columnas_requeridas:
			assert not Propiedad.__table__.columns[nombre].nullable, (
				f'Columna {nombre} debería ser NOT NULL'
			)
