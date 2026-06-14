# Implementation Plan: Propiedades base

**Branch**: `004-propiedades-base` | **Date**: 2026-06-14 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/004-propiedades-base/spec.md`

## Summary

Habilitar el dominio `propiedades` como primer módulo vertical del proyecto Realtor.
Crear la tabla `propiedades` con catálogo cerrado de estados vía enum tipado,
migración Alembic reversible, y carga inicial idempotente de 10 propiedades de
Miami. La feature es puramente de capa de datos: no incluye endpoints HTTP ni
cambios visuales.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI, SQLAlchemy 2.x async, Alembic, asyncpg, Pydantic v2
**Storage**: PostgreSQL vía Docker Compose
**Testing**: pytest + pytest-asyncio + httpx.AsyncClient + Testcontainers
**Target Platform**: Linux server (desarrollo local con Docker)
**Project Type**: web-service (monolito FastAPI + Jinja2/HTMX)
**Performance Goals**: N/A (capa de datos sin endpoints)
**Constraints**: Migraciones reversibles, timestamps server-side, sin psycopg2
**Scale/Scope**: 1 tabla, 1 enum, 10 filas de seed

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Regla | Estado | Evidencia |
|-------|--------|-----------|
| II. Stack: Python 3.13+, uv, FastAPI, SQLAlchemy async, Alembic, Pydantic v2 | ✅ | plan usa stack canónico |
| II. Stack: asyncpg para PostgreSQL | ✅ | seed script usa `create_async_engine` + asyncpg |
| III. Prohibiciones: sin `Column`, `Query`, sesiones sync | ✅ | `Mapped[...]`, `mapped_column`, `AsyncSession` |
| III. Prohibiciones: sin strings mágicos para estados | ✅ | `StrEnum` + `Enum` de SQLAlchemy |
| III. Prohibiciones: sin `.yml` | ✅ | contracts usan `.yaml` |
| III. Prohibiciones: sin exponer entidades SQLAlchemy como HTTP | ✅ | sin endpoints en esta feature |
| IV. Vertical Slice: módulo en `app/modules/propiedades/` | ✅ | estructura completa del slice |
| VIII. TDD: pruebas primero | ✅ | tests de modelo, estados, seed y migraciones |
| X. Base de datos: PostgreSQL local, Alembic, `.env.example` | ✅ | migración reversible, seed idempotente |
| XI. Async-First: I/O asíncrono | ✅ | repositorio y servicio async |
| XII. Blindaje visual: sin modificar tokens protegidos | ✅ | VTG-001 a VTG-006 |
| XIV. Contratos: DTOs con `frozen=True` | ✅ | schemas Pydantic v2 |

## Project Structure

### Documentation (this feature)

```text
specs/004-propiedades-base/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── propiedades.yaml # Contrato de entidad y seed
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
app/modules/propiedades/
├── __init__.py
├── models.py            # Entidad Propiedad + Enum EstadoPropiedad
├── schemas.py           # DTOs Pydantic v2 (PropiedadIn, PropiedadOut)
├── repository.py        # Acceso a datos async
├── service.py           # Lógica de negocio (validación de estados, upsert)
├── routes.py            # Placeholder (sin endpoints en esta feature)
├── templates/           # Placeholder (sin vistas en esta feature)
└── tests/
    ├── __init__.py
    ├── conftest.py      # Fixtures: async session, testcontainers
    ├── test_models.py   # Pruebas de entidad y enum
    ├── test_schemas.py  # Pruebas de validación Pydantic
    ├── test_repository.py
    ├── test_service.py
    └── test_seed.py     # Pruebas de carga inicial

alembic/versions/
└── 002_create_propiedades.py  # Migración de estructura

scripts/
└── seed_propiedades.py  # Script de carga inicial idempotente
```

**Structure Decision**: Módulo vertical estándar bajo `app/modules/propiedades/`. El
script de seed es independiente de la aplicación FastAPI, ejecutable vía
`python scripts/seed_propiedades.py` después de `alembic upgrade head`.

## Complexity Tracking

> No se registran desviaciones de la constitución. Todas las reglas se cumplen.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | — | — |

## Riesgos técnicos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Doble creación del tipo enum `estado_propiedad` | Media | Alto | Declarar enum como tipo de columna con `create_type=True` solo en la migración de estructura. No invocar `sa.Enum.create()` explícitamente |
| Uso incorrecto de `op.execute(sql, params)` | Media | Alto | Usar exclusivamente `op.get_bind().execute(sa.text(...), {...})`. Revisar en code review |
| `:param::uuid` en `sa.text` | Alta | Medio | Usar `CAST(:param AS uuid)`. Validar con prueba de migración |
| Duplicación al re-ejecutar seed | Alta | Alto | `ON CONFLICT (titulo, direccion, ciudad) DO UPDATE`. Prueba de doble ejecución |
| Drift de imágenes entre ejecuciones | Baja | Bajo | URL determinista: `f"https://images.unsplash.com/photo-{seed}?w=800"` con seed derivado de UUID |
| Errores por fechas naive vs aware | Alta | Alto | `server_default=sa.func.now()` y `onupdate=sa.func.now()`. Sin envío de timestamps desde Python |
| Downgrade incompleto | Media | Alto | `downgrade` real: `op.drop_table("propiedades")` + eliminar enum. No `pass` |
| Historial Alembic inconsistente | Baja | Alto | Recuperación documentada: `DROP SCHEMA public CASCADE` + `CREATE SCHEMA public` + `alembic upgrade head` |
| Uso accidental de psycopg2/psycopg | Media | Medio | Dependencia solo en `asyncpg`. Revisar `pyproject.toml` |

## Gobernanza visual

Esta feature **no modifica archivos visuales protegidos**:

- ❌ `app/static/css/app.css` — sin cambios
- ❌ `app/static/icons/` — sin cambios
- ❌ `app/templates/base.html` — sin cambios
- ❌ `app/templates/components/` — sin cambios
- ❌ `app/templates/macros/` — sin cambios
- ❌ `app/modules/*/templates/` — sin cambios

Si una fase posterior toca archivos visuales protegidos, deberá trazarse en
`tasks.md` con marcador `[visual]`.
