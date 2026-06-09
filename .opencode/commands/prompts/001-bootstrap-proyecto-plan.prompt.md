---
name: 001-bootstrap-proyecto-plan
description: Genera el plan técnico de la spec 001-bootstrap-proyecto.
---

/speckit.plan

Genera el `plan.md` para la feature activa `001-bootstrap-proyecto` usando el
workflow canónico de Spec Kit.

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