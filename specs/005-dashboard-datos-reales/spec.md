# Feature Specification: Dashboard con datos reales

**Feature Branch**: `005-dashboard-datos-reales`

**Created**: 2026-06-15

**Status**: Draft

**Input**: Reemplazar métricas mockeadas del dashboard principal por datos reales
de propiedades persistidas, manteniendo la arquitectura vertical slice y el
contrato de contexto de la home.

## Escenarios de usuario y pruebas

### User Story 1 — Ver métricas reales de propiedades en la home (Priority: P1)

Como usuario del sistema inmobiliario, quiero que el dashboard principal muestre
la cantidad real de propiedades disponibles y rentadas para entender el estado
actual del inventario.

**Why this priority**: Es el primer paso para que el dashboard refleje la
realidad operativa. Sin métricas reales, la home no aporta valor de gestión.

**Independent Test**: Insertar propiedades con distintos estados en base de
datos, solicitar `GET /` y verificar que los valores de disponibles y rentadas
coinciden con los conteos reales de la base de datos.

**Acceptance Scenarios**:

1. **Given** 4 propiedades con estado `disponible` y 3 con estado `rentada`,
   **When** se solicita `GET /`, **Then** la home muestra `4` en
   "Propiedades disponibles" y `3` en "Propiedades rentadas".
2. **Given** una propiedad cambia de `disponible` a `rentada`, **When** se
   solicita `GET /`, **Then** disponibles disminuye en 1 y rentadas aumenta
   en 1 respecto a la consulta anterior.
3. **Given** no existen propiedades en la base de datos, **When** se solicita
   `GET /`, **Then** la home muestra el estado vacío del dashboard.

---

### User Story 2 — Mantener la estructura actual del dashboard (Priority: P1)

Como usuario del sistema, quiero que el dashboard conserve su estructura actual
para que la mejora de datos no cambie la experiencia visual ni la navegación.

**Why this priority**: La spec 003 definió un diseño aprobado. Cualquier cambio
estructural no solicitado rompe la experiencia del usuario y el contrato de
templates.

**Independent Test**: Solicitar `GET /` y verificar que el HTML contiene las
tres secciones (métricas, accesos rápidos, actividad reciente) en el mismo orden
vertical definido por el contrato `dashboard.yaml`.

**Acceptance Scenarios**:

1. **Given** el dashboard renderizado, **When** se inspecciona el HTML,
   **Then** la sección `.metricas` aparece antes que `.accesos-rapidos` y esta
   antes que `.actividad`.
2. **Given** el dashboard renderizado, **When** se inspeccionan los accesos
   rápidos, **Then** contienen exactamente 4 items con los mismos labels e
   iconos que el contrato vigente.
3. **Given** el dashboard renderizado, **When** se inspecciona la actividad
   reciente, **Then** conserva su estructura de grid con items que incluyen
   tipo, descripción, fecha y badge.

---

### User Story 3 — Distinguir métricas reales de métricas pendientes (Priority: P2)

Como usuario o mantenedor del sistema, quiero que ingresos y vencidos queden
marcados como no operativos para evitar interpretar datos inventados como reales.

**Why this priority**: La transparencia sobre qué datos son reales y cuáles no
es crítica para la confianza en el sistema. Sin embargo, el valor principal de
esta spec está en las métricas reales (P1).

**Independent Test**: Solicitar `GET /` y verificar que las métricas de
ingresos y vencidos muestran valor `0` con el marcador textual "No disponible",
sin depender de cálculos inventados.

**Acceptance Scenarios**:

1. **Given** el dashboard renderizado, **When** se inspeccionan las métricas,
   **Then** "Ingresos" muestra valor `0` y el marcador "No disponible".
2. **Given** el dashboard renderizado, **When** se inspeccionan las métricas,
   **Then** "Vencidos" muestra valor `0` y el marcador "No disponible".
3. **Given** el código fuente del servicio de dashboard, **When** se revisa la
   lógica de cálculo, **Then** no existe código que invente conteos de ingresos
   ni vencidos a partir de modelos inexistentes.

---

### Casos límite

- No existen propiedades persistidas: la home debe mostrar el estado vacío del
  dashboard, con un mensaje explícito indicando que no hay datos.
- Existen propiedades, pero ninguna está disponible: la métrica de disponibles
  muestra `0`; la home no entra en estado vacío.
- Existen propiedades, pero ninguna está rentada: la métrica de rentadas
  muestra `0`; la home no entra en estado vacío.
- Existen propiedades con estados distintos a `disponible` y `rentada`
  (mantenimiento, inactiva): esas propiedades no se cuentan en ninguna de las
  dos métricas reales.
- Existen propiedades en todos los estados del catálogo: disponibles y rentadas
  reflejan solo sus respectivos conteos; el total de propiedades puede ser
  mayor que la suma de disponibles + rentadas.
- La base de datos está disponible pero el inventario está vacío: el endpoint
  `GET /` no falla; renderiza el estado vacío normalmente.
- Ingresos no tiene modelo suficiente para cálculo real: la métrica se presenta
  con valor `0` y marcador "No disponible", sin intentar calcularse.
- Vencidos no tiene modelo suficiente para cálculo real: la métrica se presenta
  con valor `0` y marcador "No disponible", sin intentar calcularse.
- El contrato de contexto de la home recibe métricas reales y no operativas en
  el mismo arreglo: el template itera uniformemente; la diferenciación se da
  por el marcador textual "No disponible" en las no operativas.
- Se evalúa crear endpoint adicional sin caso funcional concreto: no se crea.
  La home server-rendered resuelve todos los datos en cada request.

---

## Requisitos

### Requisitos funcionales

- **FR-001**: El sistema DEBE calcular la cantidad de propiedades con estado
  `disponible` usando datos persistidos en la tabla `propiedades`.
- **FR-002**: El sistema DEBE calcular la cantidad de propiedades con estado
  `rentada` usando datos persistidos en la tabla `propiedades`.
- **FR-003**: La home DEBE usar las métricas reales calculadas para propiedades
  disponibles y rentadas en lugar de valores hardcodeados.
- **FR-004**: La home NO DEBE depender de valores hardcodeados para propiedades
  disponibles ni rentadas.
- **FR-005**: El contrato de contexto de la home DEBE conservar la estructura
  esperada por el template actual (`metricas` como `list[dict]` con campos
  `label`, `valor`, `icono`, `tendencia`, `estado`).
- **FR-006**: El orden de las métricas DEBE ser: Propiedades disponibles,
  Propiedades rentadas, Ingresos, Vencidos.
- **FR-007**: El orden y estructura de accesos rápidos DEBE permanecer estable
  respecto al dashboard existente (4 items: Propiedades, Inquilinos, Contratos,
  Pagos).
- **FR-008**: El estado vacío del dashboard DEBE activarse cuando no existen
  propiedades persistidas en la base de datos (cero filas en la tabla
  `propiedades`).
- **FR-009**: Si no existen propiedades persistidas, la home DEBE representar
  ese estado de forma explícita con un mensaje descriptivo.
- **FR-010**: Ingresos DEBE permanecer como métrica no operativa en esta spec,
  mostrando valor `0` y el marcador textual "No disponible".
- **FR-011**: Vencidos DEBE permanecer como métrica no operativa en esta spec,
  mostrando valor `0` y el marcador textual "No disponible".
- **FR-012**: El sistema NO DEBE inventar cálculos de ingresos sin modelo de
  rentas, pagos o contratos.
- **FR-013**: El sistema NO DEBE inventar cálculos de vencidos sin modelo de
  pagos, contratos o fechas de vencimiento.
- **FR-014**: El servicio de dashboard DEBE exponer una salida apta para el
  contexto de la home (el dict que recibe `dashboard.html`).
- **FR-015**: La lógica de cálculo de métricas DEBE vivir en la capa de
  servicio correspondiente y no en el template ni en `main.py`.
- **FR-016**: El acceso a datos DEBE permanecer separado de la lógica de
  presentación (repositorio solo consulta, servicio orquesta, template solo
  renderiza).
- **FR-017**: No DEBE crearse un endpoint adicional para refresh parcial, dado
  que no existe un caso funcional concreto que lo justifique en esta feature.

### Requisitos no funcionales y de gobernanza técnica

Estos requisitos derivan de la constitución del proyecto y de las specs
previas. No son negociables.

#### Arquitectura

- **NFR-ARCH-001**: El dashboard se implementa como vertical slice en
  `app/modules/dashboard/`. La estructura mínima requerida es:
  `__init__.py`, `routes.py`, `schemas.py`, `service.py`, `repository.py`.
  No se crearán archivos, clases ni abstracciones adicionales si no aportan
  valor verificable.
- **NFR-ARCH-002**: El endpoint `GET /` DEBE definirse en
  `app/modules/dashboard/routes.py`. `app/main.py` NO DEBE contener lógica de
  dashboard ni construcción del contexto; solo puede registrar o incluir el
  router del slice si corresponde.
- **NFR-ARCH-003**: Aplica la separación vigente entre rutas, servicios,
  repositorios y templates. `routes.py` es delgado y se limita a resolver la
  request, invocar el servicio y renderizar la home. `service.py` contiene la
  lógica de negocio y el armado del contexto. `repository.py` solo accede a
  datos. `schemas.py` contiene DTOs o estructuras tipadas cuando aporten
  claridad.
- **NFR-ARCH-004**: El módulo `dashboard` NO DEBE duplicar modelos de dominio
  de `propiedades`. El acceso a datos de propiedades se realiza a través del
  repositorio de `propiedades`, que DEBE exponer una función
  `contar_por_estado(estado)` reutilizable. No se requiere crear modelos,
  esquemas ni endpoints nuevos en el módulo `propiedades` para esta feature.
- **NFR-ARCH-005**: No se introducen dependencias nuevas de paquetes Python.
- **NFR-ARCH-006**: No se reabren decisiones técnicas heredadas de specs
  previas (estructura de `propiedades`, catálogo de estados, contrato del
  template dashboard).

#### Calidad

- **NFR-QA-001**: Aplica la política vigente de calidad: `ruff check` sin
  hallazgos, `mypy --strict` sin errores en `app/modules/dashboard/`.
- **NFR-QA-002**: Las pruebas DEBEN usar `pytest`, `pytest-asyncio` y
  `httpx.AsyncClient`.
- **NFR-QA-003**: Los tests de integración que requieran PostgreSQL DEBEN usar
  Testcontainers con `postgres:16-alpine`.
- **NFR-QA-004**: Los tests unitarios del servicio de dashboard PUEDEN mockear
  el repositorio de propiedades.
- **NFR-QA-005**: Los tests de integración DEBEN verificar el ciclo completo:
  seed de propiedades → consulta de métricas → render de home.

#### Async

- **NFR-ASYNC-001**: Todas las funciones que realicen I/O (consulta a base de
  datos, render de templates) DEBEN ser `async def`.
- **NFR-ASYNC-002**: Las funciones de cómputo puro (mapeo de resultados,
  construcción de dicts de contexto) PUEDEN ser `def` síncrono.

### Gobernanza de tokens visuales

- **VTG-001**: Esta feature NO modifica tokens visuales canónicos (colores,
  sombras, radios, espaciados, tipografía, breakpoints).
- **VTG-002**: Esta feature NO modifica CSS (`app/static/css/app.css`).
- **VTG-003**: Esta feature NO modifica iconografía (`app/static/icons/`).
  Todos los iconos requeridos por las nuevas métricas ya existen en el set
  vendoreado.
- **VTG-004**: Esta feature NO modifica componentes compartidos
  (`app/templates/components/`).
- **VTG-005**: Esta feature NO rediseña la home. La estructura visual y el
  layout permanecen idénticos a lo definido en spec 003.
- **VTG-006**: Si durante fases posteriores se toca algún archivo visual
  protegido, deberá quedar trazado en `tasks.md` con el marcador `[visual]`
  según la regla de blindaje vigente en la constitución sección XII y spec
  002.

### Entidades clave

- **Propiedad**: Entidad persistida existente en `app/modules/propiedades/`,
  usada como fuente de verdad para las métricas de inventario. Su columna
  `estado` de tipo `estado_propiedad` permite filtrar por `disponible` y
  `rentada`.
- **Estado de propiedad**: Catálogo cerrado existente (`disponible`, `rentada`,
  `mantenimiento`, `inactiva`) que permite distinguir las dos métricas reales
  incluidas en esta spec.
- **Métrica de dashboard**: Elemento del contexto `metricas` renderizado en la
  home. Estructura: `label`, `valor`, `icono`, `tendencia`, `estado`. Las
  métricas reales tienen `estado: "datos"`; las no operativas tienen `estado:
  "datos"` con marcador "No disponible".
- **Estado vacío del dashboard**: Representación explícita del dashboard cuando
  la tabla `propiedades` no contiene filas. Sustituye las tres secciones
  (métricas, accesos, actividad) por un mensaje descriptivo centrado.
- **Métrica no operativa**: Métrica presente en el arreglo `metricas` cuya
  fuente de datos real todavía no existe en el modelo de datos. Se renderiza
  con valor `0` y el marcador textual "No disponible" para evitar ambigüedad.

## Clarificaciones

Sesión de clarificación ejecutada el 2026-06-15.

| Decisión | Resolución |
|----------|-----------|
| Ubicación del dashboard | Vertical slice en `app/modules/dashboard/` |
| Endpoint `GET /` | Definido en `app/modules/dashboard/routes.py` |
| Rol de `app/main.py` | Solo registra el router del slice si corresponde; no contiene lógica de dashboard |
| Métricas no operativas | Valor `0` + marcador textual "No disponible" |
| Estado vacío | Se activa con cero filas en la tabla `propiedades` |
| Endpoints adicionales | No se crean; el render server-side es suficiente |
| Acceso a datos entre módulos | El repositorio de `propiedades` expone `contar_por_estado()`; el servicio de dashboard la invoca |
| Icono — disponibles | `building-2` |
| Icono — rentadas | `check-circle-2` |
| Icono — ingresos | `wallet` |
| Icono — vencidos | `clock` |
| Tendencia en métricas reales | Se omite el campo `tendencia` en disponibles y rentadas por no existir datos históricos; el componente `_tarjeta_metrica.html` ya soporta el campo como opcional |

La spec está lista para planificación.

## Criterios de éxito

- **SC-001**: La home deja de usar datos hardcodeados para propiedades
  disponibles.
- **SC-002**: La home deja de usar datos hardcodeados para propiedades
  rentadas.
- **SC-003**: El conteo de propiedades disponibles refleja datos persistidos
  (el valor renderizado coincide con `SELECT count(*) FROM propiedades WHERE
  estado = 'disponible'`).
- **SC-004**: El conteo de propiedades rentadas refleja datos persistidos (el
  valor renderizado coincide con `SELECT count(*) FROM propiedades WHERE
  estado = 'rentada'`).
- **SC-005**: Al cambiar estados de propiedades en base de datos, las métricas
  renderizadas en el siguiente request cambian acorde a esos datos.
- **SC-006**: El estado vacío del dashboard se activa cuando `SELECT count(*)
  FROM propiedades` retorna `0`.
- **SC-007**: Ingresos queda documentado como métrica no operativa en esta spec
  y se renderiza con valor `0` y marcador "No disponible".
- **SC-008**: Vencidos queda documentado como métrica no operativa en esta spec
  y se renderiza con valor `0` y marcador "No disponible".
- **SC-009**: La estructura del contexto de la home permanece compatible con el
  template `dashboard.html` existente (mismos keys, mismos tipos).
- **SC-010**: Los tests unitarios cubren el cálculo de métricas desde el
  servicio de dashboard (con repositorio mockeado).
- **SC-011**: Los tests de integración cubren el render de la home con valores
  reales provenientes de base de datos.
- **SC-012**: La spec deja claramente trazado qué queda pendiente para una
  feature futura de ingresos y vencidos reales (modelos de rentas, pagos o
  contratos).

## Asunciones

1. Ya existe una fuente persistida de propiedades en la tabla `propiedades`
   con el catálogo de estados definido en spec 004.
2. Los estados `disponible` y `rentada` del enum `EstadoPropiedad` son
   suficientes para calcular las dos métricas reales incluidas en esta spec.
3. La home actual ya tiene un contrato de contexto definido en
   `specs/003-redisenar-home/contracts/dashboard.yaml` que debe conservarse.
4. Ingresos y vencidos no pueden calcularse correctamente en esta spec porque
   requieren modelos de rentas, pagos o contratos que no existen.
5. No se necesita endpoint adicional porque la home server-rendered puede
   resolver todos los datos en cada request. Si en el futuro se requiere
   refresh parcial vía HTMX, se evaluará en una spec separada.
6. El seed de 10 propiedades de Miami (spec 004) contiene 4 disponibles y 3
   rentadas, lo cual es suficiente para validar las métricas reales.
7. El endpoint `GET /` debe definirse en `app/modules/dashboard/routes.py`.
   `app/main.py` solo registra el router del slice dashboard si corresponde,
   sin contener lógica de cálculo ni construcción del contexto.
8. La actividad reciente permanece con datos hardcodeados de demo en esta spec.
   Su conexión a datos reales corresponde a una feature futura.

## Riesgos y dependencias

| Riesgo / Dependencia | Impacto | Mitigación |
|----------------------|---------|------------|
| Depende de la spec 004 (propiedades base) con tabla `propiedades` y catálogo de estados | Bloqueante | Spec 004 ya está completada; la tabla y el seed existen |
| Depende de que los estados `disponible` y `rentada` representen correctamente disponibilidad y renta | Medio | El catálogo fue validado en spec 004; esta spec solo consume los valores existentes |
| El cálculo de ingresos depende de modelos futuros de rentas, pagos o contratos | Bajo (esta spec) | Se documenta explícitamente como fuera de alcance; la métrica se marca "No disponible" |
| El cálculo de vencidos depende de modelos futuros de pagos, contratos o fechas de vencimiento | Bajo (esta spec) | Se documenta explícitamente como fuera de alcance; la métrica se marca "No disponible" |
| Mezclar métricas reales con métricas no operativas sin diferenciarlas claramente | Alto | FR-010 y FR-011 exigen marcador "No disponible"; el template las distingue visualmente |
| Introducir endpoints o abstracciones no necesarias para una home server-rendered | Medio | FR-017 prohíbe endpoints adicionales; NFR-ARCH-001 limita el módulo a los artefactos estándar |
| Los tests existentes de dashboard (`tests/unit/test_dashboard.py`) esperan valores hardcodeados | Medio | Los tests se actualizarán durante la fase de implementación para verificar métricas reales |

## Trazabilidad de reglas

| Fuente | Regla | Traza a |
|--------|-------|---------|
| Prompt spec, líneas 96-108 | Ver métricas reales en home | US1, FR-001, FR-002, FR-003 |
| Prompt spec, líneas 110-119 | Mantener estructura actual | US2, FR-005, FR-006, FR-007 |
| Prompt spec, líneas 121-133 | Distinguir métricas reales de pendientes | US3, FR-010, FR-011 |
| Prompt spec, líneas 137-138 | Calcular disponibles desde DB | FR-001 |
| Prompt spec, líneas 139-140 | Calcular rentadas desde DB | FR-002 |
| Prompt spec, líneas 141-142 | Home usa métricas reales | FR-003 |
| Prompt spec, líneas 143-144 | No hardcodear disponibles/rentadas | FR-004 |
| Prompt spec, líneas 145-146 | Conservar contrato de contexto | FR-005 |
| Prompt spec, línea 147 | Orden de métricas estable | FR-006 |
| Prompt spec, línea 148 | Orden de accesos estable | FR-007 |
| Prompt spec, líneas 149-151 | Estado vacío desde datos reales | FR-008, FR-009 |
| Prompt spec, líneas 152 | Ingresos no operativo | FR-010 |
| Prompt spec, línea 153 | Vencidos no operativo | FR-011 |
| Prompt spec, líneas 154-155 | No inventar ingresos | FR-012 |
| Prompt spec, líneas 156-157 | No inventar vencidos | FR-013 |
| Prompt spec, líneas 158-159 | Servicio expone salida para home | FR-014 |
| Prompt spec, líneas 160-161 | Lógica en servicio, no en template | FR-015 |
| Prompt spec, línea 162 | Acceso a datos separado de presentación | FR-016 |
| Prompt spec, líneas 163-164 | No crear endpoint sin caso funcional | FR-017 |
| Prompt spec, líneas 195-201 | Gobernanza visual | VTG-001 a VTG-006 |
| Prompt spec, líneas 181-186 | Gobernanza técnica | NFR-ARCH-001 a NFR-ARCH-005 |
| Prompt spec, líneas 240-252 | Edge cases | Casos límite |
| Prompt spec, líneas 256-267 | Riesgos y dependencias | Riesgos y dependencias |
| Prompt spec, líneas 271-279 | Assumptions | Asunciones |
| Decisión interactiva #1 | Métricas no operativas: valor 0 + "No disponible" | FR-010, FR-011 |
| Decisión interactiva #2 | Estado vacío: cero propiedades totales | FR-008, FR-009 |
| Constitución sección IV | Vertical Slice Architecture | NFR-ARCH-001, NFR-ARCH-002 |
| Constitución sección VIII | TDD obligatorio | NFR-QA-002, NFR-QA-003 |
| Constitución sección XII | Blindaje de tokens visuales | VTG-001 a VTG-006 |
| Spec 003 | Contrato dashboard.yaml | FR-005, FR-007 |
| Spec 004 | Modelo propiedades, enum EstadoPropiedad | FR-001, FR-002, Asunción 1 |

## Métricas futuras pendientes

Esta spec deja explícitamente documentado el camino para que ingresos y
vencidos pasen de métricas no operativas a métricas reales en una feature
futura:

- **Ingresos**: Requiere un modelo de rentas, pagos o contratos que permita
  calcular ingresos mensuales, trimestrales o acumulados a partir de
  transacciones reales. Sin este modelo, cualquier cálculo sería inventado.
- **Vencidos**: Requiere un modelo de pagos con fechas de vencimiento o un
  modelo de contratos con fechas de corte que permita identificar pagos
  atrasados. Sin este modelo, cualquier cálculo sería inventado.

La spec futura que introduzca estos modelos deberá:
1. Crear el módulo correspondiente (`rentas`, `pagos` o `contratos`) con
   modelo, migración y seed.
2. Agregar funciones de conteo en el repositorio del nuevo módulo.
3. Actualizar el servicio de dashboard para reemplazar los marcadores "No
   disponible" por valores reales.
4. Actualizar los tests de dashboard para cubrir las nuevas métricas.
