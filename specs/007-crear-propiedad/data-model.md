# Data Model: Crear propiedad

**Feature**: 007-crear-propiedad
**Phase**: 1 — Design
**Date**: 2026-06-20

## Resumen

Esta spec **no introduce cambios al modelo de datos**. La entidad `Propiedad`
y el enum `EstadoPropiedad` se mantienen tal como se definieron en spec 004
(`specs/004-propiedades-base/data-model.md`). La feature opera sobre el modelo
existente añadiendo:

1. Una nueva función de servicio (`crear_propiedad_desde_formulario()`) que
   aplica defaults antes de persistir.
2. Un nuevo DTO de entrada de formulario (`PropiedadFormIn`) que valida el
   payload HTTP.
3. Una constraint relajada en `PropiedadIn.area` (`gt=0` → `ge=0,
   default=0`) para permitir `area=0` cuando el formulario lo omite.

## Modelo de datos SQL (sin cambios)

Referencia completa:
[`specs/004-propiedades-base/data-model.md`](../004-propiedades-base/data-model.md).

| Tabla | Columna | Tipo | Nullable | Default | Notas |
|-------|---------|------|----------|---------|-------|
| `propiedades` | `id` | `UUID` | NO | `gen_random_uuid()` | PK, server-side |
| `propiedades` | `titulo` | `VARCHAR(255)` | NO | — | Constraint único junto a `direccion` y `ciudad` |
| `propiedades` | `direccion` | `VARCHAR(255)` | NO | — | Constraint único |
| `propiedades` | `ciudad` | `VARCHAR(100)` | NO | `'Miami'` | Default server-side |
| `propiedades` | `precio_mensual` | `NUMERIC(10, 2)` | NO | — | — |
| `propiedades` | `habitaciones` | `INTEGER` | NO | — | — |
| `propiedades` | `banos` | `INTEGER` | NO | — | — |
| `propiedades` | `area` | `INTEGER` | NO | — | **Constraint modificada** (ver §Cambios) |
| `propiedades` | `estado` | `estado_propiedad` (enum) | NO | — | 4 valores cerrados |
| `propiedades` | `imagen` | `VARCHAR(512)` | NO | — | — |
| `propiedades` | `created_at` | `TIMESTAMPTZ` | NO | `now()` | Server-side |
| `propiedades` | `updated_at` | `TIMESTAMPTZ` | NO | `now()` | Server-side, `onupdate=now()` |

## Cambios sobre el modelo existente

### `PropiedadIn.area`: `gt=0` → `ge=0, default=0`

**Antes** (definido en spec 004):
```python
area: int = Field(gt=0)
```

**Después** (modificado en spec 007):
```python
area: int = Field(ge=0, default=0)
```

**Justificación**: La clarificación 1 de la spec establece que el campo
`area` es opcional en el formulario con default 0 aplicado en el servicio.
Para que el servicio pueda construir el DTO canónico `PropiedadIn` con
`area=0` cuando el usuario omite el campo, la constraint Pydantic debe
aceptar `0`.

**Impacto**:

- Tests existentes que usan `area=850` siguen pasando (850 ≥ 0).
- La semántica del DTO canónico cambia: `area` ya no es estrictamente
  "obligatorio > 0", ahora es "opcional, default 0, ≥ 0".
- La columna `INTEGER NOT NULL` del modelo SQL no se ve afectada (el DB
  sigue requiriendo un entero, solo que ahora puede ser 0).

**Tests nuevos** (cubiertos en `test_schemas.py`):
- `test_area_acepta_cero`: `PropiedadIn(..., area=0)` es válido.
- `test_area_default_cero`: `PropiedadIn(...)` sin `area` usa default 0.

## DTOs Pydantic (nuevos y modificados)

### `PropiedadFormIn` (NUEVO)

DTO de entrada específico para el formulario HTTP. Solo contiene los campos
que el usuario completa en el form.

```python
class PropiedadFormIn(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')

    titulo: str = Field(min_length=1, max_length=255)
    direccion: str = Field(min_length=1, max_length=255)
    precio_mensual: Decimal = Field(gt=0)
    habitaciones: int = Field(ge=1, le=20)
    banos: int = Field(ge=1, le=10)
    area: int = Field(ge=0, default=0)

    @field_validator('titulo', 'direccion', mode='before')
    @classmethod
    def _strip_whitespace(cls, v: object) -> object:
        return v.strip() if isinstance(v, str) else v
```

### `PropiedadIn` (MODIFICADO)

Ver §Cambios arriba. Solo cambia la constraint de `area`.

### `PropiedadOut` (sin cambios)

DTO de salida. Mantiene la firma de spec 004.

## Flujo de datos

```text
┌─────────────────────────────────────────────────────────────────────┐
│ Cliente (navegador)                                                 │
│   GET /propiedades/nueva  →  form HTML                              │
│   POST /propiedades       →  form-encoded body                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ app/modules/propiedades/routes.py                                   │
│                                                                     │
│  GET /nueva  ──→  renderizar crear_propiedad.html                   │
│                    con contexto {form: {}, errores: {}}            │
│                                                                     │
│  POST /       ──→  Form() params como str (W3 fix)                  │
│                    try/except (ValueError, TypeError):              │
│                      - Requeridos: mantener "" → Pydantic error     │
│                      - Opcional area: "" → None → default 0        │
│                    Construir PropiedadFormIn                       │
│                      - ValidationError → re-renderizar con errores │
│                    service.crear_propiedad_desde_formulario()       │
│                      - None (duplicado) → error global __all__      │
│                      - PropiedadOut → cookie flash + 303 /propied..│
│                                                                     │
│  GET /        ──→  service.listar_propiedades()                      │
│                    + leer cookie flash firmada                      │
│                    + delete_cookie en response                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ app/modules/propiedades/service.py                                  │
│                                                                     │
│  crear_propiedad_desde_formulario(session, form)                    │
│    ├─ _generar_url_imagen() → "https://picsum.photos/800/600"       │
│    ├─ Construir PropiedadIn:                                       │
│    │    ciudad = "Miami"                                            │
│    │    estado = EstadoPropiedad.DISPONIBLE                         │
│    │    imagen = _generar_url_imagen()                              │
│    │    area   = form.area                                          │
│    ├─ crear_propiedad(session, propiedad_in) existente              │
│    │    └─ try/except IntegrityError:                               │
│    │         ├─ await session.rollback()                            │
│    │         ├─ logger.warning(...)                                 │
│    │         └─ return None                                         │
│    └─ return PropiedadOut.model_validate(entidad)                   │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ PostgreSQL (modelo spec 004, sin migraciones nuevas)                │
│                                                                     │
│  INSERT INTO propiedades (...)                                      │
│    ON CONFLICT (titulo, direccion, ciudad) DO NOTHING  -- IntegrityError│
└─────────────────────────────────────────────────────────────────────┘
```

## Funciones del repositorio (sin cambios)

| Función | Firma | Estado |
|---------|-------|--------|
| `crear` | `(session, payload: PropiedadIn) -> Propiedad` | Sin cambios (spec 004) |
| `obtener_por_id` | `(session, prop_id: UUID) -> Propiedad \| None` | Sin cambios |
| `listar` | `(session) -> list[Propiedad]` | Sin cambios |
| `eliminar` | `(session, prop_id: UUID) -> bool` | Sin cambios |
| `contar_por_estado` | `(session, estado) -> int` | Sin cambios |
| `contar_total` | `(session) -> int` | Sin cambios |

## Estados de dominio (sin cambios)

`EstadoPropiedad` (spec 004):

| Valor | Significado |
|-------|-------------|
| `disponible` | Default al crear. Listada para renta. |
| `rentada` | Con contrato activo. |
| `mantenimiento` | Fuera de servicio temporalmente. |
| `inactiva` | Retirada del inventario. |

## Constraints únicos (sin cambios)

`uq_propiedades_identidad_negocio` sobre `(titulo, direccion, ciudad)`.
La duplicación de esta constraint genera `IntegrityError` capturado por
`crear_propiedad_desde_formulario()`.

## Índices (sin cambios)

- `ix_propiedades_estado` sobre `estado`.
- `ix_propiedades_ciudad` sobre `ciudad`.
- `ix_propiedades_precio_mensual` sobre `precio_mensual`.

## Migraciones Alembic

**Sin nuevas migraciones**. El modelo SQL es idéntico al de spec 004; solo
se relaja una constraint Pydantic en código Python.

## Relaciones con otras entidades

- `Propiedad` (spec 004): única entidad afectada. Sin cambios estructurales.
- `EstadoPropiedad` (spec 004): enum reutilizado. Estado por defecto al
  crear: `DISPONIBLE`.
- Sin FKs nuevas, sin nuevas tablas, sin migraciones.
