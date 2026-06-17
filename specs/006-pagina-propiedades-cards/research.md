# Research: Página de propiedades con cards

**Feature**: 006-pagina-propiedades-cards
**Phase**: 0 — Research
**Date**: 2026-06-16

## Decisiones técnicas investigadas

### 1. Extensión vs. reemplazo del componente `_card_propiedad.html`

**Decisión**: Extender el componente existente agregando nuevos campos como parámetros opcionales, sin modificar su estructura base.

**Alternativas consideradas**:
- Crear `_card_propiedad_grid.html` nuevo: rechazada por duplicación. Dos componentes de card generan divergencia de estilos y mantenimiento doble.
- Reescribir `_card_propiedad.html` completamente: rechazada, rompe el dashboard existente que usa el componente actual.
- Usar herencia de templates Jinja2 (`{% block %}`): sobreingeniería para un solo caso de uso.

**Fundamento**: El componente actual es mínimo (icono, título, detalle, badge, acción). Agregar campos opcionales con `{% if %}` mantiene retrocompatibilidad con el dashboard. La decisión de clarificación confirmó extender el existente.

### 2. Formato de datos: DTO vs. dicts en el servicio

**Decisión**: El servicio `listar_propiedades()` retorna `list[dict]` con strings formateados, no `list[PropiedadOut]`.

**Alternativas consideradas**:
- Retornar `list[PropiedadOut]` y formatear en el template: rechazada. Pone lógica de presentación en Jinja2 (filtros de formato). Viola FR-014 (lógica en servicio).
- Retornar `list[PropiedadOut]` con campos `str` pre-formateados: rechazada. `PropiedadOut` tiene `precio_mensual: Decimal` y `area: int`. Cambiar los tipos rompe el contrato del DTO para otros consumidores.
- Crear `PropiedadCardOut` DTO nuevo: rechazada. YAGNI. Esta vista no es una API JSON; es un contexto interno para Jinja2. Un dict es suficiente (mismo criterio que el dashboard con TypedDict).

**Fundamento**: El patrón ya está establecido en el dashboard (`construir_contexto()` retorna dict formateado para Jinja2). NFR-ARCH-004 exige reutilizar `PropiedadOut` existente, lo cual se cumple (el DTO existe y está disponible). El servicio simplemente elige el formato más adecuado para el template.

### 3. Estrategia de responsive grid

**Decisión**: CSS Grid con `grid-template-columns: repeat(N, 1fr)` y media queries en los breakpoints del sistema (1023px, 767px).

**Alternativas consideradas**:
- Flexbox con `flex-wrap`: rechazada. Requiere width fijo en cada card o cálculos de flex-basis. CSS Grid es más declarativo para grillas de cantidad fija de columnas.
- CSS Grid con `auto-fill` y `minmax()`: considerada pero rechazada. `auto-fill` llena la fila con tantas cards como quepan, lo cual no garantiza exactamente 3/2/1 columnas en los breakpoints. Con `repeat(N, 1fr)` el control es explícito.
- Framework CSS (Bootstrap, Tailwind): rechazada. Prohibido por constitución sección III.

**Fundamento**: `repeat(N, 1fr)` con media queries da control preciso sobre columnas en cada breakpoint, usa tokens existentes (`--space-*` para gaps), y es CSS estándar sin dependencias.

### 4. Placeholder de imagen: estrategia de fallback

**Decisión**: Div con `--color-surface` como fondo + icono `building-2` centrado. Maneja tanto imagen vacía como URL rota (404) con el mismo mecanismo.

**Alternativas consideradas**:
- Imagen por defecto (`/static/img/placeholder.jpg`): rechazada. Requiere mantener un asset estático. El icono SVG es más ligero y coherente con el sistema de iconografía.
- `onerror` en `<img>` para reemplazar src: considerado pero frágil (si el fallback también falla, bucle infinito).
- Solo manejar `imagen == ""` y no URLs rotas: rechazado por clarificación (404 debe mostrar mismo placeholder).
- Ocultar la card si no hay imagen: rechazada. FR-009 exige placeholder que no rompa el layout.

**Fundamento**: Un div contenedor con la imagen como `<img>` interno y un div placeholder debajo (visible solo cuando `imagen` está vacía o el `onerror` del img lo activa). Esto cubre ambos casos (vacío y 404) con un solo mecanismo, usando icono ya vendoreado.

### 5. Formato de precio: locale vs. formato manual

**Decisión**: Formatear manualmente en Python sin depender de `locale`.

**Alternativas consideradas**:
- `locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')` + `locale.currency()`: rechazada. Depende de que el locale esté instalado en el sistema (no garantizado en Docker Alpine). Puede fallar silenciosamente en CI.
- `babel.numbers.format_currency()`: rechazada. Introduce dependencia nueva (NFR-ARCH-005 prohíbe nuevas dependencias).
- Template filter Jinja2 `|format_currency`: rechazada. Lógica de presentación en template (viola FR-014).

**Fundamento**: Formateo manual con `Decimal.quantize(Decimal('0.01'))` y `f"${parte_entera:,}.{parte_decimal:02d}"`. Es determinista, no requiere locale del sistema, y vive en el servicio (FR-014).

### 6. Orden de dependencias entre fases

**Decisión**: Componente (F1) → Template (F2) → Servicio (F3) → Endpoint (F4) → CSS (F6) → Tests (F7-F8).

**Alternativas consideradas**:
- Servicio primero, template después: viable, pero requiere mock mental del template para validar el endpoint.
- CSS primero: rechazada. El CSS es más fácil de validar cuando el HTML ya existe.

**Fundamento**: El orden F1→F2→F3→F4 sigue el flujo natural de construir de atrás hacia adelante (componente → template → datos → endpoint). F6 (CSS) va después de F2 porque necesita el HTML generado para validar visualmente. F5 (sidebar) es independiente. F7-F8 (tests) requieren que F1-F6 estén completos.
