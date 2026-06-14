---
name: 002-blindar-tokens-visuales-tasks
description: >
  Genera tasks.md con tareas secuenciales, accionables y verificables para
  002-blindar-tokens-visuales.
spec_kit_command: "/speckit.tasks"
usage: "/speckit.tasks @.opencode/prompts/002-blindar-tokens-visuales.tasks.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

Genera `tasks.md` para la feature activa `002-blindar-tokens-visuales` usando el
workflow canónico de Spec Kit.

Usa la feature activa resuelta por Spec Kit. No asumas rutas fijas si el comando
ya puede resolverlas.

## Reglas

- Mantén todo en español.
- No implementes código.
- No modifiques `spec.md` ni `plan.md`.
- Respeta la constitución, `AGENTS.md`, `report.md` y las instrucciones activas.
- Si existen hallazgos críticos o advertencias pendientes en `report.md`, pausa
  e infórmalos antes de generar tareas.
- Agrupa las tareas por fases del `plan.md`.
- Cada tarea debe ser accionable y verificable.
- Toda tarea que afecte archivos visuales protegidos debe incluir trazabilidad
  explícita según la spec.

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
- Fases generadas.
- Si detectaste bloqueos.
- Siguiente comando recomendado.
