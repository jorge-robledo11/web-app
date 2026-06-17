---
name: 006-pagina-propiedades-cards-tasks
description: >
  Genera tasks.md para 006-pagina-propiedades-cards.
spec_kit_command: "/speckit.tasks"
usage: "/speckit.tasks @.opencode/prompts/006-pagina-propiedades-cards.tasks.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

## Prompt para `speckit.tasks`

Genera `tasks.md` para `specs/006-pagina-propiedades-cards/` a partir de
`spec.md` y `plan.md`.

## Estructura esperada

Tareas pequeñas, ordenadas, verificables y trazables a requisitos funcionales.
Cada tarea debe tener un identificador `T<fase>.<numero>`.

## Fases esperadas

### Fase 0: Contexto
* T0.1: Leer spec.md, plan.md, report.md.
* T0.2: Leer instrucciones backend, frontend, database y tests.

### Fase 1: Extender componente card
* T1.1: Extender `_card_propiedad.html` con campos: imagen, habitaciones,
  baños, área, precio, estado. [visual][extension]
* T1.2: Agregar placeholder visual para imagen faltante (fondo + icono). [visual][extension]
* T1.3: Agregar ellipsis para textos largos.

### Fase 2: Crear template de página
* T2.1: Crear `app/modules/propiedades/templates/propiedades.html` con grid
  y estado vacío. [visual][extension]
* T2.2: Agregar CSS para grid responsive (3/2/1 columnas). [visual][extension]
* T2.3: Agregar CSS para cards extendidas (imagen, datos, badge). [visual][extension]

### Fase 3: Lógica de servicio
* T3.1: Agregar `listar_propiedades()` en `propiedades/service.py`.
* T3.2: Formatear precio ($1,500.00) y área (1,000 m²) en el servicio.

### Fase 4: Endpoint
* T4.1: Reemplazar placeholder en `propiedades/routes.py` con `GET /propiedades`.
* T4.2: Verificar que `app/main.py` ya incluye el router de propiedades.

### Fase 5: Navegación
* T5.1: Cambiar href del enlace "Propiedades" en `_sidebar.html` de `#` a
  `/propiedades`.

### Fase 6: Tests unitarios
* T6.1: Test de `listar_propiedades()` con mock del repositorio.
* T6.2: Test de formato de precio y área.

### Fase 7: Tests de integración
* T7.1: Test de `GET /propiedades` con datos reales (Testcontainers + seed).
* T7.2: Test de render HTML: verificar cards, campos visibles, grid.
* T7.3: Test de estado vacío.
* T7.4: Test de placeholder de imagen.
* T7.5: Test de navegación desde sidebar.

### Fase 8: Calidad
* T8.1: Ruff check + format.
* T8.2: Mypy strict en `app/modules/propiedades/`.
* T8.3: Pytest con coverage ≥ 80%.

## Reglas

* No implementes código.
* Cada tarea debe ser verificable independientemente.
* Tareas que tocan archivos visuales protegidos deben tener marcador `[visual]`,
  `[visual][extension]` o `[visual][bugfix]`.
* Mantener orden de dependencias entre fases.
* Mantener todo en español.

## Salida esperada

```
Archivo actualizado: specs/006-pagina-propiedades-cards/tasks.md
Tareas: N
Siguiente comando: /speckit.implement @.opencode/prompts/006-pagina-propiedades-cards.implement.prompt.md
```
