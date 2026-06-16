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

### Fixed

- Instalación del hook `post-commit` corregida para manejar el sufijo `.changelog` en el nombre del archivo fuente al copiarlo a `.git/hooks/`.
- Timeout del script `backend.sh` corregido para evitar falsos positivos en entornos lentos.
- Contradicción interna en constitución (v1.3.0) sobre ubicación de tests: `tests/` eliminado de `app/modules/<feature>/` en la sección IV; ahora solo reside en raíz (`tests/unit/`, `tests/integration/`) según IX.5 y XIII.
- `backend.instructions.md` corregido: eliminada referencia a `tests/` dentro del módulo; texto ahora apunta a `tests/unit/<feature>/` y `tests/integration/<feature>/` en la raíz.
- `AGENTS.md` sincronizado con constitución v1.3.1: eliminado `tests/` de artefactos del módulo, agregadas secciones `Órganización de tests`, `Async-First`, `Contratos de dominio`, y árbol de estructura actualizado.
- Hook `format-docstrings`: reemplazado `inspect.cleandoc` por extracción directa del cuerpo desde líneas fuente mediante `_extract_body` y `_common_indent`, ignorando líneas vacías en la indentación para evitar ciclos de formato con `ruff format` y `trailing-whitespace`.

### Removed

- Script `sync-agent-models.sh` y archivo `config/models.yaml`, de uso transitorio durante la configuración inicial de agentes.
- Buffer técnico `.changelog-pending.md` y directorio `docs/context/`: el flujo de changelog ahora es directo (hook → recordatorio → agente cronista → `CHANGELOG.md`).
- Archivo `.repomixignore` eliminado y sus reglas de exclusión migradas a `.gitignore`.

<!-- changelog:last-processed-commit=4ac91e8701c117e6714f9629c4a5282830fbdf12 -->
