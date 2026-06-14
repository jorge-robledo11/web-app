---
name: 001-bootstrap-proyecto-plan
description: Genera el plan técnico de la spec 001-bootstrap-proyecto.
spec_kit_command: "/speckit.plan"
usage: "/speckit.plan @.opencode/prompts/001-bootstrap-proyecto.plan.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

Genera el `plan.md` para la feature activa `001-bootstrap-proyecto` usando el
workflow canónico de Spec Kit.

## Artefactos generados

Si el plan genera archivos como `research.md`, `data-model.md`, `quickstart.md`,
`contracts/*.md` u otros artefactos de planificación, esos archivos DEBEN:

- Estar escritos en Markdown válido.
- Ser claros, explícitos y consistentes con el estilo de Spec Kit.
- Contener solo el contenido esperado para ese tipo de artefacto.
- Evitar texto narrativo libre que no aporte al objetivo del artefacto.
- Mantener coherencia con `plan.md` y con la especificación de la feature.

Si algún artefacto requiere explicación narrativa, contexto o notas de diseño,
esa información debe ir en el artefacto adecuado dentro del flujo de Spec Kit,
no mezclarse con otros formatos ni con contenido fuera de lugar.

## Contratos

Si el plan genera archivos dentro de `contracts/*.md`, esos archivos DEBEN
contener contenido en Markdown válido, claro y consistente con el estilo de Spec Kit.

No escribas texto narrativo libre que no aporte a la definición del contrato.

La estructura de cada contrato debe ser consistente, explícita y adecuada al tipo
de contrato generado por Spec Kit.

Antes de finalizar, verifica que cada archivo generado por el plan:

- Sea Markdown válido.
- Mantenga coherencia con el plan técnico.
- Refleje la intención del artefacto de forma clara y utilizable.
- Sea consistente con las convenciones de Spec Kit.

Quiero que todos los artefactos generados sean `.md` y consistentes con lo de Spec Kit.