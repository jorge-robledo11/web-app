---
name: 004-propiedades-base-clarify
description: >
  Identifica ambigüedades y guía la clarificación interactiva de la spec
  004-propiedades-base.
spec_kit_command: "/speckit.clarify"
usage: "/speckit.clarify @.opencode/prompts/004-propiedades-base.clarify.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

Revisa la spec activa `004-propiedades-base`.

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
- Respeta la gobernanza visual vigente definida por `002-blindar-tokens-visuales`.
- Aplica el modo interactivo definido por la constitución y `AGENTS.md`.
- Haz solo las preguntas necesarias.
- Haz una sola pregunta a la vez.
- Si no hay ambigüedades relevantes, indícalo explícitamente.

## Ambigüedades a revisar

Considera especialmente si la spec deja claro:

- Qué secciones exactas debe contener la Home.
- Qué contenido es obligatorio y qué contenido es decorativo.
- Qué componentes compartidos deben reutilizarse.
- Si se permite crear componentes nuevos.
- Si el rediseño puede extender tokens visuales o debe reutilizar únicamente los
  existentes.
- Qué archivos visuales protegidos podrían verse afectados.
- Qué cambios necesitarán trazabilidad visual en `tasks.md`.
- Qué comportamiento responsive debe validarse.
- Qué estados visuales deben cubrirse: carga, vacío, error, éxito o navegación.
- Qué criterios de aceptación visual son verificables sin depender de gusto
  estético subjetivo.

## Resultado esperado

Al finalizar, muestra un resumen de decisiones y actualiza `spec.md` añadiendo o
ajustando la sección `Clarificaciones`.
