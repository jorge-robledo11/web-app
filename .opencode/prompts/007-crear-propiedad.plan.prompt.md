---
name: 007-crear-propiedad-plan
description: >
  Genera plan.md para 007-crear-propiedad.
spec_kit_command: "/speckit.plan"
usage: "/speckit.plan @.opencode/prompts/007-crear-propiedad.plan.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

## Prompt para `speckit.plan`

Genera `plan.md` para `specs/007-crear-propiedad/`.

## Decisiones técnicas ya definidas

* Arquitectura: extender el vertical slice de propiedades existente.
* Endpoint de formulario: `GET /propiedades/nueva` en `propiedades/routes.py`.
* Endpoint de creación: `POST /propiedades` en `propiedades/routes.py`.
* Servicio: extender `service.crear_propiedad()` con generación de imagen.
* Template: `app/modules/propiedades/templates/crear_propiedad.html`.
* Navbar: agregar botón "Nueva propiedad" en `_navbar.html`.
* Validaciones: Pydantic `PropiedadIn` ya cubre las reglas de negocio;
  validaciones de formulario adicionales en el servicio o rutas.
* Imagen: generar URL vía `https://picsum.photos/800/600` con fallback.
* Redirect: tras creación exitosa, redirigir a `/propiedades`.

## Archivos que el plan debe cubrir

### Modificar

* `app/modules/propiedades/routes.py` — agregar endpoints `GET /nueva` y
  `POST /` (o ajustar prefijo).
* `app/modules/propiedades/service.py` — extender `crear_propiedad()` con
  generación de imagen y lógica de defaults.
* `app/templates/components/_navbar.html` — agregar botón "Nueva propiedad".
* `app/static/css/app.css` — agregar clases para formulario de creación.

### Crear

* `app/modules/propiedades/templates/crear_propiedad.html` — template del
  formulario de creación.

### Posiblemente modificar

* `app/modules/propiedades/schemas.py` — si se requiere un DTO específico
  para el formulario (ej. `PropiedadFormIn` sin `estado`, `imagen`, `area`).

### No modificar

* `app/main.py` — el router de propiedades ya está registrado.
* `base.html`, `_sidebar.html` — sin cambios.
* `propiedades/models.py` — el modelo ya tiene todas las columnas necesarias.
* `propiedades/repository.py` — `crear()` ya existe y es suficiente.

## Fases sugeridas

1. **Fase 1**: Crear template `crear_propiedad.html` con formulario y
   componentes `_form_field.html`. [visual][extension]
2. **Fase 2**: Agregar CSS para formulario de creación. [visual][extension]
3. **Fase 3**: Agregar botón "Nueva propiedad" en `_navbar.html`.
   [visual][extension]
4. **Fase 4**: Agregar endpoint `GET /propiedades/nueva` en `routes.py`.
5. **Fase 5**: Agregar/ajustar endpoint `POST /propiedades` en `routes.py`
   con procesamiento de formulario.
6. **Fase 6**: Extender `service.crear_propiedad()` con generación de imagen
   y defaults (estado, ciudad).
7. **Fase 7**: Si aplica, crear DTO `PropiedadFormIn` para el formulario.
8. **Fase 8**: Tests unitarios del servicio (generación de imagen, defaults,
   validaciones).
9. **Fase 9**: Tests de integración del endpoint (flujo completo, errores,
   fallback de imagen).

## Gobernanza visual

* Clases nuevas en CSS usan tokens existentes → `[visual][extension]`.
* Nuevo template `crear_propiedad.html` → `[visual][extension]`.
* Modificación de `_navbar.html` → `[visual][extension]`.
* Cualquier modificación de token existente → `[visual]` con justificación.

## Complexity Tracking

Registrar si hay desviaciones de la constitución.

## Reglas

* No implementes código.
* No generes `tasks.md`.
* Lee `spec.md`, `constitution.md`, `AGENTS.md` y las instrucciones.
* Mantén todo en español.
* Si detectas decisiones estructurales no resueltas, pregunta en modo
  interactivo.

## Salida esperada

```
Archivo actualizado: specs/007-crear-propiedad/plan.md
Siguiente comando: /speckit.analyze @.opencode/prompts/007-crear-propiedad.analyze.prompt.md
```
