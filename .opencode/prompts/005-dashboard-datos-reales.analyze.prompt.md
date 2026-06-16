---
name: 005-dashboard-datos-reales-analyze
description: >
  Genera un reporte de consistencia entre spec, plan y artefactos para
  005-dashboard-datos-reales.
spec_kit_command: "/speckit.analyze"
usage: "/speckit.analyze @.opencode/prompts/005-dashboard-datos-reales.analyze.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

Audita la consistencia de la feature `005-dashboard-datos-reales` usando el
workflow canónico de Spec Kit.

Usa la feature activa resuelta por Spec Kit. No asumas rutas fijas si el comando
ya puede resolverlas.

## Alcance

Revisa, como mínimo:

- `spec.md`
- `plan.md`
- `research.md`, si existe
- `quickstart.md`, si existe
- `contracts/*.yaml`, si existen (especialmente `dashboard.yaml`)
- Artefactos generados por el plan, si existen

## Reglas

- Mantén todo en español.
- No edites `spec.md`, `plan.md` ni otros artefactos existentes.
- No generes tareas.
- No implementes código.
- Respeta la constitución, `AGENTS.md`, `spec.md`, clarificaciones y las
  instrucciones activas de `.opencode/instructions/*.instructions.md`.
- Respeta la gobernanza visual vigente definida por `002-blindar-tokens-visuales`.
- Verifica que el plan no proponga cambios visuales fuera de los tokens
  canónicos sin trazabilidad.
- Verifica que cualquier afectación a archivos visuales protegidos tenga
  justificación y ruta de trazabilidad.
- Verifica que los contratos `contracts/*.yaml`, si existen, sean YAML válido y
  no contengan Markdown, texto narrativo libre ni bloques de código.
- Si detectas una inconsistencia que bloquee `/speckit.tasks`, clasifícala como
  **CRÍTICO**.

## Verificaciones específicas de esta feature

Además de las verificaciones generales, audita específicamente:

- **Scope creep**: El plan NO debe proponer módulos de rentas, pagos ni
  contratos. Cualquier mención a estos conceptos como implementación es CRÍTICO.
- **GET / fuera del slice dashboard**: `GET /` debe pertenecer al slice
  dashboard en `app/modules/dashboard/routes.py`. `app/main.py` no debe contener
  lógica de cálculo ni construcción del contexto del dashboard; solo puede
  registrar o incluir el router del slice dashboard si corresponde. Cualquier
  desviación es CRÍTICO.
- **Cálculo inventado**: El plan NO debe incluir lógica que calcule ingresos o
  vencidos a partir de datos de propiedades. Esas métricas deben permanecer con
  valor `0` y marcador "No disponible". Cualquier intento de cálculo es CRÍTICO.
- **Cambios visuales no justificados**: El plan NO debe proponer cambios en CSS,
  tokens, iconografía o componentes compartidos. Si `dashboard.html` se modifica,
  debe ser solo para reflejar métricas reales y el estado vacío, sin alterar
  estructura visual ni el contrato de contexto.
- **Ruptura del contrato de contexto**: El contexto que recibe `dashboard.html`
  debe conservar las keys `metricas`, `accesos`, `actividad` y `actividad_estado`.
  Cualquier cambio en los nombres o tipos de estas keys es CRÍTICO.
- **Falta de tests**: El plan debe cubrir pruebas unitarias del servicio y
  pruebas de integración del render. La ausencia total de estrategia de pruebas
  es ADVERTENCIA.
- **Contradicciones con gobernanza vigente**: Cualquier propuesta que contradiga
  la constitución, `AGENTS.md` o las instrucciones activas es CRÍTICO.
- **Módulo dashboard mal ubicado**: El módulo debe residir en
  `app/modules/dashboard/`. Cualquier otra ubicación es CRÍTICO.
- **Lógica de dashboard en `app/main.py`**: `app/main.py` no debe contener
  lógica de cálculo ni construcción del contexto del dashboard. Si el plan o
  la implementación dejan esta lógica fuera del slice, es CRÍTICO.
- **Dependencias nuevas**: Cualquier mención a paquetes Python no existentes en
  `pyproject.toml` es ADVERTENCIA.

## Severidades

El reporte debe estar en español y organizado con estos niveles de severidad:

- **CRÍTICO**: debe corregirse antes de `/speckit.tasks`.
- **ADVERTENCIA**: debería corregirse también.
- **SUGERENCIA**: considerar para iteraciones futuras.

## Hallazgos

Cada hallazgo debe incluir:

- Severidad.
- Archivo afectado.
- Problema.
- Recomendación de corrección.

Si no hay problemas, genera igualmente `report.md` indicando que no se detectaron
inconsistencias.

## Salida esperada

Genera o actualiza el archivo `report.md` dentro de la carpeta de la feature
activa resuelta por Spec Kit.

Al finalizar, indica:

- Ruta del `report.md` generado o actualizado.
- Cantidad de hallazgos por severidad.
- Si los contratos YAML fueron validados, cuando existan.
- Si hubo inconsistencias relacionadas con gobernanza visual.
- Si hay hallazgos, la siguiente fase es `005-dashboard-datos-reales.fix-report.prompt.md`.
- Si no hay hallazgos (cero críticos y cero advertencias), la siguiente fase es
  `005-dashboard-datos-reales.tasks.prompt.md`.
