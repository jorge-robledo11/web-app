# Tareas: Bootstrap del Proyecto Realtor

**Input**: Design documents from `specs/001-bootstrap-proyecto/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

## Formato: `[ID] [P?] [Story] Descripción`

- **[P]**: Puede ejecutarse en paralelo (archivos distintos, sin dependencias)
- **[Story]**: Historia de usuario a la que pertenece (US1, US2, US3)
- Incluye rutas exactas en las descripciones

---

## Fase 1: Setup (Infraestructura compartida)

**Propósito**: Inicialización del proyecto, dependencias y PostgreSQL local.

- [ ] T1.1 Instalar dependencias con `uv sync` creando `pyproject.toml` con las dependencias de producción (`fastapi[scalar]`, `sqlalchemy[asyncio]`, `asyncpg`, `alembic`, `pydantic`, `pydantic-settings`, `jinja2`, `python-multipart`) y desarrollo (`pytest`, `pytest-asyncio`, `httpx`, `ruff`, `mypy`, `testcontainers`). Incluir configuración de `[tool.ruff]`, `[tool.mypy]` y `[tool.pytest.ini_options]`.
- [ ] T1.2 [P] Crear `docker-compose.yaml` con servicio PostgreSQL 16-alpine, puerto 5432, base `realtor_dev`, usuario `realtor_dev`, password `realtor_dev`, volumen `pgdata` y healthcheck `pg_isready`. Levantar con `docker compose up -d`.
- [ ] T1.3 [P] Crear `.env.example` documentando `DATABASE_URL`, `APP_ENV` y `LOG_LEVEL` sin secretos reales. Copiar a `.env` local.

**Checkpoint**: `uv sync` instala sin errores, PostgreSQL responde a `pg_isready`.

---

## Fase 2: Fundacional (Bloquea todas las historias de usuario)

**Propósito**: Infraestructura core que DEBE estar completa antes de implementar cualquier historia de usuario.

**⚠️ CRÍTICO**: Ninguna historia de usuario puede comenzar hasta que esta fase esté completa.

- [ ] T2.1 Crear `app/config.py` con la clase `Settings` usando `pydantic-settings`. Campos: `DATABASE_URL` (default `postgresql+asyncpg://realtor_dev:realtor_dev@localhost:5432/realtor_dev`), `APP_ENV` (default `"development"`), `LOG_LEVEL` (default `"INFO"`). Config: `SettingsConfigDict(env_file=".env", frozen=True)`.
- [ ] T2.2 Crear `app/database.py` con `AsyncEngine` (`create_async_engine`), `async_sessionmaker` (`AsyncSessionLocal`), `Base` (`DeclarativeBase`) y `get_session()` como async generator que inyecta `AsyncSession`.
- [ ] T2.3 Inicializar Alembic en modo async: crear `alembic/env.py` con `DATABASE_URL` leído de `settings.DATABASE_URL`, `target_metadata = Base.metadata`, y `run_migrations_online` con `AsyncEngine` + `run_sync`. Crear `alembic/versions/001_bootstrap_extensions.py` con `upgrade()` que ejecuta `CREATE EXTENSION IF NOT EXISTS pgcrypto` y `downgrade()` con `DROP EXTENSION IF EXISTS pgcrypto`. Crear `alembic/script.py.mako`. Ejecutar `uv run alembic upgrade head`.
- [ ] T2.4 [P] Crear `app/__init__.py` y `app/modules/__init__.py` (ambos vacíos, marcando los paquetes Python).
- [ ] T2.5 Crear `app/main.py` con la app FastAPI (`lifespan` async que hace `yield` y `await engine.dispose()`), sin handlers de endpoints todavía. La app debe arrancar con `uv run fastapi dev app/main.py`.

**Checkpoint**: Fundación lista. Servidor arranca, Alembic aplica la migración baseline, `get_session` está disponible para inyección.

---

## Fase 3: Historia de Usuario 1 — Health Check operacional (P1) 🎯 MVP

**Objetivo**: Verificar que el servidor y la base de datos responden correctamente.

**Prueba independiente**: `curl http://localhost:8000/health` retorna `200` con `{"status":"ok","database":"ok"}`.

### Tests para US1

> **Escribir estos tests PRIMERO, verificar que FALLAN antes de implementar.**

- [ ] T3.1 [P] [US1] Crear `tests/__init__.py` y `tests/conftest.py` con fixture `async_client` usando `httpx.AsyncClient` + `ASGITransport(app=app)`.
- [ ] T3.2 [P] [US1] Crear `tests/test_health.py` con `test_health_ok` (mock de `get_session` retorna éxito, verifica `200` y body `{"status":"ok","database":"ok"}`) y `test_health_db_unavailable` (mock lanza `TimeoutError`, verifica `503` y body con `"database":"unavailable"`).

### Implementación para US1

- [ ] T3.3 [US1] Implementar `GET /health` en `app/main.py` como `async def health(session: AsyncSession = Depends(get_session))`. Envolver `await session.execute(text("SELECT 1"))` en `asyncio.timeout(2)`. Retornar `200` con `{"status":"ok","database":"ok"}` en éxito, `503` con `{"status":"error","database":"unavailable","detail":"timeout after 2s"}` en fallo. Emitir `logger.warning()` solo en fallo.
- [ ] T3.4 [US1] Ejecutar `uv run pytest tests/test_health.py -v` y verificar que ambos tests pasan en verde.

**Checkpoint**: Health check funcional e independientemente testeable.

---

## Fase 4: Historia de Usuario 2 — Dashboard demo con layout base (P2)

**Objetivo**: Renderizar el layout completo con sidebar, navbar, 3 tarjetas de métrica y zona de mensajes flash.

**Prueba independiente**: `curl http://localhost:8000/` retorna HTML con `class="sidebar"`, `class="navbar"` y 3 elementos `class="tarjeta-metrica"`.

### Sistema visual (prerrequisitos de US2)

- [ ] T4.1 [P] [US2] Crear `app/static/css/app.css` con tokens en `:root` y secciones comentadas: reset, variables (colores, espaciado, radios, sombras, tipografía), tipografía, layout (sidebar + main grid), componentes (`_sidebar`, `_navbar`, `_tarjeta_metrica`, `_accesos_rapidos`, `_card_propiedad`, `_badge_estado`, `_form_field`, `_alerta`), utilidades, responsive (media queries `max-width: 1023px` y `max-width: 767px`).
- [ ] T4.2 [P] [US2] Descargar `htmx.min.js` (versión 2.x) desde fuente oficial y guardar en `app/static/vendor/htmx.min.js`.
- [ ] T4.3 [P] [US2] Descargar los 13 iconos SVG Lucide desde `https://lucide.dev/api/icons/<nombre>` y guardarlos en `app/static/icons/<nombre>.svg`. Ajustar `stroke="currentColor"` y `stroke-width="2"`. Set: `layout-dashboard`, `building-2`, `users`, `file-text`, `wallet`, `wrench`, `settings`, `menu`, `x`, `check-circle-2`, `alert-triangle`, `alert-circle`, `info`.
- [ ] T4.4 [P] [US2] Crear `app/templates/macros/icons.html` con la macro `icon(nombre, size=24, class="")` que inyecta el SVG inline desde `app/static/icons/<nombre>.svg` usando `{% include %}` o lectura de archivo.
- [ ] T4.5 [US2] Crear los 8 componentes en `app/templates/components/`: `_sidebar.html` (navegación con iconos), `_navbar.html` (breadcrumbs + acciones), `_tarjeta_metrica.html` (KPI con label, valor, icono, tendencia), `_accesos_rapidos.html` (grid de atajos), `_card_propiedad.html` (card placeholder), `_badge_estado.html` (píldora por estado), `_form_field.html` (label + input + error), `_alerta.html` (banner 4 variantes). Todos con HTML + CSS completo y funcional desde el día 1.
- [ ] T4.6 [US2] Crear `app/templates/base.html` con layout sidebar fija + main + `#flash-zone`, carga de `app.css` y `htmx.min.js`.
- [ ] T4.7 [US2] Crear `app/templates/dashboard.html` que extiende `base.html`, incluye `_sidebar`, `_navbar`, 3 `_tarjeta_metrica` y `_accesos_rapidos`. Los datos de métricas son hardcodeados: Propiedades activas (124, `building-2`), Inquilinos al día (87, `users`), Contratos vigentes (53, `file-text`).

### Tests para US2

> **Escribir estos tests PRIMERO, verificar que FALLAN antes de implementar el handler.**

- [ ] T4.8 [US2] Crear `tests/test_dashboard.py` con `test_dashboard_ok` que verifica `GET /` retorna `200`, `Content-Type: text/html`, contiene `class="sidebar"`, `class="navbar"`, al menos 3 ocurrencias de `class="tarjeta-metrica"`, y el texto `Propiedades activas` y `124`.

### Implementación para US2

- [ ] T4.9 [US2] Implementar `GET /` en `app/main.py` como `async def dashboard(request: Request)`. Retornar `Templates.TemplateResponse("dashboard.html", {"request": request, "metricas": [...]})`. Sin dependencia de base de datos. Sin logging explícito.
- [ ] T4.10 [US2] Ejecutar `uv run pytest tests/test_dashboard.py -v` y verificar que el test pasa en verde.

**Checkpoint**: Dashboard funcional, sidebar responsive, 3 tarjetas de métrica visibles.

---

## Fase 5: Historia de Usuario 3 — Herramientas de calidad estática en verde (P3)

**Objetivo**: Garantizar que `ruff` y `mypy` pasan limpiamente sobre el código base.

**Prueba independiente**: `uv run ruff check .`, `uv run ruff format --check .` y `uv run mypy --strict app/modules/` terminan con código de salida 0.

- [ ] T5.1 [US3] Ejecutar `uv run ruff check .` y corregir todos los warnings/errores hasta obtener código de salida 0.
- [ ] T5.2 [US3] Ejecutar `uv run ruff format --check .` y corregir diferencias de formato hasta obtener código de salida 0.
- [ ] T5.3 [US3] Ejecutar `uv run mypy --strict app/modules/` y corregir todos los errores de tipo hasta obtener `Success: no issues found`.
- [ ] T5.4 [US3] Ejecutar la suite completa `uv run pytest -v` y verificar que los 3 tests pasan en verde.

**Checkpoint**: Suite de calidad estática en verde. Suite de tests en verde.

---

## Fase 6: Polish y cierre

**Propósito**: Refactor final y validación completa.

- [ ] T6.1 Refactorizar el código sin cambiar comportamiento: revisar imports, docstrings en español, limpieza de código comentado o muerto.
- [ ] T6.2 Ejecutar la validación completa de `quickstart.md`: `uv sync` → `docker compose up -d` → `alembic upgrade head` → `fastapi dev` → `curl /health` → `curl /` → `ruff check .` → `ruff format --check .` → `mypy --strict app/modules/` → `pytest`.
- [ ] T6.3 Verificar criterios de aceptación SC-011 (cero referencias a Supabase) y SC-012 (cero archivos `.yml`).

---

## Dependencias y orden de ejecución

### Dependencias entre fases

```
Fase 1 (Setup) ──► Fase 2 (Fundacional) ──► Fase 3 (US1) ──► Fase 4 (US2) ──► Fase 5 (US3) ──► Fase 6 (Polish)
```

- **Fase 1**: Sin dependencias. Todas las tareas marcadas [P] pueden ejecutarse en paralelo.
- **Fase 2**: Depende de Fase 1 completa. T2.4 y T2.5 dependen de T2.1, T2.2. T2.3 depende de T2.2.
- **Fase 3**: Depende de Fase 2 completa. T3.1, T3.2 en paralelo. T3.3 después de T3.2 (Red → Green). T3.4 verifica T3.3.
- **Fase 4**: Depende de Fase 2 completa. T4.1-T4.4 en paralelo. T4.5-T4.7 dependen de T4.4. T4.8 antes de T4.9 (Red → Green).
- **Fase 5**: Depende de Fases 3 y 4 completas. T5.1, T5.2, T5.3 en cualquier orden.
- **Fase 6**: Depende de Fase 5 completa.

### Oportunidades de paralelismo

- T1.2 y T1.3 pueden ejecutarse en paralelo con T1.1.
- T2.4 puede ejecutarse en paralelo con T2.3.
- T3.1 y T3.2 pueden ejecutarse en paralelo.
- T4.1, T4.2, T4.3, T4.4 pueden ejecutarse en paralelo.
- T4.5 (_sidebar, _navbar, _tarjeta_metrica) pueden ejecutarse en paralelo entre sí.
- T4.6 debe ejecutarse después de T4.5.
- T5.1, T5.2, T5.3 pueden ejecutarse en cualquier orden.

### Bloqueos

- Ningún bloqueo fuera de las dependencias declaradas.
- Las 3 historias de usuario son independientes entre sí una vez completada la Fase 2.
- US1 no depende de ningún artefacto visual (CSS, iconos, templates).
- US2 no depende de US1 (usa handler sin DB, no toca `/health`).

---

## Estrategia de implementación

### MVP First (US1 solamente)

1. Completar Fase 1: Setup
2. Completar Fase 2: Fundacional
3. Completar Fase 3: US1 Health Check
4. **PARAR y VALIDAR**: health check responde `200` y `503` correctamente
5. Demo/despliegue si se desea

### Entrega incremental

1. Setup + Fundacional → Base lista
2. Agregar US1 Health Check → Test independiente → MVP
3. Agregar US2 Dashboard → Test independiente → Layout completo
4. Agregar US3 Calidad → Suite en verde → Feature completa
5. Polish → Validación final

### Estrategia paralela (equipo)

1. Equipo completa Setup + Fundacional juntos
2. Una vez Fundacional listo:
   - Dev A: Fase 3 (US1 Health Check)
   - Dev B: Fase 4 (US2 Dashboard, assets visuales)
3. Ambos integran y verifican Fase 5 (Calidad) juntos

---

## Notas

- [P] = archivos distintos, sin dependencias entre sí
- [US1]/[US2]/[US3] = trazabilidad a historia de usuario
- TDD: tests en rojo antes de implementar (T3.1-T3.2 antes de T3.3, T4.8 antes de T4.9)
- Commit después de cada tarea o grupo lógico
- Detenerse en cualquier checkpoint para validar la historia independientemente
- Todo el contenido en español: docstrings, comentarios, mensajes de commit
