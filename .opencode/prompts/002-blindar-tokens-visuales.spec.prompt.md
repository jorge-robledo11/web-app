---
name: 002-blindar-tokens-visuales-spec
description: >
  Crea la spec 002-blindar-tokens-visuales para blindar los tokens visuales
  canónicos del frontend.
spec_kit_command: "/speckit.specify"
usage: "/speckit.specify @.opencode/prompts/002-blindar-tokens-visuales.spec.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

Crea una nueva spec para la feature `002-blindar-tokens-visuales`.

Usa el workflow canónico de Spec Kit. No crees specs manualmente fuera de la ruta
resuelta por Spec Kit.

## Objetivo

Blindar los tokens visuales canónicos del frontend para evitar que futuras specs
cambien colores, sombras, radios, espaciados, tipografía, layout base o reglas
visuales compartidas sin autorización explícita.

La spec debe dejar claro que:

- `.opencode/instructions/frontend.instructions.md` es la fuente operativa para
  los tokens visuales, componentes compartidos, estructura de templates, CSS,
  iconografía y patrones HTMX.
- `.specify/memory/constitution.md` contiene la regla global de trazabilidad.
- Cualquier cambio futuro en tokens visuales debe quedar justificado y trazado
  explícitamente en `tasks.md`.
- Ninguna feature futura puede modificar tokens visuales por accidente como
  efecto colateral de implementar una pantalla, componente o flujo.

## Alcance funcional

La spec debe definir reglas verificables para:

1. Proteger los tokens visuales canónicos existentes.
2. Evitar cambios no autorizados en:
   - Colores.
   - Sombras.
   - Radios.
   - Espaciados.
   - Tipografía.
   - Breakpoints.
   - Layout base.
   - Componentes compartidos.
   - Macros de iconos.
   - Patrones visuales de estados.
3. Exigir trazabilidad cuando una tarea toque tokens visuales.
4. Distinguir entre:
   - Cambios visuales permitidos para una feature concreta;
   - Cambios visuales globales que requieren autorización explícita.
5. Definir criterios de aceptación para detectar cambios visuales no trazados.

## Reglas obligatorias

- No implementes código.
- No generes `plan.md`.
- No generes `tasks.md`.
- No modifiques archivos de aplicación.
- No cambies la constitución.
- Mantén todo en español.
- Respeta `AGENTS.md` y las instrucciones activas de `.opencode/instructions/*.instructions.md`.
- No uses Tailwind, Bootstrap, CDN, webfonts, emojis ni iconos externos.
- No introduzcas nuevas decisiones visuales sin declararlas como pregunta o
  criterio explícito.

## Preguntas interactivas

Si hay ambigüedad sobre el nivel de bloqueo visual, pregunta antes de cerrar la
spec.

Como mínimo, considera si hace falta preguntar:

- Si los tokens deben quedar completamente congelados.
- Si se permiten extensiones controladas.
- Si se requiere checklist visual en futuras tasks.
- Si se debe crear una prueba o auditoría específica para cambios de tokens.

## Resultado esperado

Genera o actualiza `spec.md` para `002-blindar-tokens-visuales` con:

- Objetivo claro.
- Alcance.
- User stories.
- Criterios de aceptación verificables.
- Edge cases.
- Requisitos funcionales.
- Definición de qué cuenta como cambio visual global.
- Regla de trazabilidad obligatoria en `tasks.md`.
- Relación explícita con `frontend.instructions.md` y la constitución.