# Plan de Implementación: Blindar tokens visuales canónicos del frontend

**Branch**: `002-blindar-tokens-visuales` | **Date**: 2026-06-10 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/002-blindar-tokens-visuales/spec.md`

## Resumen

Establecer una capa de gobernanza visual que proteja los tokens canónicos del
sistema Realtor. Esta spec no modifica código de aplicación: crea un script de
verificación (`check-visual-trace.sh`) que audita la trazabilidad de cambios
visuales, define marcadores obligatorios en `tasks.md` y actualiza los artefactos
de gobernanza (constitución, `AGENTS.md`, `frontend.instructions.md`,
`spec-template.md`) para que futuras specs declaren y tracen sus cambios visuales.

## Contexto técnico

**Lenguaje/Versión**: Bash (script de verificación), Python 3.13.13 (proyecto)

**Dependencias principales**: Ninguna nueva. El script usa solo `git` y `bash`
estándar.

**Almacenamiento**: N/A (no hay base de datos)

**Testing**: Prueba manual del script contra features con y sin cambios visuales

**Plataforma objetivo**: Linux (desarrollo local)

**Tipo de proyecto**: Script de gobernanza + actualización de documentación

**Metas de rendimiento**: El script `check-visual-trace.sh` debe ejecutarse en
menos de 1 segundo.

**Restricciones**: Sin nuevas dependencias de producción ni desarrollo. Sin
cambios en código de aplicación. Sin modificar tokens existentes.

**Escala/Alcance**: Un script bash (~40 líneas) + actualización de 4 artefactos
de gobernanza. Sin código de dominio.

## Verificación de constitución

*GATE: Debe pasar antes de Phase 0. Re-verificar tras Phase 1.*

| Regla | Cumple | Evidencia |
|---|---|---|
| I. Idioma español | Sí | Script, artefactos y docstrings en español |
| II. Stack inmutable | Sí | Sin cambios al stack |
| III. Prohibiciones | Sí | Sin nuevas herramientas prohibidas |
| IV. Vertical Slice | N/A | Spec de gobernanza, sin módulo de dominio |
| V. Spec-Driven | Sí | Spec aprobada antes de implementar |
| VI. Flujo Spec Kit | Sí | `specify` → `clarify` → `plan` (fase actual) |
| VIII. TDD | N/A | Sin código de aplicación; validación manual |
| IX. Calidad | N/A | Sin cambios en `app/modules/` |
| X. Base de datos | N/A | Sin cambios en base de datos |
| XI. Async-First | N/A | Sin I/O en esta spec |
| XII. Frontend | Parcial | Esta spec REFUERZA sección XII, no la modifica |
| XIII. Estructura | Sí | El script vive en `scripts/` (ubicación canónica) |
| XIV. Contratos | N/A | Sin endpoints ni DTOs |
| XV. Complexity | Sí | Sin desviaciones |

**Resultado**: PASA. Esta spec es una extensión de gobernanza, no modifica
código de aplicación.

## Estructura del proyecto

### Documentación (esta feature)

```text
specs/002-blindar-tokens-visuales/
├── spec.md
├── plan.md
├── research.md
├── quickstart.md
├── contracts/
│   └── visual-trace.yaml
└── tasks.md
```

### Código fuente (raíz del repositorio)

```text
scripts/
  check-visual-trace.sh        # Creado por esta spec
```

### Artefactos de gobernanza (ya actualizados por /speckit.constitution)

```text
.specify/memory/constitution.md       # v1.2.0, sección XII blindaje visual
.opencode/instructions/frontend.instructions.md  # Sección 0: fuente operativa
AGENTS.md                             # Regla de tokens visuales
.specify/templates/spec-template.md   # Sección Impacto visual
```

**Decisión estructural**: El script `check-visual-trace.sh` vive en `scripts/`
(scripts compartidos del proyecto), no en un módulo de feature. Es una
herramienta de uso transversal como `lint.sh` o `test.sh`. No se integra en
`make check` por decisión de las clarificaciones.

## Orden de implementación

1. Crear `scripts/check-visual-trace.sh` con `set -euo pipefail` y permisos `+x`
2. Verificar SC-001: el script existe y es ejecutable
3. Simular SC-002: ejecutar script en feature sin cambios visuales → retorna 0
4. Simular SC-003: modificar `app.css` temporalmente, ejecutar script → retorna 1
5. Restaurar `app.css` al estado original
6. Actualizar `AGENTS.md` con la referencia al plan vigente
7. Verificar que `ruff check .` y `ruff format --check .` pasan limpios

## Complexity Tracking

Sin desviaciones. Esta spec refuerza la sección XII de la constitución v1.2.0
sin modificarla.
