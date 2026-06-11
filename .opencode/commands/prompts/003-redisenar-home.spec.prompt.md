---
name: 003-redisenar-home-spec
description: >
  Crea la spec 003-redisenar-home para rediseñar la Home principal respetando
  la gobernanza visual canónica.
---

/speckit.specify

Crea una nueva spec para la feature `003-redisenar-home`.

Si el workflow de Spec Kit crea una rama Git, usa la rama
`feat/003-redisenar-home`.

Usa el workflow canónico de Spec Kit. No crees specs manualmente fuera de la ruta
resuelta por Spec Kit.

## Objetivo

Rediseñar la Home principal del proyecto Realtor respetando estrictamente la
gobernanza visual canónica del frontend.

La spec debe dejar claro que el rediseño debe cumplir con:

- `.opencode/instructions/frontend.instructions.md`
- `.specify/memory/constitution.md`
- `AGENTS.md`
- Las reglas de tokens visuales canónicos ya definidas por el proyecto.

## Alcance funcional

La spec debe incluir alcance sobre:

- Home principal.
- `index.html` o template equivalente de entrada, si existe.
- `base.html`.
- Componentes compartidos en `app/templates/components/`.
- Macros compartidas en `app/templates/macros/`, si aplica.
- `app/static/css/app.css`.
- Uso de iconografía Lucide vendoreada.
- Compatibilidad con HTMX cuando aplique.
- Estados visuales necesarios: carga, vacío, error o éxito, si corresponden.

## Gobernanza visual

La spec debe respetar la gobernanza visual vigente:

- No introducir cambios implícitos de tokens visuales.
- No cambiar colores, sombras, radios, espaciados, tipografía, breakpoints,
  layout base o patrones visuales compartidos sin autorización explícita.
- Todo cambio visual global debe tener trazabilidad en `tasks.md`.
- Todo cambio en archivos visuales protegidos debe quedar marcado de forma
  verificable según la regla definida por la spec de blindaje visual.
- Si el rediseño requiere extender tokens, componentes o patrones visuales,
  debe declararlo explícitamente como decisión de la spec.

## Reglas obligatorias

- No implementes código.
- No generes `plan.md`.
- No generes `tasks.md`.
- No modifiques archivos de aplicación.
- No cambies la constitución.
- Mantén todo en español.
- Respeta `AGENTS.md` y las instrucciones activas de `.opencode/instructions/*.instructions.md`.
- No uses Tailwind, Bootstrap, CDN, webfonts, emojis ni iconos externos.
- No introduzcas nuevas decisiones visuales sin declararlas en la spec.

## Preguntas interactivas

Si hay ambigüedad sobre alcance, diseño, componentes, contenido o impacto visual,
pregunta antes de cerrar la spec.

Como mínimo, considera si hace falta preguntar:

- Qué secciones debe tener la Home.
- Qué contenido debe mostrarse como prioridad.
- Si el rediseño puede reutilizar los componentes actuales o requiere nuevos.
- Si se permite extender tokens visuales o solo reutilizar los existentes.
- Qué comportamiento responsive debe validarse.
- Qué criterios visuales deben medirse en aceptación.
- Qué cambios requieren marcador de trazabilidad visual en `tasks.md`.

## Resultado esperado

Genera o actualiza `spec.md` para `003-redisenar-home` con:

- Objetivo claro.
- Alcance.
- User stories priorizadas.
- Criterios de aceptación medibles.
- Edge cases.
- Requisitos funcionales.
- Sección de impacto visual obligatoria.
- Relación explícita con `frontend.instructions.md`, `AGENTS.md` y la constitución.
- Reglas claras para evitar cambios visuales no autorizados.
