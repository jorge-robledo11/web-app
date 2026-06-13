---
name: setup-constitution
description: >
  Crea o actualiza constitution.md del proyecto Realtor.
---

/speckit.constitution

Crea o actualiza la constitución inicial del proyecto Realtor en `v1.0.0`.

Usa como fuente principal las reglas, herramientas y detalles definidos en:

```text
.opencode/commands/prompts/000-setup-constitution.prompt.md
```

La constitución final debe escribirse en:

```text
.specify/memory/constitution.md
```

## Reglas obligatorias

- Todo el contenido debe estar en español.
- La constitución debe declarar que es la fuente de verdad superior del proyecto.
- El proyecto es un monolito Python con FastAPI, Jinja2, HTMX, SQLAlchemy async y PostgreSQL local con Docker o Docker Compose.
- El proyecto se gestiona con `uv`.
- El flujo debe ser Spec-Driven Development, Test-Driven Development y Vertical Slice Architecture.
- No usar Supabase.
- No usar `.yml`; usar siempre `.yaml`.
- No usar Bootstrap, Tailwind, CDN, `pip`, `poetry`, `requirements.txt` ni `setup.py`.
- Mantener la estructura y las reglas detalladas del prompt fuente.
- No inventar reglas nuevas que contradigan el prompt fuente.

Al terminar, responde con:

```text
Archivo actualizado: .specify/memory/constitution.md
Versión: 1.0.0
Commit sugerido: docs: inicializar constitución del proyecto Realtor v1.0.0
```
