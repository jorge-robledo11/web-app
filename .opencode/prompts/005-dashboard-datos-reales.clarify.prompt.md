---
name: 005-dashboard-datos-reales-clarify
description: >
  Identifica ambigüedades y guía la clarificación interactiva de la spec
  005-dashboard-datos-reales.
spec_kit_command: "/speckit.clarify"
usage: "/speckit.clarify @.opencode/prompts/005-dashboard-datos-reales.clarify.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

Revisa la spec activa `005-dashboard-datos-reales`.

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

## Decisiones ya resueltas en la fase specify

Las siguientes decisiones fueron tomadas durante la fase interactiva de
`/speckit.specify` y NO deben reabrirse:

- Las métricas no operativas (ingresos, vencidos) se muestran con valor `0` y
  marcador textual "No disponible".
- El estado vacío del dashboard se activa cuando no existen propiedades
  persistidas (cero filas en `propiedades`).
- No se requiere endpoint adicional para refresh parcial; el render server-side
  en cada request es suficiente.
- El dashboard se implementa como vertical slice en `app/modules/dashboard/`.
- El endpoint `GET /` se sirve desde `app/modules/dashboard/routes.py`.
- `app/main.py` no debe construir el contexto del dashboard; solo debe incluir
  o registrar el router si corresponde.

## Ambigüedades a revisar

Considera especialmente si la spec deja claro:

- Cómo debe acceder el servicio de dashboard a los datos de propiedades:
  consulta directa a la tabla `propiedades` o a través del repositorio de
  `app/modules/propiedades/`.
- Qué iconos deben usar las métricas de disponibles y rentadas, dentro del set
  vendoreado existente.
- Si las métricas de disponibles y rentadas deben tener tendencia (dirección y
  texto) o deben omitir ese campo por no tener datos históricos.
- Si la actividad reciente permanece con datos hardcodeados o debe eliminarse
  hasta que exista una fuente real.
- Si el contrato `dashboard.yaml` definido en spec 003 necesita actualizarse
  para reflejar las métricas reales y no operativas.
- Si el estado vacío del dashboard debe reemplazar todo el contenido de la home
  o solo las métricas.
- Qué pruebas existentes (`tests/unit/test_dashboard.py`) dejarán de pasar y
  deben actualizarse.

## Resultado esperado

Al finalizar, muestra un resumen de decisiones y actualiza `spec.md` añadiendo o
ajustando la sección `Clarificaciones`.

Siguiente fase: `005-dashboard-datos-reales.plan.prompt.md`
