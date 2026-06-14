---
name: 003-redisenar-home-fix-report
description: >
  Corrige los hallazgos del reporte de análisis de la feature
  003-redisenar-home.
usage: "@.opencode/prompts/003-redisenar-home.fix-report.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---
Corrige los hallazgos documentados en `report.md` para la feature
`003-redisenar-home`.

Usa la feature activa resuelta por Spec Kit. No asumas rutas fijas si el
workflow ya puede resolverlas.

## Archivos de entrada

Lee, como mínimo:

- `report.md`
- `spec.md`
- `plan.md`
- `research.md`, si existe
- `quickstart.md`, si existe
- `contracts/*.yaml`, si existen
- Artefactos mencionados por el reporte, si existen
- `AGENTS.md`
- `.specify/memory/constitution.md`
- Instrucciones activas de `.opencode/instructions/*.instructions.md`

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
- Respeta la constitución, `AGENTS.md` y las instrucciones activas.
- Respeta la gobernanza visual vigente definida por `002-blindar-tokens-visuales`.
- Si una corrección requiere decisión del usuario, pausa y pregunta antes de
  modificar.
- Si detectas que el reporte menciona una ruta o archivo inexistente, informa el
  problema y no inventes el archivo.
- Si el reporte trata sobre gobernanza visual, conserva la distinción entre:
  regla global de proyecto y verificación limitada al área visual/frontend.
- Si hay contratos `contracts/*.yaml`, conserva YAML válido y parseable. No
  escribas Markdown, texto narrativo libre ni bloques de código dentro de
  archivos `.yaml`.

## Criterios de corrección

Al corregir hallazgos, verifica especialmente:

- Coherencia entre `spec.md`, `plan.md` y artefactos generados.
- Trazabilidad de cambios visuales protegidos.
- Ausencia de decisiones visuales no justificadas.
- Claridad de criterios responsive.
- Consistencia de estados visuales: carga, vacío, error, éxito o navegación.
- Que ninguna corrección amplíe el alcance funcional de `003-redisenar-home`.

## Salida esperada

Al finalizar, informa:

- Archivos modificados.
- Hallazgos críticos corregidos.
- Advertencias corregidas, si aplica.
- Hallazgos pendientes, si existen.
- Si hubo correcciones relacionadas con gobernanza visual.
- Si los contratos YAML siguen siendo válidos, cuando existan.
- Siguiente comando recomendado.

Después de corregir, recomienda volver a ejecutar:

```text
/003-redisenar-home-analyze
```
