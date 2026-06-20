---
name: 007-crear-propiedad-tasks
description: >
  Genera tasks.md para 007-crear-propiedad.
spec_kit_command: "/speckit.tasks"
usage: "/speckit.tasks @.opencode/prompts/007-crear-propiedad.tasks.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

## Prompt para `speckit.tasks`

Genera `tasks.md` para `specs/007-crear-propiedad/` a partir de
`spec.md` y `plan.md`.

## Estructura esperada

Tareas pequeñas, ordenadas, verificables y trazables a requisitos funcionales.
Cada tarea debe tener un identificador `T<fase>.<numero>`.

## Fases esperadas

### Fase 0: Contexto
* T0.1: Leer spec.md, plan.md, report.md.
* T0.2: Leer instrucciones backend, frontend, database y tests.

### Fase 1: Template del formulario
* T1.1: Crear `app/modules/propiedades/templates/crear_propiedad.html` con
  formulario de creación usando `_form_field.html`. [visual][extension]
* T1.2: Incluir campos: titulo, direccion, precio_mensual, habitaciones,
  banos (y area si aplica según clarificación).
* T1.3: Incluir manejo de errores inline y re-populación de campos.
* T1.4: Agregar CSS para formulario de creación. [visual][extension]

### Fase 2: Botón en navbar
* T2.1: Agregar botón "Nueva propiedad" en `_navbar.html` (sección de
  acciones). [visual][extension]
* T2.2: Si aplica, vendorear icono nuevo de Lucide (ej. `plus`).
  [visual][extension]

### Fase 3: Endpoint de formulario
* T3.1: Agregar endpoint `GET /propiedades/nueva` en `routes.py` que
  renderice el formulario vacío.

### Fase 4: Endpoint de creación
* T4.1: Agregar endpoint `POST /propiedades` en `routes.py` que procese
  el formulario.
* T4.2: Implementar parseo de datos de formulario a DTO.
* T4.3: Implementar re-renderizado del formulario con errores si validación
  falla.
* T4.4: Implementar redirect a `/propiedades` con mensaje flash tras
  creación exitosa.

### Fase 5: Lógica de servicio
* T5.1: Extender `service.crear_propiedad()` con generación automática de
  URL de imagen vía `https://picsum.photos`.
* T5.2: Implementar fallback de imagen si picsum.photos falla.
* T5.3: Aplicar defaults: estado `disponible`, ciudad `Miami`.
* T5.4: Si aplica, crear DTO `PropiedadFormIn` para el formulario (sin
  `estado`, `imagen`, `area`).

### Fase 6: Tests unitarios
* T6.1: Test de generación de URL de imagen.
* T6.2: Test de fallback de imagen cuando picsum falla.
* T6.3: Test de defaults (estado disponible, ciudad Miami).
* T6.4: Test de validación de campos obligatorios.
* T6.5: Test de campos con solo espacios tratados como vacíos.

### Fase 7: Tests de integración
* T7.1: Test de `GET /propiedades/nueva` retorna 200 con formulario.
* T7.2: Test de `POST /propiedades` con datos válidos crea y redirige.
* T7.3: Test de `POST /propiedades` con datos inválidos re-renderiza
  formulario con errores.
* T7.4: Test de campos con solo espacios retornan error.
* T7.5: Test de precio_mensual inválido (vacío, no numérico, <= 0).
* T7.6: Test de habitaciones y banos inválidos.
* T7.7: Test de fallback de imagen en creación.
* T7.8: Test de botón "Nueva propiedad" visible en navbar.

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
Archivo actualizado: specs/007-crear-propiedad/tasks.md
Tareas: N
Siguiente comando: /speckit.implement @.opencode/prompts/007-crear-propiedad.implement.prompt.md
```
