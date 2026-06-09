---
name: 001-bootstrap-proyecto-spec
description: Prompt fuente para crear la especificación fundacional del proyecto Realtor.
---

/speckit.specify

Crea la spec `001-bootstrap-proyecto`.

## OBJETIVO

Dejar el esqueleto técnico y visual del sistema Realtor en pie, listo para
recibir el primer módulo de dominio en la spec 002.

Esta es la spec fundacional: sin ella las siguientes no se sostienen.

## ALCANCE INCLUIDO

### Estructura del proyecto

- `app/__init__.py`
- `app/main.py`
- `app/config.py`
- `app/database.py`
- `app/modules/` vacío, preparado para módulos de feature futuros.
- `app/static/css/app.css`
- `app/static/vendor/htmx.min.js`
- `app/static/icons/`
- `app/templates/base.html`
- `app/templates/components/`
- `app/templates/macros/icons.html`
- `alembic/` inicializado en modo async.
- `docker-compose.yaml`
- `.env.example`

### Configuración

- `app/config.py` usa `pydantic-settings`.
- La configuración lee variables desde `.env` local.
- La configuración expone como mínimo:
  - `DATABASE_URL`
  - `APP_ENV`
  - `LOG_LEVEL`
- `.env` no debe versionarse con secretos reales.
- `.env.example` debe documentar las variables requeridas sin secretos reales.

### Base de datos

- PostgreSQL se ejecuta localmente con Docker o Docker Compose.
- `docker-compose.yaml` define el servicio local de PostgreSQL.
- `app/database.py` configura `AsyncEngine` y `AsyncSession`.
- `get_session` provee `AsyncSession` por request.
- Alembic usa configuración async.
- Alembic puede ejecutar una migración baseline local sin errores.

### Endpoints

- `GET /health` retorna JSON con estado de la app y de la base de datos.
- `GET /health` ejecuta `SELECT 1` de forma asíncrona contra PostgreSQL.
- `GET /` renderiza un dashboard demo con sidebar, navbar y 3 tarjetas de
  métrica con datos hardcodeados.

### Sistema visual

Debe respetar las instrucciones de frontend en `.opencode/instructions/frontend.md`.

- `app/static/css/app.css` contiene tokens de diseño en `:root`.
- `app/static/css/app.css` contiene secciones comentadas para:
  - reset
  - variables
  - tipografía
  - layout
  - componentes
  - utilidades
  - responsive
- `app/static/vendor/htmx.min.js` está vendoreado y no se carga desde CDN.
- `app/static/icons/` contiene SVG outline de Lucide, uno por archivo.
- Iconos iniciales requeridos:
  - `layout-dashboard`
  - `building-2`
  - `users`
  - `file-text`
  - `wallet`
  - `wrench`
  - `settings`
  - `menu`
  - `x`
  - `check-circle-2`
  - `alert-triangle`
  - `alert-circle`
  - `info`
- `app/templates/base.html` define layout con sidebar fija, área principal y zona
  de mensajes flash.
- `app/templates/macros/icons.html` define la macro `icon(nombre, size, class)`.
- `app/templates/components/` contiene componentes estructurales iniciales:
  - `_sidebar.html`
  - `_navbar.html`
  - `_card_propiedad.html`
  - `_tarjeta_metrica.html`
  - `_accesos_rapidos.html`
  - `_badge_estado.html`
  - `_form_field.html`
  - `_alerta.html`

### Calidad estática

- `ruff` queda configurado en `pyproject.toml`.
- `ruff` usa target `py313`.
- `ruff` usa `line-length = 88`.
- `ruff` activa como mínimo reglas `E`, `F`, `I`, `B`, `UP`, `ASYNC`.
- `mypy` queda configurado en modo estricto como mínimo para `app/modules/`.
- `pytest-asyncio` queda configurado con `asyncio_mode = "auto"`.

### Tests mínimos

- Smoke test de `GET /health`.
- Smoke test de `GET /`.
- Los tests HTTP usan `httpx.AsyncClient`.
- Los tests asíncronos usan `pytest-asyncio`.

## CRITERIOS DE ACEPTACIÓN

1. `uv sync` instala todas las dependencias sin errores.
2. `uv run fastapi dev app/main.py` arranca el servidor.
3. `GET /health` responde `200 OK` con estado de app y DB.
4. `GET /` renderiza dashboard demo con sidebar visible y 3 tarjetas.
5. El layout es responsive y la sidebar puede colapsar por debajo de `1024px`.
6. Todos los iconos son SVG vendoreados desde `app/static/icons/`.
7. `uv run alembic upgrade head` aplica la baseline contra PostgreSQL local sin errores.
8. `uv run ruff check .` pasa limpio.
9. `uv run ruff format --check .` pasa limpio.
10. `uv run mypy --strict app/modules/` pasa limpio.
11. Los smoke tests de `/health` y `/` pasan en verde.
12. Ningún archivo Markdown del repositorio mezcla idiomas.
13. No existen referencias a Supabase.
14. No existen archivos `.yml`; solo se usa `.yaml`.

## ALCANCE NO INCLUIDO

- Módulos de dominio como propiedades, inquilinos, contratos o pagos.
- Autenticación de usuarios.
- Manejo de archivos o storage.
- Integraciones externas.
- Tests de dominio.
- Reglas de negocio reales fuera del dashboard demo y health check.

## DEPENDENCIAS DE PRODUCCIÓN

Las dependencias deben agregarse con `uv` y quedar declaradas en `pyproject.toml`
con rangos versionados razonables.

Dependencias esperadas:

- `fastapi[scalar]`
- `sqlalchemy[asyncio]`
- `asyncpg`
- `alembic`
- `pydantic`
- `pydantic-settings`
- `jinja2`
- `python-multipart`

## DEPENDENCIAS DE DESARROLLO

Dependencias esperadas:

- `pytest`
- `pytest-asyncio`
- `httpx`
- `ruff`
- `mypy`
- `testcontainers`

## REGLAS DE CONSTITUCIÓN A RESPETAR

- Stack inmutable según constitución vigente.
- Python target: `3.13+`.
- PostgreSQL local con Docker o Docker Compose.
- `uv` como único gestor de proyecto.
- No usar Supabase.
- No usar `.yml`; usar siempre `.yaml`.
- Idioma: 100 % español en specs, plan, tasks, comentarios, docstrings y Markdown.
- No implementar código de producción sin pruebas asociadas.
- No crear módulos de dominio en esta spec.
- Usa la ruta de feature resuelta por Spec Kit.
- Si existe `.specify/feature.json`, respeta su `feature_directory`.
- No crees specs manualmente en rutas alternativas.