# Contrato: Dashboard Demo

**Endpoint**: `GET /` | **Feature**: `001-bootstrap-proyecto`

## Request

```
GET / HTTP/1.1
Accept: text/html
```

Sin parámetros, sin body.

## Response — Éxito (200 OK)

**Content-Type**: `text/html; charset=utf-8`

### Estructura del DOM esperada

| Elemento | Selector/Atributo | Origen |
|---|---|---|
| Layout global | `.layout` | `base.html` |
| Sidebar | `.sidebar` | `_sidebar.html` |
| Navbar | `.navbar` | `_navbar.html` |
| Zona flash | `#flash-zone` | `base.html` |
| Tarjeta métrica 1 | `.tarjeta-metrica` | `_tarjeta_metrica.html` |
| Tarjeta métrica 2 | `.tarjeta-metrica` | `_tarjeta_metrica.html` |
| Tarjeta métrica 3 | `.tarjeta-metrica` | `_tarjeta_metrica.html` |
| Accesos rápidos | `.accesos-rapidos` | `_accesos_rapidos.html` |

### Métricas hardcodeadas

| Label | Valor | Icono |
|---|---|---|
| Propiedades activas | 124 | `building-2` |
| Inquilinos al día | 87 | `users` |
| Contratos vigentes | 53 | `file-text` |

### Assets cargados

- CSS: `<link rel="stylesheet" href="/static/css/app.css">`
- JS: `<script src="/static/vendor/htmx.min.js"></script>`
- Iconos: renderizados inline vía macro `icon(nombre, size=24)`

## Comportamiento

1. Sin dependencia de base de datos (datos hardcodeados).
2. Template `dashboard.html` extiende `base.html`.
3. Componentes incluidos con `{% include "components/_nombre.html" %}`.
4. Iconos renderizados con `{% from "macros/icons.html" import icon %}`.
5. Sin logging explícito en el handler.

## Notas

- El dashboard es estático en esta spec. En specs futuras las métricas vendrán
  de consultas a base de datos.
- `base.html` define la estructura sidebar + main + `#flash-zone` que
  reutilizarán todos los módulos.
