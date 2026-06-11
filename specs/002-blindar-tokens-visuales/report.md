# Reporte de Auditoría: Blindar tokens visuales canónicos del frontend

**Feature**: `002-blindar-tokens-visuales` | **Date**: 2026-06-10

**Artefactos revisados**: `spec.md`, `plan.md`, `research.md`, `data-model.md`,
`quickstart.md`, `contracts/visual-trace.yaml`

---

## Resumen

| Severidad | Cantidad |
|---|---|
| CRÍTICO | 0 |
| ADVERTENCIA | 1 |
| SUGERENCIA | 1 |

---

## Hallazgos

### ADVERTENCIA

#### A1 — research.md omite htmx.min.js de la lista de archivos protegidos

- **Archivo**: `research.md:27-30`
- **Problema**: La sección 3 describe la lista de archivos protegidos como "6
  patrones" y enumera solo 6 elementos, pero la spec (línea 172), el data-model
  (línea 20) y el contrato (línea 20) incluyen 7 categorías. Falta
  `app/static/vendor/htmx.min.js` en la lista textual de research.md.
- **Recomendación**: Agregar `app/static/vendor/htmx.min.js` a la enumeración en
  research.md y corregir "6 patrones" por "7 patrones".

---

### SUGERENCIA

#### S1 — El script no detecta archivos nuevos no commiteados

- **Archivo**: `contracts/visual-trace.yaml:11`
- **Problema**: El contrato define `git diff main...HEAD --name-only` como
  mecanismo de detección, pero este comando solo muestra diferencias entre
  commits. Si una feature agrega un icono nuevo (`app/static/icons/nuevo.svg`)
  que aún no fue commiteado, el script no lo detectará.
- **Recomendación**: Durante la implementación del script, considerar agregar
  `git ls-files --others --exclude-standard` o `git status --porcelain` para
  cubrir archivos nuevos no trackeados. Documentar esta limitación en el
  quickstart si no se implementa.

---

## Verificación de consistencia entre artefactos

| Par de artefactos | Estado |
|---|---|
| `spec.md` ↔ `plan.md` | Consistente |
| `spec.md` ↔ `contracts/visual-trace.yaml` | Consistente (7 categorías, exit codes, mensajes) |
| `spec.md` ↔ `data-model.md` | Consistente (5 marcadores, 7 archivos protegidos) |
| `spec.md` ↔ `quickstart.md` | Consistente (SC-002, SC-003 validados) |
| `spec.md` ↔ `research.md` | A1 — htmx.min.js omitido |
| `plan.md` ↔ `research.md` | Consistente |
| `plan.md` ↔ `data-model.md` | Consistente |
| `plan.md` ↔ `contracts/` | Consistente |
| `contracts/` ↔ `data-model.md` | Consistente |

---

## Conclusión

Sin hallazgos CRÍTICOS. La spec y el plan son consistentes en sus decisiones
centrales. La ADVERTENCIA A1 es una omisión menor en research.md que no bloquea
`/speckit.tasks`. La SUGERENCIA S1 es una mejora de implementación para el
script.

La feature está lista para `/speckit.tasks`.
