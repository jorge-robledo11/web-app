# Reporte de Análisis: Rediseñar Home principal

**Feature**: `003-redisenar-home` | **Date**: 2026-06-13 | **Iteración**: 3

## Resumen

| Severidad | Cantidad |
|-----------|----------|
| CRÍTICO | 0 |
| ADVERTENCIA | 1 |
| SUGERENCIA | 1 |

No se detectaron inconsistencias que bloqueen `/speckit.tasks`.

---

## Hallazgos

### ADVERTENCIA 1 — Convención mixta de breakpoints en la spec

- **Archivos**: `spec.md` (FR-008 vs. Impacto visual)
- **Problema**: FR-008 declara el breakpoint como `1023px` (valor CSS `max-width`), mientras que la sección Impacto visual lista los tokens canónicos con `1024px` (umbral conceptual de `frontend.instructions.md`). Ambas convenciones describen el mismo comportamiento: tablet se activa en viewports ≤ 1023px (equivalente a "menores a 1024px"). SC-004 (768px tablet) y SC-005 (1024px desktop) son correctos con ambas interpretaciones.
- **Recomendación**: Para futuras specs, elegir una convención y mantenerla en todo el documento. La convención de `frontend.instructions.md` es 1024px/768px como umbrales. No requiere corrección para esta spec — no es funcional.

---

### SUGERENCIA 1 — Sin criterios de accesibilidad explícitos para el nuevo componente

- **Archivos**: `spec.md`, `plan.md`, `.opencode/instructions/frontend.instructions.md`
- **Problema**: `frontend.instructions.md` exige `<label for>`, `aria-*`, foco visible y contraste AA. El nuevo componente `_actividad_item.html` y los estados de carga/error no mencionan requisitos de accesibilidad.
- **Recomendación**: Agregar en `tasks.md` una tarea de verificación de accesibilidad.

---

## Validación de contratos YAML

| Archivo | Estado |
|---------|--------|
| `contracts/dashboard.yaml` | ✅ Válido |
| `contracts/estados.yaml` | ✅ Válido |

---

## Verificación de gobernanza visual

- **Archivos protegidos afectados**: 5 + 2 iconos nuevos
- **Marcadores requeridos**: `[visual]`, `[visual][extension]`, `[visual][componente]`
- **Tokens canónicos modificados**: Ninguno
- **base.html modificado**: No
- **Estado**: Consistente con spec 002. Sin violaciones.

---

## Historial de iteraciones

| Iteración | CRÍTICO | ADVERTENCIA | SUGERENCIA |
|-----------|---------|-------------|------------|
| 1 (inicial) | 0 | 3 | 1 |
| 2 (post-corrección) | 1 | 0 | 1 |
| 3 (actual) | 0 | 1 | 1 |

Los 3 hallazgos de la iteración 1 (breakpoint, tendencia, arrow-up-right) y el CRÍTICO de la iteración 2 (SC-005 1023px desktop) fueron corregidos.

---

## Conclusión

La spec, plan, research, data-model, quickstart y contratos son consistentes entre sí. No hay bloqueos para `/speckit.tasks`. La ADVERTENCIA sobre convención mixta de breakpoints es puramente documental.

**Siguiente paso**: `/speckit.tasks`
