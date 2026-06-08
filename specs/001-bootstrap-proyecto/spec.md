# Feature Specification: Bootstrap del Proyecto Realtor

**Feature Branch**: `001-bootstrap-proyecto`

**Creada**: 2026-06-08

**Estado**: Draft

**Input**: Prompt fuente `001-bootstrap-proyecto` — especificación fundacional del sistema Realtor.

## User Scenarios & Testing *(obligatorio)*

### User Story 1 - Health check del sistema (Priority: P1)

Un operador o herramienta de monitoreo necesita verificar que el sistema y su
base de datos están vivos. Invoca `GET /health` y recibe un JSON con el estado
de la aplicación y el resultado de una consulta de conectividad a PostgreSQL.

**Por qué esta prioridad**: Sin health check no hay forma de saber si el
deploy funcionó o si la base de datos responde. Es el endpoint mínimo para
validar que todo el stack está cableado correctamente.

**Test independiente**: `curl /health` retorna `200 OK` con un JSON que
contiene `app` y `database` con estado `ok`.

**Acceptance Scenarios**:

1. **Given** la app está corriendo y PostgreSQL responde, **When** se hace
   `GET /health`, **Then** responde `200` con `{"app": "ok", "database": "ok"}`.
2. **Given** la app está corriendo pero PostgreSQL no responde, **When** se
   hace `GET /health`, **Then** responde `503` con `{"app": "ok", "database":
   "error", "detail": "<mensaje>"}`.

---

### User Story 2 - Dashboard demo inicial (Priority: P1)

Un usuario abre el navegador en la raíz del sitio y ve un panel de control con
barra lateral de navegación, barra superior y tres tarjetas de métrica con
valores hardcodeados. Esto confirma que todo el pipeline de templates, CSS,
íconos y layout funciona de extremo a extremo.

**Por qué esta prioridad**: El dashboard es el punto de entrada visual. Sin
él no se puede validar que Jinja2, HTMX, CSS propio, iconografía SVG y
componentes parciales funcionan integrados.

**Test independiente**: `GET /` retorna HTML con sidebar visible, navbar y
al menos 3 elementos con clase `tarjeta-metrica`.

**Acceptance Scenarios**:

1. **Given** el servidor está corriendo, **When** se hace `GET /`, **Then**
   el HTML contiene una sidebar con clase `sidebar`, una navbar con clase
   `navbar` y al menos 3 elementos con clase `tarjeta-metrica`.
2. **Given** viewport menor a 768px, **When** se carga `GET /`, **Then**
   la sidebar está colapsada y tiene un botón hamburguesa para expandirla.

---

### User Story 3 - Infraestructura de base de datos (Priority: P2)

Un desarrollador levanta PostgreSQL con Docker Compose, ejecuta las migraciones
con Alembic y obtiene una migración baseline aplicada sin errores. La base de
datos queda lista para que módulos futuros creen sus tablas.

**Por qué esta prioridad**: Sin base de datos operativa no se puede persistir
ningún dato de dominio. Es prerequisito para cualquier spec posterior.

**Test independiente**: `docker compose up -d && uv run alembic upgrade head`
completa sin errores y la migración baseline queda registrada en la tabla
`alembic_version`.

**Acceptance Scenarios**:

1. **Given** Docker está corriendo, **When** se ejecuta `docker compose up -d`,
   **Then** PostgreSQL acepta conexiones en `localhost:5432`.
2. **Given** PostgreSQL está corriendo, **When** se ejecuta
   `uv run alembic upgrade head`, **Then** la migración baseline se aplica sin
   errores.
3. **Given** la migración baseline fue aplicada, **When** se ejecuta
   `SELECT 1` vía `GET /health`, **Then** la respuesta es exitosa.

---

### User Story 4 - Sistema visual base (Priority: P2)

El sistema visual base está operativo: tokens de diseño en `:root`, layout
responsive con sidebar colapsable, componentes parciales reutilizables y
macro de iconos. Cualquier spec futura puede extender este sistema sin
redefinir estilos base.

**Por qué esta prioridad**: El sistema visual es la piel de toda la
aplicación. Sin él, cada feature tendría que definir sus propios estilos,
rompiendo la consistencia visual.

**Test independiente**: El CSS contiene variables en `:root` con al menos
`--color-bg`, `--color-accent`, `--space-4`; la sidebar colapsa bajo 1024px;
la macro `icon("layout-dashboard")` inyecta SVG inline.

**Acceptance Scenarios**:

1. **Given** el CSS está cargado, **When** se inspeccionan las variables en
   `:root`, **Then** existen `--color-bg`, `--color-surface`, `--color-text`,
   `--color-accent`, `--color-success`, `--color-warning`, `--color-danger`,
   `--color-info`, escalas de `--space-*`, `--radius-*` y `--shadow-*`.
2. **Given** viewport >= 768px, **When** se renderiza la página, **Then**
   la sidebar es visible y fija al costado izquierdo (240px en ≥1024px,
   200px en 768-1023px).
3. **Given** viewport < 768px, **When** se renderiza la página, **Then**
   la sidebar está oculta y un botón hamburguesa (`menu`) la muestra como
   overlay toggle.

---

### User Story 5 - Calidad estática (Priority: P2)

El proyecto pasa limpiamente las verificaciones de linting, formato y type
checking. Esto garantiza que el código base cumple los estándares definidos
en la constitución desde el primer commit.

**Por qué esta prioridad**: Las herramientas de calidad son la primera línea
de defensa contra errores. Deben estar configuradas y pasar limpias antes de
escribir cualquier lógica de dominio.

**Test independiente**: `uv run ruff check .`, `uv run ruff format --check .`
y `uv run mypy --strict app/modules/` retornan cero errores.

**Acceptance Scenarios**:

1. **Given** todo el código fuente está escrito, **When** se ejecuta
   `uv run ruff check .`, **Then** no hay errores ni advertencias.
2. **Given** todo el código fuente está escrito, **When** se ejecuta
   `uv run ruff format --check .`, **Then** el formato es correcto.
3. **Given** existen archivos Python en `app/modules/`, **When** se ejecuta
   `uv run mypy --strict app/modules/`, **Then** no hay errores de tipo.

---

### User Story 6 - Iconografía vendoreada (Priority: P3)

Todos los iconos del sistema son SVG outline de Lucide, almacenados
localmente en `app/static/icons/`, accesibles mediante la macro Jinja2
`icon(nombre, size, class)`. No hay dependencias externas de iconografía.

**Por qué esta prioridad**: Los iconos son necesarios para la interfaz pero
no bloquean la funcionalidad core. Pueden agregarse incrementalmente.

**Test independiente**: Verificar que cada archivo `.svg` del set inicial
existe en `app/static/icons/` y que `icon("layout-dashboard")` renderiza
el SVG inline con `currentColor`.

**Acceptance Scenarios**:

1. **Given** el set inicial de 13 iconos, **When** se lista
   `app/static/icons/`, **Then** existen exactamente los archivos:
   `layout-dashboard.svg`, `building-2.svg`, `users.svg`, `file-text.svg`,
   `wallet.svg`, `wrench.svg`, `settings.svg`, `menu.svg`, `x.svg`,
   `check-circle-2.svg`, `alert-triangle.svg`, `alert-circle.svg`, `info.svg`.
2. **Given** la macro `icon("layout-dashboard")`, **When** se invoca en un
   template, **Then** retorna el SVG inline con `stroke="currentColor"` y sin
   atributos `fill`.

---

### Edge Cases

- ¿Qué sucede si `DATABASE_URL` no está definida en `.env`? La app debe
  arrancar igual pero `GET /health` debe responder `503` con `database:
  "error"` y `detail` descriptivo.
- ¿Qué sucede si PostgreSQL no está corriendo al hacer `GET /health`? Debe
  responder `503` con `database: "error"` y `detail` con el mensaje de
  conexión, sin crashear la app.
- ¿Qué sucede si se solicita un icono que no existe? La macro `icon()` debe
  retornar un fallback silencioso (SVG vacío o placeholder) sin romper el
  renderizado.
- ¿Qué sucede si `docker compose up` encuentra el puerto 5432 ocupado? El
  compose debe reportar el error claramente.
- ¿Qué sucede si `alembic upgrade head` se ejecuta sin la base de datos
  corriendo? Debe fallar con un mensaje descriptivo de conexión rechazada.
- ¿Qué sucede si `uv sync` se ejecuta sin Python 3.13+? `uv` debe reportar
  que la versión requerida no está disponible.
 - ¿Qué sucede si el dashboard se renderiza sin JavaScript? La sidebar debe
   ser visible por defecto (desktop-first), sin depender de JS para el layout
   base.

## Clarificaciones

Decisiones tomadas durante la sesión de clarificación del 2026-06-08.

### C1 — Breakpoints responsive de la sidebar

Dos breakpoints definidos:

- **≥1024px**: sidebar fija de 240px de ancho, siempre visible.
- **768-1023px**: sidebar fija de 200px de ancho, siempre visible.
- **<768px**: sidebar colapsada. Un botón hamburguesa (ícono `menu`) la muestra
  como overlay toggle sobre el contenido.

### C2 — Respuesta de `GET /health` con base de datos caída

Cuando PostgreSQL no responde, el endpoint retorna:

```json
HTTP 503 Service Unavailable
{
  "app": "ok",
  "database": "error",
  "detail": "<mensaje de la excepción>"
}
```

Se emite `logger.warning` con el error de conexión.

### C3 — Contenido de las 3 tarjetas de métrica del dashboard

| Label              | Número    | Icono           |
|--------------------|-----------|-----------------|
| Propiedades        | 24        | `building-2`    |
| Inquilinos         | 56        | `users`         |
| Ingresos mensuales | $128,500  | `wallet`        |

Valores hardcodeados. Sin conexión a base de datos.

### C4 — Nivel de completitud de los componentes estructurales

Todos los componentes parciales se implementan con **HTML + CSS funcional
completo**, incluyendo estilos reales, datos de ejemplo representativos y
estados visuales según lo definido en `.opencode/instructions/frontend.md`.
No se usan placeholders "lorem ipsum" ni esqueletos sin estilo.

### C5 — Generación de los 13 archivos SVG de Lucide

Durante la fase de implementación, el agente descarga los 13 iconos SVG desde
el repositorio oficial de Lucide (https://github.com/lucide-icons/lucide) usando
un script de shell. Cada SVG se almacena en `app/static/icons/<nombre>.svg` con
`stroke-width="2"`, `stroke="currentColor"` y sin atributos `fill`.

### C6 — Migración baseline de Alembic

La migración baseline incluye la activación de la extensión `pgcrypto`:

```sql
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
```

Esto garantiza que `gen_random_uuid()` esté disponible para todas las entidades
futuras sin requerir una migración adicional.

### C7 — Política de logging en `/health` y `/`

- `logger.info` al inicio de cada request (`extra={"path": "..."}`).
- `logger.info` al final exitoso.
- `logger.warning` en fallo de conectividad a la base de datos.
- `logger.error` ante excepciones no esperadas.
- Sin incluir IPs, headers ni datos sensibles.
- Formato estructurado según `backend.md`.

## Requirements *(obligatorio)*

### Functional Requirements

**Estructura del proyecto**

- **FR-001**: El proyecto DEBE contener el directorio `app/` con `__init__.py`,
  `main.py`, `config.py` y `database.py`.
- **FR-002**: El proyecto DEBE contener `app/modules/` como paquete Python
  vacío, preparado para módulos de feature futuros.
- **FR-003**: El proyecto DEBE contener `app/static/css/app.css` con tokens de
  diseño en `:root` y secciones comentadas para reset, variables, tipografía,
  layout, componentes, utilidades y responsive.
- **FR-004**: El proyecto DEBE contener `app/static/vendor/htmx.min.js`
  vendoreado localmente. PROHIBIDO cargarlo desde CDN.
- **FR-005**: El proyecto DEBE contener `app/static/icons/` con exactamente
  13 iconos SVG outline de Lucide, uno por archivo.
- **FR-006**: El proyecto DEBE contener `alembic/` inicializado en modo async
  con su `env.py` leyendo `DATABASE_URL` del entorno. La migración baseline
  DEBE incluir `CREATE EXTENSION IF NOT EXISTS "pgcrypto"`.

**Configuración**

- **FR-007**: `app/config.py` DEBE usar `pydantic-settings` para leer
  configuración desde variables de entorno y archivo `.env`.
- **FR-008**: La configuración DEBE exponer como mínimo `DATABASE_URL`,
  `APP_ENV` y `LOG_LEVEL`.
- **FR-009**: El proyecto DEBE contener `.env.example` documentando las
  variables requeridas sin secretos reales.
- **FR-010**: El archivo `.env` NUNCA debe versionarse (listado en
  `.gitignore`).

**Base de datos**

- **FR-011**: El proyecto DEBE contener `docker-compose.yaml` en la raíz
  definiendo un servicio PostgreSQL 16 Alpine.
- **FR-012**: `app/database.py` DEBE configurar un `AsyncEngine` y una fábrica
  de `AsyncSession` usando `asyncpg`.
- **FR-013**: `app/database.py` DEBE exponer una dependencia `get_session` que
  provea `AsyncSession` por request.
- **FR-014**: Alembic DEBE estar configurado en modo async, leyendo
  `DATABASE_URL` desde el entorno.
- **FR-015**: Alembic DEBE poder ejecutar `alembic upgrade head` contra
  PostgreSQL local sin errores.
- **FR-016**: La entidad `Base` de SQLAlchemy DEBE declararse en
  `app/database.py` usando `DeclarativeBase`.

**Endpoints**

- **FR-017**: `GET /health` DEBE retornar JSON con `{"app": "ok", "database":
  "ok"}` cuando todo está saludable (200). Con base de datos caída, DEBE
  retornar `{"app": "ok", "database": "error", "detail": "<mensaje>"}` (503).
- **FR-018**: `GET /health` DEBE ejecutar `SELECT 1` asíncrono contra
  PostgreSQL para verificar conectividad y emitir `logger.warning` en caso
  de fallo.
- **FR-019**: `GET /` DEBE renderizar un dashboard demo con sidebar fija,
  navbar superior y al menos 3 tarjetas de métrica con datos hardcodeados.
- **FR-020**: `GET /` DEBE usar `app/templates/base.html` como layout base y
  los componentes parciales de `app/templates/components/`.

**Sistema visual**

- **FR-021**: `app/static/css/app.css` DEBE declarar en `:root` todos los
  tokens de diseño definidos en `.opencode/instructions/frontend.md`:
  colores (`--color-bg`, `--color-surface`, `--color-text`,
  `--color-text-muted`, `--color-border`, `--color-accent`,
  `--color-success`, `--color-warning`, `--color-danger`, `--color-info`),
  espaciado (escala `--space-1` a `--space-12`), radios (`--radius-sm`,
  `--radius-md`, `--radius-lg`), sombras (`--shadow-sm`, `--shadow-md`,
  `--shadow-lg`), tipografía (`--font-sans`, `--font-size-base`,
  `--line-height-base`).
- **FR-022**: `app/templates/base.html` DEBE definir un layout con sidebar
  lateral fija, área de contenido principal y zona de mensajes flash
  (`#flash-zone`).
- **FR-023**: `app/templates/macros/icons.html` DEBE definir la macro
  `icon(nombre, size, class)` que inyecta el SVG inline desde
  `app/static/icons/<nombre>.svg`.
- **FR-024**: `app/templates/components/` DEBE contener 8 componentes
  parciales: `_sidebar.html`, `_navbar.html`, `_card_propiedad.html`,
  `_tarjeta_metrica.html`, `_accesos_rapidos.html`, `_badge_estado.html`,
  `_form_field.html`, `_alerta.html`.
- **FR-025**: La sidebar DEBE ser fija en desktop/tablet (≥768px, 240px en
  ≥1024px, 200px en 768-1023px) y colapsable como overlay toggle en <768px
  con un botón hamburguesa.
- **FR-026**: El layout DEBE seguir la convención desktop-first con media
  queries `max-width`.
- **FR-027**: Los componentes parciales NO deben contener lógica de negocio
  ni llamadas a base de datos. Reciben datos por contexto Jinja2.

**Calidad estática**

- **FR-028**: `pyproject.toml` DEBE configurar `ruff` con target `py313`,
  `line-length = 88` y reglas `E`, `F`, `I`, `B`, `UP`, `ASYNC` como mínimo.
- **FR-029**: `pyproject.toml` DEBE configurar `mypy` en modo estricto como
  mínimo para `app/modules/`.
- **FR-030**: `pyproject.toml` DEBE configurar `pytest-asyncio` con
  `asyncio_mode = "auto"`.

**Tests**

- **FR-031**: El proyecto DEBE incluir un smoke test de `GET /health` que
  verifique status 200 y estructura JSON.
- **FR-032**: El proyecto DEBE incluir un smoke test de `GET /` que verifique
  status 200 y presencia de sidebar, navbar y tarjetas de métrica.
- **FR-033**: Los tests HTTP DEBEN usar `httpx.AsyncClient`.

### Key Entities

- **Config**: Parámetros de configuración de la aplicación (`DATABASE_URL`,
  `APP_ENV`, `LOG_LEVEL`) leídos desde variables de entorno vía
  `pydantic-settings`.
- **Base**: Clase base declarativa de SQLAlchemy 2.x para todas las entidades
  futuras. No tiene tablas propias en esta spec.

## Success Criteria *(obligatorio)*

### Measurable Outcomes

- **SC-001**: `uv sync` instala todas las dependencias sin errores.
- **SC-002**: `uv run fastapi dev app/main.py` arranca el servidor y responde
  en `http://localhost:8000`.
- **SC-003**: `GET /health` responde `200 OK` con `{"app": "ok", "database":
  "ok"}`.
- **SC-004**: `GET /` renderiza un dashboard demo con sidebar visible y al
  menos 3 tarjetas de métrica.
- **SC-005**: El layout es responsive: la sidebar colapsa bajo 768px de
  viewport y tiene breakpoints en 768px y 1024px.
- **SC-006**: Los 13 iconos del set inicial son SVG vendoreados desde
  `app/static/icons/`, sin dependencias externas.
- **SC-007**: `uv run alembic upgrade head` aplica la migración baseline
  contra PostgreSQL local sin errores.
- **SC-008**: `uv run ruff check .` pasa limpio (cero errores).
- **SC-009**: `uv run ruff format --check .` pasa limpio.
- **SC-010**: `uv run mypy --strict app/modules/` pasa limpio.
- **SC-011**: Los smoke tests de `/health` y `/` pasan en verde con
  `uv run pytest`.
- **SC-012**: Ningún archivo Markdown del repositorio mezcla idiomas
  (100 % español en specs, plan, tasks, comentarios y docstrings).
- **SC-013**: No existen referencias a Supabase en ningún archivo del
  repositorio.
- **SC-014**: No existen archivos con extensión `.yml` creados por el
  proyecto; todos los archivos YAML propios usan extensión `.yaml`.

## Assumptions

- PostgreSQL 16 Alpine se ejecuta localmente con Docker Compose. El
  desarrollador tiene Docker instalado y corriendo.
- Python 3.13 o superior está disponible en el sistema. El archivo
  `.python-version` ya existe y `uv` lo respeta.
- `uv` está instalado globalmente y es el único gestor de paquetes y
  proyectos.
- HTMX 1.x minified (`htmx.min.js`) se descarga y vendorea manualmente en
  `app/static/vendor/`. No se usa CDN.
- Los iconos SVG de Lucide se descargan individualmente desde
  https://lucide.dev/icons/ con atributos `stroke-width="2"` y sin `fill`.
- La migración baseline de Alembic es una revisión inicial que activa la
  extensión `pgcrypto` (para `gen_random_uuid()`) y crea la tabla
  `alembic_version`. Las tablas de dominio se crearán en specs posteriores.
- El dashboard demo usa datos hardcodeados. No requiere base de datos para
  renderizarse.
- No se necesita autenticación, autorización ni manejo de usuarios en esta
  spec.
- El proyecto se ejecuta en `localhost:8000` durante desarrollo.
- Los scripts auxiliares en `scripts/` (dev-setup.sh, db/*.sh) son atajos
  de conveniencia y no reemplazan los comandos canónicos (`uv sync`,
  `uv run alembic`, `docker compose`).
