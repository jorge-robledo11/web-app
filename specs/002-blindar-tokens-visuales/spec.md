# Feature Specification: Blindar tokens visuales canónicos del frontend

**Feature Branch**: `002-blindar-tokens-visuales`

**Created**: 2026-06-10

**Status**: Draft

**Input**: /speckit.specify 002-blindar-tokens-visuales

## Objetivo

Proteger los tokens visuales canónicos del sistema Realtor para que ninguna
feature futura pueda modificarlos accidentalmente como efecto colateral de su
implementación. Esta spec es una capa de gobernanza visual que establece reglas
de trazabilidad, visibilidad y autorización sobre los cambios que afecten al
sistema visual compartido.

## Relación con artefactos existentes

- **`.opencode/instructions/frontend.instructions.md`**: fuente operativa de los
  tokens visuales (colores, sombras, radios, espaciados, tipografía, breakpoints,
  layout base), componentes compartidos, estructura de templates, iconografía y
  patrones HTMX. Cualquier cambio en tokens debe ser consistente con este
  documento.
- **`.specify/memory/constitution.md`**: regla global de trazabilidad (sección
  XII, v1.2.0). Toda desviación de tokens visuales debe cumplir con
  `Complexity Tracking` según la sección XV de la constitución.

## User Scenarios & Testing

### User Story 1 — Auditor detecta cambio visual no trazado (Priority: P1)

Como revisor de una spec o pull request, necesito poder detectar que una tarea
modifica tokens visuales compartidos sin declararlo explícitamente, para evitar
cambios accidentales en el sistema visual.

**Why this priority**: Sin detección, los tokens se erosionan con cada feature.
Un cambio de sombra, color o breakpoint que parezca inofensivo puede romper la
consistencia visual de toda la aplicación.

**Independent Test**: Revisar el diff de una feature que toca `app.css` o un
componente compartido; verificar que `tasks.md` de esa feature contiene al menos
una tarea con marcador visual explícito si se modificó algún token.

**Acceptance Scenarios**:

1. **Given** una feature modifica `app/static/css/app.css` en una sección de
   tokens (`:root`, variables), **When** se revisa su `tasks.md`, **Then** debe
   existir al menos una tarea que describa el cambio visual y lo justifique.
2. **Given** una feature modifica un componente en `app/templates/components/`,
   **When** ese cambio altera clases CSS que afectan tokens globales, **Then**
   la tarea debe estar marcada con el prefijo `[visual]`.
3. **Given** una feature solo agrega estilos scoped a su propio módulo sin tocar
   tokens globales ni componentes compartidos, **When** se revisa, **Then** no
   requiere marcado visual en sus tareas.

---

### User Story 2 — Feature necesita un nuevo token visual (Priority: P2)

Como desarrollador de una feature, necesito poder extender los tokens visuales
con un nuevo valor (por ejemplo, un color de acento secundario) sin modificar los
tokens existentes, siguiendo un proceso claro y trazable.

**Why this priority**: El sistema visual debe poder crecer. Prohibir toda
extensión genera frustración y workarounds. La clave es que las extensiones sean
explícitas, compatibles hacia atrás y trazables.

**Independent Test**: Agregar un nuevo token `--color-accent-secondary: #XXXXXX`
en `:root` de `app.css`; verificar que la tarea en `tasks.md` lo declara como
extensión y no modifica ningún token existente.

**Acceptance Scenarios**:

1. **Given** una feature necesita un nuevo color que no existe en los tokens
   canónicos, **When** se agrega como nueva variable en `:root` sin modificar
   variables existentes, **Then** se permite con una tarea marcada
   `[visual][extension]` en `tasks.md`.
2. **Given** una feature modifica el valor de un token existente (ej. cambia
   `--color-accent` de `#2563eb` a `#7c3aed`), **When** se revisa el cambio,
   **Then** DEBE estar justificado en `plan.md` bajo `Complexity Tracking` y
   aprobado explícitamente.

---

### User Story 3 — CI o pre-commit detecta regresión visual no declarada (Priority: P3)

Como mantenedor del proyecto, necesito que una verificación automática (script o
hook) alerte cuando un cambio toca archivos visuales sensibles sin el marcador
correspondiente en `tasks.md`.

**Why this priority**: La verificación manual no escala. Un mecanismo automático
reduce la carga del revisor y previene regresiones silenciosas.

**Independent Test**: Ejecutar el script `scripts/check-visual-trace.sh` sobre
la feature actual; si hay cambios en `app.css` o componentes compartidos sin
tareas `[visual]` en `tasks.md`, el script falla con código distinto de cero.

**Acceptance Scenarios**:

1. **Given** el script `scripts/check-visual-trace.sh` existe, **When** se
   ejecuta en una feature que modificó `app.css` sin tareas `[visual]`, **Then**
   el script retorna código de salida 1 con un mensaje descriptivo.
2. **Given** el script existe, **When** se ejecuta en una feature que no tocó
   archivos visuales, **Then** retorna código de salida 0.

---

### Edge Cases

- ¿Qué sucede si una feature necesita corregir un bug visual (ej. un color que
  no cumple contraste AA)? Se permite con tarea `[visual][bugfix]` y
  justificación en `plan.md`.
- ¿Qué sucede si dos features concurrentes necesitan modificar el mismo token?
  La segunda en merge debe resolver el conflicto y ambas deben tener trazabilidad
  `[visual]`.
- ¿Qué sucede si el cambio visual es solo en un template de módulo sin tocar
  `app.css` ni componentes compartidos? No requiere marcado `[visual]`.
- ¿Qué sucede si se modifica `frontend.instructions.md`? Requiere tarea
  `[visual][instrucción]` y actualización de esta spec si el cambio es material.
- ¿Qué sucede si un script de build minifica `app.css`? Los scripts de build no
  son cambios de fuente; no requieren trazabilidad.
- ¿Qué sucede si se agrega un nuevo componente en `app/templates/components/`?
  Requiere tarea `[visual][componente]` porque amplía el conjunto compartido.

## Requirements

### Functional Requirements

- **FR-001**: Toda tarea que modifique `app/static/css/app.css` en secciones de
  tokens (`:root`, variables, tipografía, layout, responsive) DEBE incluir el
  marcador `[visual]` en `tasks.md`.
- **FR-002**: Toda tarea que modifique un componente en
  `app/templates/components/` DEBE incluir el marcador `[visual]` en `tasks.md`.
- **FR-003**: Toda modificación del valor de un token existente (no adición de
  uno nuevo) DEBE registrarse en `Complexity Tracking` de `plan.md` con
  justificación.
- **FR-004**: La adición de nuevos tokens visuales (variables CSS, componentes,
  breakpoints) sin modificar los existentes se permite con marcador
  `[visual][extension]`.
- **FR-005**: Correcciones de bugs visuales (contraste, accesibilidad, regresión)
  se permiten con marcador `[visual][bugfix]` y justificación en `plan.md`.
- **FR-006**: Las instrucciones visuales canónicas residen en
  `.opencode/instructions/frontend.instructions.md`. Cualquier cambio en ese
  archivo requiere marcador `[visual][instrucción]`.
- **FR-007**: La constitución (`.specify/memory/constitution.md`, sección XII
  v1.2.0) es la regla global de trazabilidad. Toda desviación de tokens visuales
  debe cumplir con `Complexity Tracking` según la sección XV de la constitución.
- **FR-008**: El script `scripts/check-visual-trace.sh` DEBE verificar que los
  cambios en archivos visuales sensibles tienen tareas `[visual]` asociadas en
  `tasks.md`.
- **FR-009**: El script `scripts/check-visual-trace.sh` DEBE ser ejecutable y
  usar `set -euo pipefail`.
- **FR-010**: Los marcadores `[visual]`, `[visual][extension]`,
  `[visual][bugfix]`, `[visual][componente]` y `[visual][instrucción]` son los
  únicos prefijos válidos para trazabilidad visual en `tasks.md`.

### Definición de cambio visual global

Un cambio se considera **global** (requiere trazabilidad `[visual]`) cuando
afecta:

| Categoría | Archivos afectados | Marcador requerido |
|---|---|---|
| Tokens CSS | `app/static/css/app.css` (secciones `:root`, variables, tipografía, layout, responsive) | `[visual]` |
| Componentes compartidos | `app/templates/components/_*.html` | `[visual]` o `[visual][componente]` |
| Macros | `app/templates/macros/*.html` | `[visual]` |
| Layout base | `app/templates/base.html` | `[visual]` |
| Iconografía | `app/static/icons/` (agregar/quitar iconos) | `[visual]` |
| Instrucciones visuales | `.opencode/instructions/frontend.instructions.md` | `[visual][instrucción]` |
| HTMX vendoreado | `app/static/vendor/htmx.min.js` (cambio de versión) | `[visual]` |

Un cambio es **local** (no requiere `[visual]`) cuando solo afecta:

- Templates dentro de `app/modules/<feature>/templates/`.
- CSS inline o scoped que no modifica tokens `:root`.
- Lógica de endpoints que renderizan templates (sin cambiar el HTML/CSS).

### Key Entities

- **Token visual canónico**: Variable CSS en `:root` de `app.css` o regla visual
  en `frontend.instructions.md` que define colores, sombras, radios, espaciados,
  tipografía, breakpoints o layout base.
- **Componente compartido**: Parcial Jinja2 en `app/templates/components/` que es
  reutilizado por múltiples módulos.
- **Marcador visual**: Prefijo `[visual]` en una tarea de `tasks.md` que indica
  que la tarea toca el sistema visual compartido.
- **Extensión visual**: Adición de un nuevo token o componente sin modificar los
  existentes, trazada con `[visual][extension]`.

## Success Criteria

### Measurable Outcomes

- **SC-001**: `scripts/check-visual-trace.sh` existe y tiene permisos de
  ejecución.
- **SC-002**: El script retorna 0 cuando se ejecuta en una feature sin cambios
  visuales.
- **SC-003**: El script retorna 1 cuando hay cambios en `app.css` o componentes
  compartidos sin tareas `[visual]` en `tasks.md`.
- **SC-004**: Toda tarea futura que modifique `app.css` en secciones de tokens
  incluye `[visual]` en su descripción.
- **SC-005**: `frontend.instructions.md` permanece como la única fuente de verdad
  operativa para tokens visuales.
- **SC-006**: Ninguna feature fusionada en `main` modifica tokens canónicos sin
  trazabilidad en `plan.md` y `tasks.md`.

## Assumptions

- El script `check-visual-trace.sh` se ejecuta manualmente. No está integrado en
  `make check`. No se asume integración CI automatizada en este momento.
- La detección de cambios se basa en `git diff main...HEAD` (triple dot: solo
  cambios únicos de la feature desde la bifurcación de `main`).
- Los marcadores `[visual]` se buscan solo en líneas de tarea
  (`- [ ]` / `- [X]`) de `tasks.md`, no en comentarios ni notas.
- Esta spec no modifica tokens existentes; solo establece reglas de gobernanza.
- Las reglas aplican a partir de la spec `003` en adelante. La spec `001` y
  `002` son fundacionales y establecen la base.

## Clarificaciones

Resoluciones de `/speckit.clarify` del 2026-06-10.

### Base del diff para el script

El script `check-visual-trace.sh` usa `git diff main...HEAD` (triple dot) para
detectar cambios. Esto muestra solo los commits exclusivos de la feature desde
que bifurcó de `main`, excluyendo cambios en `main` que no están en la feature.

### Alcance de búsqueda del marcador [visual]

El script busca el marcador `[visual]` exclusivamente en líneas de tarea de
`tasks.md`, es decir, líneas que comienzan con `- [ ]` o `- [X]`. No busca en
comentarios, notas, ejemplos ni texto narrativo del archivo.

### Integración con make check

`check-visual-trace.sh` no se integra en `make check`. Se ejecuta manualmente
cuando el revisor o desarrollador necesita auditar la trazabilidad visual de una
feature. Esto evita falsos fallos en `make check` cuando una feature está en fase
temprana sin `tasks.md` completo.
