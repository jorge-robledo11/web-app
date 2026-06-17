# Data Model: Página de propiedades con cards

**Feature**: 006-pagina-propiedades-cards
**Phase**: 1 — Design
**Date**: 2026-06-16

## Contexto del template

El endpoint `GET /propiedades` renderiza `propiedades.html` con el siguiente contexto Jinja2:

| Key | Tipo | Origen | Descripción |
|-----|------|--------|-------------|
| `request` | `Request` | FastAPI | Objeto request (requerido por Jinja2) |
| `propiedades` | `list[dict]` | `service.listar_propiedades()` | Lista de propiedades formateadas para el template |
| `vacio` | `bool` | `len(lista) == 0` | Indica si la página debe mostrar estado vacío |

## Estructura del dict de propiedad

Cada elemento de `propiedades`:

```yaml
- id: string              # UUID de la propiedad
  titulo: string          # Título de la propiedad (truncado a 60 chars con ellipsis)
  direccion: string       # Dirección completa (truncada a 80 chars con ellipsis)
  ciudad: string          # Ciudad (ej. "Miami")
  precio_mensual: string  # Precio formateado "$X,XXX.00"
  habitaciones: integer   # Número de habitaciones
  banos: integer          # Número de baños
  area: string            # Área formateada "X,XXX m²"
  estado: string          # Valor del enum EstadoPropiedad
  imagen: string          # URL de imagen o cadena vacía
  created_at: string      # Fecha ISO 8601
```

## Flujo de datos

```text
┌────────────────────────────────────────────────────────────────┐
│ app/modules/propiedades/                                       │
│                                                                │
│  routes.py               service.py          repository.py    │
│  ┌───────────────┐      ┌────────────────┐   ┌──────────────┐ │
│  │ GET            │      │ listar_        │   │ listar()     │ │
│  │ /propiedades   │ ←────│ propiedades()  │ ←─│              │ │
│  └───────────────┘      └────────────────┘   └──────────────┘ │
│       │                                                       │
│       │ renderiza                                             │
│       ▼                                                       │
│  propiedades.html                                             │
│       │                                                       │
│       │ {% include %}                                         │
│       ▼                                                       │
│  _card_propiedad.html (extendido)                             │
│       │                                                       │
│       │ {% include %}                                         │
│       ▼                                                       │
│  _badge_estado.html (reutilizado)                             │
└────────────────────────────────────────────────────────────────┘
```

## Funciones del repositorio de propiedades (existentes, reutilizadas)

| Función | Firma | Retorno | Uso en esta feature |
|---------|-------|---------|---------------------|
| `listar` | `(session: AsyncSession) -> list[Propiedad]` | Lista de entidades Propiedad | Fuente de datos para el grid |

No se agregan funciones nuevas al repositorio. `listar()` ya existe y retorna todas las propiedades ordenadas por `created_at` descendente.

## Funciones del servicio (nuevas)

| Función | Firma | Retorno | Descripción |
|---------|-------|---------|-------------|
| `listar_propiedades` | `(session: AsyncSession) -> list[dict[str, object]]` | Lista de dicts formateados | Obtiene propiedades del repo, formatea precio y área, mapea a dict |

## Formateo de datos en el servicio

| Campo origen | Tipo origen | Campo destino | Formato |
|-------------|-------------|---------------|---------|
| `precio_mensual` | `Decimal` | `precio_mensual` (str) | `$X,XXX.00` (símbolo, separador miles, 2 decimales) |
| `area` | `int` | `area` (str) | `X,XXX m²` (separador miles, unidad) |
| `id` | `UUID` | `id` (str) | Conversión a string |
| `created_at` | `datetime` | `created_at` (str) | ISO 8601 |

## Estados de la página

| Estado | Condición | Render |
|--------|-----------|--------|
| Normal | `vacio == False` | Grid de cards con `.propiedades-grid` |
| Vacío | `vacio == True` | Mensaje "No hay propiedades registradas" + icono `info` |

## Relaciones con otras entidades

- `Propiedad` (spec 004): entidad fuente de datos. Sin FK nuevas.
- `EstadoPropiedad` (spec 004): enum reutilizado para renderizar badge.
- `PropiedadOut` (spec 004): DTO existente. No se usa directamente en el template (el servicio retorna dicts formateados), pero está disponible si se requiere en el futuro.
- Sin entidades nuevas en esta feature.
