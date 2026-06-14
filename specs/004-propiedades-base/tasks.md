# Tasks: Propiedades base

**Input**: Design documents from `/specs/004-propiedades-base/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, quickstart.md ✅, contracts/propiedades.yaml ✅, report.md ✅

**Tests**: Incluidas. Las pruebas deben escribirse primero y fallar antes de implementar (TDD).

**Organization**: Tareas agrupadas por fase. Cada fase depende de la anterior.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Puede ejecutarse en paralelo (archivos distintos, sin dependencias)
- **[Story]**: Historia de usuario asociada (US1, US2, US3)

## Path Conventions

- Módulo vertical: `app/modules/propiedades/`
- Tests: `app/modules/propiedades/tests/`
- Migraciones: `alembic/versions/`
- Scripts: `scripts/`

---

## Phase 1: Setup (Infraestructura compartida)

**Purpose**: Crear estructura del módulo y dependencias base

- [ ] T1.1 Crear estructura de directorios `app/modules/propiedades/` con `__init__.py`, `models.py`, `schemas.py`, `repository.py`, `service.py`, `routes.py`, `templates/__init__.py`, `tests/__init__.py`
- [ ] T1.2 [P] Crear `app/modules/propiedades/tests/conftest.py` con fixtures: `async_session` (Testcontainers PostgreSQL), `async_client` (httpx.AsyncClient)
- [ ] T1.3 [P] Verificar que `alembic/script.py.mako` está versionado y `alembic/env.py` configurado en modo async

**Checkpoint**: Estructura lista. Módulo vacío pero con todos los archivos placeholder.

---

## Phase 2: Foundational (Modelo y esquemas)

**Purpose**: Entidad Propiedad y catálogo de estados. Bloquea todas las fases siguientes.

**⚠️ CRITICAL**: Ninguna tarea de migración, seed o pruebas puede comenzar sin modelo y enum definidos.

### Tests for Phase 2 (escribir PRIMERO, verificar que fallen)

- [ ] T2.1 [P] [US3] Prueba de modelo: `test_models.py` — verifica que `Propiedad` tiene los 11 atributos (FR-001) y que `EstadoPropiedad` es un `StrEnum` con 4 valores (FR-002)
- [ ] T2.2 [P] [US3] Prueba de esquemas: `test_schemas.py` — verifica que `PropiedadIn` y `PropiedadOut` son Pydantic v2 con `frozen=True`, que rechazan estado inválido (FR-003)

### Implementation for Phase 2

- [ ] T2.3 [US1, US2, US3] Crear `app/modules/propiedades/models.py`: definir `EstadoPropiedad(StrEnum)` con `disponible`, `rentada`, `mantenimiento`, `inactiva`; definir entidad `Propiedad` con `Mapped[...]`, `mapped_column`, UUID PK, columnas NOT NULL, `UniqueConstraint(titulo, direccion, ciudad)`, `server_default=func.now()` en timestamps, `sa.Enum(EstadoPropiedad, create_type=True)` en estado, índices en `estado`, `ciudad`, `precio_mensual` (NFR-DB-001, NFR-DB-002, NFR-CODE-001, NFR-CODE-002)
- [ ] T2.4 [US1, US3] Crear `app/modules/propiedades/schemas.py`: `PropiedadIn` (todos los campos, sin id/created_at/updated_at), `PropiedadOut` (todos los campos, readonly), ambos con `model_config = ConfigDict(frozen=True)`, validación de estado con `EstadoPropiedad` (NFR-CODE-003, NFR-CODE-007)

**Checkpoint**: `test_models.py` y `test_schemas.py` en verde. Entidad y DTOs definidos.

---

## Phase 3: Migración de estructura

**Purpose**: Migración Alembic reversible que crea enum y tabla

### Tests for Phase 3 (escribir PRIMERO)

- [ ] T3.1 [US2] Prueba de migración: `test_migration.py` — verifica que `alembic upgrade head` crea tabla `propiedades` con enum `estado_propiedad`, columnas correctas, constraints e índices (SC-001)
- [ ] T3.2 [US2] Prueba de reversibilidad: `test_migration.py` — verifica ciclo `upgrade → downgrade → upgrade` sin errores, que `downgrade` no es `pass` (FR-008, SC-006, NFR-DB-005)

### Implementation for Phase 3

- [ ] T3.3 [US2] Generar migración: `alembic revision -m "crear enum estado_propiedad y tabla propiedades"` → renombrar a `002_create_propiedades.py`
- [ ] T3.4 [US2] Implementar `upgrade()`: crear tabla `propiedades` con `sa.Column(...)` para cada atributo del data-model, `sa.Enum(EstadoPropiedad, create_type=True)` para estado, `UniqueConstraint`, índices. Usar `op.create_table()` — el enum se crea implícitamente. Prohibido invocar `sa.Enum.create()` explícito (NFR-DB-001, NFR-DB-002)
- [ ] T3.5 [US2] Implementar `downgrade()`: `op.drop_table("propiedades")` y `op.execute("DROP TYPE IF EXISTS estado_propiedad")`. Prohibido `pass` (NFR-DB-005)

**Checkpoint**: `test_migration.py` en verde. Migración aplicable y reversible.

---

## Phase 4: Carga inicial de propiedades (seed)

**Purpose**: Script idempotente que carga 10 propiedades de Miami

### Tests for Phase 4 (escribir PRIMERO)

- [ ] T4.1 [P] [US1] Prueba de seed primera ejecución: `test_seed.py` — ejecuta seed sobre BD limpia, verifica exactamente 10 propiedades, todas en Miami, con atributos completos (FR-010, SC-002)
- [ ] T4.2 [P] [US1] Prueba de seed idempotencia: `test_seed.py` — ejecuta seed 2 veces, verifica cardinalidad estable (10), sin duplicados (FR-005, SC-003)
- [ ] T4.3 [P] [US1] Prueba de estados válidos: `test_seed.py` — verifica que el 100% de propiedades tiene estado dentro del catálogo (SC-004)
- [ ] T4.4 [P] [US1] Prueba de imagen determinista: `test_seed.py` — ejecuta seed 2 veces, verifica que cada propiedad tiene la misma imagen en ambas ejecuciones (FR-007, SC-005)
- [ ] T4.5 [P] [US1] Prueba de timestamps server-side: `test_seed.py` — verifica que `created_at` y `updated_at` tienen valor no nulo generado por la BD, no enviado desde Python (FR-006, NFR-DB-006)
- [ ] T4.6 [P] [US1] Prueba de ausencia de psycopg2: verifica que `scripts/dev/seed_propiedades.py` no importa `psycopg2` ni `psycopg` (SC-009)

### Implementation for Phase 4

- [ ] T4.7 [US1] Crear `scripts/dev/seed_propiedades.py`: script standalone con `create_async_engine(DATABASE_URL)`, 10 tuplas de propiedades de Miami según data-model, inserción vía `ON CONFLICT (titulo, direccion, ciudad) DO UPDATE` para cada propiedad individualmente, imagen determinista `f"https://images.unsplash.com/photo-{hash}?w=800"`, sin enviar `created_at` ni `updated_at`, usando solo `asyncpg` (FR-004, FR-005, FR-006, FR-007, NFR-DB-003, NFR-DB-004, NFR-DB-007, NFR-QA-005)

**Checkpoint**: `test_seed.py` en verde. 10 propiedades cargadas idempotentemente.

---

## Phase 5: Repositorio y servicio

**Purpose**: Capa de acceso a datos y lógica de negocio

### Tests for Phase 5 (escribir PRIMERO)

- [ ] T5.1 [P] [US1] Prueba de repositorio: `test_repository.py` — verifica `crear(propiedad_in)`, `obtener_por_id(id)`, `listar(filtros)`, `actualizar(id, update)`, `eliminar(id)` con `AsyncSession`
- [ ] T5.2 [P] [US3] Prueba de servicio: `test_service.py` — verifica validación de estado (rechaza valor fuera del catálogo), validación de atributos obligatorios, upsert por clave de negocio

### Implementation for Phase 5

- [ ] T5.3 [US1] Crear `app/modules/propiedades/repository.py`: funciones async con `session: AsyncSession`, usando `select()`, `insert()`, `update()`, `delete()` — solo acceso a datos (NFR-CODE-005, NFR-CODE-006)
- [ ] T5.4 [US1, US3] Crear `app/modules/propiedades/service.py`: lógica de negocio — validar estado contra `EstadoPropiedad`, validar atributos obligatorios, mapear entidad ↔ DTO (NFR-CODE-005, NFR-CODE-006)
- [ ] T5.5 [US1] Crear `app/modules/propiedades/routes.py`: placeholder con router vacío (sin endpoints en esta feature). Documentar que los endpoints se agregarán en spec posterior

**Checkpoint**: `test_repository.py` y `test_service.py` en verde.

---

## Phase 6: Calidad y validación final

**Purpose**: Verificar que todo el módulo cumple gates de calidad

- [ ] T6.1 [P] [US3] Ejecutar `ruff check app/modules/propiedades/` — debe finalizar sin hallazgos (NFR-QA-001)
- [ ] T6.2 [P] [US3] Ejecutar `mypy --strict app/modules/propiedades/` — debe finalizar sin errores (SC-008, NFR-QA-002)
- [ ] T6.3 [US3] Ejecutar `pytest app/modules/propiedades/tests/ -q` — todos los tests en verde
- [ ] T6.4 [P] [US2] Validar ciclo completo `upgrade → downgrade → upgrade` + `reset schema public → upgrade head → seed` según quickstart.md
- [ ] T6.5 [P] [US3] Verificar gobernanza visual: ningún archivo protegido modificado (`app/static/css/app.css`, `app/static/icons/`, `app/templates/`, `app/templates/components/`, `app/templates/macros/`) (VTG-001 a VTG-006)

**Checkpoint**: Suite completa en verde. Gates de calidad pasan. Feature lista para revisión.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Sin dependencias — inicia inmediatamente
- **Foundational (Phase 2)**: Depende de Setup — BLOQUEA todas las fases posteriores
- **Migración (Phase 3)**: Depende de Foundational (modelo y enum deben existir)
- **Seed (Phase 4)**: Depende de Migración (tabla debe existir) + Foundational (modelo)
- **Repositorio/Servicio (Phase 5)**: Depende de Foundational (modelo y schemas)
- **Calidad (Phase 6)**: Depende de todas las fases anteriores

### User Story Dependencies

- **US1 (Carga inicial)**: Fases 2 → 3 → 4 → 5 (modelo → migración → seed → repositorio/servicio)
- **US2 (Reversibilidad)**: Fases 2 → 3 (modelo → migración)
- **US3 (Calidad)**: Fases 2 → 5 → 6 (modelo → repositorio/servicio → validación)

### Within Each Phase

- Tests MUST fail before implementation (TDD — constitución VIII)
- Models before schemas
- Schemas before repository/service
- Migration after model/enum
- Seed after migration

### Parallel Opportunities

- T1.2, T1.3 en Setup pueden ejecutarse en paralelo
- T2.1, T2.2 (tests de modelo y esquemas) en paralelo
- T4.1 a T4.6 (tests de seed) en paralelo
- T5.1, T5.2 (tests de repositorio y servicio) en paralelo
- T6.1, T6.2, T6.4, T6.5 en Phase 6 en paralelo

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1: Setup
2. Phase 2: Foundational (CRITICAL)
3. Phase 3: Migration
4. Phase 4: Seed
5. **STOP and VALIDATE**: 10 propiedades de Miami cargadas, idempotencia verificada
6. Continuar con US2 y US3

### Incremental Delivery

1. Setup + Foundational → módulo vacío con modelo y schemas
2. Migration → tabla y enum creados, reversibilidad verificada
3. Seed → 10 propiedades cargadas idempotentemente
4. Repository + Service → lógica de negocio y acceso a datos
5. Quality → todos los gates en verde

---

## Notes

- [P] tasks = diferentes archivos, sin dependencias
- [Story] label mapea tarea a historia de usuario para trazabilidad
- TDD obligatorio: tests primero, verificar que fallen, luego implementar
- Commit después de cada tarea o grupo lógico
- Detenerse en cada checkpoint para validar independientemente
- Evitar: tareas vagas, conflictos de mismo archivo, dependencias cruzadas que rompan independencia
- La feature no modifica archivos visuales protegidos — sin tareas `[visual]`
