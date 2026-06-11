# Tareas: Blindar tokens visuales canónicos del frontend

**Input**: Design documents from `specs/002-blindar-tokens-visuales/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

## Formato: `[ID] [P?] [Story] Descripción`

- **[P]**: Puede ejecutarse en paralelo (archivos distintos, sin dependencias)
- **[Story]**: Historia de usuario a la que pertenece (US1, US2, US3)
- Incluye rutas exactas en las descripciones

---

## Fase 1: Implementación del script (US1 + US3)

**Propósito**: Crear el script `check-visual-trace.sh` que audita trazabilidad
visual.

- [ ] T1.1 [P] [US3] Crear `scripts/check-visual-trace.sh` con `set -euo pipefail`. El script debe: listar archivos modificados con `git diff main...HEAD --name-only`, listar archivos nuevos no trackeados con `git ls-files --others --exclude-standard`, comparar contra la lista hardcodeada de 7 archivos protegidos (definida en `contracts/visual-trace.yaml`), y verificar que `tasks.md` del directorio `specs/<feature-actual>/` contiene al menos una línea de tarea con marcador `[visual]` (solo en líneas `- [ ]` o `- [X]`). Retorna 0 si OK, 1 si hay archivos protegidos modificados sin `[visual]` o si `tasks.md` no existe. **Marcador requerido: `[visual]` — esta tarea crea el script que implementa la gobernanza visual.**

---

## Fase 2: Validación del script (US3)

**Propósito**: Verificar que el script cumple los criterios de aceptación SC-001,
SC-002 y SC-003.

- [ ] T2.1 [US3] Asignar permisos de ejecución al script: `chmod +x scripts/check-visual-trace.sh`. Verificar SC-001.
- [ ] T2.2 [US3] Ejecutar `bash scripts/check-visual-trace.sh` desde la raíz del proyecto. El script debe buscar automáticamente `tasks.md` en `specs/002-blindar-tokens-visuales/tasks.md`. Verificar que retorna 0 (SC-002: esta feature no modifica archivos visuales protegidos).
- [ ] T2.3 [US3] Simular SC-003: modificar `app/static/css/app.css` temporalmente (agregar una línea de comentario), ejecutar el script, verificar que retorna 1 con mensaje descriptivo. Restaurar `app.css` con `git checkout app/static/css/app.css`.

---

## Fase 3: Cierre y calidad

**Propósito**: Verificar que la feature no introduce regresiones y que los
artefactos de gobernanza están actualizados.

- [ ] T3.1 Ejecutar `uv run ruff check .` y verificar que pasa limpio.
- [ ] T3.2 Ejecutar `uv run ruff format --check .` y verificar que pasa limpio.
- [ ] T3.3 Verificar que `AGENTS.md` tiene la referencia al plan vigente (`specs/002-blindar-tokens-visuales/plan.md`).
- [ ] T3.4 Ejecutar la validación completa de `quickstart.md`: verificar existencia del script, ejecución en la feature actual, simulación de fallo.

---

## Dependencias y orden de ejecución

```
T1.1 ──► T2.1 ──► T2.2 ──► T2.3 ──► T3.1 ──► T3.2 ──► T3.3 ──► T3.4
```

Todas las tareas son secuenciales. No hay oportunidades de paralelismo en esta
spec porque cada paso depende del anterior.

### Bloqueos

Ninguno. T1.1 es la única tarea de creación; el resto son verificaciones.

---

## Estrategia de implementación

1. Crear el script (T1.1)
2. Validar que funciona en el caso feliz (T2.1, T2.2)
3. Validar que detecta fallos (T2.3)
4. Verificar calidad (T3.1, T3.2)
5. Verificar gobernanza (T3.3)
6. Validación final (T3.4)

---

## Notas

- Esta spec no modifica código de aplicación. Solo crea `scripts/check-visual-trace.sh`.
- Los artefactos de gobernanza (constitución v1.2.0, `frontend.instructions.md`,
  `AGENTS.md`, `spec-template.md`) ya fueron actualizados por `/speckit.constitution`.
- El marcador `[visual]` en T1.1 es obligatorio según FR-002 de esta misma spec
  (el script es parte del sistema de gobernanza visual).
- Las reglas de trazabilidad aplican a partir de la spec `003`. Esta spec `002`
  es fundacional y establece la base.
