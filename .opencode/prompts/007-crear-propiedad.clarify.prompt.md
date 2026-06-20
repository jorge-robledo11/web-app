---
name: 007-crear-propiedad-clarify
description: >
  Clarifica ambigüedades de la spec 007-crear-propiedad antes del plan.
spec_kit_command: "/speckit.clarify"
usage: "/speckit.clarify @.opencode/prompts/007-crear-propiedad.clarify.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

## Prompt para `speckit.clarify`

Ejecuta clarificación interactiva sobre `specs/007-crear-propiedad/spec.md`.

## Decisiones ya tomadas

Las siguientes decisiones están cerradas y no deben reabrirse:

* Arquitectura: extender el vertical slice de propiedades existente.
* Campos obligatorios: titulo, direccion, precio_mensual, habitaciones, banos.
* Estado por defecto: `disponible`.
* Imagen: generada automáticamente vía `https://picsum.photos`.
* Navegación: botón "Nueva propiedad" en `_navbar.html`.
* Validaciones: campos con solo espacios se tratan como vacíos.

## Áreas donde puede existir ambigüedad

Evalúa si hace falta preguntar sobre:

1. **Campo `area`**: el modelo requiere `area > 0` pero no está en los campos
   obligatorios del formulario. ¿Se incluye como campo en el formulario o se
   define un default (ej. 0 o un valor calculado)?
2. **Campo `ciudad`**: el modelo tiene default `'Miami'`. ¿Se incluye como
   campo opcional en el formulario o se usa siempre el default?
3. **Mecanismo de envío del formulario**: ¿POST tradicional con redirect
   completo o HTMX con swap parcial y feedback inline?
4. **Política de fallback de picsum.photos**: ¿string vacío (usa placeholder
   visual del listado) o URL fija de un placeholder local vendoreado?
5. **Icono del botón "Nueva propiedad"**: ¿se vendorea un icono nuevo de
   Lucide (ej. `plus`, `plus-circle`) o se usa texto sin icono?
6. **Rango de negocio para habitaciones y banos**: ¿cuál es el máximo
   razonable? (ej. habitaciones <= 20, banos <= 20).
7. **Manejo de duplicados**: el constraint `uq_propiedades_identidad_negocio`
   (titulo + direccion + ciudad) puede fallar. ¿Se muestra error inline al
   usuario o se maneja de otra forma?
8. **Redirección post-creación**: ¿a `/propiedades` (listado) o a la página
   de detalle de la propiedad creada (si existe en spec futura)?

## Reglas

* Modo interactivo: una pregunta a la vez.
* Formato de pregunta según constitución sección VII.
* No reabras decisiones ya tomadas.
* Mantén todo en español.
* Actualiza la sección `Clarificaciones` de `spec.md` con las decisiones.

## Salida esperada

```
Clarificaciones integradas en specs/007-crear-propiedad/spec.md
Siguiente comando: /speckit.plan @.opencode/prompts/007-crear-propiedad.plan.prompt.md
```
