---
name: 003-redisenar-home-analyze
description: >
  Genera un reporte de consistencia entre spec, plan y artefactos para
  003-redisenar-home.
---

/speckit.analyze

Audita la consistencia de la feature `003-redisenar-home` usando el workflow
canónico de Spec Kit.

Usa la feature activa resuelta por Spec Kit. No asumas rutas fijas si el comando
ya puede resolverlas.

## Alcance

Revisa, como mínimo:

- `spec.md`
- `plan.md`
- `research.md`, si existe
- `quickstart.md`, si existe
- `contracts/*.yaml`, si existen
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

## Severidades

El reporte debe estar en español y organizado con estos niveles de severidad:

- **CRÍTICO**: debe corregirse antes de `/speckit.tasks`.
- **ADVERTENCIA**: debería atenderse o documentarse.
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
- Siguiente comando recomendado.
