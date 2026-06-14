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

### Fixed

- Instalación del hook `post-commit` corregida para manejar el sufijo `.changelog` en el nombre del archivo fuente al copiarlo a `.git/hooks/`.
- Timeout del script `backend.sh` corregido para evitar falsos positivos en entornos lentos.

### Removed

- Script `sync-agent-models.sh` y archivo `config/models.yaml`, de uso transitorio durante la configuración inicial de agentes.
- Buffer técnico `.changelog-pending.md` y directorio `docs/context/`: el flujo de changelog ahora es directo (hook → recordatorio → agente cronista → `CHANGELOG.md`).
- Archivo `.repomixignore` eliminado y sus reglas de exclusión migradas a `.gitignore`.

<!-- changelog:last-processed-commit=b96e7f114dd41c7f6c98b9adbb5dc6d21f470bb3 -->
