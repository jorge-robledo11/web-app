---
name: 006-pagina-propiedades-cards-implement
description: >
  Implementa 006-pagina-propiedades-cards siguiendo tasks.md.
spec_kit_command: "/speckit.implement"
usage: "/speckit.implement @.opencode/prompts/006-pagina-propiedades-cards.implement.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

## Prompt para `speckit.implement`

Implementa `006-pagina-propiedades-cards` siguiendo `tasks.md` en orden,
respetando TDD y la constitución.

## Precondiciones

* `spec.md`, `plan.md`, `tasks.md` aprobados.
* `report.md` sin hallazgos críticos.
* Branch `006-pagina-propiedades-cards` activo.

## Orden de ejecución

Seguir las fases de `tasks.md` en orden numérico. Dentro de cada fase,
ejecutar las tareas en orden.

## Reglas TDD

* Escribir tests antes del código de producción (Red-Green-Refactor).
* No escribir código sin test asociado.

## Reglas de calidad

* Ejecutar `uv run ruff check .` y `uv run ruff format --check .` tras cada
  fase.
* Ejecutar `uv run mypy --strict app/modules/propiedades/` tras cambios en
  `propiedades/`.
* Ejecutar tests tras cada fase.

## Gobernanza visual

* Tareas con `[visual][extension]`: permitido agregar CSS/clases nuevas sin
  modificar tokens existentes.
* Tareas con `[visual]`: requieren justificación en `Complexity Tracking`.

## Restricciones

* No modificar tokens visuales canónicos.
* No crear endpoints adicionales.
* No introducir dependencias nuevas.
* No modificar modelos de datos.
* No crear módulos de rentas, pagos ni contratos.
* Mantener todo en español.

## Validación final

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict app/modules/propiedades/
uv run pytest tests/unit/propiedades tests/integration/propiedades -q
uv run pytest --cov=app/modules/propiedades --cov-report=term-missing
```

## Salida esperada

```
Feature implementada: 006-pagina-propiedades-cards
Tests: N pasados
Cobertura: X%
```
