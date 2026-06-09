# Investigación: Bootstrap del Proyecto Realtor

**Feature**: `001-bootstrap-proyecto` | **Date**: 2026-06-08

## 1. Gestor de proyecto: uv

- **Decisión**: `uv` como único gestor de proyecto.
- **Fundamento**: La constitución (II) lo establece como runtime obligatorio.
  `uv` unifica gestor de paquetes, entorno virtual y lock file. `uv.lock`
  garantiza reproducibilidad exacta.
- **Alternativas descartadas**: `pip` + `venv` (prohibido por constitución III),
  `poetry` (prohibido), `pipenv` (prohibido).

## 2. FastAPI lifespan vs on_event

- **Decisión**: `lifespan` async context manager (`@asynccontextmanager`).
- **Fundamento**: `on_event` está deprecado desde FastAPI 0.93. El lifespan es
  el mecanismo recomendado para inicializar y limpiar recursos como el
  `AsyncEngine`. Permite `yield` para separar setup de teardown de forma
  idiomática.
- **Alternativas descartadas**: `on_event("startup")` / `on_event("shutdown")`
  (deprecados, producen warnings).

## 3. Dependencia de sesión: async generator

- **Decisión**: `get_session` como async generator inyectado vía `Depends()`.
- **Fundamento**: Patrón estándar FastAPI + SQLAlchemy async. El generator
  asegura `session.close()` en `finally`. La inyección por dependencia mantiene
  rutas delgadas y testeables (mock de `get_session` trivial).
- **Alternativas descartadas**: Middleware de sesión (acopla infraestructura a
  capa HTTP, dificulta tests unitarios).

## 4. Timeout en health check

- **Decisión**: `asyncio.timeout(2)` envolviendo `SELECT 1`.
- **Fundamento**: `asyncio.timeout` es nativo desde Python 3.11. 2 segundos es
  suficiente para un `SELECT 1` local. Captura `TimeoutError` y retorna 503 con
  detalle. Sin dependencias externas.
- **Alternativas descartadas**: `asyncio.wait_for` (equivalente pero menos
  legible), timeout a nivel driver `asyncpg` (configuración más compleja).

## 5. Migración baseline: pgcrypto

- **Decisión**: `CREATE EXTENSION IF NOT EXISTS pgcrypto`.
- **Fundamento**: Decisión de las clarificaciones. Modelos futuros usarán
  `UUID` como PK con `gen_random_uuid()`. `IF NOT EXISTS` es idempotente.
- **Alternativas descartadas**: Migración vacía (requeriría migración extra en
  spec 002), esquema `realtor` dedicado (innecesario para bootstrap).

## 6. Tests: mocks vs Testcontainers para smoke tests

- **Decisión**: `unittest.mock` sobre `get_session`.
- **Fundamento**: Smoke tests de `/health` y `/` validan comportamiento HTTP,
  no integración real con BD. Mocks los hacen rápidos (< 100ms), deterministas
  y ejecutables sin Docker. Testcontainers se reserva para módulos de dominio.
- **Alternativas descartadas**: Testcontainers en smoke tests (sobre-ingeniería,
  añade 10-30s de startup por suite).

## 7. CSS: desktop-first con custom properties

- **Decisión**: CSS 100% propio con tokens en `:root`, enfoque desktop-first,
  media queries `max-width`. Breakpoints: 1024px tablet, 768px móvil.
- **Fundamento**: Instrucciones de `.opencode/instructions/frontend.md`.
  Constitución III prohíbe frameworks CSS. Desktop-first es la convención del
  proyecto.
- **Alternativas descartadas**: Bootstrap, Tailwind, Bulma (prohibidos).

## 8. Vendoreo de HTMX

- **Decisión**: Descargar `htmx.min.js` 1.x desde fuente oficial y guardar en
  `app/static/vendor/htmx.min.js`.
- **Fundamento**: Constitución XII exige HTMX vendoreado, no desde CDN. La
  descarga ocurre una vez durante implementación. El archivo se versiona en git.
- **Alternativas descartadas**: CDN en runtime (prohibido), npm install
  (introduce Node.js como dependencia innecesaria).

## 9. Descarga de iconos SVG Lucide

- **Decisión**: Descargar cada SVG desde `https://lucide.dev/api/icons/<nombre>`
  y guardar en `app/static/icons/<nombre>.svg`.
- **Fundamento**: Decisión de clarificaciones. La API retorna SVG limpio que
  solo requiere ajustar `stroke="currentColor"` y `stroke-width="2"`. Más fiable
  que copiar manualmente.
- **Alternativas descartadas**: SVG inline escritos a mano (riesgo de
  malformación), descarga manual por developer (bloquea automatización).

## 10. Alembic async: programático vs alembic.ini

- **Decisión**: Configuración programática en `alembic/env.py` con URL desde
  `settings.DATABASE_URL`.
- **Fundamento**: Evita duplicar la URL de conexión en `alembic.ini`. La URL se
  construye desde variables de entorno consistentes con el resto de la app.
- **Alternativas descartadas**: URL hardcodeada en `alembic.ini` (duplica
  configuración, riesgo de desincronización con `.env`).

## 11. Endpoints de infraestructura: main.py vs módulo

- **Decisión**: Definir `/health` y `/` directamente en `app/main.py`.
- **Fundamento**: No son features de dominio. Crear un módulo `core` o `home`
  viola el principio de no crear módulos por anticipación (constitución IV).
- **Alternativas descartadas**: `app/modules/core/` (estructura de módulo sin
  dominio real), `app/routes.py` (carpeta global por capa, prohibida).
