# Lista de verificación de calidad: Blindar tokens visuales canónicos

**Propósito**: Validar completitud y calidad de la especificación antes de proceder a planificación
**Creado**: 2026-06-10
**Feature**: [spec.md](../spec.md)

## Calidad del contenido

- [x] Sin detalles de implementación (lenguajes, frameworks, APIs)
- [x] Enfocado en valor de usuario y necesidades de negocio
- [x] Escrito para interesados no técnicos
- [x] Todas las secciones obligatorias completadas

## Completitud de requisitos

- [x] Sin marcadores [NEEDS CLARIFICATION] pendientes
- [x] Los requisitos son comprobables y no ambiguos
- [x] Los criterios de éxito son medibles
- [x] Los criterios de éxito son agnósticos a la tecnología (sin detalles de implementación)
- [x] Todos los escenarios de aceptación están definidos
- [x] Los casos límite están identificados
- [x] El alcance está claramente delimitado
- [x] Las dependencias y asunciones están identificadas

## Preparación de la feature

- [x] Todos los requisitos funcionales tienen criterios de aceptación claros
- [x] Los escenarios de usuario cubren los flujos principales
- [x] La feature cumple los resultados medibles definidos en los criterios de éxito
- [x] Sin filtraciones de detalles de implementación en la especificación

## Notas

- Spec de gobernanza visual. No modifica tokens existentes; establece reglas de
  trazabilidad, visibilidad y autorización para cambios al sistema visual
  compartido.
- 10 requisitos funcionales (FR-001 a FR-010) que definen los marcadores
  `[visual]`, `[visual][extension]`, `[visual][bugfix]`, `[visual][componente]`,
  `[visual][instrucción]` y las reglas de trazabilidad en `plan.md` y `tasks.md`.
- 6 criterios de éxito (SC-001 a SC-006) centrados en la existencia y
  funcionamiento del script `check-visual-trace.sh`.
- Tabla de definición de cambio visual global: tokens CSS, componentes
  compartidos, macros, layout base, iconografía, instrucciones visuales, HTMX.
- 6 casos límite: bugfix visual, features concurrentes, cambios locales en
  templates de módulo, modificación de `frontend.instructions.md`, scripts de
  build, nuevos componentes compartidos.
- 3 clarificaciones resueltas en sesión 2026-06-10: base del diff (`git diff
  main...HEAD`), alcance de búsqueda del marcador (solo líneas `- [ ]`/`- [X]`),
  no integración con `make check`.
- 5 asunciones: ejecución manual del script, detección basada en git diff,
  búsqueda solo en líneas de tarea, aplica a specs 003 en adelante, no modifica
  tokens existentes.
