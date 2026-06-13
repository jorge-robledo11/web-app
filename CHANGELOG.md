# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/) y este proyecto sigue versionado SemVer cuando aplique.

## [Unreleased]

### Added

- Bootstrap del proyecto Realtor (spec 001): aplicación FastAPI con Jinja2 + HTMX, sistema de diseño CSS con tokens visuales canónicos, componentes compartidos (sidebar, navbar, cards de propiedad, tarjetas de métrica, badges de estado, alertas, campos de formulario), iconografía Lucide vendoreada en 13 iconos SVG outline, configuración Alembic con PostgreSQL vía Docker Compose y tests con pytest + httpx.
- Infraestructura de changelog automatizado: hook `post-commit` que genera entradas mecánicas, script `changelog.sh` y agente cronista (`000-changelog.prompt.md`) para auditoría y curaduría de CHANGELOG.md.
- Gobernanza visual (spec 002): script `visual-check.sh` que verifica integridad de tokens CSS, contratos de trazabilidad `visual-trace.yaml` y tareas de blindaje documentadas en `tasks.md`.
- Script `install-git-hooks.sh` para instalación de hooks de git en el repositorio.
- Spec 003 (`rediseñar home`): spec.md, checklist de requisitos y prompts de Spec Kit creados.
- Agente `improve-commits` para auditoría y corrección de mensajes de commit según Conventional Commits y convenciones del proyecto.
- Instrucciones unificadas de convenciones (`conventions.instructions.md`) que consolidan nomenclatura, formato, commits, ramas, tests, CSS y gobernanza visual en un solo archivo de referencia.

### Changed

- Scripts del proyecto reorganizados: unificados bajo `scripts/`, movidos de `scripts/db/` a `scripts/`, Makefile actualizado con nuevos targets (`check`, `clean`, `context`, `create`, `format`, `lint`, `reset`, `typecheck`, `visual-check`).
- Instrucciones por área renombradas de `*.md` a `*.instructions.md` (`backend`, `database`, `frontend`, `tests`) y referenciadas desde `opencode.json` en la raíz del repositorio.
- Instrucciones de frontend extendidas con la sección 0 (tokens visuales canónicos como fuente operativa única) y reglas de trazabilidad para cambios visuales.
- Constitución del proyecto (`.specify/memory/constitution.md`) ampliada con sección XII: protección de tokens visuales y reglas de gobernanza.
- Agente `changelog` refactorizado: responsabilidad de auditoría de commits extraída al agente `improve-commits`; permisos reducidos (eliminados `git commit --amend`, `git rebase`, `git merge-base`, `mktemp`, `cat`).

<!-- changelog:last-processed-commit=1d1b13087b017712defd464e6ad668ec5ec9bfa1 -->
