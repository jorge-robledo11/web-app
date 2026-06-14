# Feature Specification: Propiedades base

**Feature Branch**: `004-propiedades-base`

**Created**: 2026-06-14

**Status**: Draft

**Input**: Habilitar base persistente inicial de propiedades inmobiliarias del proyecto Realtor.

## Escenarios de usuario y pruebas

### User Story 1 — Carga inicial de propiedades (Priority: P1)

Como administrador del sistema Realtor, necesito disponer de un conjunto inicial de
propiedades para que el dashboard y los reportes dejen de mostrar datos vacíos y
permitan validar el comportamiento funcional con casos realistas.

**Why this priority**: Es la fuente de datos fundacional. Sin propiedades
persistentes, ninguna feature posterior (listado, búsqueda, reportes, dashboard
real) puede operar.

**Independent Test**: Ejecutar la carga inicial sobre una base de datos limpia y
verificar que existen exactamente 10 propiedades con atributos completos,
estados válidos e imágenes asociadas.

**Acceptance Scenarios**:

1. **Given** una base de datos con esquema `public` recién creado, **When** se
   ejecuta `alembic upgrade head` seguido de la carga inicial de propiedades,
   **Then** existen exactamente 10 propiedades de Miami con todos los atributos
   obligatorios completos.
2. **Given** la carga inicial ya fue ejecutada una vez, **When** se re-ejecuta la
   carga inicial, **Then** el sistema mantiene exactamente 10 propiedades sin
   duplicados, actualizando in-place las existentes por clave de negocio.
3. **Given** las 10 propiedades cargadas, **When** se verifica cada una, **Then**
   el 100% tiene un estado dentro del catálogo permitido (`disponible`,
   `rentada`, `mantenimiento`, `inactiva`) y una imagen asociada con semilla
   estable.

---

### User Story 2 — Evolución y reversibilidad de base de datos (Priority: P1)

Como desarrollador del proyecto, necesito que las migraciones de base de datos
sean aplicables y reversibles para garantizar la integridad del esquema en
cualquier entorno (desarrollo, CI, producción).

**Why this priority**: Las migraciones irreversibles o con errores bloquean el
despliegue y la iteración del equipo.

**Independent Test**: Ejecutar el ciclo completo `alembic upgrade head` →
`alembic downgrade -1` → `alembic upgrade head` sobre `public` recién creado y
verificar que todas las etapas finalizan sin errores.

**Acceptance Scenarios**:

1. **Given** un esquema `public` vacío, **When** se ejecuta `alembic upgrade head`,
   **Then** la migración finaliza en verde sin intervención manual y sin uso de
   `alembic stamp`.
2. **Given** la migración aplicada, **When** se ejecuta `alembic downgrade -1`,
   **Then** el downgrade revierte los cambios sin errores (nunca es `pass`).
3. **Given** el downgrade completado, **When** se re-ejecuta `alembic upgrade head`,
   **Then** la migración se reaplica limpiamente, completando el ciclo de
   ida y vuelta.

---

### User Story 3 — Validación de integridad y calidad (Priority: P2)

Como desarrollador del proyecto, necesito que el módulo `propiedades` cumpla con
las reglas de calidad estática y las restricciones técnicas heredadas de la
constitución para poder integrarlo al pipeline de CI sin hallazgos.

**Why this priority**: La calidad estática es un gate obligatorio del proyecto.
Sin ella, ninguna feature puede considerarse completa.

**Independent Test**: Ejecutar `mypy --strict` y `ruff check` sobre el módulo
`app/modules/propiedades/` y verificar que ambos finalizan sin errores.

**Acceptance Scenarios**:

1. **Given** el código del módulo `propiedades` implementado, **When** se ejecuta
   `mypy --strict app/modules/propiedades/`, **Then** no se reportan errores.
2. **Given** el código implementado, **When** se ejecuta `ruff check .`,
   **Then** no se reportan hallazgos.
3. **Given** cualquier script auxiliar de base de datos, **When** se inspecciona
   su código, **Then** no depende de `psycopg2` ni `psycopg`, usando
   exclusivamente `asyncpg` vía `create_async_engine`.

---

### Casos límite

- Intentar registrar una propiedad con estado fuera del catálogo (`disponible`,
  `rentada`, `mantenimiento`, `inactiva`): debe rechazarse.
- Ejecutar la carga inicial varias veces con datos parcialmente presentes: la
  cardinalidad debe mantenerse estable (10 propiedades), aplicando upsert por
  clave compuesta de negocio (`título + dirección + ciudad`).
- Aplicar `alembic upgrade head` en un entorno con esquema `public` en estado
  inconsistente: la mitigación es `DROP SCHEMA public CASCADE` + `CREATE SCHEMA
  public` + `alembic upgrade head`, nunca `alembic stamp`.
- `CREATE TYPE` choca con un enum preexistente: la mitigación es declarar el enum
  en la columna y dejar que el DDL de creación de tabla lo materialice
  implícitamente, sin invocar creación explícita del tipo en paralelo.
- Inserciones con SQL parametrizado usando `:param::uuid`: la mitigación es
  `CAST(:param AS uuid)` dentro de `sa.text`. Está prohibido `:param::uuid`.
- Ejecución del seed dos veces consecutivas: la cardinalidad debe permanecer en
  10, con actualización in-place de registros existentes por clave de negocio.
- Detección de diferencias de zona horaria entre datos generados por aplicación y
  datos gestionados por la base de datos: los timestamps deben ser server-side,
  nunca enviados desde Python en migraciones ni seeds.
- Alembic reporta una revisión que no existe en `alembic/versions/`: la
  mitigación es reset de schema `public` + `upgrade head`, nunca `alembic stamp`.

## Requisitos

### Requisitos funcionales

- **FR-001**: El sistema DEBE persistir propiedades con los siguientes atributos
  mínimos: título, dirección, ciudad, precio mensual, número de habitaciones,
  número de baños, área, estado, imagen, marca temporal de creación y marca
  temporal de actualización.
- **FR-002**: El estado de una propiedad SOLO puede tomar uno de estos valores:
  `disponible`, `rentada`, `mantenimiento`, `inactiva`.
- **FR-003**: El sistema DEBE rechazar cualquier intento de registrar una
  propiedad con un estado fuera del catálogo permitido.
- **FR-004**: La identidad de negocio del seed DEBE ser la combinación única
  `título + dirección + ciudad`. Dos propiedades con la misma combinación se
  consideran la misma entidad de negocio.
- **FR-005**: Re-ejecutar la carga inicial NUNCA debe duplicar propiedades. Si
  una propiedad ya existe con la misma identidad de negocio, DEBE actualizarse
  in-place (upsert por clave compuesta).
- **FR-006**: Las marcas temporales (`created_at`, `updated_at`) DEBEN ser
  gestionadas exclusivamente por la base de datos (server-side). La carga inicial
  NUNCA debe enviar `created_at` ni `updated_at` desde Python.
- **FR-007**: Cada propiedad inicial DEBE tener una imagen determinista asociada,
  generada a partir de un identificador o semilla visual estable que garantice la
  misma imagen en cada ejecución.
- **FR-008**: Las migraciones de base de datos DEBEN ser aplicables y reversibles
  en entorno limpio. El ciclo completo `upgrade → downgrade → upgrade` DEBE
  finalizar sin errores.
- **FR-009**: La migración de estructura NO DEBE producir errores por mezcla de
  fechas con y sin zona horaria (naive vs aware).
- **FR-010**: El sistema DEBE contener una carga inicial idempotente de
  exactamente 10 propiedades de prueba ubicadas en Miami, con atributos
  realistas de alquiler residencial.

### Requisitos no funcionales y de gobernanza técnica

Estos requisitos derivan de la constitución del proyecto y de lecciones
aprendidas. No son negociables.

#### Migraciones de base de datos

- **NFR-DB-001**: Cada tipo enumerado del dominio DEBE crearse exactamente una
  vez por evolución de estructura. El enum DEBE declararse como tipo de columna y
  materializarse implícitamente por el DDL de creación de tabla.
- **NFR-DB-002**: Está PROHIBIDO invocar la creación explícita del tipo enum en
  paralelo a su declaración en columna sin desactivar la creación implícita.
- **NFR-DB-003**: El SQL parametrizado dentro de migraciones DEBE ejecutarse
  usando `op.get_bind().execute(sa.text("..."), {...})`. Está PROHIBIDO usar
  `op.execute(sql, params)`.
- **NFR-DB-004**: Los casteos a UUID en SQL parametrizado DEBEN usar
  `CAST(:param AS uuid)`. Está PROHIBIDO usar `:param::uuid` dentro de
  `sa.text`.
- **NFR-DB-005**: Las migraciones DEBEN ser reversibles reales. `downgrade`
  NUNCA puede ser `pass`.
- **NFR-DB-006**: Los timestamps DEBEN ser server-side. Está PROHIBIDO enviar
  `created_at` o `updated_at` desde Python en migraciones o seeds.
- **NFR-DB-007**: El seed DEBE ser idempotente por clave de negocio usando
  `ON CONFLICT (...) DO UPDATE`.
- **NFR-DB-008**: Ante un estado inconsistente del historial de migraciones, la
  recuperación obligatoria es reiniciar el esquema (`DROP SCHEMA public CASCADE`
  + `CREATE SCHEMA public`) y reaplicar `alembic upgrade head`.

#### Dominio y código

- **NFR-CODE-001**: Usar SQLAlchemy 2.x async con `Mapped[...]`,
  `mapped_column` y `AsyncSession`. PROHIBIDO el estilo legacy (`Column`,
  `Query`, sesiones síncronas).
- **NFR-CODE-002**: Los estados de dominio DEBEN modelarse como enum tipado
  usando `StrEnum` y `Enum` de SQLAlchemy. PROHIBIDOS los strings mágicos.
- **NFR-CODE-003**: Los DTOs DEBEN usar Pydantic v2 con
  `model_config = ConfigDict(frozen=True)`.
- **NFR-CODE-004**: El módulo DEBE residir en `app/modules/propiedades/`
  siguiendo Vertical Slice Architecture.
- **NFR-CODE-005**: La lógica de negocio DEBE vivir solo en `service.py`.
  `routes.py` DEBE mantenerse delgado. `repository.py` DEBE limitarse al acceso
  a datos.
- **NFR-CODE-006**: Las funciones de I/O DEBEN ser async. `def` síncrono SOLO
  debe usarse para cómputo puro en memoria.
- **NFR-CODE-007**: No se DEBEN exponer entidades SQLAlchemy como respuesta
  HTTP. Las respuestas se mapean a DTOs Pydantic.

#### Calidad

- **NFR-QA-001**: `ruff check` DEBE finalizar sin hallazgos.
- **NFR-QA-002**: `mypy --strict` NO DEBE reportar errores en
  `app/modules/propiedades/`.
- **NFR-QA-003**: Las pruebas DEBEN usar `pytest`, `pytest-asyncio` y
  `httpx.AsyncClient` cuando aplique.
- **NFR-QA-004**: La plantilla `alembic/script.py.mako` DEBE estar versionada.
- **NFR-QA-005**: Cualquier script auxiliar de base de datos DEBE usar `asyncpg`
  vía `create_async_engine`. PROHIBIDO depender de `psycopg2` o `psycopg`.

### Gobernanza de tokens visuales

- **VTG-001**: Esta feature NO modifica tokens visuales canónicos (colores,
  sombras, radios, espaciados, tipografía, breakpoints).
- **VTG-002**: Esta feature NO modifica templates (`app/templates/`,
  `app/modules/*/templates/`).
- **VTG-003**: Esta feature NO modifica CSS (`app/static/css/app.css`).
- **VTG-004**: Esta feature NO modifica iconografía (`app/static/icons/`).
- **VTG-005**: Esta feature NO modifica componentes compartidos
  (`app/templates/components/`).
- **VTG-006**: Si en fases posteriores se toca algún archivo visual protegido,
  deberá quedar trazado en `tasks.md` con el marcador `[visual]` según la regla
  de blindaje vigente en la constitución sección XII.

### Entidades clave

- **Propiedad**: Entidad central del dominio inmobiliario. Representa un inmueble
  en alquiler con atributos de negocio (título, dirección, ciudad, precio,
  habitaciones, baños, área), un estado operativo controlado por catálogo
  cerrado, una imagen asociada y marcas temporales gestionadas por la base de
  datos. Su identidad de negocio es la combinación única `título + dirección +
  ciudad`.

## Criterios de éxito

- **SC-001**: `alembic upgrade head` sobre `public` recién creado finaliza en
  verde sin intervención manual y sin uso de `alembic stamp`.
- **SC-002**: La carga inicial deja exactamente 10 propiedades de Miami.
- **SC-003**: La carga inicial mantiene exactamente 10 propiedades después de dos
  ejecuciones consecutivas (cardinalidad estable).
- **SC-004**: El 100% de las propiedades iniciales tiene estado dentro del
  catálogo permitido (`disponible`, `rentada`, `mantenimiento`, `inactiva`).
- **SC-005**: El 100% de las propiedades iniciales tiene una imagen asociada con
  semilla estable (misma propiedad → misma imagen en cada ejecución).
- **SC-006**: El ciclo completo `upgrade → downgrade → upgrade` finaliza con
  éxito en el 100% de las ejecuciones de validación.
- **SC-007**: La migración completa no reporta errores por mezcla de fechas naive
  vs aware.
- **SC-008**: `mypy --strict app/modules/propiedades/` no reporta errores.
- **SC-009**: Ningún script auxiliar de base de datos usa `psycopg2` ni
  `psycopg`.
- **SC-010**: La materialización del catálogo de estados no produce conflictos
  por declaración duplicada de tipo enum al aplicar la migración.

## Asunciones

1. **Dataset de prueba**: Las 10 propiedades iniciales se generan como dataset
   realista de prueba con datos sintéticos pero verosímiles de alquiler
   residencial en Miami. No requieren definición manual por parte del usuario.
2. **Precio mensual**: Se expresa como valor decimal (ej. `2500.00`) representando
   dólares estadounidenses.
3. **Área**: Se almacena en pies cuadrados (sq ft), unidad estándar del mercado
   inmobiliario de Miami.
4. **Imagen**: Cada propiedad tiene una URL determinista generada a partir de su
   identificador único (UUID), permitiendo que la misma propiedad siempre
   obtenga la misma imagen sin depender de servicios externos.
5. **Ciudad**: El campo `ciudad` es un atributo abierto de la entidad. El seed
   inicial usa exclusivamente `Miami`, pero el esquema no restringe el valor,
   permitiendo expansión futura a otras ciudades sin cambios de migración.
6. **Distribución de estados**: Las 10 propiedades iniciales se distribuyen entre
   los cuatro estados del catálogo para maximizar el realismo de las pruebas
   (ej. 4 disponibles, 3 rentadas, 2 en mantenimiento, 1 inactiva).
7. **Timestamps**: `created_at` y `updated_at` se definen como columnas con
   `server_default` y `onupdate` en la base de datos. Python nunca envía estos
   valores.
8. **Seed script**: Se implementa como un script independiente usando
   `create_async_engine` + `asyncpg`, ejecutable después de `alembic upgrade
   head`. No es parte de la migración.
9. **UUID**: Las claves primarias usan `uuid.UUID` con `server_default=sa.text
   ("gen_random_uuid()")`.
10. **Migración única**: Se espera exactamente una migración nueva para crear la
    tabla `propiedades` con el enum de estado implícito.

## Trazabilidad de reglas de negocio y restricciones técnicas

| Fuente | Regla | Traza a |
|--------|-------|---------|
| Prompt spec, línea 66-77 | Atributos mínimos de propiedad | FR-001 |
| Prompt spec, línea 78-82 | Catálogo cerrado de estados | FR-002, FR-003 |
| Prompt spec, línea 84-85 | Identidad de negocio del seed | FR-004 |
| Prompt spec, línea 86-88 | Idempotencia y upsert | FR-005 |
| Prompt spec, línea 89-90 | Timestamps server-side | FR-006, NFR-DB-006 |
| Prompt spec, línea 91-92 | Imagen determinista | FR-007 |
| Prompt spec, línea 93 | Reversibilidad de migraciones | FR-008 |
| Prompt spec, línea 94-95 | Fechas naive vs aware | FR-009 |
| Prompt spec, línea 108-133 | Reglas de migraciones DB | NFR-DB-001 a NFR-DB-008 |
| Prompt spec, línea 137-156 | Reglas de dominio y código | NFR-CODE-001 a NFR-CODE-007 |
| Prompt spec, línea 160-163 | Reglas de calidad | NFR-QA-001 a NFR-QA-005 |
| Prompt spec, línea 171-184 | Gobernanza visual | VTG-001 a VTG-006 |
| Constitución sección XII | Blindaje de tokens visuales | VTG-006 |
| Constitución sección II | Stack obligatorio | NFR-CODE-001, NFR-CODE-002 |
| Constitución sección IV | Vertical Slice Architecture | NFR-CODE-004 |
