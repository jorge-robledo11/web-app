# Feature Specification: Rediseñar Home principal

**Feature Branch**: `feat/003-redisenar-home`

**Created**: 2026-06-10

**Status**: Draft

**Input**: /speckit.specify 003-redisenar-home

## Objetivo

Rediseñar la Home principal del proyecto Realtor (`GET /`) para mejorar la
jerarquía visual, la organización del contenido y la experiencia de navegación
inicial, respetando estrictamente la gobernanza visual canónica definida en la
constitución (sección XII), `.opencode/instructions/frontend.instructions.md` y
la spec `002-blindar-tokens-visuales`.

El rediseño parte de la base existente (`dashboard.html`, `base.html`, 8
componentes compartidos, 13 iconos Lucide, `app.css`) y la evoluciona sin
romperla.

## Relación con artefactos existentes

- **`.opencode/instructions/frontend.instructions.md`**: fuente operativa de
  tokens visuales, componentes, layout, iconografía y patrones HTMX. El rediseño
  debe ser compatible con todas las reglas de este documento.
- **`.specify/memory/constitution.md`**: sección XII (blindaje visual) y sección
  XV (Complexity Tracking). Todo cambio en tokens canónicos o componentes
  compartidos requiere trazabilidad `[visual]` en `tasks.md`.
- **`specs/002-blindar-tokens-visuales/spec.md`**: reglas de gobernanza visual
  vigentes. El script `check-visual-trace.sh` auditará la trazabilidad de esta
  feature.
- **`AGENTS.md`**: reglas generales del proyecto (idioma español, stack
  obligatorio, arquitectura Vertical Slice, TDD).

## User Scenarios & Testing

### User Story 1 — Ver métricas clave del negocio al abrir la app (Priority: P1)

Como usuario del sistema Realtor, necesito ver los indicadores principales del
negocio inmobiliario apenas cargo la Home, con valores claros, iconos
representativos y tendencias visibles, para entender el estado general sin
navegar a ninguna sección.

**Why this priority**: Es la función principal de la Home. Sin métricas visibles
y comprensibles, la página de inicio no aporta valor. Es el primer punto de
contacto del usuario con el sistema.

**Independent Test**: Cargar `GET /` y verificar que se renderizan tarjetas de
métrica con valor numérico, etiqueta descriptiva, icono y tendencia (si aplica).
Puede probarse sin accesos rápidos ni otras secciones; entrega valor por sí sola.

**Acceptance Scenarios**:

1. **Given** que el sistema tiene datos disponibles, **When** el usuario carga la
   Home, **Then** ve al menos 3 tarjetas de métrica con valor numérico grande,
   etiqueta descriptiva, icono Lucide y tendencia (porcentaje y dirección) cuando
   el dato lo soporte.
2. **Given** que los datos están en proceso de carga, **When** el usuario abre la
   Home, **Then** ve un indicador visual de carga (spinner o skeleton) en cada
   tarjeta de métrica mientras los datos no están disponibles. En esta spec, los
   estados de carga se implementan como clases CSS (`.is-loading`) y estructura de
   template, verificables manualmente; no requieren endpoints HTMX asíncronos.
3. **Given** que ocurre un error al obtener las métricas, **When** el usuario
   carga la Home, **Then** ve un mensaje de error descriptivo en la sección de
   métricas, no un error genérico ni una página en blanco. Igual que el estado de
   carga, el estado de error se implementa como clase CSS (`.is-error`) y
   estructura de template, verificable manualmente sin endpoints asíncronos.
4. **Given** que no hay datos para una métrica (valor cero o nulo), **When** se
   renderiza la Home, **Then** la tarjeta muestra el valor «0» o «—» con la
   etiqueta correspondiente, sin ocultar la tarjeta.

---

### User Story 2 — Navegar rápido a los módulos principales (Priority: P2)

Como usuario del sistema, necesito acceder a los módulos principales
(Propiedades, Inquilinos, Contratos, Pagos, Mantenimiento) desde la Home con un
solo clic, mediante accesos rápidos visualmente claros y organizados, para
reducir la fricción de navegación.

**Why this priority**: Los accesos rápidos son el segundo elemento más importante
de la Home. Guían al usuario hacia las secciones de trabajo. Sin ellos, el
usuario depende exclusivamente de la sidebar para navegar.

**Independent Test**: Cargar `GET /` y verificar que existe una sección de
accesos rápidos con tarjetas cliqueables. Cada tarjeta muestra un icono Lucide,
un título y una URL de destino. Puede probarse sin las métricas; entrega valor
de navegación por sí sola.

**Acceptance Scenarios**:

1. **Given** que la Home está cargada, **When** el usuario observa la sección de
   accesos rápidos, **Then** ve al menos 4 tarjetas (Propiedades, Inquilinos,
   Contratos, Pagos), cada una con icono Lucide, título y URL funcional.
2. **Given** que el usuario hace clic en una tarjeta de acceso rápido, **When** la
   URL de destino existe, **Then** es navegado a esa sección. Si la URL no existe
   aún, la tarjeta usa `#` como placeholder sin generar error visual.
3. **Given** que la pantalla es menor a 768px, **When** se renderizan los accesos
   rápidos, **Then** las tarjetas se reorganizan en 2 columnas sin desbordamiento
   ni scroll horizontal.

---

### User Story 3 — Ver resumen de actividad reciente del portafolio (Priority: P3)

Como usuario del sistema, necesito ver un resumen de la actividad reciente del
portafolio inmobiliario (últimas propiedades registradas, contratos próximos a
vencer o pagos recientes) directamente en la Home, para tener contexto sin
navegar a cada módulo.

**Why this priority**: Agrega profundidad a la Home y reduce la necesidad de
navegar para tareas de consulta rápida. No es crítico para el funcionamiento
básico, pero mejora significativamente la experiencia.

**Independent Test**: Cargar `GET /` y verificar que existe una sección de
actividad reciente debajo de accesos rápidos, con al menos 3 ítems. Cada ítem
muestra un resumen relevante (título, fecha, estado). Puede probarse sin
métricas ni accesos rápidos.

**Acceptance Scenarios**:

1. **Given** que existen registros en el sistema, **When** el usuario carga la
   Home, **Then** ve una lista de al menos 3 ítems de actividad reciente con
   fecha, descripción corta y badge de estado.
2. **Given** que no existen registros en el sistema (estado vacío), **When** el
   usuario carga la Home, **Then** ve un mensaje descriptivo tipo «Aún no hay
   actividad registrada» con icono, sin errores ni secciones colapsadas.
3. **Given** que ocurre un error al obtener la actividad reciente, **When** el
   usuario carga la Home, **Then** la sección muestra un mensaje de error
   específico («No se pudo cargar la actividad reciente»), sin afectar al resto
   de secciones de la Home.
4. **Given** que la sección combina múltiples tipos de actividad (últimas
   propiedades, contratos próximos a vencer y últimos pagos), **When** se renderiza
   la sección, **Then** cada ítem muestra su tipo (propiedad, contrato o pago)
   mediante un badge o etiqueta visual, con la descripción y fecha
   correspondientes, y los ítems de contratos próximos a vencer destacan
   visualmente con badge warning/danger según urgencia.

---

### Edge Cases

- ¿Qué sucede si todas las métricas fallan al cargar? Cada tarjeta muestra su
  propio estado de error; no se colapsa la sección completa.
- ¿Qué sucede si un acceso rápido apunta a una URL que aún no existe? La tarjeta
  se renderiza con `href="#"` y se muestra igual visualmente, sin error.
- ¿Qué sucede en pantallas menores a 1023px (tablet)? La sidebar se oculta con
  toggle; el contenido principal ocupa el ancho completo; las métricas se
  reorganizan en 2 columnas.
- ¿Qué sucede en pantallas menores a 768px (móvil)? Las métricas se reorganizan en
  1 columna; los accesos rápidos en 2 columnas; los espaciados se reducen a
  `--space-4`.
- ¿Qué sucede si la Home se carga sin JavaScript (HTMX no disponible)? Las
  secciones estáticas se renderizan normalmente desde el servidor. Las
  interacciones HTMX (si las hubiera) degradan gracefulmente.
- ¿Qué sucede si se agrega una nueva métrica en el futuro? La grilla de métricas
  debe adaptarse automáticamente (CSS grid con `auto-fill` o `auto-fit`) sin
  requerir cambios de layout.
- ¿Qué sucede si una tendencia es negativa? Se muestra en color
  `--color-danger` con flecha hacia abajo. Si es positiva, en `--color-success`
  con flecha hacia arriba. Si es neutra, sin flecha en `--color-text-muted`.
- ¿Qué sucede con el scroll en móvil cuando hay muchas secciones? El layout es
  scrollable verticalmente; la navbar permanece sticky en el top.

## Requirements

### Functional Requirements

- **FR-001**: La Home DEBE renderizar 3 tarjetas de métrica con valor
  numérico, etiqueta, icono Lucide y tendencia (dirección y porcentaje):
  Propiedades activas (`building-2`), Inquilinos al día (`users`), Contratos
  vigentes (`file-text`).
- **FR-002**: Cada tarjeta de métrica DEBE tener un estado de carga visible
  (spinner o skeleton) implementado como clase CSS (`.is-loading`) y estructura
  de template. No requiere endpoint HTMX asíncrono en esta spec; los datos se
  sirven hardcodeados desde `GET /`.
- **FR-003**: Cada tarjeta de métrica DEBE tener un estado de error visible
  implementado como clase CSS (`.is-error`) y estructura de template.
  Verificable manualmente; los endpoints de fragmento HTMX para carga asíncrona
  real se difieren a specs futuras.
- **FR-004**: La Home DEBE incluir una sección de accesos rápidos con al menos 4
  tarjetas cliqueables (Propiedades, Inquilinos, Contratos, Pagos), cada una con
  icono Lucide, título y URL.
- **FR-005**: La Home DEBE incluir una sección de actividad reciente con al
  menos 3 ítems, cada uno con fecha, descripción y badge de estado.
- **FR-006**: La sección de actividad reciente DEBE tener un estado vacío visible
  (icono + mensaje) cuando no haya registros.
- **FR-007**: La sección de actividad reciente DEBE tener un estado de error
  visible cuando falle la obtención de datos.
- **FR-008**: El layout DEBE adaptarse responsive a los breakpoints definidos:
  1023px (tablet, sidebar overlay) y 768px (móvil, 1 columna métricas, 2
  columnas accesos).
- **FR-009**: Todos los valores visuales (colores, espaciados, sombras, radios,
  tipografía) DEBEN consumirse exclusivamente desde los tokens CSS definidos en
  `:root` de `app/static/css/app.css`.
- **FR-010**: Los iconos DEBEN renderizarse con la macro `icon()` de
  `app/templates/macros/icons.html` usando SVGs Lucide vendoreados en
  `app/static/icons/`.
- **FR-011**: Cualquier modificación a tokens visuales canónicos, componentes
  compartidos, `base.html` o `app.css` en secciones de tokens DEBE tener
  trazabilidad con marcador `[visual]` en `tasks.md`.
- **FR-012**: La extensión de nuevos tokens visuales (sin modificar existentes)
  DEBE declararse con marcador `[visual][extension]` en `tasks.md`.
- **FR-013**: La Home DEBE extender `base.html` y respetar su estructura de
  layout (sidebar + navbar + flash-zone + content).
- **FR-014**: Las interacciones que usen HTMX DEBEN usar HTMX vendoreado en
  `app/static/vendor/htmx.min.js`. No se permite cargar HTMX ni ningún JS de
  terceros desde CDN.
- **FR-015**: El CSS nuevo o modificado DEBE residir en `app/static/css/app.css`
  respetando sus 7 secciones existentes (Reset, Variables, Tipografía, Layout,
  Componentes, Utilidades, Responsive). No se permite crear nuevos archivos CSS.
- **FR-016**: Las 3 secciones DEBEN renderizarse en orden vertical fijo: Métricas
  primero, Accesos rápidos segundo, Actividad reciente tercero.

### Key Entities

- **Sección de Home**: Bloque visual autónomo dentro de la Home (métricas,
  accesos rápidos, actividad reciente). Cada sección tiene su propio estado
  (carga, éxito, vacío, error) y es independiente de las demás.
- **Tarjeta de métrica**: Componente que muestra un KPI numérico con etiqueta,
  icono Lucide y tendencia opcional (dirección y porcentaje). Reutiliza y
  extiende el componente `_tarjeta_metrica.html` existente.
- **Acceso rápido**: Tarjeta cliqueable con icono, título y URL que dirige al
  usuario a un módulo del sistema. Reutiliza el componente `_accesos_rapidos.html`
  existente.
- **Ítem de actividad**: Registro individual en la sección de actividad reciente
  que muestra fecha, descripción y badge de estado. Se implementa con el nuevo
  componente compartido `_actividad_item.html`.

## Success Criteria

### Measurable Outcomes

- **SC-001**: La Home renderiza 3 secciones visualmente distintas en orden
  Métricas → Accesos rápidos → Actividad reciente, en desktop sin scroll
  horizontal.
- **SC-002**: Las 3 secciones muestran estados de carga, éxito, vacío y error
  según corresponda, verificables aislando cada sección.
- **SC-003**: En viewport de 360px de ancho (móvil pequeño), todas las secciones
  son legibles sin overflow horizontal.
- **SC-004**: En viewport de 768px (tablet), las métricas se reorganizan en 2
  columnas y los accesos rápidos en 2 columnas.
- **SC-005**: En viewport de 1024px (desktop), las métricas se muestran en 3
  columnas y los accesos rápidos en 4 columnas.
- **SC-006**: El 100% de los colores, espaciados, sombras, radios y fuentes
  usados en la Home provienen de tokens CSS definidos en `:root` de `app.css`.
- **SC-007**: Ningún token visual canónico existente es modificado sin
  autorización explícita, trazabilidad `[visual]` en `tasks.md` y registro en
  `Complexity Tracking` de `plan.md`.
- **SC-008**: `make visual-check` pasa (exit 0) al finalizar la implementación,
  confirmando que todos los cambios visuales tienen trazabilidad.
- **SC-009**: `ruff check` y `ruff format --check` pasan sin errores en todo el
  código Python modificado.
- **SC-010**: Los tests de la Home verifican al menos: renderizado exitoso (200),
  presencia de las 3 secciones, estados de carga y error para métricas, y estado
  vacío para actividad reciente.

## Clarificaciones

### Session 2026-06-10

- Q: ¿Los estados de carga y error deben implementarse con endpoints HTMX asíncronos reales o como preparación visual server-rendered? → A: Server-rendered con CSS preparado. La Home se renderiza con datos hardcodeados desde `GET /`. Los estados de carga/error se implementan como estructura de template y clases CSS (`.is-loading`, `.is-error`), verificables vía manipulación manual en tests, sin nuevos endpoints HTMX asíncronos. Los endpoints de fragmento se implementarán en specs futuras cuando los datos sean reales.
- Q: ¿Se puede crear un nuevo componente compartido para los ítems de actividad o debe reutilizarse `_card_propiedad.html`? → A: Se crea el nuevo componente `_actividad_item.html` en `app/templates/components/` con props específicos (tipo, descripción, fecha, badge). No se modifica `_card_propiedad.html`. Requiere marcador `[visual][componente]` en tasks.md.
- Q: ¿Qué métricas específicas debe mostrar la Home? → A: Las 3 métricas actuales: Propiedades activas (icono `building-2`), Inquilinos al día (icono `users`), Contratos vigentes (icono `file-text`). Se agregan tendencias (dirección y porcentaje) a cada una.
- Q: ¿Se modifica `base.html` o solo `dashboard.html`? → A: No se modifica `base.html`, `_sidebar.html` ni `_navbar.html`. Todo el rediseño cabe dentro del bloque `{% block content %}` de `dashboard.html`. Sidebar, navbar y layout base quedan intactos.
- Q: ¿Orden vertical explícito de las 3 secciones? → A: Métricas → Accesos rápidos → Actividad reciente (orden por prioridad: P1, P2, P3).

## Impacto visual

- [ ] Esta feature NO modifica tokens visuales canónicos ni componentes compartidos (sin impacto visual).
- [x] Esta feature SÍ modifica tokens visuales canónicos o componentes compartidos (requiere marcador `[visual]` en tasks.md).

**Archivos y componentes afectados**:

| Archivo | Tipo de cambio | Marcador requerido |
|---|---|---|
| `app/static/css/app.css` | Nuevos estilos para sección de actividad reciente, estados de carga/vacío/error, mejoras responsive | `[visual]` |
| `app/templates/base.html` | No se modifica (rediseño solo afecta `dashboard.html`) | — |
| `app/templates/dashboard.html` | Reorganización completa del contenido en 3 secciones | `[visual]` |
| `app/templates/components/_tarjeta_metrica.html` | Extensión para soportar tendencia, estado de carga y estado de error | `[visual][extension]` |
| `app/templates/components/_accesos_rapidos.html` | Mejora visual (espaciado, jerarquía, iconos más prominentes) | `[visual]` |
| `app/templates/components/_alerta.html` | Posible reutilización para estados de error inline en secciones | Sin cambios (reutilización) |
| `app/templates/components/_badge_estado.html` | Posible reutilización para items de actividad | Sin cambios (reutilización) |
| `app/templates/components/_card_propiedad.html` | No se modifica | — |
| `app/templates/components/_actividad_item.html` | Nuevo componente para ítems de actividad reciente | `[visual][componente]` |
| `app/templates/macros/icons.html` | Sin cambios previsibles | — |
| `app/static/icons/` | Posibles nuevos iconos Lucide para actividad reciente | `[visual][extension]` |

**Justificación**: El rediseño de la Home es inherentemente un cambio visual
global. Afecta la página principal, componentes compartidos existentes y el CSS
base. Todos los cambios se declaran explícitamente y se trazarán con marcadores
`[visual]` en `tasks.md`.

**Tokens existentes que NO se modificarán**:
- Colores (`--color-bg`, `--color-surface`, `--color-text`, `--color-text-muted`,
  `--color-border`, `--color-accent`, `--color-success`, `--color-warning`,
  `--color-danger`, `--color-info`)
- Sombras (`--shadow-sm`, `--shadow-md`, `--shadow-lg`)
- Radios (`--radius-sm`, `--radius-md`, `--radius-lg`)
- Espaciados (`--space-1` a `--space-12`)
- Tipografía (`--font-sans`, `--font-size-base`, `--line-height-base`)
- Breakpoints (1024px, 768px)
- Layout base (sidebar 260px + main 1fr, navbar 56px sticky)

## Assumptions

- La Home se sirve desde el endpoint `GET /` con datos hardcodeados vía
  server-rendering tradicional (Jinja2). Los endpoints de fragmento HTMX para
  carga asíncrona real se implementarán en specs futuras cuando existan los
  módulos de dominio con datos reales. Los estados de carga y error se diseñan
  como preparación estructural (CSS + template) lista para activarse en ese
  momento.
- Los componentes existentes (`_tarjeta_metrica.html`, `_accesos_rapidos.html`,
  `_badge_estado.html`, `_alerta.html`, `_card_propiedad.html`) se reutilizan
  como base. Solo se extienden si el rediseño requiere atributos adicionales que
  no pueden lograrse con los props actuales.
- La sidebar (`_sidebar.html`) y la navbar (`_navbar.html`) mantienen su
  estructura y contenido actual. El rediseño se enfoca en el área de contenido
  principal (`.content` dentro de `base.html`).
- El `#flash-zone` de `base.html` se mantiene para mensajes flash globales. Las
  secciones individuales manejan sus propios estados inline, no vía flash-zone.
- Los iconos Lucide nuevos que requiera la sección de actividad reciente (ej.
  `clock`, `calendar`) se agregan como archivos SVG
  individuales en `app/static/icons/`.
- El rediseño no introduce dependencias nuevas de CSS, JS ni templates externos.
- La especificación sigue el flujo canónico de Spec Kit y las reglas de la
  constitución del proyecto.
