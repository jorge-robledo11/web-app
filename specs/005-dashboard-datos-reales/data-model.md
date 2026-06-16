# Data Model: Dashboard con datos reales

**Feature**: 005-dashboard-datos-reales
**Phase**: 1 — Design
**Date**: 2026-06-15

## Contexto del template

El endpoint `GET /` renderiza `dashboard.html` con el siguiente contexto Jinja2:

| Key | Tipo | Origen | Descripción |
|-----|------|--------|-------------|
| `request` | `Request` | FastAPI | Objeto request (requerido por Jinja2) |
| `metricas` | `list[dict]` | `service.construir_contexto()` | Métricas renderizadas en tarjetas KPI |
| `accesos` | `list[dict]` | Hardcodeado en servicio | Accesos rápidos (sin cambios vs spec 003) |
| `actividad` | `list[dict]` | Hardcodeado en servicio | Actividad reciente demo (sin cambios vs spec 003) |
| `actividad_estado` | `str` | Hardcodeado `"datos"` | Estado visual de la sección de actividad |
| `vacio` | `bool` | `contar_total() == 0` | Indica si el dashboard debe mostrar estado vacío |

## Estructura del dict de métrica

Cada elemento de `metricas`:

```yaml
- label: string          # Texto descriptivo (ej. "Propiedades disponibles")
  valor: integer         # Número a mostrar (0 para métricas no operativas)
  icono: string          # Nombre del icono Lucide en app/static/icons/
  tendencia: dict|null   # Opcional. Omitido en métricas reales sin histórico.
    direccion: string    # "up" | "down"
    texto: string        # Ej. "+8% vs mes anterior"
  marcador: string|null  # Nuevo. "No disponible" en métricas no operativas.
  estado: string         # "datos" | "carga" | "error". Default "datos".
```

## Métricas definidas

| # | Label | Fuente | Icono | Tendencia | Marcador |
|---|-------|--------|-------|-----------|----------|
| 1 | Propiedades disponibles | `count(*) WHERE estado='disponible'` | `building-2` | — | — |
| 2 | Propiedades rentadas | `count(*) WHERE estado='rentada'` | `check-circle-2` | — | — |
| 3 | Ingresos | Hardcodeado `0` | `wallet` | — | `No disponible` |
| 4 | Vencidos | Hardcodeado `0` | `clock` | — | `No disponible` |

## Flujo de datos entre módulos

```text
┌─────────────────────────────────────────────────────────────┐
│ app/modules/dashboard/                                      │
│                                                             │
│  routes.py                 service.py        repository.py │
│  ┌──────────┐    dict     ┌───────────┐    ┌─────────────┐ │
│  │ GET /    │ ←────────── │ construir │ ←── │ obtener_    │ │
│  │dashboard │             │ _contexto │    │ metricas()  │ │
│  └──────────┘             └───────────┘    └──────┬──────┘ │
│       │                                            │        │
│       │ renderiza                                  │ invoca │
│       ▼                                            ▼        │
│  dashboard.html                          ┌────────────────┐│
│                                          │ propiedades/   ││
│                                          │ repository.py  ││
│                                          │                ││
│                                          │ contar_por_    ││
│                                          │ estado(estado) ││
│                                          │ contar_total() ││
│                                          └────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## Funciones del repositorio de propiedades (nuevas)

| Función | Firma | Retorno | SQL equivalente |
|---------|-------|---------|-----------------|
| `contar_por_estado` | `(session, estado: EstadoPropiedad) -> int` | Cantidad de propiedades con ese estado | `SELECT count(*) FROM propiedades WHERE estado = ?` |
| `contar_total` | `(session) -> int` | Cantidad total de propiedades | `SELECT count(*) FROM propiedades` |

Ambas usan `select(func.count()).select_from(Propiedad)` con `.scalar_one()`.

## Estados del dashboard

| Estado | Condición | Render |
|--------|-----------|--------|
| Normal | `vacio == False` | 4 tarjetas de métrica + accesos rápidos + actividad demo |
| Vacío | `vacio == True` | Mensaje centrado: "No hay datos disponibles" |
| Error | Excepción en consulta | `try/except` en routes.py → renderiza `actividad_estado: "error"` |

## Relaciones con otras entidades

- `Propiedad` (spec 004): fuente de datos para métricas de disponibles y
  rentadas. Sin relación de FK desde dashboard.
- `EstadoPropiedad` (spec 004): enum reutilizado para filtrar conteos.
- Sin entidades nuevas en esta feature.
