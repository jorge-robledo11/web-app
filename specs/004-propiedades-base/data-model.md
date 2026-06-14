# Data Model: Propiedades base

**Feature**: 004-propiedades-base
**Phase**: 1 — Design
**Date**: 2026-06-14

## Entidad: Propiedad

| Atributo | Tipo Python | Tipo PostgreSQL | Restricciones |
|----------|-------------|-----------------|---------------|
| `id` | `uuid.UUID` | `UUID` | PK, `server_default=gen_random_uuid()` |
| `titulo` | `str` | `VARCHAR(255)` | NOT NULL |
| `direccion` | `str` | `VARCHAR(255)` | NOT NULL |
| `ciudad` | `str` | `VARCHAR(100)` | NOT NULL, default `'Miami'` |
| `precio_mensual` | `Decimal` | `NUMERIC(10,2)` | NOT NULL, > 0 |
| `habitaciones` | `int` | `INTEGER` | NOT NULL, >= 1 |
| `banos` | `int` | `INTEGER` | NOT NULL, >= 1 |
| `area` | `int` | `INTEGER` | NOT NULL, > 0 (sq ft) |
| `estado` | `EstadoPropiedad` | `estado_propiedad` | NOT NULL, enum tipado |
| `imagen` | `str` | `VARCHAR(512)` | NOT NULL |
| `created_at` | `datetime` | `TIMESTAMPTZ` | NOT NULL, `server_default=now()` |
| `updated_at` | `datetime` | `TIMESTAMPTZ` | NOT NULL, `server_default=now()`, `onupdate=now()` |

### Unique constraint de negocio

```sql
UNIQUE (titulo, direccion, ciudad)
```

Esta constraint es la base del upsert idempotente del seed (FR-004, FR-005).

## Enum: EstadoPropiedad

| Valor | Significado |
|-------|-------------|
| `disponible` | Propiedad lista para alquilar |
| `rentada` | Propiedad con contrato activo |
| `mantenimiento` | Propiedad en reparación o mejora |
| `inactiva` | Propiedad fuera del mercado |

### Definición en Python

```python
import enum

class EstadoPropiedad(enum.StrEnum):
    DISPONIBLE = "disponible"
    RENTADA = "rentada"
    MANTENIMIENTO = "mantenimiento"
    INACTIVA = "inactiva"
```

### Definición en SQLAlchemy

```python
from sqlalchemy import Enum

mapped_column(
    Enum(EstadoPropiedad, name="estado_propiedad", create_type=True),
    nullable=False,
)
```

### Creación en migración

El tipo `estado_propiedad` se crea implícitamente cuando Alembic genera el DDL
de `CREATE TABLE propiedades`. No se requiere `op.execute("CREATE TYPE ...")`
explícito.

## Índices

| Índice | Columnas | Propósito |
|--------|----------|-----------|
| `ix_propiedades_estado` | `estado` | Filtrado por estado |
| `ix_propiedades_ciudad` | `ciudad` | Filtrado por ciudad |
| `ix_propiedades_precio_mensual` | `precio_mensual` | Ordenamiento por precio |

## Relaciones

Ninguna en esta feature. La entidad `Propiedad` no tiene claves foráneas en su
versión inicial. Las relaciones con `propietarios`, `inquilinos` y `contratos`
se agregarán en specs posteriores.

## Seed data: 10 propiedades de Miami

| # | Título | Dirección | Ciudad | Precio | Hab. | Baños | Área | Estado |
|---|--------|-----------|--------|--------|------|-------|------|--------|
| 1 | Sunny Palms Apartments | 123 Ocean Drive | Miami | 2500.00 | 2 | 1 | 850 | disponible |
| 2 | Bayfront Lofts | 456 Biscayne Blvd | Miami | 3200.00 | 3 | 2 | 1200 | disponible |
| 3 | Coconut Grove Studio | 789 Main Highway | Miami | 1800.00 | 1 | 1 | 550 | disponible |
| 4 | Brickell Heights | 1000 Brickell Ave | Miami | 4200.00 | 3 | 2 | 1500 | disponible |
| 5 | Little Havana Casa | 234 Calle Ocho | Miami | 1500.00 | 2 | 1 | 700 | rentada |
| 6 | Design District Loft | 567 NE 2nd Ave | Miami | 3800.00 | 2 | 2 | 1100 | rentada |
| 7 | Wynwood Arts Residence | 890 NW 3rd Ave | Miami | 2900.00 | 2 | 1 | 950 | rentada |
| 8 | Coral Gables Manor | 345 Miracle Mile | Miami | 5500.00 | 4 | 3 | 2200 | mantenimiento |
| 9 | Key Biscayne Villa | 678 Crandon Blvd | Miami | 6500.00 | 4 | 3 | 2800 | mantenimiento |
| 10 | South Beach Retreat | 901 Collins Ave | Miami | 2000.00 | 1 | 1 | 600 | inactiva |

La imagen de cada propiedad es determinista: `f"https://images.unsplash.com/photo-{hash}?w=800"`
donde `hash = int(uuid.UUID(prop.id).int % 1000)`.
