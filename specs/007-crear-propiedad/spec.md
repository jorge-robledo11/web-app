# Feature Specification: Crear propiedad

**Feature Branch**: `007-crear-propiedad`

**Created**: 2026-06-20

**Status**: Draft

**Input**: Crear una página server-rendered con formulario para dar de alta
nuevas propiedades, con validaciones obligatorias, valores por defecto y
generación automática de imagen usando https://picsum.photos.

## Escenarios de usuario y pruebas

### User Story 1 — Crear una nueva propiedad desde el formulario (Priority: P1)

Como usuario del sistema, quiero acceder a una página con formulario para
registrar una nueva propiedad con los datos obligatorios.

**Why this priority**: Es la funcionalidad central de la feature. Sin un
formulario de alta, no existe manera operativa de añadir propiedades al
inventario desde la UI.

**Independent Test**: Acceder a `GET /propiedades/nueva`, completar los campos
obligatorios con datos válidos, enviar el formulario y verificar que la
propiedad queda persistida, con id autogenerado, estado `disponible` e imagen
generada, y que el usuario es redirigido a `/propiedades` con mensaje flash.

**Acceptance Scenarios**:

1. **Given** el usuario navega a `GET /propiedades/nueva`, **When** la página
   carga, **Then** ve un formulario con los campos obligatorios: titulo,
   direccion, precio_mensual, habitaciones, banos.
2. **Given** el usuario completa todos los campos obligatorios con datos
   válidos, **When** envía el formulario, **Then** la propiedad queda
   persistida con id autogenerado, estado `disponible`, ciudad `Miami` e
   imagen generada automáticamente vía `https://picsum.photos`.
3. **Given** la propiedad fue creada exitosamente, **When** el servidor
   responde, **Then** redirige a `/propiedades` con un mensaje flash de éxito.

---

### User Story 2 — Navegar a la página de creación desde el navbar (Priority: P1)

Como usuario del sistema, quiero que el botón "Nueva propiedad" del navbar
me lleve a la página de creación.

**Why this priority**: Sin este enlace, la página existe pero es inaccesible
desde la navegación principal.

**Independent Test**: En cualquier página con navbar, hacer clic en "Nueva
propiedad" y verificar que el navegador navega a `GET /propiedades/nueva`.

**Acceptance Scenarios**:

1. **Given** el usuario está en cualquier página con navbar, **When** inspecciona
   la barra superior, **Then** existe un botón o enlace con texto
   "Nueva propiedad" y `href="/propiedades/nueva"`.
2. **Given** el usuario hace clic en el botón "Nueva propiedad", **When** se
   procesa la navegación, **Then** el navegador carga `GET /propiedades/nueva`.

---

### User Story 3 — Ver errores de validación al enviar datos inválidos (Priority: P2)

Como usuario del sistema, quiero ver mensajes de error claros cuando envío
datos inválidos para corregirlos.

**Why this priority**: La validación inline es parte del contrato visual del
sistema. Sin ella, el usuario no sabe por qué el formulario fue rechazado.

**Independent Test**: Enviar el formulario con campos vacíos, con solo
espacios, o con valores fuera de rango, y verificar que la página re-renderiza
el formulario con errores inline junto a cada campo y conserva los datos
ingresados.

**Acceptance Scenarios**:

1. **Given** el usuario envía el formulario con campos obligatorios vacíos,
   **When** el servidor valida, **Then** re-renderiza el formulario con
   mensajes de error inline junto a cada campo vacío.
2. **Given** el usuario envía campos con solo espacios en blanco,
   **When** el servidor valida, **Then** los trata como vacíos y muestra
   error inline.
3. **Given** el usuario envía `precio_mensual` no numérico o `<= 0`,
   **When** el servidor valida, **Then** muestra error inline específico.
4. **Given** el usuario envía `habitaciones` o `banos` no numéricos o fuera
   de rango de negocio, **When** el servidor valida, **Then** muestra error
   inline específico.
5. **Given** el formulario re-renderiza con errores, **When** el usuario
   inspecciona el HTML, **Then** los campos conservan los valores previamente
   ingresados.

---

### User Story 4 — Generación automática de imagen con fallback (Priority: P2)

Como sistema, necesito generar automáticamente una imagen para la propiedad
usando `https://picsum.photos`, con fallback si el servicio falla.

**Why this priority**: La imagen es requerida por el modelo. Sin una imagen
válida, el listado no puede renderizar la card correctamente.

**Independent Test**: Crear una propiedad forzando una falla simulada del
servicio picsum.photos y verificar que la propiedad queda persistida con
imagen vacía (string vacío) para que el placeholder visual del listado se
active.

**Acceptance Scenarios**:

1. **Given** el servicio `https://picsum.photos` responde correctamente,
   **When** se crea una propiedad, **Then** el campo `imagen` contiene una
   URL válida con formato `https://picsum.photos/<width>/<height>`.
2. **Given** el servicio `https://picsum.photos` falla temporalmente,
   **When** se crea una propiedad, **Then** se aplica la política de
   fallback (string vacío) sin romper la creación, y el placeholder visual
   del listado se muestra en lugar de la imagen.

---

### Casos límite

- Campos obligatorios vacíos: la página re-renderiza el formulario con error
  inline por cada campo vacío; el campo conserva el valor previo.
- Campos con solo espacios en blanco: tratados como vacíos, error inline.
- `precio_mensual` no numérico: error inline.
- `precio_mensual` <= 0 (negativo o cero): error inline.
- `habitaciones` o `banos` no numéricos: error inline.
- `habitaciones` o `banos` fuera de rango de negocio (ej. > 100): error
  inline.
- Falla temporal de `https://picsum.photos`: fallback a string vacío para
  activar el placeholder visual del listado.
- `titulo` o `direccion` con más de 255 caracteres: error de validación o
  truncamiento según `String(255)` del modelo.
- Duplicado de `titulo` + `direccion` + `ciudad` (constraint único
  `uq_propiedades_identidad_negocio`): error de negocio manejado
  gracefully, formulario re-renderiza con mensaje específico.
- `area` no enviado en el formulario: el modelo requiere `area > 0`; se
  define un default razonable (ej. 0 o se solicita en el formulario).

---

## Requisitos

### Requisitos funcionales

- **FR-001**: El sistema DEBE exponer `GET /propiedades/nueva` que renderice
  el formulario de creación.
- **FR-002**: El sistema DEBE exponer `POST /propiedades` que procese los
  datos del formulario y persista la propiedad.
- **FR-003**: El botón "Nueva propiedad" del navbar DEBE navegar a
  `/propiedades/nueva`.
- **FR-004**: Los campos obligatorios del formulario son: `titulo`,
  `direccion`, `precio_mensual`, `habitaciones`, `banos`.
- **FR-005**: Campos con solo espacios en blanco DEBEN considerarse vacíos
  para efectos de validación.
- **FR-006**: El estado por defecto al crear DEBE ser `disponible`.
- **FR-007**: La ciudad por defecto DEBE ser `Miami` (ya definido en el
  modelo).
- **FR-008**: La imagen DEBE generarse automáticamente usando
  `https://picsum.photos/<width>/<height>` (ej. `/800/600`).
- **FR-009**: Si `https://picsum.photos` falla temporalmente, el sistema
  DEBE aplicar fallback a string vacío (placeholder visual existente se
  activa en el listado).
- **FR-010**: El id DEBE ser autogenerado por la base de datos vía
  `func.gen_random_uuid()`.
- **FR-011**: Tras creación exitosa, el sistema DEBE redirigir a
  `/propiedades` con un mensaje flash de éxito.
- **FR-012**: Los errores de validación DEBEN mostrarse inline junto al
  campo correspondiente.
- **FR-013**: El formulario DEBE conservar los datos ingresados al
  re-renderizar con errores (re-popular campos).
- **FR-014**: `precio_mensual` DEBE ser numérico y mayor que cero.
- **FR-015**: `habitaciones` DEBE ser entero mayor o igual a 1.
- **FR-016**: `banos` DEBE ser entero mayor o igual a 1.
- **FR-017**: La lógica de creación DEBE usar `service.crear_propiedad()`
  existente.
- **FR-018**: El template del formulario DEBE vivir en
  `app/modules/propiedades/templates/crear_propiedad.html`.
- **FR-019**: El formulario DEBE usar el componente `_form_field.html`
  existente para cada campo.
- **FR-020**: El campo `area` puede omitirse en el formulario o tener un
  default razonable (definido en clarificación).

### Requisitos no funcionales y de gobernanza técnica

#### Arquitectura

- **NFR-ARCH-001**: La página extiende el vertical slice de propiedades
  existente. No se crean nuevos módulos.
- **NFR-ARCH-002**: El endpoint `GET /propiedades/nueva` y `POST /propiedades`
  se definen en `app/modules/propiedades/routes.py`.
- **NFR-ARCH-003**: Aplica la separación vigente: `routes.py` es delgado,
  `service.py` contiene la lógica (generación de imagen, defaults),
  `repository.py` solo acceso a datos.
- **NFR-ARCH-004**: Se reutiliza `PropiedadIn` existente como DTO o se crea
  `PropiedadFormIn` específico para el formulario (decidido en clarificación).
- **NFR-ARCH-005**: No se introducen dependencias nuevas de paquetes
  Python.

#### Calidad

- **NFR-QA-001**: Aplica política vigente: ruff sin hallazgos, mypy strict
  sin errores en `app/modules/propiedades/`.
- **NFR-QA-002**: Tests unitarios del servicio con repositorio mockeado
  (generación de imagen, fallback, defaults, validaciones).
- **NFR-QA-003**: Tests de integración con Testcontainers y seed real que
  cubren el flujo completo de creación y los edge cases.

#### Async

- **NFR-ASYNC-001**: Todas las funciones con I/O deben ser `async def`.
- **NFR-ASYNC-002**: Funciones de formato y mapeo pueden ser `def` síncrono.

### Gobernanza de tokens visuales

- **VTG-001**: Esta feature NO modifica tokens visuales canónicos (colores,
  sombras, radios, espaciados, tipografía, breakpoints).
- **VTG-002**: Esta feature EXTIENDE `app/static/css/app.css` con clases
  nuevas para el formulario de creación. Las clases nuevas usan tokens
  existentes. [visual][extension]
- **VTG-003**: Esta feature NO modifica iconografía existente. Si se requiere
  un icono nuevo para el botón "Nueva propiedad" (ej. `plus` o
  `plus-circle` de Lucide), tarea explícita con `[visual][extension]`.
- **VTG-004**: Esta feature MODIFICA `_navbar.html` para agregar el botón
  "Nueva propiedad". [visual][extension]
- **VTG-005**: Esta feature NO modifica `base.html` ni `_sidebar.html`.
- **VTG-006**: Esta feature NO rediseña páginas existentes.
- **VTG-007**: Si durante fases posteriores se modifica un token visual
  canónico, debe quedar trazado en `tasks.md` con marcador `[visual]`.

### Entidades clave

- **Propiedad**: Entidad persistida existente en `app/modules/propiedades/`.
  Columnas usadas: `id`, `titulo`, `direccion`, `ciudad`, `precio_mensual`,
  `habitaciones`, `banos`, `area`, `estado`, `imagen`, `created_at`,
  `updated_at`.
- **PropiedadIn**: DTO existente usado como entrada al servicio. Valida
  `precio_mensual > 0`, `habitaciones >= 1`, `banos >= 1`, `area > 0`.
- **PropiedadOut**: DTO existente usado como salida del servicio.
- **EstadoPropiedad**: Enum con catálogo cerrado
  (`disponible`, `rentada`, `mantenimiento`, `inactiva`).
- **Formulario de creación**: Página server-rendered con campos obligatorios
  y validación inline.
- **Servicio picsum.photos**: Generador externo de imágenes placeholder
  (`https://picsum.photos/<width>/<height>`).
- **Fallback de imagen**: Política de string vacío cuando picsum.photos
  falla, para activar el placeholder visual del listado.

---

## Success Criteria

- **SC-001**: `GET /propiedades/nueva` retorna 200 con el formulario HTML
  y el layout base.
- **SC-002**: `POST /propiedades` con datos válidos crea la propiedad y
  redirige a `/propiedades` con mensaje flash de éxito.
- **SC-003**: La propiedad creada tiene id autogenerado (UUID), estado
  `disponible`, ciudad `Miami` e imagen generada vía picsum.photos.
- **SC-004**: `POST /propiedades` con datos inválidos re-renderiza el
  formulario con errores inline y conserva los datos ingresados.
- **SC-005**: El botón "Nueva propiedad" del navbar navega a
  `/propiedades/nueva`.
- **SC-006**: Campos con solo espacios en blanco se tratan como vacíos y
  muestran error inline.
- **SC-007**: `precio_mensual` `<= 0` o no numérico muestra error inline.
- **SC-008**: `habitaciones` y `banos` fuera de rango de negocio muestran
  error inline.
- **SC-009**: Si picsum.photos falla, se aplica fallback a string vacío sin
  romper la creación.
- **SC-010**: Tests unitarios cubren las validaciones y la creación exitosa
  con mocks del repositorio y del servicio picsum.
- **SC-011**: Tests de integración con Testcontainers cubren el flujo
  completo de creación, los edge cases y la navegación desde el navbar.

---

## Asunciones

1. `service.crear_propiedad()` ya existe y acepta `PropiedadIn`.
2. `repository.crear()` ya existe y persiste la propiedad en base de datos.
3. El modelo `Propiedad` ya tiene todas las columnas necesarias.
4. El id se autogenera vía `func.gen_random_uuid()` en la base de datos.
5. El estado `disponible` existe en `EstadoPropiedad`.
6. El componente `_form_field.html` existe y es reutilizable para los
   campos del formulario.
7. `https://picsum.photos` retorna una URL de imagen válida con formato
   `https://picsum.photos/<width>/<height>` (ej. `/800/600`).
8. El router de propiedades ya está registrado en `app/main.py`.

## Clarificaciones

Sesión de clarificación ejecutada el 2026-06-20.

| Decisión | Resolución |
|----------|-----------|
| Campo `area` en el formulario | Opcional con default 0 aplicado en `service.py` |
| Campo `ciudad` en el formulario | Omitido (siempre `Miami` vía default del modelo) |
| Mecanismo de envío del formulario | POST tradicional con redirect 303 a `/propiedades` y flash message en sesión/cookie |
| Política de fallback de picsum.photos | String vacío en `imagen` (placeholder visual del listado se activa automáticamente) |
| Icono del botón "Nueva propiedad" | Texto + icono `plus` de Lucide (vendorear `app/static/icons/plus.svg`) con marcador `[visual][extension]` |
| Rango de habitaciones y banos | `habitaciones <= 20` y `banos <= 10` (rango residencial urbano) |
| Manejo de duplicados (constraint único) | Capturar `IntegrityError` en `service.py`, retornar `None` y mostrar error inline específico en el formulario |
| Redirección post-creación | Redirect 303 a `/propiedades` (listado, coherente con spec 006) |

---

## Riesgos y dependencias

| Riesgo / Dependencia | Impacto | Mitigación |
|----------------------|---------|------------|
| Depende de spec 004 (propiedades base con modelo, repositorio y seed) | Bloqueante | Spec 004 ya está completada |
| Depende de spec 006 (página de propiedades con cards para redirect post-creación) | Bloqueante | Spec 006 ya está completada |
| `service.crear_propiedad()` ya existe pero puede requerir ajuste para generar imagen automáticamente | Medio | Extender `service.py` con función de generación de imagen y fallback |
| `https://picsum.photos` es un servicio externo que puede fallar | Medio | Política de fallback a string vacío (FR-009) |
| El constraint único `uq_propiedades_identidad_negocio` puede generar error de duplicado | Bajo | Manejar error gracefully con mensaje inline específico |
| El campo `area` es obligatorio en el modelo pero no en el formulario | Medio | Definir default razonable en clarificación |
| `PropiedadIn` requiere `estado` y `imagen` que el formulario no solicita | Medio | Crear `PropiedadFormIn` específico o aplicar defaults en `service.py` |

---

## Trazabilidad de reglas

| Fuente | Regla | Traza a |
|--------|-------|---------|
| Prompt spec | Crear propiedad desde formulario | US1, FR-001, FR-002 |
| Prompt spec | Navegar desde navbar | US2, FR-003 |
| Prompt spec | Validaciones inline | US3, FR-004, FR-012, FR-013 |
| Prompt spec | Generación de imagen con picsum | US4, FR-008, FR-009 |
| Prompt spec | Estado por defecto disponible | FR-006 |
| Prompt spec | Ciudad por defecto Miami | FR-007 |
| Prompt spec | id autogenerado | FR-010 |
| Prompt spec | Redirect post-creación con flash | FR-011 |
| Prompt spec | Validaciones numéricas | FR-014, FR-015, FR-016 |
| Prompt spec | Tratamiento de espacios como vacío | FR-005, US3 |
| Prompt spec | Reutilizar servicio existente | FR-017, NFR-ARCH-003 |
| Prompt spec | Template en vertical slice | FR-018, NFR-ARCH-001 |
| Prompt spec | Usar _form_field.html | FR-019 |
| Constitución sección IV | Vertical Slice | NFR-ARCH-001, NFR-ARCH-003 |
| Constitución sección VIII | TDD obligatorio | NFR-QA-002, NFR-QA-003 |
| Constitución sección XII | Blindaje de tokens visuales | VTG-001 a VTG-007 |
| Spec 004 | Modelo Propiedad, PropiedadIn, PropiedadOut, repository.crear | FR-002, FR-017, Asunción 1-3 |
| Spec 006 | Página de propiedades con cards para redirect | FR-011, US2 |
| Spec 002 | Componente _form_field.html | FR-019, Asunción 6 |
