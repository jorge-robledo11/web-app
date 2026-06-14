---
name: 002-blindar-tokens-visuales-clarify
description: >
  Identifica ambigüedades y guía la clarificación interactiva de la spec
  002-blindar-tokens-visuales.
---

/speckit.clarify

Revisa la spec activa `002-blindar-tokens-visuales`.

Identifica ambigüedades, decisiones implícitas o gaps que puedan afectar el
plan, las tareas o la implementación.

Usa la feature activa resuelta por Spec Kit. No asumas rutas fijas si el comando
ya puede resolverlas.

## Reglas

- Mantén todo en español.
- No implementes código.
- No generes `plan.md` ni `tasks.md`.
- Respeta la constitución, `AGENTS.md`, `spec.md` y las instrucciones activas de
  `.opencode/instructions/*.instructions.md`.
- Aplica el modo interactivo definido por la constitución y `AGENTS.md`.
- Haz solo las preguntas necesarias.
- Haz una sola pregunta a la vez.
- Si no hay ambigüedades relevantes, indícalo explícitamente.

## Resultado esperado

Al finalizar, muestra un resumen de decisiones y actualiza `spec.md` añadiendo o
ajustando la sección `Clarificaciones`.