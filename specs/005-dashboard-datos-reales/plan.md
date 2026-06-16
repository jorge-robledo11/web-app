# Implementation Plan: Dashboard con datos reales

**Branch**: `005-dashboard-datos-reales` | **Date**: 2026-06-15 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/005-dashboard-datos-reales/spec.md`

## Summary

Reemplazar las métricas hardcodeadas del dashboard principal por datos reales
desde la base de datos. Implementar el slice vertical `app/modules/dashboard/`
que consulte el repositorio de `propiedades` para obtener conteos por estado,
construya el contexto de la home y sirva el endpoint `GET /`. Las métricas de
ingresos y vencidos permanecen no operativas (valor `0`, marcador "No
disponible"). El estado vacío se activa cuando la tabla `propiedades` no
contiene filas.

## Technical Context

**Language/Version**: Python 3.13.13
**Primary Dependencies**: FastAPI, SQLAlchemy 2.x async, Jinja2, Pydantic v2
**Storage**: PostgreSQL vía Docker Compose (tabla `propiedades` existente)
**Testing**: pytest + pytest-asyncio + httpx.AsyncClient + Testcontainers
**Target Platform**: Linux server (desarrollo local con Docker)
**Project Type**: web-service (monolito FastAPI + Jinja2/HTMX)
**Performance Goals**: Sin requerimientos de latencia estrictos; consultas de conteo simples
**Constraints**: Sin endpoints nuevos, sin dependencias nuevas, sin cambios visuales
**Scale/Scope**: 1 módulo nuevo, 1 función nueva en repo existente, ~4 archivos modificados

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Regla | Estado | Evidencia |
|-------|--------|-----------|
| II. Stack: Python 3.13.13, uv, FastAPI, SQLAlchemy async, Pydantic v2 | ✅ | plan usa stack canónico |
| II. Stack: asyncpg para PostgreSQL | ✅ | repositorio usa AsyncSession |
| III. Prohibiciones: sin strings mágicos para estados | ✅ | usa `EstadoPropiedad` enum de spec 004 |
| III. Prohibiciones: sin exponer entidades SQLAlchemy | ✅ | servicio retorna dicts para Jinja2, no entidades |
| IV. Vertical Slice: módulo en `app/modules/dashboard/` | ✅ | `routes.py`, `service.py`, `repository.py`, `schemas.py` |
| VIII. TDD: pruebas primero | ✅ | tests unitarios (servicio mockeado) + integración (seed → render) |
| X. Base de datos: PostgreSQL local, Alembic | ✅ | sin migraciones nuevas en esta feature |
| XI. Async-First: I/O asíncrono | ✅ | todas las funciones de I/O son `async def` |
| XII. Blindaje visual: sin modificar tokens protegidos | ✅ | VTG-001 a VTG-006; cambio en `dashboard.html` limitado a datos |
| XIV. Contratos: DTOs con `frozen=True` | ✅ | schemas Pydantic cuando aporten claridad |
| V. Flujo Spec Kit | ✅ | `/speckit.specify` → `/speckit.clarify` → `/speckit.plan` |

## Project Structure

### Documentation (this feature)

```text
specs/005-dashboard-datos-reales/
├── spec.md              # Especificación funcional
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── checklists/
│   └── requirements.md  # Checklist de calidad
├── contracts/           # Phase 1 output
│   └── dashboard.yaml   # Contrato actualizado del endpoint GET /
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
app/modules/dashboard/         # NUEVO: slice vertical del dashboard
├── __init__.py
├── routes.py                 # GET / — endpoint delgado, invoca servicio y renderiza
├── schemas.py                # DTOs de contexto (opcional, si aportan claridad)
├── service.py                # Lógica de negocio: calcular métricas, armar contexto
├── repository.py             # Acceso a datos: consultas de conteo a propiedades
└── templates/                # Sin templates propios (usa app/templates/dashboard.html)

app/modules/propiedades/
├── repository.py             # MODIFICADO: agregar contar_por_estado()

app/
├── main.py                   # MODIFICADO: eliminar lógica de dashboard, registrar router

app/templates/
├── dashboard.html            # MODIFICADO: reflejar métricas reales y estado vacío

tests/
├── unit/
│   └── dashboard/            # NUEVO
│       └── test_service.py   # Pruebas unitarias del servicio (repo mockeado)
└── integration/
    └── dashboard/            # NUEVO
        └── test_dashboard.py # Pruebas de integración: seed → GET / → métricas reales
```

**Structure Decision**: El módulo `dashboard` sigue vertical slice estándar. El acceso a
datos de `propiedades` se hace a través del repositorio existente
(`contar_por_estado()`), sin duplicar modelos ni consultas directas a la tabla.

## Fases de implementación

### Fase 0 — Preparación y lectura de contexto

1. Leer el endpoint actual `GET /` en `app/main.py` para identificar todos los
   valores hardcodeados.
2. Leer el template `dashboard.html` y el componente `_tarjeta_metrica.html`
   para confirmar que `tendencia` es opcional.
3. Leer el contrato `specs/003-redisenar-home/contracts/dashboard.yaml`.
4. Leer el repositorio de `propiedades` para planificar la función
   `contar_por_estado()`.

### Fase 1 — Extender repositorio de propiedades

Agregar `contar_por_estado(session, estado: EstadoPropiedad) -> int` y
`contar_total(session) -> int` en `app/modules/propiedades/repository.py`.

- `contar_por_estado`: `SELECT count(*) FROM propiedades WHERE estado = :estado`
- `contar_total`: `SELECT count(*) FROM propiedades`
- Ambas usan `AsyncSession`, `select(func.count())` y `.scalar_one()`.
- Sin modificar modelos, schemas ni routes de `propiedades`.

### Fase 2 — Crear módulo dashboard

Crear `app/modules/dashboard/` con la estructura mínima:

| Artefacto | Responsabilidad |
|-----------|----------------|
| `__init__.py` | Vacío o con docstring del módulo |
| `repository.py` | `obtener_metricas(session) -> dict` — invoca `contar_por_estado` y `contar_total` del repo de propiedades |
| `service.py` | `construir_contexto(session) -> dict` — orquesta el repo, construye listas `metricas`, `accesos`, `actividad`, determina `vacio` |
| `schemas.py` | Solo si se necesitan DTOs tipados; por defecto la salida es un dict compatible con Jinja2 |
| `routes.py` | `GET /` — recibe `Request` y `AsyncSession`, invoca `service.construir_contexto()`, renderiza `dashboard.html` |

**Flujo de datos**:

```text
GET / → routes.dashboard(request, session)
  → service.construir_contexto(session)
    → repo.dashboard.obtener_metricas(session)
      → repo.propiedades.contar_por_estado(session, DISPONIBLE)
      → repo.propiedades.contar_por_estado(session, RENTADA)
      → repo.propiedades.contar_total(session)
    → service construye:
        metricas: [
          {label: "Propiedades disponibles", valor: N, icono: "building-2"},
          {label: "Propiedades rentadas", valor: N, icono: "check-circle-2"},
          {label: "Ingresos", valor: 0, marcador: "No disponible", icono: "wallet"},
          {label: "Vencidos", valor: 0, marcador: "No disponible", icono: "clock"},
        ]
        vacio: True/False (contar_total == 0)
  → routes renderiza dashboard.html o estado_vacio
```

**Decisión sobre schemas.py**: Las métricas son dicts simples compatibles con
el contrato existente. No se requiere un DTO Pydantic para el contexto a menos
que el tipado estático lo justifique. Si se crea, debe usar
`model_config = ConfigDict(frozen=True)`.

### Fase 3 — Migrar GET / a app/modules/dashboard/routes.py

1. Crear `app/modules/dashboard/routes.py` con:
   - `router = APIRouter(tags=["dashboard"])`
   - `@router.get("/", response_class=HTMLResponse)`
   - `async def dashboard(request: Request, session: SessionDep)`
2. En `app/main.py`:
   - Eliminar la función `dashboard()` y los datos hardcodeados.
   - Importar y registrar el router: `app.include_router(dashboard_router)`.
   - Conservar `health`, `lifespan`, `StaticFiles` y `templates` (los usa el
     módulo dashboard vía `templates.get_template` o inyección).

### Fase 4 — Estado vacío del dashboard

1. El servicio retorna `vacio: True` cuando `contar_total()` retorna `0`.
2. Si `vacio` es `True`, `routes.py` renderiza un template o parcial de estado
   vacío con un mensaje descriptivo.
3. El estado vacío puede implementarse como:
   - Una condición en `dashboard.html` (`{% if vacio %}`).
   - O un partial Jinja2 en `app/templates/components/_dashboard_vacio.html`.

### Fase 5 — Actualizar template dashboard.html

Cambios mínimos en `app/templates/dashboard.html`:

1. Mantener el bucle `{% for metrica in metricas %}` — el contrato no cambia.
2. Si la métrica tiene `marcador` (no operativa), mostrarlo debajo del valor
   en `_tarjeta_metrica.html` o directamente en el loop de `dashboard.html`.
3. Agregar bloque condicional para estado vacío al inicio del bloque `content`.
4. La sección de accesos rápidos permanece idéntica.
5. La sección de actividad reciente permanece idéntica (datos hardcodeados).

### Fase 6 — Pruebas

#### Pruebas unitarias (`tests/unit/dashboard/test_service.py`)

- Mock del repositorio de propiedades (`contar_por_estado`, `contar_total`).
- `test_construir_contexto_con_datos`: verifica que disponibles y rentadas
  reflejan los valores del mock.
- `test_construir_contexto_sin_propiedades`: verifica `vacio: True`.
- `test_construir_contexto_solo_disponibles`: rentadas = 0, no vacío.
- `test_construir_contexto_solo_rentadas`: disponibles = 0, no vacío.
- `test_metricas_no_operativas`: verifica que ingresos y vencidos tienen
  valor `0` y marcador "No disponible".
- `test_orden_metricas`: verifica el orden fijo (disponibles, rentadas,
  ingresos, vencidos).

#### Pruebas de integración (`tests/integration/dashboard/test_dashboard.py`)

- Requieren PostgreSQL vía Testcontainers + seed de propiedades.
- `test_dashboard_metricas_reales`: ejecuta seed → `GET /` → verifica que el
  HTML contiene los conteos reales (4 disponibles, 3 rentadas).
- `test_dashboard_estado_vacio`: base de datos sin propiedades → `GET /` →
  verifica mensaje de estado vacío.
- `test_dashboard_metricas_no_operativas`: verifica `0` y "No disponible" en
  el HTML.
- `test_dashboard_orden_secciones`: verifica `.metricas` < `.accesos-rapidos`
  < `.actividad`.
- `test_dashboard_accesos_rapidos`: verifica 4 items sin cambios.

#### Actualización de tests existentes

`tests/unit/test_dashboard.py` debe actualizarse porque los valores
hardcodeados (`124`, `87`, `53`, "Propiedades activas", "+8%") ya no
existirán. Los tests deben adaptarse para verificar métricas reales o moverse
a `tests/integration/dashboard/`.

## Riesgos técnicos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Romper el contrato de contexto al cambiar métricas | Baja | Alto | El dict `metricas` conserva las keys `label`, `valor`, `icono`, `tendencia`, `estado`. `tendencia` se omite, lo cual ya soporta el template |
| Consultas ineficientes al contar por estado | Baja | Bajo | Dos `SELECT count(*) ... WHERE estado = ?` más un `SELECT count(*)` son consultas simples con índice `ix_propiedades_estado` |
| Tests existentes fallan por valores hardcodeados | Alta | Medio | Se actualizan o migran a tests de integración; la spec lo prevé explícitamente |
| Estado vacío no distingue BD caída de inventario vacío | Baja | Medio | `GET /health` ya cubre conectividad. Si la consulta falla, se captura con try/except y se renderiza estado de error |
| Módulo dashboard acoplado a detalles de propiedades | Baja | Medio | El repo de dashboard solo invoca funciones públicas del repo de propiedades; no importa `Propiedad` directamente |
| Modificar accidentalmente archivos visuales protegidos | Baja | Alto | Solo se modifica `dashboard.html` (cambios de datos, no de estructura). `base.html`, CSS e iconos no se tocan |

## Gobernanza visual

Esta feature **modifica únicamente `app/templates/dashboard.html`** para reflejar
datos reales. Los cambios son exclusivamente de contenido, no de estructura
visual:

| Archivo protegido | ¿Modificado? | Justificación |
|-------------------|-------------|---------------|
| `app/static/css/app.css` | ❌ No | Sin cambios |
| `app/static/icons/` | ❌ No | Iconos usados ya existen en el set vendoreado |
| `app/templates/base.html` | ❌ No | Sin cambios |
| `app/templates/components/_tarjeta_metrica.html` | ❌ No | Ya soporta `tendencia` opcional |
| `app/templates/components/_accesos_rapidos.html` | ❌ No | Sin cambios |
| `app/templates/components/_actividad_item.html` | ❌ No | Sin cambios |
| `app/templates/macros/icons.html` | ❌ No | Sin cambios |
| `app/templates/dashboard.html` | ✅ Sí | Solo para reflejar métricas reales, marcador "No disponible" y estado vacío. Sin cambios de layout, estilos ni estructura |

El cambio en `dashboard.html` no requiere marcador `[visual]` porque no altera
tokens visuales canónicos, estructura de layout ni patrones de diseño. Es un
cambio de datos dentro del contrato existente.

## Complexity Tracking

> No se registran desviaciones de la constitución. Todas las reglas se cumplen.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | — | — |

## Contratos

El contrato existente en `specs/003-redisenar-home/contracts/dashboard.yaml`
requiere revisión. Si se actualiza, debe reflejar:

- `metricas`: 4 elementos en orden fijo (disponibles, rentadas, ingresos,
  vencidos).
- `tendencia`: campo opcional que las métricas reales omiten.
- `marcador`: campo nuevo en métricas no operativas con valor
  `"No disponible"`.
- `vacio`: nuevo key en el contexto que indica estado vacío.

Si no se actualiza el contrato, el plan igualmente es válido porque el template
ya itera sobre `metricas` dinámicamente.

## Próxima fase

`/speckit.analyze @.opencode/prompts/005-dashboard-datos-reales.analyze.prompt.md`
