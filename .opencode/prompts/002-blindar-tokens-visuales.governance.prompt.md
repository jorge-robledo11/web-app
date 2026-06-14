---
name: 002-blindar-tokens-visuales-governance
description: >
  Actualiza la gobernanza del proyecto para blindar los tokens visuales
  canónicos antes de crear la spec 002-blindar-tokens-visuales.
spec_kit_command: "/speckit.constitution"
usage: "/speckit.constitution @.opencode/prompts/002-blindar-tokens-visuales.governance.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

Actualiza los archivos de gobernanza necesarios para soportar la futura spec
`002-blindar-tokens-visuales`.

## Objetivo

Establecer que los tokens visuales canónicos del frontend no pueden modificarse
sin autorización explícita, justificación y trazabilidad en `tasks.md`.

## Archivos a revisar

- `.opencode/instructions/frontend.instructions.md`
- `.specify/memory/constitution.md`
- `AGENTS.md`
- `.specify/templates/spec-template.md`, si existe.

## Cambios esperados

1. En `.opencode/instructions/frontend.instructions.md`, declarar que este
   archivo es la fuente operativa para:
   - Tokens de color.
   - Espaciado.
   - Radios.
   - Sombras.
   - Tipografía.
   - Breakpoints.
   - Layout base.
   - Componentes visuales compartidos.

2. En `.specify/memory/constitution.md`, agregar una regla global que indique que
   cualquier cambio en tokens visuales canónicos requiere:
   - Autorización explícita.
   - Justificación.
   - Trazabilidad en `tasks.md`.
   - Registro en `Complexity Tracking` si implica desviación visual global.

3. En `AGENTS.md`, reflejar la misma regla como instrucción operativa para
   agentes.

4. Si existe `.specify/templates/spec-template.md`, agregar una sección breve para
   que futuras specs declaren si tocan o no tokens visuales canónicos.

## Reglas

- No implementes código de aplicación.
- No crees la spec todavía.
- No generes `plan.md` ni `tasks.md`.
- Mantén todo en español.
- No dupliques reglas extensas si basta con referenciar la fuente operativa.
- No cambies el stack ni la arquitectura.
- No modifiques rutas de specs.
- Si una modificación a la constitución requiere subir versión, actualiza el
  historial de versiones de la constitución.

## Salida esperada

Al finalizar, informa:

- Archivos modificados.
- Regla agregada a la constitución.
- Si se actualizó el template de specs.
- Nueva versión de la constitución, si cambió.
- Siguiente comando recomendado.
