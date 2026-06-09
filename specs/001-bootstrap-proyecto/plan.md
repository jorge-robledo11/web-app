# Plan de Implementación: Bootstrap del Proyecto Realtor

**Branch**: `001-bootstrap-proyecto` | **Date**: 2026-06-08 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-bootstrap-proyecto/spec.md`

## Resumen

Dejar el esqueleto técnico y visual del sistema Realtor en pie. Esta spec es
fundacional: configura `pyproject.toml` con `uv`, levanta PostgreSQL local vía
Docker Compose, establece la capa de base de datos async (SQLAlchemy 2.x +
Alembic), implementa `GET /health` y `GET /` como endpoints mínimos, y crea el
sistema visual completo con CSS propio, 13 iconos SVG de Lucide vendoreados,
templates Jinja2 y 8 componentes estructurales. Todo el código debe pasar
`ruff`, `ruff format --check` y `mypy --strict` sin errores.

## Contexto técnico

**Lenguaje/Versión**: Python 3.13.13, gestionado con `uv` (`pyproject.toml` + `uv.lock`)

**Dependencias principales**:
- Producción: `fastapi[scalar]>=0.115,<1.0`, `sqlalchemy[asyncio]>=2.0,<3.0`,
  `asyncpg>=0.30,<1.0`, `alembic>=1.14,<2.0`, `pydantic>=2.0,<3.0`,
  `pydantic-settings>=2.0,<3.0`, `jinja2>=3.1,<4.0`, `python-multipart>=0.0.18,<1.0`
- Desarrollo: `pytest>=8.0,<9.0`, `pytest-asyncio>=0.24,<1.0`, `httpx>=0.27,<1.0`,
  `ruff>=0.8,<1.0`, `mypy>=1.14,<2.0`, `testcontainers>=4.0,<5.0`

**Almacenamiento**: PostgreSQL 16-alpine local vía Docker Compose (`docker-compose.yaml`)

**Testing**: pytest + pytest-asyncio (`asyncio_mode = "auto"`) + httpx.AsyncClient.
Smoke tests con mocks de sesión.

**Plataforma objetivo**: Linux server (desarrollo local con Docker)

**Tipo de proyecto**: Web app monolítica server-rendered (FastAPI + Jinja2 + HTMX)

**Metas de rendimiento**: `GET /health` < 500ms con BD disponible

**Restricciones**: Python 3.13+, async-first para I/O, CSS 100% propio sin frameworks,
cero dependencias CDN en runtime, sin Supabase, extensión `.yaml` nunca `.yml`

**Escala/Alcance**: Bootstrap inicial; sin usuarios reales ni módulos de dominio.
Dashboard demo con 3 métricas hardcodeadas.

## Verificación de constitución

*GATE: Debe pasar antes de Phase 0. Re-verificar tras Phase 1.*

| Regla | Cumple | Evidencia |
|---|---|---|
| I. Idioma español | Sí | Todo Markdown, docstrings, comentarios y commits en español |
| II. Stack inmutable | Sí | FastAPI + Jinja2 + HTMX + SQLAlchemy 2.x async + Pydantic v2 + PostgreSQL + Alembic + pytest + Ruff + mypy + Lucide |
| III. Prohibiciones | Sí | Sin pip/poetry, sin frameworks CSS, sin CDN, sin `Column` legacy, sin carpetas globales, sin Supabase, sin `.yml` |
| IV. Vertical Slice | N/A | `app/modules/` queda vacío; sin módulos de dominio en esta spec |
| V. Spec-Driven | Sí | Spec aprobada antes de implementar |
| VI. Flujo Spec Kit | Sí | `specify` → `clarify` → `plan` (fase actual) |
| VIII. TDD | Sí | Smoke tests primero (Red), luego implementación (Green) |
| IX. Calidad | Sí | `uv sync && uv run pytest && uv run ruff check . && uv run ruff format --check . && uv run mypy --strict app/modules/` |
| X. Base de datos | Sí | PostgreSQL local Docker Compose, Alembic async, `.env` no versionado, `.env.example` presente, `.yaml` no `.yml` |
| XI. Async-First | Sí | `get_session` async, `SELECT 1` async con timeout, endpoints `async def` |
| XII. Frontend | Sí | HTMX vendoreado, CSS propio, iconos SVG Lucide, macros Jinja2 |
| XIII. Estructura | Sí | Layout exacto según constitución sección XIII |
| XIV. Contratos | Sí | Health response usa Pydantic `frozen=True` |
| XV. Complexity | Sí | Sin desviaciones |

**Resultado**: PASA. Sin violaciones.

## Estructura del proyecto

### Documentación (esta feature)

```text
specs/001-bootstrap-proyecto/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── health.md
│   └── dashboard.md
└── tasks.md
```

### Código fuente (raíz del repositorio)

```text
app/
  __init__.py
  main.py
  config.py
  database.py
  modules/
    __init__.py
  static/
    css/
      app.css
    vendor/
      htmx.min.js
    icons/
      *.svg
  templates/
    base.html
    dashboard.html
    components/
      _sidebar.html
      _navbar.html
      _tarjeta_metrica.html
      _accesos_rapidos.html
      _card_propiedad.html
      _badge_estado.html
      _form_field.html
      _alerta.html
    macros/
      icons.html
alembic/
  env.py
  script.py.mako
  versions/
    001_bootstrap_extensions.py
pyproject.toml
uv.lock
docker-compose.yaml
.env.example
tests/
  __init__.py
  conftest.py
  test_health.py
  test_dashboard.py
```

**Decisión estructural**: Los endpoints `/health` y `/` son infraestructura de
aplicación, no pertenecen a un módulo de dominio. Viven directamente en
`app/main.py`. `app/modules/` queda vacío con `__init__.py`. Los tests de estos
endpoints viven en `tests/` en la raíz del repositorio.

## Orden de implementación

1. `pyproject.toml` → `uv sync`
2. `docker-compose.yaml` → `docker compose up -d`
3. `.env.example` → `.env`
4. `app/config.py`
5. `app/database.py`
6. `alembic/` → `alembic upgrade head`
7. `app/static/css/app.css`
8. `app/static/vendor/htmx.min.js`
9. `app/static/icons/*.svg` (13 iconos)
10. `app/templates/macros/icons.html`
11. `app/templates/components/_*.html` (8 componentes)
12. `app/templates/base.html`
13. `app/templates/dashboard.html`
14. `app/__init__.py` + `app/modules/__init__.py`
15. `app/main.py` (app FastAPI + lifespan sin handlers de endpoints)
16. `tests/conftest.py` + `tests/test_health.py` (Red)
17. Implementar `GET /health` en `main.py` (Green)
18. `tests/test_dashboard.py` (Red)
19. Implementar `GET /` en `main.py` (Green)
20. `ruff check .` + `ruff format --check .` + `mypy --strict app/modules/`
21. Refactor final si es necesario

## Complexity Tracking

Sin desviaciones. Esta spec respeta íntegramente la constitución v1.1.0.
