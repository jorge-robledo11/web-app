---
name: 001-bootstrap-proyecto-fix-report
description: >
  Corrige los hallazgos del reporte de análisis de la feature
  001-bootstrap-proyecto.
usage: "@.opencode/prompts/001-bootstrap-proyecto.fix-report.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

Corrige los hallazgos documentados en `report.md` para la feature
`001-bootstrap-proyecto`.

Usa la feature activa resuelta por Spec Kit. No asumas rutas fijas si el
workflow ya puede resolverlas.

## Archivos de entrada

Lee, como mínimo:

- `report.md`
- `spec.md`
- `plan.md`
- Artefactos mencionados por el reporte, si existen

## Alcance

Corrige todos los hallazgos marcados como **CRÍTICO**.

También puedes corregir hallazgos marcados como **ADVERTENCIA** cuando sean
correcciones documentales directas, no requieran decisión del usuario y no
cambien el alcance funcional de la spec.

No corrijas hallazgos marcados como **SUGERENCIA** salvo que sean triviales y no
introduzcan nuevas decisiones.

## Reglas

- No implementes código de producción.
- No generes `tasks.md`.
- No modifiques archivos fuera de la feature activa, salvo que el reporte lo
  indique explícitamente.
- No cambies la intención funcional de la spec.
- No inventes decisiones nuevas.
- Mantén todo el contenido en español.
- Respeta la constitución y `AGENTS.md`.
- Si una corrección requiere decisión del usuario, pausa y pregunta antes de
  modificar.
- Si detectas que el reporte menciona una ruta o archivo inexistente, informa el
  problema y no inventes el archivo.

## Salida esperada

Al finalizar, informa:

- Archivos modificados.
- Hallazgos críticos corregidos.
- Advertencias corregidas, si aplica.
- Hallazgos pendientes, si existen.
- Siguiente comando recomendado.

Después de corregir, recomienda volver a ejecutar:

```text
/001-bootstrap-proyecto-analyze
```