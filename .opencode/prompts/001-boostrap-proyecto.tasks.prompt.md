---
name: 001-bootstrap-proyecto-tasks
description: >
  Genera tasks.md con tareas secuenciales, accionables y verificables para
  001-bootstrap-proyecto.
spec_kit_command: "/speckit.tasks"
usage: "/speckit.tasks @.opencode/prompts/001-boostrap-proyecto.tasks.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

Genera `tasks.md` para la feature activa `001-bootstrap-proyecto` usando el
workflow canónico de Spec Kit.

Usa la feature activa resuelta por Spec Kit. No asumas rutas fijas si el comando
ya puede resolverlas.

## Formato de numeración

Usa este formato para los identificadores de tareas:

```text
T<fase>.<orden>
```

Ejemplos:

```text
T1.1
T1.2
T2.1
T2.2
```

Al finalizar, informa:

- Ruta de `tasks.md`.
- Número total de tareas.
- Fases generadas,
- Si detectaste bloqueos.
- Siguiente comando recomendado.
