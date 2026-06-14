---
name: 001-bootstrap-proyecto-implement
description: >
  Implementa 001-bootstrap-proyecto siguiendo tasks.md, una fase a la vez y con
  confirmación manual entre fases.
spec_kit_command: "/speckit.implement"
usage: "/speckit.implement @.opencode/prompts/001-bootstrap-proyecto.implement.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

Implementa la feature activa `001-bootstrap-proyecto` siguiendo `tasks.md`.

Usa la feature activa resuelta por Spec Kit. No asumas rutas fijas si el comando
ya puede resolverlas.

## Reglas

- Respeta `tasks.md`, `plan.md`, `spec.md`, `AGENTS.md` y la constitución.
- Trabaja una fase a la vez.
- Al terminar cada fase, pausa y espera mi confirmación antes de continuar.
- Mantén el intercambio en español.
- No agregues alcance no definido por los artefactos de la feature.
- Si detectas contradicciones o bloqueos, pausa e informa antes de continuar.

## Cierre de cada fase

Al finalizar cada fase, informa brevemente:

- Fase completada.
- Tareas completadas.
- Archivos modificados.
- Verificaciones ejecutadas.
- Bloqueos, si existen.
- Siguiente fase pendiente.