---
name: 005-dashboard-datos-reales-fix-report
description: >
  Corrige los hallazgos del reporte de análisis de la feature
  005-dashboard-datos-reales.
usage: "@.opencode/prompts/005-dashboard-datos-reales.fix-report.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

Corrige los hallazgos documentados en `report.md` para la feature
`005-dashboard-datos-reales`.

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

## Verificaciones específicas de esta feature

Al corregir hallazgos, verifica especialmente:

- Que ninguna corrección introduzca scope creep (módulos de rentas, pagos o
  contratos).
- Que ninguna corrección invente cálculos de ingresos o vencidos.
- Que ninguna corrección proponga endpoints adicionales sin justificación
  funcional concreta.
- Que ninguna corrección modifique tokens visuales, CSS, iconografía o
  componentes compartidos.
- Que el contrato de contexto de la home permanezca compatible con
  `dashboard.html`.
- Que el estado vacío se active con cero propiedades totales.
- Que las métricas no operativas mantengan valor `0` y marcador
  "No disponible".
- Que el orden de métricas sea: disponibles, rentadas, ingresos, vencidos.
- Que ninguna corrección amplíe el alcance funcional de
  `005-dashboard-datos-reales`.
- Si `report.md` detecta lógica de dashboard en `app/main.py`, corregirla
  moviéndola al slice `app/modules/dashboard/`.
- Si `GET /` no está definido en `app/modules/dashboard/routes.py`, corregirlo
  salvo que exista una limitación técnica documentada y aprobada.
- Si `service.py` o `repository.py` no respetan responsabilidades del slice,
  corregir la separación.

## Criterios de corrección

Al corregir hallazgos, verifica especialmente:

- Coherencia entre `spec.md`, `plan.md` y artefactos generados.
- Trazabilidad de cambios visuales protegidos.
- Ausencia de decisiones visuales no justificadas.
- Consistencia de estados: datos, vacío, error en métricas.
- Que las métricas no operativas estén claramente diferenciadas de las reales.
- Que ninguna corrección amplíe el alcance funcional de
  `005-dashboard-datos-reales`.

## Salida esperada

Al finalizar, informa:

- Archivos modificados.
- Hallazgos críticos corregidos.
- Advertencias corregidas, si aplica.
- Hallazgos pendientes, si existen.
- Si hubo correcciones relacionadas con gobernanza visual.
- Si los contratos YAML siguen siendo válidos, cuando existan.
- Siguiente comando recomendado.

Después de corregir, la siguiente fase obligatoria es re-ejecutar el análisis
para confirmar cero hallazgos:

```text
/speckit.analyze @.opencode/prompts/005-dashboard-datos-reales.analyze.prompt.md
```

Si el segundo analyze confirma cero hallazgos, continuar con:

```text
/speckit.tasks @.opencode/prompts/005-dashboard-datos-reales.tasks.prompt.md
```
