# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/) y este proyecto sigue versionado SemVer cuando aplique.

## [Unreleased]

### Added

- Repositorio inicializado desde plantilla Specify con tooling Spec Kit, estructura de specs, workflows y scripts de automatización.
- Constitución del proyecto Realtor v1.0 (`constitution.md`) con stack obligatorio, arquitectura de vertical slice, prohibiciones y reglas de calidad.
- Infraestructura base (spec 001): Docker Compose con PostgreSQL, Alembic para migraciones, `.env.example`, `Makefile` con targets de desarrollo (`up`, `down`, `migrate`, `dev`, `reset`) y scripts de base de datos.
- Bootstrap de la aplicación (spec 001): FastAPI con motor ASGI, SQLAlchemy 2.x async con `Mapped` y `mapped_column`, Jinja2 server-rendered + HTMX vendoreado, Pydantic v2 con `frozen=True`, pytest + pytest-asyncio + httpx.AsyncClient.
- Sistema de diseño CSS completo en `app/static/css/app.css`: tokens visuales canónicos en `:root` (colores, sombras, radios, espaciado, tipografía, breakpoints), reset, layout sidebar + main, y CSS responsive desktop-first.
- Ocho componentes compartidos en `app/templates/components/`: `_sidebar.html`, `_navbar.html`, `_card_propiedad.html`, `_tarjeta_metrica.html`, `_accesos_rapidos.html`, `_badge_estado.html`, `_alerta.html`, `_form_field.html`.
- Trece iconos SVG outline de Lucide vendoreados en `app/static/icons/`: `layout-dashboard`, `building-2`, `users`, `file-text`, `wallet`, `wrench`, `settings`, `menu`, `x`, `check-circle-2`, `alert-triangle`, `alert-circle`, `info`.
- Macro `icon()` en `app/templates/macros/icons.html` para inyectar iconos SVG inline con `currentColor`.
- Layout base `app/templates/base.html` con sidebar fija, navbar superior y zona de flash messages.
- Dashboard inicial con endpoint de health check y tests de cobertura.
- Gobernanza visual (spec 002): script `scripts/tools/check-visual-trace.sh` que verifica integridad de tokens CSS comparando `:root` contra el contrato `visual-trace.yaml`; tareas de blindaje con marcadores `[visual]` en `tasks.md`.
- Sección XII de la constitución: protección de tokens visuales canónicos y reglas de trazabilidad obligatoria para cualquier modificación.
- Spec 003 (`rediseñar home`): spec.md, checklist de requisitos, contratos, data model, plan, research, quickstart y tareas.
- Dashboard rediseñado (spec 003): tarjetas de métricas con estados de carga (`hx-indicator`), error y datos; sección de accesos rápidos con iconografía a 28px y espaciado consistente; componente `_actividad_item.html` con badge de tipo, descripción y fecha relativa; iconos `clock` y `calendar` agregados al set vendoreado; CSS responsive para los tres breakpoints (desktop, tablet 1023px, móvil 767px).
- Infraestructura de changelog automatizado: hook `post-commit` vía `scripts/tools/changelog.sh` que recuerda curar el changelog tras cada commit; agente cronista (`.opencode/agents/changelog.md`) que cura `CHANGELOG.md` desde el historial Git usando la marca `last-processed-commit`.
- Agente `improve-commits` (`.opencode/agents/improve-commits.md`) para auditoría y renombrado de mensajes de commit según Conventional Commits.
- Instrucciones unificadas de convenciones (`conventions.instructions.md`) que consolidan nomenclatura, formato de commits, ramas, tests, CSS, iconografía y gobernanza visual.
- Comandos `changelog` e `improve-commits` registrados en `opencode.json` con plantillas de ejecución y agentes asociados.
- `openCode.json` en la raíz del repositorio para configuración declarativa de comandos y carga de instrucciones.
- `scripts/tools/install-git-hooks.sh`: instalador de hooks Git que copia hooks desde `scripts/hooks/` a `.git/hooks/` con respaldo automático vía timestamp.
- `scripts/tools/context.sh`: generador de contexto para repomix (`npx repomix --output docs/context/repo-state.xml`).
- `.repomixignore`: reglas de exclusión para repomix (virtualenvs, cachés Python, artefactos de build, logs, IDE, binarios).
- Hook `ruff-format` en `.pre-commit-config.yaml` con auto-formateo (respeta `[tool.ruff.format]` en `pyproject.toml`).
- Sección «Pre-commit y calidad automatizada» en `conventions.instructions.md` documentando hooks automáticos, manuales y comandos Makefile equivalentes.
- `.pre-commit-config.yaml`, `pyupgrade`, `ruff-format` y `pydocstyle` registrados en el stack obligatorio de la constitución y `AGENTS.md`.
- Módulo `propiedades` (spec 004): modelos SQLAlchemy, repositorio async, servicio con lógica de negocio, esquemas Pydantic y rutas FastAPI para la gestión de propiedades inmobiliarias.
- Migración Alembic `002_create_propiedades.py` con la tabla `propiedades`, incluyendo columnas, constraints, índices y claves foráneas.
- Scripts de base de datos: `seed_propiedades.py` para datos de prueba y `db_preflight.py` para validación del estado de migraciones antes de operaciones.
- Tests del módulo `propiedades`: tests unitarios de modelos y esquemas; tests de integración con Testcontainers para repositorio, servicio, migración y seed.
- Skill `db-preflight` para validación automatizada del estado de la base de datos antes de ejecutar implementaciones Spec Kit.
- Documentación completa de spec 004: spec, plan, tasks, modelo de datos, contratos YAML, checklist de requisitos, quickstart, research y report.
- Prompts de Spec Kit para spec 004: 7 prompts (spec, clarify, plan, analyze, tasks, implement, fix-report) con frontmatter estandarizado.
- Hook `format-docstrings` como script local en `scripts/ci/format-docstrings.py` que convierte docstrings single-line de funciones y clases a formato multi-línea respetando la convención Google de pydocstyle; integrado en `.pre-commit-config.yaml` después de `ruff-format` y antes de `pydocstyle`.
- `.repomixignore` restaurado con sus 94 líneas de patrones de exclusión originales; eliminada su entrada de `.gitignore` para que git lo trackee nuevamente.
- Comandos PonyTail de auditoría y gestión de deuda técnica registrados en `opencode.json` y `Makefile`.
- Script `scripts/ci/auto-checks.sh` para ejecución optimizada de pre-commit con captura de salida y reintento en caso de error.
- Flujo Spec Kit expandido de 6 a 8 pasos en constitución (v1.4.0) y AGENTS.md: integrado el loop `analyze → fix-report → analyze` para garantizar cero hallazgos antes de generar `tasks.md`; `report.md` pasa a ser requisito previo a la implementación.
- Módulo vertical `dashboard` (spec 005): servicio, repositorio, rutas y esquemas Pydantic para la página principal del sistema; endpoint `GET /` migrado de `app/main.py` a `app/modules/dashboard/routes.py`.
- Funciones `contar_por_estado()` y `contar_total()` en el repositorio de propiedades para consultas agregadas por estado del catálogo, utilizadas por el dashboard.
- Métricas reales desde base de datos en el dashboard: propiedades disponibles y rentadas calculadas con datos persistidos.
- Métricas no operativas (ingresos y vencidos) con valor 0 y marcador "No disponible" hasta que exista el módulo de transacciones.
- Estado vacío del dashboard: se activa automáticamente cuando no hay propiedades en la base de datos, mostrando mensaje informativo en lugar de las secciones de métricas, accesos y actividad.
- Template `dashboard.html` actualizado con métricas dinámicas desde el servicio, estado vacío condicional y marcador visual de métrica no disponible.
- 9 tests unitarios del servicio de dashboard con mocks del repositorio (`tests/unit/dashboard/test_service.py`).
- 6 tests de integración del dashboard con Testcontainers: endpoint, estado vacío, orden vertical de secciones, accesos rápidos, presencia de sidebar/navbar y respuesta HTTP 200 (`tests/integration/dashboard/test_dashboard.py`).
- Artefactos completos de spec 005 en `specs/005-dashboard-datos-reales/`: spec, plan, tasks, report de análisis, research, modelo de datos, quickstart, checklist de requisitos y contratos YAML.
- 7 prompts de Spec Kit para spec 005 en `.opencode/prompts/` con frontmatter estandarizado (specify, clarify, plan, analyze, tasks, implement, fix-report).
- Tests unitarios de rutas del dashboard con mocks del servicio: verificación de renderizado HTML con métricas (`test_dashboard_route_renderiza_html_con_metricas`) y estado vacío (`test_dashboard_route_renderiza_estado_vacio`), sin dependencia de PostgreSQL (spec 005).
- Tests unitarios del repositorio del dashboard con mocks de `contar_por_estado` y `contar_total`: verificación de `obtener_metricas` con y sin datos (spec 005).
- Tests unitarios de `Propiedad.__repr__`: verifica que el método incluye id, título y estado del modelo.
- Tests unitarios de `PropiedadIn`: validación de tipo de estado no soportado (`estado=42`) rechazado por Pydantic.
- Tests de integración del repositorio de propiedades: `test_eliminar_id_inexistente_retorna_false`, `test_contar_por_estado_con_datos`, `test_contar_por_estado_sin_datos`, `test_contar_total_con_datos`, `test_contar_total_sin_datos` (spec 004).
- Tests de integración del dashboard: `test_marcador_dentro_de_tarjeta` (verifica que "No disponible" se renderiza dentro de la tarjeta métrica) y `test_metricas_valores_reales_4_y_3` (verifica valores 4 y 3 del seed) (spec 005).
- Funciones helper en `conftest.py` de integración: `alembic_ok()`, `seed_ok()` y `setup_db()` con validación de returncode de Alembic y seed (spec 005).
- Módulo vertical `health` (spec 005): endpoint `GET /health` con rutas, esquemas y tests propios, extraído de `app/main.py`.
- Soporte para `pydantic-settings[yaml]` en dependencias del proyecto para lectura de `config/app.yaml`.
- Página `GET /propiedades` con grid de 3 columnas de cards, encabezado con título y subtítulo, y estado vacío con icono y mensaje (spec 006).
- Sección CSS `.propiedades-grid` con layout responsive: 3 columnas en desktop, 2 en tablet (≤1023px) y 1 en móvil (≤767px) (spec 006).
- Función `listar_propiedades()` en el servicio de propiedades: formatea precio como `$X,XXX.00`, área como `X,XXX m²` y mapea entidades a diccionario con 8 campos (spec 006).
- Tests unitarios del servicio `listar_propiedades`: verifica formato de precio, área, lista vacía y 8 campos requeridos (`tests/unit/propiedades/test_service_listar.py`) (spec 006).
- Tests de integración del endpoint `GET /propiedades`: respuesta 200 con layout, renderizado de 10 cards del seed, estructura de cards (media/body/footer), imágenes explícitas, ausencia de estilos inline, estado vacío, placeholder de imagen, sidebar activo, breadcrumb dinámico y 7 items de navegación separados (`tests/integration/propiedades/test_routes.py`) (spec 006).
- Tests del seed: verificación de ausencia de `hashlib`/`picsum.photos`, imagen explícita por propiedad, persistencia de imágenes en BD y migración en `ON CONFLICT` (`tests/integration/propiedades/test_seed.py`) (spec 006).
- Artefactos completos de spec 006 en `specs/006-pagina-propiedades-cards/`: spec, plan, tasks, report, research, data-model, quickstart, contratos YAML y checklist de requisitos.
- Siete prompts de Spec Kit para spec 007-crear-propiedad (`007-crear-propiedad.specify`, `.clarify`, `.plan`, `.analyze`, `.fix-report`, `.tasks` y `.implement`) en `.opencode/prompts/`, con frontmatter estandarizado y referencias cruzadas a las fases del flujo (spec 007).
- Grafo de conocimiento del repositorio con Graphify: vendoreado en `.opencode/vendor/graphify/` (plugin y skill), comandos `graphify`, `graphify-query`, `graphify-path` y `graphify-explain` registrados en `.opencode/commands/`, plugin añadido a `opencode.json`, archivo `.graphifyignore` con exclusiones para el grafo y artefactos generados en `graphify-out/` (`graph.json`, `graph.html`, `GRAPH_REPORT.md`, `manifest.json`, `cost.json`).

### Changed

- Prompts de Spec Kit reorganizados con nomenclatura consistente: `<spec>.fase.prompt.md` (ej. `001-bootstrap-proyecto.plan.prompt.md`).
- Instrucciones por área renombradas de `*.md` a `*.instructions.md` (`backend`, `database`, `frontend`, `tests`) y referenciadas desde `opencode.json` mediante el patrón `.opencode/instructions/*.instructions.md`.
- Instrucciones de frontend extendidas con sección 0: tokens visuales canónicos como fuente operativa única, con lista explícita de valores obligatorios para `:root` y reglas de trazabilidad para cambios visuales.
- Scripts del proyecto reorganizados en subdirectorios `ci/`, `dev/` y `tools/` con `Makefile` actualizado (`check`, `clean`, `context`, `create`, `format`, `lint`, `reset`, `typecheck`, `visual-check`).
- Agente `changelog` refactorizado: responsabilidad de auditoría de commits extraída al agente `improve-commits`; permisos de escritura Git eliminados; eliminado el buffer intermedio `.changelog-pending.md`, la curaduría ahora usa exclusivamente `git log` desde la marca `last-processed-commit`.
- Agente `improve-commits` ampliado con reglas consolidadas de nomenclatura del proyecto (tipos, scopes, descripciones).
- Actualizados los 49 commits del historial de `main` para cumplir con Conventional Commits (tipos correctos, scopes de spec, descripciones en imperativo presente).
- Prompts de Spec Kit movidos de `.opencode/commands/prompts/` a `.opencode/prompts/` con frontmatter de ejecución estandarizado que incluye metadatos de restricciones, descripción y referencias (specs 001, 002, 003).
- Comandos de `opencode.json` eliminados: los flujos de Spec Kit ahora se ejecutan exclusivamente mediante prompts estandarizados con metadatos de ejecución, simplificando la configuración declarativa del proyecto.
- Constitución actualizada (v1.3.1): sección IX de calidad reemplaza comandos manuales por `make auto-checks`/`make ci` como entry point unificado; stack ampliado con `pre-commit`, `pyupgrade`, `ruff-format` y `pydocstyle`; estructura del repositorio incluye `.pre-commit-config.yaml`.
- `conventions.instructions.md`: versión de constitución corregida (`v1.2.0` → `v1.3.1`); sección 12 agregada con tabla completa de hooks pre-commit.
- Makefile y CI: simplificado el hook manual `format-project` eliminándolo de `.pre-commit-config.yaml`; separados `manual-checks` en scripts directos (`test.sh`, `coverage.sh`, `clean.sh`); corregido `ruff-check` para usar `--fix .` en lugar de `--fix --check`; actualizada la receta `ci` para usar `$(MAKE)` llamadas explícitas.
- `pyproject.toml`: agregada regla `D107` a la lista de ignorados de `pydocstyle` (docstring faltante en `__init__`).
- `conventions.instructions.md`: agregada fila `format-docstrings` en la tabla de hooks automáticos de la sección 12.
- `.pre-commit-config.yaml`: reorganizado el orden de hooks ubicando `format-docstrings` después de `ruff-format` y antes de las verificaciones generales; agregado `fail_fast: true` para abortar ante el primer fallo.
- Prompts de specs 001-004: añadido campo `siguiente_fase` en frontmatter para trazabilidad del avance entre fases de Spec Kit.
- Tipado del contexto del dashboard: `schemas.py` ahora define `MetricaDashboard`, `AccesoDashboard`, `ActividadDashboard`, `MetricasPropiedades` y `ContextoDashboard` como `TypedDict` explícitos en lugar de `dict` genéricos; `repository.py` y `service.py` usan tipos concretos (spec 005).
- Componente `_tarjeta_metrica.html` extendido: acepta `marcador` opcional y lo renderiza dentro de la tarjeta como `<div class="text-muted">` (spec 005). ⚠️ Cambio en componente compartido protegido sin marcador `[visual]` en `tasks.md`.
- Consolidada la configuración del proyecto en `config/app.yaml` como fuente única de parámetros; eliminados `.env` y `.env.example`.
- Infraestructura de base de datos migrada de `app/database.py` a `app/infra/database.py`; configuración de `app/config.py` movida a `app/config/` (módulo `settings.py` + `paths.py`).
- `app/main.py` simplificado: ahora solo registra routers (`dashboard`, `health`, `propiedades`); endpoint `GET /health` extraído a `app/modules/health/routes.py`.
- Dashboard routes usa `get_paths()` del path manager en lugar de `Path(__file__).resolve()` hardcodeado.
- Constitución actualizada a v1.4.0: eliminada referencia a `.env` como fuente de configuración; estructura del repositorio corregida (`app/config.py` → `app/config/`, `app/database.py` → `app/infra/database.py`, `.env.example` → `config/app.example.yaml`); agregado `app/modules/health/` al árbol.
- `AGENTS.md` sincronizado con constitución v1.4.0: referencias actualizadas de `.env` a `config/app.yaml`.
- `database.instructions.md` actualizado: referencias de `.env` a `config/app.yaml`, y de `app/database.py` a `app/infra/database.py`.
- Corregidos imports de `settings` en `alembic/env.py`, `scripts/dev/seed_propiedades.py` y `scripts/dev/db_preflight.py`: migrados de `from app.config import settings` (módulo) a `from app.config import get_settings` (instancia); acceso a `settings.DATABASE_URL` → `get_settings().database_url`.
- `pyproject.toml`: mypy strict limitado a `app.modules.*` con override para `app.config.settings` que permite `call-arg`.
- `.gitignore` simplificado: eliminadas reglas genéricas redundantes; reemplazadas por entrada única `config/app.yaml` como única fuente de configuración local.
- **[visual][extension]** Card de propiedad (`_card_propiedad.html`) extendida con modo grid: incluye imagen, dirección, precio, habitaciones, baños, área y badge de estado; mantiene retrocompatibilidad con el modo dashboard original (spec 006, tareas T1.1–T1.3).
- **[visual][extension]** Placeholder visual para imagen faltante en card: fondo con `--color-surface` e icono `building-2` centrado, activo cuando la imagen está vacía o falla al cargar (spec 006, tarea T1.2).
- Sidebar: enlace «Propiedades» cambiado de `href="#"` a `href="/propiedades"` (spec 006, tarea T5.1).
- Sidebar: estado activo calculado dinámicamente desde `request.url.path` con clase `sidebar__item--active` y `aria-current="page"`; Dashboard activo solo en `/`, Propiedades activo en rutas `/propiedades`; Inquilinos y Contratos separados en dos `<a>` independientes.
- Navbar: breadcrumb dinámico que refleja la sección actual (`Inicio / Propiedades` en `/propiedades`, `Inicio / Dashboard` en `/`).
- Seed de propiedades: URLs de imágenes reemplazadas de hash MD5 determinista a URLs explícitas curadas de Unsplash con contenido inmobiliario real (apartamentos, fachadas, condominios, interiores, casas/villas).
- Import de `settings` en seed corregido: migrado de `settings.DATABASE_URL` a `get_settings().database_url`.
- Prompts de Spec Kit de specs 001-006 renombrados: extensión `.spec.prompt.md` → `.specify.prompt.md`, con los campos `name:` y `usage:` del frontmatter actualizados para reflejar la nueva ruta del archivo.
- Sección 0 de `frontend.instructions.md` (tokens visuales canónicos) ampliada con dos patrones nuevos: navegación dinámica (estado activo del sidebar y breadcrumb del navbar calculados desde `request.url.path`) y fallback de imagen en cards (visibilidad y placeholder controlados exclusivamente por clases CSS). Eliminada la excepción que permitía `style="display:none"` como estado inicial HTMX. Cambios trazados como `[visual][extension]` en `tasks.md` de spec 006.
- `plan.md` y `tasks.md` de spec 006 actualizados: marcadores `[visual][extension]` añadidos para `_sidebar.html`, `_navbar.html` y `frontend.instructions.md`; añadida la tarea T5.2 para el sidebar/navbar dinámico y la actualización de instrucciones; tareas T0–T8 marcadas como completadas.
- Comando de desarrollo renombrado: target `backend` del Makefile → `server`; `scripts/dev/backend.sh` reemplazado por `scripts/dev/server.sh` (sin flag `--reload`).
- FastAPI actualizado de 0.136.3 a 0.138.0 en `pyproject.toml` y `uv.lock`.
- `AGENTS.md` ampliado con la sección `graphify` que documenta el grafo de conocimiento del repo: cuándo usarlo, comandos disponibles (`query`, `path`, `explain`), reglas de omisión, manejo de API keys y notas de integración SDD.
- `.repomixignore` ajustado: `.opencode/` permanece excluido pero se reabren `.opencode/prompts/` y `.opencode/instructions/` para que repomix incluya esos artefactos en el contexto de IA.
- `.gitignore` reorganizado con secciones comentadas por categoría; entrada `graphify-out/` añadida para no versionar la salida del grafo de Graphify.

### Fixed

- Instalación del hook `post-commit` corregida para manejar el sufijo `.changelog` en el nombre del archivo fuente al copiarlo a `.git/hooks/`.
- Timeout del script `backend.sh` corregido para evitar falsos positivos en entornos lentos.
- Contradicción interna en constitución (v1.3.0) sobre ubicación de tests: `tests/` eliminado de `app/modules/<feature>/` en la sección IV; ahora solo reside en raíz (`tests/unit/`, `tests/integration/`) según IX.5 y XIII.
- `backend.instructions.md` corregido: eliminada referencia a `tests/` dentro del módulo; texto ahora apunta a `tests/unit/<feature>/` y `tests/integration/<feature>/` en la raíz.
- `AGENTS.md` sincronizado con constitución v1.3.1: eliminado `tests/` de artefactos del módulo, agregadas secciones `Órganización de tests`, `Async-First`, `Contratos de dominio`, y árbol de estructura actualizado.
- Hook `format-docstrings`: reemplazado `inspect.cleandoc` por extracción directa del cuerpo desde líneas fuente mediante `_extract_body` y `_common_indent`, ignorando líneas vacías en la indentación para evitar ciclos de formato con `ruff format` y `trailing-whitespace`.
- Marcador "No disponible" ahora se renderiza DENTRO de la tarjeta métrica (`_tarjeta_metrica.html`) en lugar de fuera como hermano directo del grid `.metricas` (spec 005).
- Dashboard ya no duplica los accesos rápidos: reemplazado bloque hardcodeado en `dashboard.html` por `accesos=accesos` del contexto del servicio (spec 005).
- Tests de integración del dashboard ahora validan returncode de Alembic (`alembic_ok`) y seed (`seed_ok`) con `assert` explícito, en lugar de ignorar errores silenciosos (spec 005).
- Test `test_dashboard_estado_vacio` corregido: el truncado de propiedades se ejecuta antes de sobrescribir `dependency_overrides` para evitar fugas de datos entre tests (spec 005).
- Test `test_upgrade_head_crea_tabla` corregido: ahora usa `_reset_db()` con DROP/CREATE schema y `asyncio.run()` en lugar de `Base.metadata.create_all` mixto, garantizando estado limpio en cada ejecución (spec 004).
- Regresión en test de migración corregida: `async_session` fixture ya no ejecuta `Base.metadata.create_all` (inconsistente con Alembic); el esquema se prepara exclusivamente con `setup_db()` vía Alembic (spec 004).
- `async_session` fixture en `conftest.py` de integración simplificado: eliminada creación directa de tablas con `Base.metadata.create_all`; ahora solo crea engine y session factory delegando el esquema a Alembic.
- Cards de propiedad: títulos largos ahora usan `line-clamp: 2` para evitar desborde horizontal; altura consistente entre cards del grid con `height: 100%` y `flex: 1`.
- Imágenes del seed: eliminada dependencia de `picsum.photos` para imágenes aleatorias; reemplazadas por URLs estables y curadas de Unsplash visibles en la UI.
- Control de visibilidad de imagen/placeholder en card: eliminados estilos inline (`style="display:none"`) y manipulación de `onerror`; reemplazados por modificadores de clase CSS (`card-propiedad--has-image`, `card-propiedad--no-image`, `card-propiedad__imagen--error`).
- Sidebar: corregido el estado activo que antes usaba `sidebar__item--active` fijo en Dashboard; ahora se aplica condicionalmente según la ruta.

### Removed

- Script `sync-agent-models.sh` y archivo `config/models.yaml`, de uso transitorio durante la configuración inicial de agentes.
- Buffer técnico `.changelog-pending.md` y directorio `docs/context/`: el flujo de changelog ahora es directo (hook → recordatorio → agente cronista → `CHANGELOG.md`).
- Archivo `.repomixignore` eliminado y sus reglas de exclusión migradas a `.gitignore`.
- Archivo `tests/unit/test_dashboard.py` removido: dependía de PostgreSQL como test unitario; reemplazado por tests unitarios con mocks en `tests/unit/dashboard/test_routes.py` y tests de integración dedicados.
- Archivos `app/config.py` y `app/database.py` eliminados; reemplazados por `app/config/` (módulo) y `app/infra/database.py`.
- Archivos `.env`, `.env.example` y `.env.*.local` removidos del repositorio y del `.gitignore`; `config/app.yaml` es la fuente única de configuración.
- Función `_imagen_determinista()` y `import hashlib` del script de seed; las imágenes ya no se generan con hash MD5 (spec 006).
- Llamada a `picsum.photos` en el seed; reemplazada por URLs explícitas en cada propiedad.
- Estilos inline y manipulación directa de `style.display` en `_card_propiedad.html`.
- `scripts/dev/backend.sh` eliminado al consolidarse en `scripts/dev/server.sh`.

<!-- changelog:last-processed-commit=a3e3c9f3e00193439cb546c4c2b03ced268757e7 -->
