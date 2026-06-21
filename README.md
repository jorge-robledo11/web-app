# Realtor

Sistema de gestión inmobiliaria para administradores de propiedades en Miami.
Permite llevar el control de propiedades, sus estados y, progresivamente,
inquilinos, contratos de renta y pagos.

Este repositorio implementa el monolito Python con **server-rendered
(Jinja2 + HTMX)**, persistencia en **PostgreSQL** y un flujo de
**Spec-Driven Development** riguroso: ninguna feature se implementa sin una
`spec.md` aprobada y su `plan.md`, `tasks.md` y contrato asociados.

---

## Estado del proyecto

Versión actual: `0.1.0` (en desarrollo activo).

Specs aprobadas e implementadas:

| Spec | Feature |
|------|---------|
| 001 | Bootstrap del proyecto (FastAPI + Docker + Alembic + sistema visual) |
| 002 | Blindaje de tokens visuales canónicos |
| 003 | Rediseño del home (dashboard con métricas, accesos rápidos, actividad) |
| 004 | Propiedades base (modelo, migración, seed de 10 propiedades) |
| 005 | Dashboard con datos reales desde base de datos |
| 006 | Página `/propiedades` con grid de cards |
| 007 | Crear propiedad (formulario server-rendered + flash messages) |

Módulos verticales activos en `app/modules/`:

- `health` — endpoint `GET /health` con verificación de PostgreSQL.
- `dashboard` — página principal con métricas reales y estado vacío.
- `propiedades` — modelo de dominio, listado y creación de propiedades.

El historial completo de cambios vive en `CHANGELOG.md` siguiendo
[Keep a Changelog](https://keepachangelog.com/).

---

## Stack obligatorio

El stack es **inmutable**: ningún componente puede sustituirse sin una
enmienda formal a la constitución. Esta es la versión declarativa resumida:

| Capa | Tecnología |
|------|------------|
| Runtime | Python 3.13.13, gestionado con [`uv`](https://docs.astral.sh/uv/) |
| HTTP | [FastAPI](https://fastapi.tiangolo.com/) |
| Vistas | Jinja2 server-rendered + [HTMX](https://htmx.org/) vendoreado |
| ORM | SQLAlchemy 2.x async con `Mapped[...]`, `mapped_column`, `select()` y `AsyncSession` |
| Validación | Pydantic v2 con `model_config = ConfigDict(frozen=True)` |
| Base de datos | PostgreSQL 16 vía `asyncpg`, ejecutado en Docker local |
| Migraciones | Alembic |
| Tests | pytest + pytest-asyncio + httpx.AsyncClient + Testcontainers |
| Calidad | Ruff (lint + format) + mypy `--strict` + pydocstyle + pre-commit |
| Mutation testing | [`mutmut`](https://mutmut.readthedocs.io/) (focalizado por slice) |
| Iconografía | SVG outline de [Lucide](https://lucide.dev/) vendoreados |

Prohibiciones absolutas (resumen): nada de `pip`, `poetry`, `requirements.txt`
ni `setup.py`; nada de Bootstrap, Tailwind o frameworks CSS; nada de CDN para
HTMX; nada de Supabase; nada de exponer entidades SQLAlchemy como respuesta
HTTP; nada de carpetas globales `controllers/`, `services/`, `repositories/`
fuera de un módulo. La lista completa está en `.specify/memory/constitution.md`
sección III.

---

## Arquitectura: Vertical Slice

Cada feature vive en su propio módulo bajo `app/modules/<feature>/` con
exactamente estos artefactos:

```text
app/modules/<feature>/
  routes.py        # capa delgada: parsea entrada, llama al servicio, retorna respuesta
  schemas.py       # DTOs Pydantic v2 (frozen=True)
  models.py        # entidades SQLAlchemy 2.x async
  repository.py    # solo acceso a datos (select, insert, update, delete)
  service.py       # lógica de negocio
  templates/       # plantillas Jinja2 del módulo
```

Reglas clave:

- `service.py` es el **único** lugar donde vive lógica de negocio.
- `routes.py` y `repository.py` no contienen reglas de negocio.
- La lógica compartida solo se extrae cuando existe duplicación real
  demostrable, nunca por anticipación.
- Las pruebas viven en la raíz del repositorio
  (`tests/unit/<feature>/` y `tests/integration/<feature>/`),
  nunca dentro del módulo.

La especificación arquitectónica completa está en
`.specify/memory/constitution.md` secciones IV y IX.5.

---

## Estructura del repositorio

```text
app/
  config/                  # configuración (pydantic-settings + YAML)
  infra/                   # database engine, infraestructura compartida
  modules/
    health/                # GET /health
    dashboard/             # GET /
    propiedades/           # GET /propiedades, GET /propiedades/nueva, POST /propiedades
  static/
    css/app.css            # tokens visuales canónicos y layout
    vendor/htmx.min.js     # HTMX vendoreado
    icons/                 # SVG outline de Lucide
  templates/
    base.html              # layout base: sidebar + main + #flash-zone
    components/            # parciales compartidos
    macros/                # iconos, formateo
alembic/
  versions/                # migraciones versionadas
config/
  app.example.yaml         # plantilla de configuración (sin secretos)
  app.yaml                 # configuración local (ignorada por git)
specs/                     # spec.md, plan.md, tasks.md por feature
tests/
  unit/<feature>/          # tests unitarios sin infraestructura
  integration/<feature>/   # tests de integración con Testcontainers
docker-compose.yaml        # PostgreSQL 16 local
Makefile                   # entry point de comandos de desarrollo
pyproject.toml             # dependencias, ruff, mypy, mutmut, pytest
.pre-commit-config.yaml    # hooks de calidad unificados
```

---

## Requisitos

- Python 3.13.13 (lo descarga automáticamente `uv`).
- [`uv`](https://docs.astral.sh/uv/) como gestor de dependencias y runtime.
- Docker y Docker Compose para PostgreSQL local.
- `make` (GNU Make) para los atajos de comandos.
- Git.

---

## Setup local

### 1. Instalar dependencias

```bash
uv sync
```

### 2. Configurar la aplicación

```bash
cp config/app.example.yaml config/app.yaml
```

Edita `config/app.yaml` solo si necesitas ajustar `database_url` o
`session_secret`. El archivo está ignorado por git para evitar commits
accidentales de secretos.

### 3. Levantar PostgreSQL

```bash
make db-up
make db-status       # confirma que el contenedor está "healthy"
```

### 4. Aplicar migraciones y seed

```bash
make db-migrate
uv run python scripts/db/seed_propiedades.py
```

### 5. Arrancar el servidor

```bash
make server
```

La aplicación queda disponible en `http://localhost:8000`.

Endpoints útiles:

| Ruta | Descripción |
|------|-------------|
| `GET /` | Dashboard con métricas reales |
| `GET /health` | Health check de aplicación y base de datos |
| `GET /propiedades` | Grid de cards de propiedades |
| `GET /propiedades/nueva` | Formulario de creación |
| `POST /propiedades` | Procesa el formulario de creación |

---

## Comandos de desarrollo (Makefile)

### Aplicación y base de datos

```bash
make server          # arranca FastAPI con autoreload
make db-up           # levanta PostgreSQL con Docker Compose
make db-down         # detiene PostgreSQL
make db-status       # estado de los contenedores
make db-logs         # últimos 50 logs de PostgreSQL
make db-migrate      # aplica migraciones pendientes (alembic upgrade head)
make db-create name="agrega columna X"  # crea una nueva migración
make db-reset        # BORRA los datos y reinicia el esquema
```

### Calidad automatizada

```bash
make auto-checks     # pre-commit run --all-files
make ci              # auto-checks + tests + coverage + clean
make visual-check    # auditoría de trazabilidad visual (spec 002)
```

### Tests

```bash
make test            # suite completa con pytest
make coverage        # suite + reporte de cobertura
make mutation        # mutation testing focalizado con mutmut
make mutation-results # resumen de mutantes sobrevivientes
make mutation-clean  # limpia el directorio mutants/
```

### Tooling auxiliar

```bash
make context         # genera docs/context/repo-state.xml con Repomix
make hooks-install   # instala hooks Git locales
make help            # lista todos los targets disponibles
```

---

## Spec-Driven Development

Toda feature sigue un flujo obligatorio de ocho fases, ejecutado con los
comandos de Spec Kit:

```text
/speckit.specify
/speckit.clarify
/speckit.plan
/speckit.analyze
fix-report (solo si analyze encuentra hallazgos)
/speckit.analyze (confirma 0 hallazgos antes de tasks)
/speckit.tasks
/speckit.implement
```

Cada spec aprobada vive en `specs/NNN-nombre-slug/` y debe contener como
mínimo los siete archivos:

```text
spec.md          # qué: requisitos funcionales y criterios de aceptación
plan.md          # cómo: decisiones técnicas, fases, gobernanza visual
tasks.md         # cuándo: tareas pequeñas, ordenadas, trazables a FR/SC
data-model.md    # entidades, columnas, índices, migraciones, DTOs
contracts/<feature>.yaml  # contrato formal de endpoints HTTP
quickstart.md    # pasos manuales reproducibles para validar end-to-end
research.md      # decisiones técnicas investigadas y fundamento
```

Ninguna fase puede saltarse. Ningún archivo puede estar ausente. El
desarrollador nunca crea specs manualmente fuera de los comandos de Spec Kit.

---

## Test-Driven Development

El ciclo **Red-Green-Refactor** es obligatorio para todo el código de
producción:

1. **Red**: escribir primero una prueba que falle por el motivo correcto.
2. **Green**: implementar el código mínimo necesario para que pase.
3. **Refactor**: mejorar el diseño con la suite en verde.

Reglas operativas:

- No se escribe código de producción sin una prueba asociada.
- Toda regla de negocio debe estar cubierta por pruebas capaces de matar
  mutantes relevantes.
- Las pruebas HTTP usan `httpx.AsyncClient` con `ASGITransport`.
- Las pruebas de integración con PostgreSQL usan **Testcontainers**
  (`postgres:16-alpine`), nunca la base de datos de desarrollo.
- Los tests unitarios viven en `tests/unit/<feature>/` y no pueden
  depender de infraestructura externa.
- La operación de métricas (coverage, mutation score) es responsabilidad
  del desarrollador humano, no de los agentes de IA.

La política completa está en `.specify/memory/constitution.md` sección X y en
`.opencode/instructions/tests.instructions.md`.

---

## Gobernanza visual

Los tokens visuales canónicos —colores, sombras, radios, espaciados,
tipografía, breakpoints, layout base, componentes compartidos y macros de
iconos— están protegidos contra modificaciones no autorizadas.

Cualquier cambio en estos tokens requiere:

1. Spec aprobada que lo justifique.
2. Marcador `[visual]` (o `[visual][extension]` / `[visual][bugfix]`) en
   `tasks.md` con la justificación correspondiente.
3. Actualización explícita de `app/static/css/app.css`,
   `.opencode/instructions/frontend.instructions.md` y, si aplica, la
   constitución.
4. Registro en `Complexity Tracking` de `plan.md` si introduce una
   desviación visual global.

La auditoría puede ejecutarse con `make visual-check`.

La fuente operativa única de los tokens es
`.opencode/instructions/frontend.instructions.md`. La spec
`specs/002-blindar-tokens-visuales/spec.md` define el proceso completo.

---

## Documentación adicional

- [`.specify/memory/constitution.md`](.specify/memory/constitution.md) —
  constitución del proyecto, fuente de verdad suprema (v1.7.0).
- [`AGENTS.md`](AGENTS.md) — reglas operativas para el agente de IA y los
  colaboradores.
- [`CHANGELOG.md`](CHANGELOG.md) — historial de cambios versionado.
- [`.opencode/instructions/`](.opencode/instructions/) — instrucciones
  operativas por área:
  - `backend.instructions.md` — módulos Python, FastAPI, SQLAlchemy.
  - `frontend.instructions.md` — Jinja2, HTMX, sistema visual.
  - `database.instructions.md` — PostgreSQL, Alembic, migraciones.
  - `tests.instructions.md` — pytest, Testcontainers, mutmut.
  - `conventions.instructions.md` — nomenclatura, formato, pre-commit.
- [`docs/testing/`](docs/testing/) — guías operativas de testing y
  mutation testing.
- [`specs/`](specs/) — todas las specs aprobadas, cada una con sus
  artefactos completos.

---

## Licencia

Proyecto privado. Sin licencia pública definida todavía.
