# Research: Propiedades base

**Feature**: 004-propiedades-base
**Phase**: 0 — Research
**Date**: 2026-06-14

## Decisiones técnicas investigadas

### 1. Modelado de estados de dominio con SQLAlchemy + PostgreSQL

**Decisión**: Usar `StrEnum` de Python + `sqlalchemy.Enum` con `create_type=True`
en la declaración de columna.

**Alternativas consideradas**:
- `sa.Enum` con `create_type=False` + creación explícita vía `op.execute`: rechazada
  por riesgo de doble creación y violación de NFR-DB-001.
- `String` + validación en aplicación: rechazada por prohibición de strings
  mágicos (constitución III).
- `Integer` + enum en Python: rechazada, menos legible en SQL directo.

**Fundamento**: `sa.Enum(EstadoPropiedad, create_type=True)` declarado en
`mapped_column` crea el tipo PostgreSQL implícitamente en la migración de
creación de tabla. Esto cumple NFR-DB-001 y NFR-DB-002.

### 2. Estrategia de seed idempotente

**Decisión**: Script independiente con `ON CONFLICT (titulo, direccion, ciudad)
DO UPDATE`.

**Alternativas consideradas**:
- Seed dentro de migración Alembic: rechazada, mezcla estructura con datos.
- `INSERT ... WHERE NOT EXISTS`: rechazada, no actualiza registros existentes.
- `DELETE` + `INSERT`: rechazada, pierde `created_at` original.

**Fundamento**: Upsert por clave compuesta de negocio garantiza idempotencia sin
perder trazabilidad temporal. Script Python independiente permite re-ejecución
sin depender de Alembic.

### 3. Timestamps server-side

**Decisión**: `server_default=sa.func.now()` y `onupdate=sa.func.now()` en la
definición de columna. Sin envío de valores desde Python.

**Alternativas consideradas**:
- `default=datetime.utcnow` en Python: rechazada, mezcla zona horaria.
- `server_default=sa.text("now()")`: rechazada, menos portable.

**Fundamento**: `sa.func.now()` genera `now()` en SQL, que PostgreSQL interpreta
como `timestamp with time zone` al inicio de la transacción. `onupdate` garantiza
actualización automática.

### 4. Imagen determinista por UUID

**Decisión**: Campo `imagen` como `String(512)` con URL generada a partir de hash
del UUID.

**Alternativas consideradas**:
- URL externa fija: rechazada, no determinista.
- Archivo local vendoreado: rechazado, agrega assets binarios al repo.
- Tabla separada de imágenes: rechazada, sobre-ingeniería para seed.

**Fundamento**: `f"https://images.unsplash.com/photo-{hash}?w=800"` donde `hash`
es `int(uuid.UUID(prop_id).int % 1000)` produce URLs estables y variadas sin
dependencias externas.

### 5. Conexión para seed script

**Decisión**: `create_async_engine(DATABASE_URL)` con `asyncpg`.

**Alternativas consideradas**:
- `psycopg2` / `psycopg`: rechazada por NFR-QA-005.
- `databases` library: rechazada, dependencia innecesaria.
- Reutilizar `AsyncSession` de FastAPI: rechazada, el seed es independiente de la app.

**Fundamento**: `create_async_engine` + `asyncpg` es el stack canónico del
proyecto. El script se ejecuta standalone sin depender de FastAPI.

### 6. Reversibilidad de migraciones

**Decisión**: `downgrade` que elimina la tabla y el enum.

**Alternativas consideradas**:
- `downgrade` como `pass`: rechazada por NFR-DB-005.
- Solo eliminar tabla sin eliminar enum: rechazada, deja el tipo huérfano.

**Fundamento**: `op.drop_table("propiedades")` seguido de
`op.execute("DROP TYPE estado_propiedad")` garantiza reversibilidad completa.
