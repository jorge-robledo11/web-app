---
name: 003-redisenar-home-implement
description: >
  Implementa 003-redisenar-home siguiendo tasks.md, una fase a la vez y con
  confirmación manual entre fases.
---

/speckit.implement

Implementa la feature activa `003-redisenar-home` siguiendo `tasks.md`.

Usa la feature activa resuelta por Spec Kit. No asumas rutas fijas si el comando
ya puede resolverlas.

## Reglas

- Respeta `tasks.md`, `plan.md`, `spec.md`, `report.md`, `AGENTS.md` y la constitución.
- Respeta las instrucciones activas de `.opencode/instructions/*.instructions.md`.
- Respeta la gobernanza visual vigente definida por `002-blindar-tokens-visuales`.
- Trabaja una fase a la vez.
- Al terminar cada fase, pausa y espera mi confirmación antes de continuar.
- Mantén el intercambio en español.
- No agregues alcance no definido por los artefactos de la feature.
- No cambies tokens visuales canónicos sin trazabilidad explícita en `tasks.md`.
- Si detectas contradicciones, hallazgos críticos pendientes o bloqueos, pausa e
  informa antes de continuar.

## Verificaciones por fase

Al finalizar cada fase, ejecuta o informa las verificaciones indicadas por
`tasks.md`. Cuando aplique, considera:

- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run mypy app`
- `uv run pytest`
- Verificación manual o quickstart definido por la feature.
- Verificación de trazabilidad visual cuando se afecten archivos protegidos.

## Cierre de cada fase

Al finalizar cada fase, informa brevemente:

- Fase completada.
- Tareas completadas.
- Archivos modificados.
- Verificaciones ejecutadas.
- Cambios visuales protegidos afectados, si aplica.
- Bloqueos, si existen.
- Siguiente fase pendiente.

## Salida final

Al completar todas las fases, informa:

- Tareas completadas.
- Archivos modificados.
- Verificaciones finales ejecutadas.
- Si hubo desviaciones de gobernanza visual.
- Siguiente comando recomendado.
