---
name: 002-blindar-tokens-visuales-plan
description: >
  Genera el plan técnico de la spec 002-blindar-tokens-visuales.
spec_kit_command: "/speckit.plan"
usage: "/speckit.plan @.opencode/prompts/002-blindar-tokens-visuales.plan.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

Genera `plan.md` para la feature activa `002-blindar-tokens-visuales` usando el
workflow canónico de Spec Kit.

Usa la feature activa resuelta por Spec Kit. No asumas rutas fijas si el comando
ya puede resolverlas.

## Reglas

- Mantén todo en español.
- No implementes código.
- No generes `tasks.md`.
- Respeta la constitución, `AGENTS.md`, `spec.md`, clarificaciones y las
  instrucciones activas de `.opencode/instructions/*.instructions.md`.
- No agregues decisiones nuevas que no estén respaldadas por la spec o sus
  clarificaciones.
- Si detectas una ambigüedad que bloquee el plan, pausa y pregunta antes de
  continuar.
- Registra cualquier desviación en `Complexity Tracking`.

## Contratos

Si el plan genera archivos dentro de `contracts/*.yaml`, esos archivos DEBEN
contener YAML válido y parseable.

No escribas Markdown, texto narrativo libre ni bloques de código dentro de
archivos `.yaml`.

La estructura de cada contrato debe ser consistente, explícita y adecuada al tipo
de contrato generado por Spec Kit.

Si el contenido necesita explicación narrativa, contexto o notas de diseño, debe
ir en `plan.md`, `research.md` o `quickstart.md`, no en `contracts/*.yaml`.

Antes de finalizar, verifica que cada archivo `contracts/*.yaml` pueda abrirse
como YAML válido sin errores de sintaxis.

## Salida esperada

Al finalizar, informa:

- Ruta del `plan.md` generado o actualizado.
- Artefactos generados o actualizados.
- Si hubo preguntas interactivas.
- Si se registraron desviaciones en `Complexity Tracking`.
- Siguiente comando recomendado.