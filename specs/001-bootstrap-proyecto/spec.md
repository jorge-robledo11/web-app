# Feature Specification: Bootstrap del Proyecto Realtor

**Feature Branch**: `001-bootstrap-proyecto`

**Created**: 2026-06-08

**Status**: Draft

**Input**: /speckit.specify 001-bootstrap-proyecto

## User Scenarios & Testing

### User Story 1 - Health Check operacional (Priority: P1)

Como desarrollador u operador, necesito verificar que el servidor y la base de
datos responden correctamente para confirmar que el despliegue local es funcional.

**Why this priority**: Sin un health check que valide la conectividad con
PostgreSQL, ninguna otra feature puede desarrollarse ni probarse. Es el
prerrequisito absoluto del resto del sistema.

**Independent Test**: Ejecutar `GET /health` contra el servidor en ejecución y
verificar que retorna `200 OK` con un JSON que incluye estado de la aplicación y
estado de la base de datos.

**Acceptance Scenarios**:

1. **Given** el servidor FastAPI está corriendo y PostgreSQL está disponible,
   **When** se hace `GET /health`, **Then** retorna `200 OK` con
   `{"status": "ok", "database": "ok"}`.
2. **Given** el servidor FastAPI está corriendo pero PostgreSQL no responde,
   **When** se hace `GET /health`, **Then** retorna `503 Service Unavailable` con
   `{"status": "error", "database": "unavailable", "detail": "timeout after 2s"}`.

---

### User Story 2 - Dashboard demo con layout base (Priority: P2)

Como usuario, necesito ver el layout completo de la aplicación (sidebar, navbar,
área de contenido) con datos de demostración para validar que la estructura
visual funciona antes de integrar módulos de dominio.

**Why this priority**: El layout es el cascarón visual que contendrá todos los
módulos futuros. Sin él, ninguna feature de dominio puede renderizarse.

**Independent Test**: Ejecutar `GET /` contra el servidor y verificar que el HTML
retornado contiene sidebar con navegación, navbar superior, y al menos 3 tarjetas
de métrica con datos hardcodeados.

**Acceptance Scenarios**:

1. **Given** el servidor está corriendo, **When** se hace `GET /`, **Then**
   retorna `200 OK` con HTML que incluye `class="sidebar"`, `class="navbar"` y al
   menos 3 elementos `class="tarjeta-metrica"`.
2. **Given** el viewport es menor a 1024px, **When** se renderiza el dashboard,
   **Then** la sidebar está colapsada y se muestra un botón de menú hamburguesa.
3. **Given** el viewport es mayor o igual a 1024px, **When** se renderiza el
   dashboard, **Then** la sidebar está visible y expandida.

---

### User Story 3 - Herramientas de calidad estática en verde (Priority: P3)

Como desarrollador, necesito que `ruff` y `mypy` pasen limpiamente sobre el
código base para garantizar que el esqueleto cumple con los estándares de calidad
del proyecto antes de escribir código de dominio.

**Why this priority**: La calidad estática es un gate obligatorio. Sin ella, el
código de features futuras podría acumular deuda técnica desde el inicio.

**Independent Test**: Ejecutar `uv run ruff check .`, `uv run ruff format --check .`
y `uv run mypy --strict app/modules/` y verificar que todos terminan sin errores.

**Acceptance Scenarios**:

1. **Given** el código del bootstrap está completo, **When** se ejecuta
   `uv run ruff check .`, **Then** termina con código de salida 0 y sin warnings.
2. **Given** el código del bootstrap está completo, **When** se ejecuta
   `uv run ruff format --check .`, **Then** termina con código de salida 0.
3. **Given** el código del bootstrap está completo, **When** se ejecuta
   `uv run mypy --strict app/modules/`, **Then** termina con código de salida 0.

---

### Edge Cases

- ¿Qué sucede si el archivo `.env` no existe al iniciar? La aplicación debe
  arrancar usando defaults razonables de `pydantic-settings` y advertir en logs.
- ¿Qué sucede si PostgreSQL no está disponible al iniciar? La aplicación debe
  arrancar, pero `GET /health` debe reportar `database: "unavailable"` con `503`
  y detalle del fallo.
- ¿Qué sucede si `alembic upgrade head` se ejecuta sin migraciones? No debe
  fallar; la migración baseline que instala `pgcrypto` debe existir.
- ¿Qué sucede si el dashboard se renderiza con HTMX deshabilitado? Debe
  mostrarse igual; el layout base no depende de HTMX para la estructura inicial.
- ¿Qué sucede si el servidor se detiene durante `SELECT 1` en el health check?
  La corrutina debe manejarlo con timeout y retornar error controlado.

## Requirements

### Functional Requirements

- **FR-001**: El proyecto DEBE usar `uv` como único gestor de dependencias y
  entorno, con `pyproject.toml` y `uv.lock`.
- **FR-002**: El sistema DEBE exponer `GET /health` que ejecute `SELECT 1`
  asíncrono contra PostgreSQL y retorne JSON con estados de app y base de datos.
- **FR-003**: El sistema DEBE exponer `GET /` que renderice un dashboard demo
  con sidebar, navbar, 3 tarjetas de métrica y zona de mensajes flash.
- **FR-004**: La configuración DEBE leerse desde `.env` local mediante
  `pydantic-settings`, exponiendo `DATABASE_URL`, `APP_ENV` y `LOG_LEVEL`.
- **FR-005**: `.env` NO DEBE versionarse con secretos reales; `.env.example`
  DEBE documentar las variables requeridas sin valores secretos.
- **FR-006**: PostgreSQL DEBE ejecutarse localmente con Docker Compose mediante
  `docker-compose.yaml`.
- **FR-007**: `app/database.py` DEBE configurar `AsyncEngine` y `AsyncSession`, y
  proveer una dependencia `get_session` que inyecte `AsyncSession` por request.
- **FR-008**: Alembic DEBE configurarse en modo async y DEBE poder ejecutar una
  migración baseline sin errores.
- **FR-009**: `app/static/css/app.css` DEBE contener tokens de diseño en `:root`
  y secciones comentadas para reset, variables, tipografía, layout, componentes,
  utilidades y responsive.
- **FR-010**: HTMX DEBE estar vendoreado en `app/static/vendor/htmx.min.js` y NO
  cargarse desde CDN.
- **FR-011**: Los iconos SVG outline de Lucide DEBEN vendorearse uno por archivo
  en `app/static/icons/`. Set inicial: `layout-dashboard`, `building-2`, `users`,
  `file-text`, `wallet`, `wrench`, `settings`, `menu`, `x`, `check-circle-2`,
  `alert-triangle`, `alert-circle`, `info`.
- **FR-012**: `app/templates/base.html` DEBE definir layout con sidebar fija,
  área principal y zona de mensajes flash (`#flash-zone`).
- **FR-013**: `app/templates/macros/icons.html` DEBE definir la macro
  `icon(nombre, size, class)` que inyecte el SVG inline desde
  `app/static/icons/`.
- **FR-014**: Los componentes en `app/templates/components/` DEBEN incluir:
  `_sidebar.html`, `_navbar.html`, `_card_propiedad.html`,
  `_tarjeta_metrica.html`, `_accesos_rapidos.html`, `_badge_estado.html`,
  `_form_field.html`, `_alerta.html`.
- **FR-015**: La sidebar DEBE colapsar a overlay por debajo de 1024px y ocultarse
  completamente con toggle hamburguesa por debajo de 768px.
- **FR-016**: `ruff` DEBE configurarse en `pyproject.toml` con target `py313`,
  `line-length = 88` y reglas `E`, `F`, `I`, `B`, `UP`, `ASYNC`.
- **FR-017**: `mypy` DEBE configurarse en modo estricto como mínimo para
  `app/modules/`.
- **FR-018**: `pytest-asyncio` DEBE configurarse con `asyncio_mode = "auto"` en
  `pyproject.toml`.
- **FR-019**: Los tests DEBEN incluir smoke test de `GET /health` y smoke test de
  `GET /`, usando `httpx.AsyncClient` y `pytest-asyncio`.
- **FR-020**: La estructura de directorios DEBE respetar el layout definido en la
  constitución (sección XIII).
- **FR-021**: Todo el contenido Markdown, comentarios, docstrings y mensajes de
  commit DEBEN estar en español, sin mezclar idiomas.
- **FR-022**: NO DEBE existir referencia alguna a Supabase en el código,
  configuración o documentación.
- **FR-023**: NO DEBEN existir archivos `.yml`; toda infraestructura YAML DEBE
  usar extensión `.yaml`.
- **FR-024**: `pyproject.toml` DEBE declarar las dependencias de producción:
  `fastapi[scalar]`, `sqlalchemy[asyncio]`, `asyncpg`, `alembic`, `pydantic`,
  `pydantic-settings`, `jinja2`, `python-multipart`.
- **FR-025**: `pyproject.toml` DEBE declarar las dependencias de desarrollo:
  `pytest`, `pytest-asyncio`, `httpx`, `ruff`, `mypy`, `testcontainers`.

### Key Entities

- **Configuración**: Parámetros de entorno (`DATABASE_URL`, `APP_ENV`,
  `LOG_LEVEL`) validados por `pydantic-settings`. Sin entidad de base de datos
  asociada.
- **Dashboard Demo**: Estructura de página con datos hardcodeados (métricas,
  accesos rápidos). No persiste entidades; es puramente presentacional.
- **Migración Baseline**: Primera migración Alembic que instala la extensión
  `pgcrypto` mediante `CREATE EXTENSION IF NOT EXISTS pgcrypto` para dejar
  disponible `gen_random_uuid()` a los módulos futuros.

## Success Criteria

### Measurable Outcomes

- **SC-001**: `uv sync` instala todas las dependencias de producción y desarrollo
  sin errores en una sola ejecución.
- **SC-002**: `uv run fastapi dev app/main.py` arranca el servidor en menos de 5
  segundos.
- **SC-003**: `GET /health` responde en menos de 500ms cuando PostgreSQL está
  disponible.
- **SC-004**: `GET /` retorna HTML completo con sidebar, navbar y 3 tarjetas de
  métrica.
- **SC-005**: La sidebar colapsa a overlay por debajo de 1024px y se oculta
  completamente con toggle hamburguesa por debajo de 768px, expandiéndose
  correctamente al superar cada breakpoint.
- **SC-006**: `uv run alembic upgrade head` aplica la baseline contra PostgreSQL
  local sin errores.
- **SC-007**: `uv run ruff check .` termina con 0 errores y 0 warnings.
- **SC-008**: `uv run ruff format --check .` termina sin diferencias de formato.
- **SC-009**: `uv run mypy --strict app/modules/` termina sin errores de tipo.
- **SC-010**: Los smoke tests de `/health` y `/` pasan en verde con
  `uv run pytest`.
- **SC-011**: Cero referencias a Supabase en todo el repositorio.
- **SC-012**: Cero archivos con extensión `.yml` en todo el repositorio.

## Assumptions

- El desarrollador tiene Docker y Docker Compose instalados localmente para
  ejecutar PostgreSQL.
- El desarrollador tiene Python 3.13.13 disponible o `uv` puede descargarlo
  automáticamente.
- El puerto por defecto de PostgreSQL en Docker Compose será `5432`.
- Las credenciales por defecto de la base de datos local serán
  `realtor_dev` / `realtor_dev` / `realtor_dev`.
- La migración baseline de Alembic incluirá `CREATE EXTENSION IF NOT EXISTS
  pgcrypto` para habilitar `gen_random_uuid()` en futuros módulos.
- La versión de PostgreSQL en Docker Compose será `16-alpine`.
- El dashboard demo usará datos hardcodeados en el template, sin acceso a base
  de datos.
- Los iconos SVG de Lucide se descargarán por el agente desde
  `https://lucide.dev/api/icons/<nombre>` durante la implementación y se
  guardarán en `app/static/icons/`.
- El modo `asyncio_mode = "auto"` de pytest-asyncio aplica a todo el proyecto,
  no solo a `app/modules/`.
- HTMX 1.x se vendoreará desde su fuente oficial en una tarea explícita de
  descarga, no en runtime.
- La configuración de `mypy --strict` aplica como mínimo a `app/modules/`; puede
  extenderse a más directorios sin romper el criterio.

## Clarificaciones

Resoluciones de `/speckit.clarify` del 2026-06-08.

### Breakpoints responsive de la sidebar

- **Desktop** (≥ 1024px): sidebar visible y expandida.
- **Tablet** (768px – 1023px): sidebar colapsada como overlay; se despliega con
  toggle hamburguesa superpuesto sobre el contenido.
- **Móvil** (< 768px): sidebar oculta; toggle hamburguesa la revela como overlay
  de ancho completo.
- Implementación: media queries `max-width` con enfoque desktop-first.

### Comportamiento de GET /health ante fallo de BD

- Timeout de 2 segundos en la ejecución de `SELECT 1`.
- Código HTTP: `503 Service Unavailable`.
- Cuerpo JSON:
  ```json
  {"status": "error", "database": "unavailable", "detail": "timeout after 2s"}
  ```

### Tarjetas de métrica del dashboard

| Label               | Número | Icono          |
|---------------------|--------|----------------|
| Propiedades activas | 124    | `building-2`   |
| Inquilinos al día   | 87     | `users`        |
| Contratos vigentes  | 53     | `file-text`    |

### Alcance de componentes estructurales

Los 8 componentes de `app/templates/components/` se entregan con HTML + CSS
completo y funcional desde el día 1:

- `_sidebar.html`, `_navbar.html`, `_tarjeta_metrica.html`,
  `_accesos_rapidos.html`, `_card_propiedad.html`, `_badge_estado.html`,
  `_form_field.html`, `_alerta.html`.

### Generación de los 13 SVG de Lucide

El agente descarga cada icono desde `https://lucide.dev/api/icons/<nombre>`
durante la implementación y lo guarda en `app/static/icons/<nombre>.svg`.

Set inicial: `layout-dashboard`, `building-2`, `users`, `file-text`, `wallet`,
`wrench`, `settings`, `menu`, `x`, `check-circle-2`, `alert-triangle`,
`alert-circle`, `info`.

### Migración baseline de Alembic

La migración baseline incluye `CREATE EXTENSION IF NOT EXISTS pgcrypto` para
dejar disponible `gen_random_uuid()` a los módulos futuros. No se crean esquemas
adicionales ni tablas de dominio en esta migración.

### Política de logging

- `GET /health`: registra `WARNING` solo en caso de fallo de base de datos
  (timeout o error de conexión). En éxito no emite logs propios.
- `GET /`: sin logging explícito. Solo aplican los logs automáticos de acceso
  HTTP de uvicorn.
