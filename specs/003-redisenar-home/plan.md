# Implementation Plan: Rediseñar Home principal

**Branch**: `003-redisenar-home` | **Date**: 2026-06-13 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-redisenar-home/spec.md`

## Summary

Rediseñar la Home principal (`GET /`) del sistema Realtor reorganizando el contenido
en tres secciones verticales (Métricas → Accesos rápidos → Actividad reciente),
extendiendo dos componentes compartidos existentes, creando uno nuevo y agregando
estados visuales (carga, error, vacío) como clases CSS estructurales. La Home se
sirve vía server-rendering tradicional con datos hardcodeados, sin endpoints HTMX
asíncronos nuevos. No se modifican tokens visuales canónicos ni `base.html`.

## Technical Context

**Language/Version**: Python 3.13+

**Primary Dependencies**: FastAPI, Jinja2, HTMX (vendoreado), SQLAlchemy 2.x async

**Storage**: N/A (datos hardcodeados en endpoint `GET /`)

**Testing**: pytest + httpx.AsyncClient (endpoint tests) + CSS validation manual

**Target Platform**: Web (desktop-first, responsive a tablet 1023px y móvil 767px)

**Project Type**: Web application (server-rendered Jinja2 + HTMX)

**Performance Goals**: Renderizado server-side < 500ms (datos hardcodeados, sin I/O de BD)

**Constraints**: Sin endpoints HTMX nuevos, sin nuevos archivos CSS, sin modificar tokens `:root`

**Scale/Scope**: 3 secciones, ~100 líneas nuevas de CSS, 1 componente nuevo, 2 componentes extendidos

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| Idioma español | ✅ | Todo el contenido en español |
| Stack obligatorio | ✅ | FastAPI + Jinja2 + HTMX, sin frameworks CSS |
| Vertical Slice | ✅ | Cambios en `app/main.py` (endpoint existente) |
| Spec-Driven | ✅ | Spec 003 aprobada con clarificaciones |
| TDD | ✅ | Tests antes de implementación |
| Ruff + mypy strict | ✅ | Solo `app/main.py` modificado (pasa sin errores) |
| Sin Supabase, CDN, webfonts | ✅ | Sin dependencias externas nuevas |
| Gobernanza visual (XII) | ✅ | Marcadores `[visual]` requeridos, sin modificar tokens canónicos |
| Prohibiciones | ✅ | Sin CSS framework, sin `pip`, sin `.yml` |

## Project Structure

### Documentation (this feature)

```text
specs/003-redisenar-home/
├── plan.md              # This file
├── research.md          # Phase 0: estados visuales, CSS patterns, componentes
├── data-model.md        # Phase 1: estructuras de datos para las 3 secciones
├── quickstart.md        # Phase 1: cómo probar y verificar
├── contracts/           # Phase 1: contratos visuales
│   ├── dashboard.yaml   # Contrato del endpoint GET /
│   └── estados.yaml     # Contrato de estados visuales por componente
└── tasks.md             # Phase 2 (generado por /speckit.tasks)
```

### Source Code (repository root)

```text
app/
├── main.py                          # Modificar: endpoint GET / con 3 secciones
├── templates/
│   ├── base.html                    # Sin cambios
│   ├── dashboard.html               # Modificar: reorganizar en 3 secciones
│   └── components/
│       ├── _tarjeta_metrica.html    # Extender: estados carga/error (tendencia ya soportada)
│       ├── _accesos_rapidos.html    # Extender: mejora visual de jerarquía
│       ├── _actividad_item.html     # NUEVO: ítem de actividad reciente
│       ├── _alerta.html             # Reutilizar (sin cambios)
│       ├── _badge_estado.html       # Reutilizar (sin cambios)
│       └── _card_propiedad.html     # Sin cambios
├── static/
│   ├── css/app.css                  # Modificar: sección Componentes y Responsive
│   └── icons/                       # Extender: nuevos iconos para actividad
│       ├── clock.svg                # NUEVO
│       └── calendar.svg             # NUEVO
```

**Structure Decision**: No se crean nuevos módulos. El rediseño es un cambio en el endpoint existente `GET /` y en los templates y CSS existentes. No requiere estructura de módulo nueva.

## Complexity Tracking

No se registran desviaciones de la constitución. El plan cumple con todas las reglas:

- Stack inmutable: sin nuevas dependencias
- Vertical Slice: sin nuevos módulos, solo modificación de endpoint existente
- Gobernanza visual: todos los cambios visuales tendrán marcadores `[visual]` en tasks.md
- Sin frameworks CSS: todo el CSS nuevo en `app.css` sección Componentes
- Sin CDN: iconos nuevos vendoreados en `app/static/icons/`

## Riesgos técnicos

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| El componente `_tarjeta_metrica.html` ya tiene soporte de tendencia (props `tendencia`, `direccion`, `texto`). La extensión es solo para estados de carga/error | Bajo | El delta real son ~20 líneas de template para los nuevos estados |
| Los iconos Lucide nuevos (`clock`, `calendar`, `arrow-up-right`) requieren descarga manual si la API de Lucide falla | Bajo | Crear manualmente como se hizo con `check-circle-2`, `alert-triangle`, `alert-circle` |
| La sección de actividad reciente con 3 tipos mezclados puede generar confusión visual sin un diseño claro de badge por tipo | Medio | Definir badge por tipo en el contrato de estados (propiedad=accent, contrato=warning/danger, pago=success) |
| Los estados de carga/error son solo CSS, no hay datos reales que los activen | Bajo | Los tests verifican las clases CSS presentes en el template, no comportamiento asíncrono |

## Archivos visuales protegidos afectados

| Archivo | Marcador requerido | Tipo de cambio |
|---------|-------------------|----------------|
| `app/static/css/app.css` | `[visual]` | Nuevos estilos en sección Componentes y Responsive |
| `app/templates/dashboard.html` | `[visual]` | Reorganización en 3 secciones |
| `app/templates/components/_tarjeta_metrica.html` | `[visual][extension]` | Estados de carga y error (tendencia ya implementada) |
| `app/templates/components/_accesos_rapidos.html` | `[visual]` | Mejora de jerarquía visual |
| `app/templates/components/_actividad_item.html` | `[visual][componente]` | Nuevo componente compartido |
| `app/static/icons/` | `[visual][extension]` | Nuevos iconos Lucide |
