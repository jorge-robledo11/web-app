---
name: 002-blindar-tokens-visuales-analyze
description: >
  Genera un reporte de consistencia entre spec, plan y artefactos para
  002-blindar-tokens-visuales.
---

/speckit.analyze

Audita la consistencia de la feature `002-blindar-tokens-visuales` usando el workflow
canónico de Spec Kit.

Usa la feature activa resuelta por Spec Kit. No asumas rutas fijas si el comando
ya puede resolverlas.

## Alcance

Revisa, como mínimo:

- `spec.md`
- `plan.md`
- Artefactos generados por el plan, si existen

## Salida esperada

Genera o actualiza el archivo `report.md` dentro de la carpeta de la feature
activa resuelta por Spec Kit.

El reporte debe estar en español y organizado con estos niveles de severidad:

- **CRÍTICO**: debe corregirse antes de `/speckit.tasks`.
- **ADVERTENCIA**: debería atenderse o documentarse.
- **SUGERENCIA**: considerar para iteraciones futuras.

## Reglas

- No edites `spec.md`, `plan.md` ni otros artefactos existentes.
- No generes tareas.
- No implementes código.
- Cada hallazgo debe incluir:
  - Severidad
  - Archivo afectado
  - Problema
  - Recomendación de corrección
- Si no hay problemas, genera igualmente `report.md` indicando que no se
  detectaron inconsistencias.

Al finalizar, indica:

- Ruta del `report.md` generado o actualizado.
- Cantidad de hallazgos por severidad.
- Siguiente comando recomendado.