# Reporte de Auditoría: Bootstrap del Proyecto Realtor

**Feature**: `001-bootstrap-proyecto` | **Date**: 2026-06-08 (segunda pasada)

**Artefactos revisados**: `spec.md`, `plan.md`, `research.md`, `data-model.md`,
`quickstart.md`, `contracts/health.md`, `contracts/dashboard.md`

---

## Resumen

| Severidad | Cantidad |
|---|---|
| CRÍTICO | 0 |
| ADVERTENCIA | 4 |
| SUGERENCIA | 2 |

Los 2 hallazgos CRÍTICOS de la auditoría anterior (C1: respuesta health,
C2: orden TDD) fueron corregidos y ya no aparecen.

---

## Hallazgos

### ADVERTENCIA

#### A1 — Edge case de health aún referencia valor antiguo

- **Archivo**: `spec.md:90`
- **Problema**: El edge case "PostgreSQL no está disponible al iniciar" dice
  `database: "error"`, pero el acceptance scenario (línea 33), las clarificaciones
  (línea 238) y `contracts/health.md` (línea 37) usan `"unavailable"`.
- **Recomendación**: Cambiar `database: "error"` por `database: "unavailable"` en
  la línea 90 para mantener consistencia.

#### A2 — Edge case de migración referencia "vacía"

- **Archivo**: `spec.md:93`
- **Problema**: El edge case dice "la migración baseline (vacía o inicial)", pero
  Key Entities (línea 166), clarificaciones (línea 269) y `data-model.md` (línea
  63) establecen que instala `pgcrypto`.
- **Recomendación**: Cambiar "vacía o inicial" por "que instala pgcrypto" en la
  línea 93.

#### A3 — Docstring de migración desincronizado con revision ID

- **Archivo**: `data-model.md:51`
- **Problema**: El docstring dice `Revision ID: 001` pero el código en la línea
  58 usa `revision: str = "001_bootstrap"`. Alembic usa el valor de `revision`
  como ID real; el docstring debe coincidir.
- **Recomendación**: Cambiar el docstring a `Revision ID: 001_bootstrap`.

#### A4 — FR-015 no refleja el breakpoint de 768px

- **Archivo**: `spec.md:136`
- **Problema**: FR-015 solo menciona "por debajo de 1024px", pero SC-005
  (línea 182) y las clarificaciones (línea 228) definen dos breakpoints:
  1024px (overlay) y 768px (oculta con toggle). El FR quedó desactualizado
  respecto a las clarificaciones.
- **Recomendación**: Ampliar FR-015 para incluir ambos breakpoints:
  "colapsar a overlay por debajo de 1024px y ocultarse con toggle por debajo
  de 768px".

---

### SUGERENCIA

#### S1 — Versión de HTMX no especificada

- **Archivo**: `research.md:70`
- **Problema**: Se referencia "HTMX 1.x" sin versión concreta. La versión afecta
  la API de atributos disponible en templates.
- **Recomendación**: Especificar la versión exacta (ej. `2.0.4`) en `research.md`
  o en el plan.

#### S2 — Falta `.gitignore` en los artefactos

- **Archivo**: `plan.md`
- **Problema**: Ni spec ni plan mencionan `.gitignore`. Sin él, `.env`,
  `__pycache__/` y `.venv/` podrían versionarse.
- **Recomendación**: Incluir `.gitignore` en la estructura del plan y en el orden
  de implementación.

---

## Verificación de consistencia entre artefactos

| Par de artefactos | Estado |
|---|---|
| `spec.md:33` ↔ `clarificaciones:238` | Consistente (corregido C1) |
| `spec.md:33` ↔ `contracts/health.md:37` | Consistente |
| `spec.md:90` (edge case) ↔ `spec.md:33` | A1 — `"error"` vs `"unavailable"` |
| `spec.md:93` (edge case) ↔ Key Entities:166 | A2 — "vacía" vs "pgcrypto" |
| `plan.md:152-159` (orden TDD) | Consistente (corregido C2) |
| `data-model.md:51` ↔ `data-model.md:58` | A3 — docstring vs código |
| `FR-015:136` ↔ `SC-005:182` | A4 — un breakpoint vs dos |
| `spec.md` ↔ `contracts/dashboard.md` | Consistente |
| `spec.md` ↔ `quickstart.md` | Consistente |
| `plan.md` ↔ `research.md` | Consistente |
| `plan.md` ↔ `data-model.md` | Consistente |

---

## Conclusión

Los 2 hallazgos CRÍTICOS de la auditoría anterior están corregidos. Los
artefactos son consistentes en sus decisiones centrales. Las 4 ADVERTENCIAS
son correcciones de precisión en edge cases y documentación interna que no
bloquean `/speckit.tasks`. Las 2 SUGERENCIAS son mejoras opcionales.

La feature está lista para avanzar a `/speckit.tasks`.
