# Plan de implementación: Página de propiedades con cards

**Feature**: 006-pagina-propiedades-cards
**Spec**: [spec.md](./spec.md)
**Created**: 2026-06-16

## Constitution Check

Verificación de reglas constitucionales obligatorias antes de implementar.

| Regla | Estado | Evidencia |
|-------|--------|-----------|
| Vertical slice (IV) | ✅ | Extiende `app/modules/propiedades/` existente; no crea módulo nuevo |
| Stack obligatorio (II) | ✅ | FastAPI + Jinja2 + SQLAlchemy async + Pydantic v2 |
| Async-first (XI) | ✅ | `routes.py`, `service.py`, `repository.py` async; formato síncrono permitido |
| Prohibiciones (III) | ✅ | Sin frameworks CSS, sin CDN, sin `pip`, sin legacy SQLAlchemy |
| Spec-driven (V) | ✅ | `spec.md` aprobado; `clarify` completado |
| TDD (VIII) | ✅ | Fases 7-8: tests antes de código de producción |
| Separación de capas (IV) | ✅ | `routes.py` delgado, `service.py` lógica, `repository.py` datos |
| Gobernanza visual (XII) | ✅ | VTG-001 a VTG-007 declarados; extensiones con `[visual][extension]` |

## Estructura del proyecto

### Archivos a modificar

| Archivo | Cambio |
|---------|--------|
| `app/modules/propiedades/routes.py` | Reemplazar placeholder `# pragma: no cover` con endpoint `GET /propiedades` |
| `app/modules/propiedades/service.py` | Agregar `listar_propiedades(session)` que obtiene, formatea y retorna datos para template |
| `app/templates/components/_card_propiedad.html` | Extender con imagen, habitaciones, baños, área, precio y estado |
| `app/templates/components/_sidebar.html` | Cambiar `href="#"` → `href="/propiedades"` en el enlace "Propiedades" |
| `app/static/css/app.css` | Agregar clases para `.propiedades-grid`, `.card-propiedad` extendida y responsive |

### Archivos a crear

| Archivo | Propósito |
|---------|-----------|
| `app/modules/propiedades/templates/propiedades.html` | Template server-rendered de la página de propiedades |

### Archivos no modificados

- `app/main.py` — el router ya está registrado
- `app/templates/base.html` — sin cambios
- `app/templates/components/_navbar.html` — sin cambios
- `app/modules/propiedades/models.py` — sin cambios
- `app/modules/propiedades/repository.py` — `listar()` ya existe y es suficiente
- `app/modules/propiedades/schemas.py` — `PropiedadOut` ya es suficiente

## Fases de implementación

### Fase 0: Lectura de contexto
- T0.1: Leer `spec.md`, `plan.md` y decisiones de clarificación
- T0.2: Leer instrucciones de backend, frontend, database y tests

### Fase 1: Extender `_card_propiedad.html` [visual][extension]
- Agregar bloque de imagen con fallback a placeholder (fondo + icono `building-2`)
- Agregar campos: habitaciones, baños, área (m²), precio (`$X,XXX.00`), badge de estado
- Agregar ellipsis CSS para textos largos en título y dirección
- El componente acepta todos los campos como parámetros opcionales (retrocompatible)

### Fase 2: Crear template `propiedades.html` [visual][extension]
- Extender `base.html`
- Grid de cards con `{% for %}` iterando propiedades del contexto
- Estado vacío: mensaje "No hay propiedades registradas" + icono `info`
- Sin links en las cards (divs estáticos, según clarificación)

### Fase 3: Agregar `listar_propiedades()` en `service.py`
- Función async que recibe `AsyncSession`
- Invoca `repository.listar(session)` del repositorio existente
- Formatea cada `Propiedad` a dict con los 8 campos requeridos
- Formato de precio: `$X,XXX.00`
- Formato de área: `X,XXX m²`
- Retorna `list[dict]` lista para el template

### Fase 4: Implementar endpoint `GET /propiedades` en `routes.py`
- Eliminar `# pragma: no cover` del placeholder
- Definir `@router.get('', response_class=HTMLResponse)` (el router ya tiene `prefix='/propiedades'`)
- Inyectar `AsyncSession` vía `Depends(get_session)`
- Llamar a `service.listar_propiedades(session)`
- Renderizar `propiedades.html` con el contexto `{'propiedades': [...], 'request': request, 'vacio': len == 0}`
- Configurar `Jinja2Templates` usando `get_paths()` del path manager (`paths.templates_dir`, `paths.static_dir`), mismo patrón que `dashboard/routes.py`

### Fase 5: Actualizar navegación lateral
- Cambiar `href="#"` → `href="/propiedades"` en `_sidebar.html`
- Un solo cambio de atributo; sin modificar estructura ni estilos

### Fase 6: Agregar CSS [visual][extension]
- `.propiedades-grid`: CSS Grid con `grid-template-columns: repeat(3, 1fr)`, gap con `--space-6`
- `.card-propiedad`: extender estilos existentes con `.card-propiedad__imagen`, `.card-propiedad__datos`, `.card-propiedad__precio`, `.card-propiedad__area`
- `.card-propiedad__imagen-placeholder`: fondo `--color-surface`, icono centrado
- Responsive:
  - `max-width: 1023px` → 2 columnas
  - `max-width: 767px` → 1 columna
- Ellipsis: `.card-propiedad__titulo`, `.card-propiedad__direccion` con `text-overflow: ellipsis; overflow: hidden; white-space: nowrap`

### Fase 7: Tests unitarios
- `tests/unit/propiedades/test_service_listar.py`:
  - Mock `repository.listar()` con propiedades de prueba
  - Verificar que `listar_propiedades()` retorna lista de dicts con los 8 campos
  - Verificar formato de precio (`$1,500.00`)
  - Verificar formato de área (`1,000 m²`)
  - Verificar lista vacía retorna `[]`

### Fase 8: Tests de integración
- `tests/integration/propiedades/test_routes.py` (nuevo) o extender existente:
  - `GET /propiedades` retorna 200 con HTML y layout base
  - El HTML contiene `.card-propiedad` por cada propiedad del seed (10)
  - Cada card contiene los 8 campos visibles
  - `GET /propiedades` con BD sin propiedades muestra estado vacío
  - `GET /propiedades` muestra placeholder para propiedad sin imagen
- `tests/integration/propiedades/test_sidebar.py` (nuevo):
  - Verificar que `GET /` contiene `href="/propiedades"` en el sidebar

### Fase 9: Calidad
- `ruff check .` y `ruff format --check .` sin hallazgos
- `mypy --strict app/modules/propiedades/` sin errores
- `pytest tests/unit/propiedades tests/integration/propiedades -q` todos verdes
- `pytest --cov=app/modules/propiedades --cov-fail-under=80`

## Contrato de contexto del template

El endpoint `GET /propiedades` pasa este contexto a `propiedades.html`:

```yaml
contexto:
  request:
    type: Request
    source: fastapi
  propiedades:
    type: list[dict]
    required: true
    items:
      id: str
      titulo: str
      direccion: str
      ciudad: str
      precio_mensual: str       # formateado "$X,XXX.00"
      habitaciones: int
      banos: int
      area: str                 # formateado "X,XXX m²"
      estado: str               # valor del enum
      imagen: str               # URL o cadena vacía
      created_at: str           # ISO format
  vacio:
    type: bool
```

## Gobernanza visual

| Marcador | Archivo | Justificación |
|----------|---------|---------------|
| `[visual][extension]` | `_card_propiedad.html` | Nuevos campos (imagen, datos, badge) sin modificar estructura base ni tokens |
| `[visual][extension]` | `app.css` | Nuevas clases `.propiedades-grid`, `.card-propiedad__*` usando tokens existentes |
| `[visual][extension]` | `propiedades.html` | Nuevo template que extiende `base.html` sin modificar layout global |

Sin modificación de tokens visuales canónicos. Sin cambios en `base.html`, `_navbar.html` ni iconografía.

## Complexity Tracking

Sin desviaciones de la constitución. Todas las reglas aplicables verificadas en Constitution Check.
