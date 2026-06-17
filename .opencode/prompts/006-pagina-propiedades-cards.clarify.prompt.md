---
name: 006-pagina-propiedades-cards-clarify
description: >
  Clarifica ambigüedades de la spec 006-pagina-propiedades-cards antes del plan.
spec_kit_command: "/speckit.clarify"
usage: "/speckit.clarify @.opencode/prompts/006-pagina-propiedades-cards.clarify.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

## Prompt para `speckit.clarify`

Ejecuta clarificación interactiva sobre `specs/006-pagina-propiedades-cards/spec.md`.

## Decisiones ya tomadas

Las siguientes decisiones están cerradas y no deben reabrirse:

* Componente de card: extender `_card_propiedad.html` existente.
* Imagen placeholder: fondo `--color-surface` + icono `building-2` existente.
* Formato de precio: `$1,500.00` con símbolo y dos decimales.
* Arquitectura: extender `propiedades/routes.py` placeholder.
* Template: `app/modules/propiedades/templates/propiedades.html`.

## Áreas donde puede existir ambigüedad

Evalúa si hace falta preguntar sobre:

1. **Ordenamiento de propiedades**: si el orden por defecto del repositorio
   (`created_at` descendente) es suficiente o se requiere otro criterio.
2. **Comportamiento de imagen rota**: si una URL de imagen retorna 404 en
   runtime, ¿se muestra placeholder igual que cuando no hay imagen?
3. **Interacción con la card**: si cada card debe ser cliqueable para navegar
   a un detalle futuro, o son solo informativas en esta spec.
4. **Estilo visual de la card**: si hay un diseño visual específico esperado
   (imagen arriba, datos abajo, badge superpuesto, etc.) o se deja a criterio
   de implementación respetando tokens.
5. **Cantidad de campos en card**: si los 8 campos son obligatorios o algunos
   pueden omitirse en ciertos breakpoints (ej. ocultar área en móvil).

## Reglas

* Modo interactivo: una pregunta a la vez.
* Formato de pregunta según constitución sección VII.
* No reabras decisiones ya tomadas.
* Mantén todo en español.
* Actualiza la sección `Clarificaciones` de `spec.md` con las decisiones.

## Salida esperada

```
Clarificaciones integradas en specs/006-pagina-propiedades-cards/spec.md
Siguiente comando: /speckit.plan @.opencode/prompts/006-pagina-propiedades-cards.plan.prompt.md
```
