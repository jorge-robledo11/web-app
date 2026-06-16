---
name: 005-dashboard-datos-reales-plan
description: >
  Genera el plan técnico de la spec 005-dashboard-datos-reales.
spec_kit_command: "/speckit.plan"
usage: "/speckit.plan @.opencode/prompts/005-dashboard-datos-reales.plan.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

Genera `plan.md` para la feature activa `005-dashboard-datos-reales` usando el
workflow canónico de Spec Kit.

Usa la feature activa resuelta por Spec Kit. No asumas rutas fijas si el comando
ya puede resolverlas.

## Reglas

- Mantén todo en español.
- No implementes código.
- No generes `tasks.md`.
- Respeta la constitución, `AGENTS.md`, `spec.md`, clarificaciones y las
  instrucciones activas de `.opencode/instructions/*.instructions.md`.
- Respeta la gobernanza visual vigente definida por `002-blindar-tokens-visuales`.
- No agregues decisiones nuevas que no estén respaldadas por la spec o sus
  clarificaciones.
- No reabras decisiones técnicas ya cerradas por la constitución, la spec o las
  lecciones previas del proyecto.
- Si detectas una ambigüedad que bloquee el plan, pausa y pregunta antes de
  continuar.
- Registra cualquier desviación en `Complexity Tracking`.

## Alcance esperado

El plan debe cubrir, cuando aplique:

- Estructura del módulo `dashboard` en `app/modules/dashboard/` con artefactos
  estándar: `service.py`, `repository.py`, `routes.py`, `schemas.py`.
- Servicio de dashboard como punto de cálculo de métricas reales.
- Acceso a datos de propiedades: definir si el repositorio de dashboard consulta
  directamente la tabla `propiedades` o si reutiliza el repositorio de
  `app/modules/propiedades/`.
- Estrategia para calcular conteo de propiedades disponibles (`COUNT WHERE
  estado = 'disponible'`).
- Estrategia para calcular conteo de propiedades rentadas (`COUNT WHERE
  estado = 'rentada'`).
- Construcción del contexto `metricas` conservando el contrato actual. El orden
  debe ser: disponibles, rentadas, ingresos, vencidos.
- Representación de métricas no operativas (ingresos, vencidos) con valor `0` y
  marcador "No disponible".
- Estado vacío del dashboard: detección de cero propiedades totales y render
  condicional en el template.
- Mover o definir el endpoint `GET /` en `app/modules/dashboard/routes.py`
  como parte del vertical slice dashboard.
- Conservación del contrato de contexto de la home definido en
  `specs/003-redisenar-home/contracts/dashboard.yaml`.
- No creación de endpoints adicionales (FR-017).
- No modificación de templates existentes salvo `dashboard.html` para reflejar
  métricas reales y el estado vacío.
- No modificación de CSS, iconos, tokens visuales ni componentes compartidos.
- Estrategia de pruebas unitarias (servicio con repositorio mockeado).
- Estrategia de pruebas de integración (ciclo completo: seed → métricas →
  render).
- Actualización de tests existentes en `tests/unit/test_dashboard.py`.
- Riesgos técnicos específicos de esta feature.
- Gobernanza visual: confirmar que no hay impacto en archivos protegidos.

## Decisiones técnicas cerradas

El plan debe tratar estas decisiones como no negociables:

- La feature NO crea módulos de rentas, pagos ni contratos.
- La feature NO inventa cálculos de ingresos ni vencidos.
- Las métricas no operativas muestran valor `0` y marcador "No disponible".
- El estado vacío se activa con cero propiedades totales en la base de datos.
- No se crea endpoint adicional para refresh parcial.
- El orden de métricas es fijo: disponibles, rentadas, ingresos, vencidos.
- El orden y estructura de accesos rápidos permanece sin cambios.
- La actividad reciente permanece con datos hardcodeados de demo.
- No se modifican tokens visuales, CSS, iconografía ni componentes compartidos.
- No se introducen dependencias nuevas de paquetes Python.
- El módulo dashboard vive en `app/modules/dashboard/`.
- El endpoint `GET /` pertenece al slice dashboard y se define en
  `app/modules/dashboard/routes.py`.
- `app/main.py` no contiene lógica de dashboard ni construcción del contexto;
  solo registra el router si corresponde.
- La lógica de cálculo vive en `app/modules/dashboard/service.py`.
- El acceso a datos vive en `app/modules/dashboard/repository.py`.
- Los DTOs o estructuras de contexto viven en `app/modules/dashboard/schemas.py`
  cuando aporten claridad.
- No crear archivos, clases ni abstracciones adicionales fuera de los artefactos
  mínimos del slice si no aportan valor verificable.

## Contratos

El plan debe considerar el contrato existente en
`specs/003-redisenar-home/contracts/dashboard.yaml`.

Si el plan requiere actualizar ese contrato para reflejar métricas reales vs.
no operativas, debe hacerlo respetando YAML válido. No escribas Markdown, texto
narrativo libre ni bloques de código dentro de archivos `.yaml`.

Si el plan genera archivos nuevos dentro de `contracts/*.yaml`, esos archivos
DEBEN contener YAML válido y parseable.

Antes de finalizar, verifica que cada archivo `contracts/*.yaml` pueda abrirse
como YAML válido sin errores de sintaxis.

## Riesgos técnicos

El plan debe registrar riesgos y mitigaciones para:

- Romper el contrato de contexto de la home al cambiar el número o estructura
  de métricas.
- Consultas N+1 o ineficientes al contar propiedades por estado.
- Los tests existentes de dashboard (`tests/unit/test_dashboard.py`) fallan
  porque esperan valores hardcodeados que ya no existirán.
- La detección del estado vacío no cubre el caso de base de datos caída vs.
  inventario vacío.
- El módulo `dashboard` acoplándose incorrectamente a detalles internos del
  modelo de `propiedades`.
- Crear un endpoint nuevo sin caso funcional concreto (prohibido por FR-017).
- Modificar accidentalmente archivos visuales protegidos.

## Gobernanza visual

Aunque esta feature modifica el template `dashboard.html`, el plan debe dejar
explícito que:

- No modifica tokens visuales canónicos.
- No modifica CSS (`app/static/css/app.css`).
- No modifica iconografía (`app/static/icons/`).
- No modifica componentes compartidos (`app/templates/components/`).
- No modifica `base.html`.
- No rediseña la home.
- Cualquier cambio en `dashboard.html` se limita a reflejar datos reales, no a
  alterar estructura visual, layout ni estilos.
- Si una fase posterior toca archivos visuales protegidos, debe quedar trazada
  en `tasks.md` según la gobernanza visual vigente.

## Pruebas y validaciones

El plan debe cubrir, cuando aplique:

- Pruebas unitarias del servicio de dashboard con repositorio mockeado.
- Pruebas de integración del ciclo completo: seed → `GET /` → métricas reales.
- Pruebas de estado vacío (base de datos sin propiedades).
- Pruebas de métricas no operativas (valor `0`, marcador "No disponible").
- Pruebas de orden de métricas en el HTML renderizado.
- Pruebas de conservación de estructura de accesos rápidos.
- Actualización de tests existentes en `tests/unit/test_dashboard.py`.
- Pruebas de que el endpoint `GET /` responde 200 con datos reales.

Comandos esperados de calidad:

```bash
uv run ruff check .
uv run mypy --strict app/modules/dashboard
uv run pytest tests/unit/test_dashboard.py tests/integration/dashboard/ -q
```

## Salida esperada

Al finalizar, informa:

- Ruta del `plan.md` generado o actualizado.
- Phase 0: `research.md`
- Phase 1: `data-model.md`, `quickstart.md`
- Contratos: `contracts/*.yaml` (si aplica)
- Si hubo preguntas interactivas.
- Si se registraron desviaciones en `Complexity Tracking`.
- Módulos o archivos backend que podrían verse afectados.
- Confirmación de que no hay archivos visuales protegidos afectados, o
  justificación si `dashboard.html` requiere marcador `[visual]`.
- Siguiente comando recomendado.
