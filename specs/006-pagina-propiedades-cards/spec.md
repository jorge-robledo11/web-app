# Feature Specification: Página de propiedades con cards

**Feature Branch**: `006-pagina-propiedades-cards`

**Created**: 2026-06-16

**Status**: Draft

**Input**: Crear una página server-rendered de propiedades que liste todas las
propiedades persistidas en formato de cards responsive, con endpoint dedicado y
navegación lateral corregida.

## Escenarios de usuario y pruebas

### User Story 1 — Ver listado de propiedades en grid de cards (Priority: P1)

Como usuario del sistema inmobiliario, quiero navegar a una página que muestre
todas las propiedades registradas en formato de cards para explorar el inventario
completo.

**Why this priority**: Es la funcionalidad central de la feature. Sin esta vista,
el enlace "Propiedades" del menú lateral no tiene destino útil.

**Independent Test**: Insertar propiedades en base de datos, solicitar
`GET /propiedades` y verificar que el HTML renderiza una card por cada propiedad
con todos los campos visibles requeridos.

**Acceptance Scenarios**:

1. **Given** 5 propiedades persistidas, **When** se solicita `GET /propiedades`,
   **Then** la página muestra exactamente 5 cards.
2. **Given** una propiedad con todos los campos completos, **When** se renderiza
   su card, **Then** muestra imagen, título, dirección, habitaciones, baños,
   área, precio y estado.
3. **Given** una propiedad sin imagen, **When** se renderiza su card, **Then**
   muestra un placeholder visual en lugar de la imagen, sin romper el layout.

---

### User Story 2 — Navegar a propiedades desde el menú lateral (Priority: P1)

Como usuario del sistema, quiero que el enlace "Propiedades" del sidebar me
lleve a la página de propiedades para acceder al inventario desde cualquier
sección.

**Why this priority**: Sin esta conexión, la página existe pero es inaccesible
desde la navegación principal.

**Independent Test**: Solicitar `GET /` (dashboard), hacer clic en el enlace
"Propiedades" del sidebar y verificar que navega a `/propiedades`.

**Acceptance Scenarios**:

1. **Given** el dashboard renderizado, **When** se inspecciona el sidebar,
   **Then** el enlace "Propiedades" tiene `href="/propiedades"`.
2. **Given** el usuario está en cualquier página con sidebar, **When** hace clic
   en "Propiedades", **Then** el navegador carga `GET /propiedades`.

---

### User Story 3 — Ver comportamiento responsive del grid (Priority: P2)

Como usuario del sistema, quiero que el grid de propiedades se adapte al tamaño
de mi pantalla para ver las cards correctamente en desktop, tablet o móvil.

**Why this priority**: La experiencia responsive es parte del diseño solicitado.
Sin embargo, la funcionalidad core (P1) es más prioritaria.

**Independent Test**: Renderizar la página y verificar mediante media queries
que el grid muestra 3, 2 o 1 columna según el ancho de viewport.

**Acceptance Scenarios**:

1. **Given** viewport > 1023px, **When** se renderiza la página, **Then** el
   grid muestra 3 cards por fila.
2. **Given** viewport entre 768px y 1023px, **When** se renderiza la página,
   **Then** el grid muestra 2 cards por fila.
3. **Given** viewport < 768px, **When** se renderiza la página, **Then** el
   grid muestra 1 card por fila.

---

### User Story 4 — Ver estado vacío cuando no hay propiedades (Priority: P2)

Como usuario del sistema, quiero ver un mensaje claro cuando no existen
propiedades registradas, en lugar de una página en blanco.

**Why this priority**: El manejo de estados vacíos es parte del contrato visual
del sistema. Sin embargo, con el seed actual siempre hay propiedades.

**Independent Test**: Truncar la tabla propiedades, solicitar `GET /propiedades`
y verificar que la página muestra un mensaje de estado vacío.

**Acceptance Scenarios**:

1. **Given** cero propiedades en base de datos, **When** se solicita
   `GET /propiedades`, **Then** la página muestra el mensaje
   "No hay propiedades registradas" con un icono informativo.
2. **Given** el estado vacío renderizado, **When** se inspecciona el HTML,
   **Then** no existen elementos con clase `.card-propiedad`.

---

### Casos límite

- No existen propiedades persistidas: la página muestra estado vacío, no un
  grid vacío ni error 500.
- Existe una propiedad sin imagen (`imagen` es string vacío o URL rota): la
  card muestra un placeholder visual (fondo de color + icono building-2), sin
  romper el layout del grid.
- Una propiedad tiene título o dirección con más de 100 caracteres: el texto
  se trunca con ellipsis en la card, sin desbordar el contenedor.
- Una propiedad tiene estado `mantenimiento` o `inactiva`: la card se renderiza
  normalmente; el badge de estado refleja el color correspondiente del sistema
  de diseño.
- Existen 50+ propiedades: el grid crece verticalmente sin paginación. El
  rendimiento es aceptable para un listado server-rendered sin lazy loading.
- El área tiene un valor numérico grande (ej. 10000): se formatea con
  separador de miles y unidad "m²".
- El precio de renta tiene decimales: se formatea como `$X,XXX.00`.
- El viewport tiene exactamente 1024px de ancho: aplica breakpoint tablet
  (2 columnas).
- La base de datos está disponible pero lanza error de conexión: el endpoint
  retorna 500 con página de error genérica del sistema.

---

## Requisitos

### Requisitos funcionales

- **FR-001**: El sistema DEBE exponer un endpoint `GET /propiedades` que
  consulte todas las propiedades persistidas desde base de datos.
- **FR-002**: El endpoint DEBE usar el repositorio de propiedades existente
  (`listar()`) para obtener los datos.
- **FR-003**: El sistema DEBE renderizar una página HTML server-rendered con
  un grid de cards, una card por cada propiedad.
- **FR-004**: Cada card DEBE mostrar: imagen, título, dirección, número de
  habitaciones, número de baños, área en m², precio de renta y estado.
- **FR-005**: El grid DEBE ser responsive: 3 columnas en desktop (> 1023px),
  2 columnas en tablet (768px–1023px), 1 columna en móvil (< 768px).
- **FR-006**: El enlace "Propiedades" del sidebar DEBE apuntar a
  `/propiedades`.
- **FR-007**: La página DEBE reutilizar el layout base existente
  (`base.html`) sin modificarlo.
- **FR-008**: Si no existen propiedades en base de datos, la página DEBE
  mostrar un estado vacío explícito con mensaje descriptivo.
- **FR-009**: Si una propiedad no tiene imagen utilizable, la card DEBE
  mostrar un placeholder visual (fondo + icono building-2) que no rompa
  el layout.
- **FR-010**: Textos largos en título y dirección DEBEN truncarse con
  ellipsis sin desbordar la card.
- **FR-011**: El área DEBE mostrarse con unidad "m²" y separador de miles.
- **FR-012**: El precio DEBE mostrarse con formato de moneda (símbolo `$`,
  separador de miles, dos decimales).
- **FR-013**: El estado DEBE renderizarse como badge usando el componente
  `_badge_estado.html` existente.
- **FR-014**: La lógica de obtención de datos DEBE vivir en
  `propiedades/service.py`; `propiedades/routes.py` solo debe orquestar.
- **FR-015**: El template de la página DEBE vivir en
  `app/modules/propiedades/templates/`.

### Requisitos no funcionales y de gobernanza técnica

Estos requisitos derivan de la constitución y specs previas. No son negociables.

#### Arquitectura

- **NFR-ARCH-001**: La página extiende el vertical slice de propiedades
  existente. No se crean nuevos módulos.
- **NFR-ARCH-002**: El endpoint `GET /propiedades` se define en
  `app/modules/propiedades/routes.py`, reemplazando el placeholder actual.
- **NFR-ARCH-003**: Aplica la separación vigente: `routes.py` es delgado,
  `service.py` contiene la lógica, `repository.py` solo acceso a datos.
- **NFR-ARCH-004**: Se reutiliza `PropiedadOut` existente como DTO. No se
  crean esquemas nuevos para esta vista.
- **NFR-ARCH-005**: No se introducen dependencias nuevas de paquetes Python.

#### Calidad

- **NFR-QA-001**: Aplica política vigente: ruff sin hallazgos, mypy strict
  sin errores en `app/modules/propiedades/`.
- **NFR-QA-002**: Tests unitarios del servicio con repositorio mockeado.
- **NFR-QA-003**: Tests de integración con Testcontainers y seed real.

#### Async

- **NFR-ASYNC-001**: Todas las funciones con I/O deben ser `async def`.
- **NFR-ASYNC-002**: Funciones de formato y mapeo pueden ser `def` síncrono.

### Gobernanza de tokens visuales

- **VTG-001**: Esta feature NO modifica tokens visuales canónicos (colores,
  sombras, radios, espaciados, tipografía, breakpoints).
- **VTG-002**: Esta feature EXTIENDE `app/static/css/app.css` con clases
  nuevas para el grid de propiedades y las cards extendidas. Las clases
  nuevas usan tokens existentes. [visual][extension]
- **VTG-003**: Esta feature NO modifica iconografía existente. El placeholder
  de imagen usa el icono `building-2` ya vendoreado.
- **VTG-004**: Esta feature EXTIENDE el componente `_card_propiedad.html`
  con nuevos campos. [visual][extension]
- **VTG-005**: Esta feature NO modifica `base.html` ni `_navbar.html`. El
  sidebar solo cambia un href.
- **VTG-006**: Esta feature NO rediseña páginas existentes.
- **VTG-007**: Si durante fases posteriores se modifica un token visual
  canónico, debe quedar trazado en `tasks.md` con marcador `[visual]`.

### Entidades clave

- **Propiedad**: Entidad persistida existente en `app/modules/propiedades/`.
  Sus columnas `titulo`, `direccion`, `habitaciones`, `banos`, `area`,
  `precio_mensual`, `estado` e `imagen` alimentan la card.
- **PropiedadOut**: DTO existente usado para transportar los datos desde el
  servicio al template. No se requiere un DTO nuevo.
- **Card de propiedad**: Componente visual extendido desde
  `_card_propiedad.html` existente. Muestra los 8 campos requeridos.
- **Grid de propiedades**: Contenedor CSS Grid responsive que organiza las
  cards en 3, 2 o 1 columna según viewport.
- **Estado vacío**: Representación explícita cuando `listar()` retorna una
  lista vacía, con mensaje e icono informativo.

---

## Clarificaciones

Sesión de clarificación ejecutada el 2026-06-16.

| Decisión | Resolución |
|----------|-----------|
| Componente de card | Extender `_card_propiedad.html` existente con los 8 campos requeridos |
| Imagen placeholder | Fondo `--color-surface` + icono `building-2` existente |
| Formato de precio | Símbolo `$`, separador de miles, dos decimales (`$1,500.00`) |
| Ordenamiento | `created_at` descendente (orden por defecto del repositorio) |
| Arquitectura | Extender el vertical slice de propiedades; reemplazar placeholder en `routes.py` |
| Template | `app/modules/propiedades/templates/propiedades.html` |
| Imagen con URL rota (404) | Mismo placeholder que cuando no hay imagen (fondo + icono) |
| Interacción de la card | Solo informativas (div estático). Navegación a detalle en spec futura |
| Estilo visual | La spec define los 8 campos requeridos; el layout visual queda a criterio de implementación respetando tokens |
| Campos en móvil | Los 8 campos siempre visibles en todos los breakpoints |

---

## Criterios de éxito

- **SC-001**: `GET /propiedades` retorna 200 y renderiza una página HTML con
  el layout base.
- **SC-002**: La página muestra exactamente una card por cada propiedad
  persistida en base de datos.
- **SC-003**: Cada card contiene los 8 campos visibles requeridos (imagen,
  título, dirección, habitaciones, baños, área, precio, estado).
- **SC-004**: El grid respeta 3 columnas en desktop, 2 en tablet, 1 en móvil.
- **SC-005**: El enlace "Propiedades" del sidebar navega a `/propiedades`.
- **SC-006**: Con cero propiedades, la página muestra estado vacío sin cards.
- **SC-007**: Una propiedad sin imagen muestra placeholder sin romper layout.
- **SC-008**: Textos largos se truncan con ellipsis.
- **SC-009**: Tests unitarios cubren la obtención de propiedades desde el
  servicio (con repositorio mockeado).
- **SC-010**: Tests de integración cubren el render HTML con datos reales y
  el estado vacío.

---

## Asunciones

1. El repositorio `propiedades.repository.listar()` ya existe y retorna todas
   las propiedades ordenadas por `created_at` descendente.
2. El DTO `PropiedadOut` ya existe y es suficiente para el contrato del
   template. No se requiere un DTO nuevo para esta vista.
3. El componente `_card_propiedad.html` existente se extiende sin modificar
   su estructura base. Los campos nuevos se agregan respetando tokens.
4. El seed de 10 propiedades de Miami (spec 004) contiene propiedades con
   todos los estados del catálogo, suficiente para validar el render.
5. Los breakpoints responsive son los definidos en el sistema: 1023px
   (tablet) y 767px (móvil).
6. No se requiere paginación, filtros ni búsqueda en esta spec. El listado
   completo server-rendered es suficiente para el volumen actual de datos.
7. El archivo `app/modules/propiedades/routes.py` existe como placeholder y
   será reemplazado por la implementación real de esta spec.
8. El router de propiedades ya está registrado en `app/main.py` (incluido en
   el refactor de configuración v1.4.0).

---

## Riesgos y dependencias

| Riesgo / Dependencia | Impacto | Mitigación |
|----------------------|---------|------------|
| Depende de spec 004 (propiedades base) con modelo, repositorio y seed | Bloqueante | Spec 004 ya está completada |
| El componente `_card_propiedad.html` actual es mínimo y requiere extensión significativa | Medio | La spec permite extenderlo; los campos nuevos se agregan respetando la estructura base y tokens existentes |
| Propiedades sin imagen pueden romper el layout | Medio | FR-009 exige placeholder con fondo + icono |
| Textos largos pueden desbordar cards | Bajo | FR-010 exige ellipsis vía CSS |
| El placeholder `propiedades/routes.py` debe ser reemplazado | Bajo | Ya tiene `# pragma: no cover`; se elimina al implementar |

---

## Trazabilidad de reglas

| Fuente | Regla | Traza a |
|--------|-------|---------|
| Prompt spec | Ver listado de propiedades en grid | US1, FR-001, FR-003, FR-004 |
| Prompt spec | Navegar desde menú lateral | US2, FR-006 |
| Prompt spec | Comportamiento responsive | US3, FR-005 |
| Prompt spec | Estado vacío | US4, FR-008 |
| Prompt spec | Placeholder de imagen | FR-009 |
| Prompt spec | Formato de precio y área | FR-011, FR-012 |
| Prompt spec | Badge de estado | FR-013 |
| Decisión interactiva | Extender `_card_propiedad.html` | FR-004, VTG-004 |
| Decisión interactiva | Placeholder fondo + icono building-2 | FR-009, VTG-003 |
| Decisión interactiva | Precio `$X,XXX.00` | FR-012 |
| Constitución sección IV | Vertical Slice | NFR-ARCH-001, NFR-ARCH-003 |
| Constitución sección VIII | TDD obligatorio | NFR-QA-002, NFR-QA-003 |
| Constitución sección XII | Blindaje de tokens visuales | VTG-001 a VTG-007 |
| Spec 004 | Modelo propiedades, repositorio listar(), PropiedadOut | FR-002, Asunción 1, Asunción 2 |
