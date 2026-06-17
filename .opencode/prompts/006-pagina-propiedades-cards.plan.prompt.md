---
name: 006-pagina-propiedades-cards-plan
description: >
  Genera plan.md para 006-pagina-propiedades-cards.
spec_kit_command: "/speckit.plan"
usage: "/speckit.plan @.opencode/prompts/006-pagina-propiedades-cards.plan.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

## Prompt para `speckit.plan`

Genera `plan.md` para `specs/006-pagina-propiedades-cards/`.

## Decisiones técnicas ya definidas

* Arquitectura: extender el vertical slice de propiedades existente.
* Endpoint: `GET /propiedades` en `propiedades/routes.py`.
* Servicio: nueva función en `propiedades/service.py` que obtiene propiedades
  y las formatea para el template.
* Template: `app/modules/propiedades/templates/propiedades.html`.
* Componente: extender `_card_propiedad.html` con campos nuevos.
* Datos: usar `PropiedadOut` existente como DTO.
* Responsive: CSS Grid con 3/2/1 columnas usando breakpoints del sistema.
* Imagen placeholder: div con `--color-surface` + icono building-2.

## Archivos que el plan debe cubrir

### Modificar

* `app/modules/propiedades/routes.py` — reemplazar placeholder con endpoint real.
* `app/modules/propiedades/service.py` — agregar función `listar_propiedades()`.
* `app/templates/components/_card_propiedad.html` — extender con campos nuevos.
* `app/templates/components/_sidebar.html` — cambiar href `#` → `/propiedades`.
* `app/static/css/app.css` — agregar clases de grid y card extendida.

### Crear

* `app/modules/propiedades/templates/propiedades.html` — template de la página.

### No modificar

* `app/main.py` — el router de propiedades ya está registrado.
* `base.html`, `_navbar.html` — sin cambios.
* `propiedades/models.py`, `propiedades/repository.py` — ya tienen lo necesario.
* `propiedades/schemas.py` — `PropiedadOut` ya es suficiente.

## Fases sugeridas

1. **Fase 1**: Extender `_card_propiedad.html` con los 8 campos.
2. **Fase 2**: Crear template `propiedades.html` con grid y estado vacío.
3. **Fase 3**: Agregar `listar_propiedades()` en `propiedades/service.py`.
4. **Fase 4**: Implementar endpoint `GET /propiedades` en `routes.py`.
5. **Fase 5**: Actualizar `_sidebar.html` con href `/propiedades`.
6. **Fase 6**: Agregar CSS para grid responsive y cards extendidas.
7. **Fase 7**: Tests unitarios del servicio.
8. **Fase 8**: Tests de integración del endpoint y render.

## Gobernanza visual

* Clases nuevas en CSS usan tokens existentes → `[visual][extension]`.
* Extensión de `_card_propiedad.html` → `[visual][extension]`.
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
Archivo actualizado: specs/006-pagina-propiedades-cards/plan.md
Siguiente comando: /speckit.analyze @.opencode/prompts/006-pagina-propiedades-cards.analyze.prompt.md
```
