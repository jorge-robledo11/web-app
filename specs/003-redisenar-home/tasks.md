# Tasks: Rediseñar Home principal

**Feature**: `003-redisenar-home` | **Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Diagrama de dependencias

```
Fase 1 (Setup)
  T1.1, T1.2
    │
    ▼
Fase 2 (US1 — Métricas P1)
  T2.1 ──► T2.2 ──► T2.3
    │
    ▼
Fase 3 (US2 — Accesos rápidos P2)
  T3.1 ──► T3.2 ──► T3.3
    │
    ▼
Fase 4 (US3 — Actividad reciente P3)
  T4.1 ──► T4.2 ──► T4.3
    │
    ▼
Fase 5 (Polish)
  T5.1 ──► T5.2 ──► T5.3 ──► T5.4, T5.5
```

**Estrategia**: TDD obligatorio. Cada fase empieza con una prueba que falle (Red), luego se implementa el código mínimo (Green), luego se refina (Refactor). Las fases 2, 3 y 4 son independientes entre sí y pueden implementarse en paralelo si se desea.

---

## Fase 1: Setup

### T1.1 [P1] Agregar iconos Lucide `clock` y `calendar`

**Archivos**: `app/static/icons/clock.svg`, `app/static/icons/calendar.svg`

**Verificación**: Los archivos SVG existen en `app/static/icons/`, son SVG outline válidos de Lucide (24x24, trazo 2px, `currentColor`), y son legibles por la macro `icon()`.

**Trazabilidad visual**: `[visual][extension]` — nuevos iconos en directorio protegido.

---

### T1.2 [P1] Agregar datos mock de actividad reciente en el endpoint `GET /`

**Archivo**: `app/main.py`

**Verificación**: El endpoint `GET /` expone las variables `accesos` y `actividad` en el contexto del template además de `metricas`. Los datos coinciden con los definidos en `data-model.md`: 4 accesos rápidos y 3 ítems de actividad con tipos propiedad, contrato y pago.

---

## Fase 2: US1 — Métricas con estados visuales (P1)

### T2.1 [P1] [US1] Test: verificar estados de carga y error en tarjeta de métrica

**Archivo**: `app/tests/test_dashboard.py`

**Verificación**: El test carga `GET /` con métricas en estado `"carga"` y verifica que el HTML contiene `class="tarjeta-metrica is-loading"`. Otro test con estado `"error"` verifica `class="tarjeta-metrica is-error"`. Un tercer test verifica que con estado `"datos"` NO están presentes las clases de carga ni error.

---

### T2.2 [P1] [US1] [visual][extension] Extender `_tarjeta_metrica.html` con estados de carga y error

**Archivo**: `app/templates/components/_tarjeta_metrica.html`

**Cambios**:
- Nuevo prop `estado` con valores `"datos"`, `"carga"`, `"error"` (default `"datos"`)
- Clase modificadora `.is-loading` o `.is-error` en el wrapper según el estado
- Sub-elemento `.tarjeta-metrica__estado-carga` con skeleton o spinner CSS
- Sub-elemento `.tarjeta-metrica__estado-error` con mensaje e icono `alert-circle`
- Sub-elemento `.tarjeta-metrica__estado-datos` envolviendo el contenido normal

**Verificación**: Tests de T2.1 pasan. El componente existente (sin estado) sigue funcionando por retrocompatibilidad (default `"datos"`).

**Trazabilidad visual**: `[visual][extension]` — extensión de componente compartido existente. No modifica tokens canónicos. Reutiliza `_badge_estado.html` e `_alerta.html` sin cambios.

---

### T2.3 [P1] [US1] [visual] Agregar CSS para estados de carga y error en métricas

**Archivo**: `app/static/css/app.css` (sección Componentes)

**Cambios**:
- `.tarjeta-metrica__estado-carga` — skeleton/spinner con `currentColor` y opacidad
- `.tarjeta-metrica__estado-error` — mensaje centrado con icono `alert-circle`
- `.tarjeta-metrica__estado-datos` — wrapper del contenido normal
- `.tarjeta-metrica.is-loading .tarjeta-metrica__estado-carga` — visible
- `.tarjeta-metrica.is-loading .tarjeta-metrica__estado-datos` — oculto
- `.tarjeta-metrica.is-error .tarjeta-metrica__estado-error` — visible
- `.tarjeta-metrica.is-error .tarjeta-metrica__estado-datos` — oculto

**Verificación**: Los tests de T2.1 verifican la presencia de las clases CSS en el HTML renderizado. Inspección visual confirma que solo un estado es visible a la vez.

**Trazabilidad visual**: `[visual]` — nuevos estilos en `app.css` sección Componentes. Todos los colores provienen de tokens `:root`. Sin modificar tokens canónicos.

---

## Fase 3: US2 — Accesos rápidos con mejora visual (P2)

### T3.1 [P2] [US2] Test: verificar sección de accesos rápidos

**Archivo**: `app/tests/test_dashboard.py`

**Verificación**: El test carga `GET /` y verifica que existe `<section class="accesos-rapidos">` con al menos 4 tarjetas `<a class="acceso-rapido">`. Cada tarjeta contiene un icono Lucide y un texto de label. Los `href` son `"#"`.

---

### T3.2 [P2] [US2] [visual] Mejorar `_accesos_rapidos.html`

**Archivo**: `app/templates/components/_accesos_rapidos.html`

**Cambios**:
- Iconos de 24px → 28px (`{{ icon(acceso.icono, size=28) }}`)
- Mejor espaciado entre icono y label (usar `--space-2` en gap)

**Verificación**: Test de T3.1 pasa. Inspección visual confirma iconos más prominentes y mejor separación.

**Trazabilidad visual**: `[visual]` — modificación de componente compartido existente. Sin cambios estructurales.

---

### T3.3 [P2] [US2] [visual] Agregar CSS de mejora visual de accesos rápidos

**Archivo**: `app/static/css/app.css` (sección Componentes)

**Cambios**:
- `.acceso-rapido__icono` — tamaño 28px, color `--color-accent`
- `.acceso-rapido` — gap `--space-2` entre icono y label

**Verificación**: Inspección visual. Los iconos usan `currentColor` heredado de `--color-accent`.

**Trazabilidad visual**: `[visual]` — ajustes en sección Componentes. Sin modificar tokens `:root`.

---

## Fase 4: US3 — Actividad reciente (P3)

### T4.1 [P3] [US3] Test: verificar sección de actividad reciente

**Archivo**: `app/tests/test_dashboard.py`

**Verificación**:
- Test con datos: carga `GET /` y verifica que existe al menos 3 elementos `class="actividad-item"` con `class="actividad-item__tipo"`, descripción y fecha.
- Test con estado vacío: verifica `class="actividad--empty"` y el mensaje «Aún no hay actividad registrada».
- Test con estado error: verifica `class="actividad--error"` y mensaje «No se pudo cargar la actividad reciente».

---

### T4.2 [P3] [US3] [visual][componente] Crear `_actividad_item.html`

**Archivo**: `app/templates/components/_actividad_item.html` (nuevo)

**Props**:
- `tipo`: `"propiedad" | "contrato" | "pago"`
- `descripcion`: string
- `fecha`: string
- `badge_variante`: `"success" | "warning" | "danger" | "accent" | "info" | "muted"`
- `estado`: `"datos" | "vacio" | "error"` (default `"datos"`)

**Estructura**:
- Wrapper `.actividad-item`
- Badge de tipo usando `_badge_estado.html` (reutilización del componente existente)
- Descripción en `.actividad-item__descripcion`
- Fecha en `.actividad-item__fecha`

**Verificación**: Tests de T4.1 pasan.

**Trazabilidad visual**: `[visual][componente]` — nuevo componente compartido en `app/templates/components/`.

---

### T4.3 [P3] [US3] [visual] Agregar CSS de sección de actividad

**Archivo**: `app/static/css/app.css` (sección Componentes)

**Cambios**:
- `.actividad` — contenedor de la sección, borde superior sutil con `--color-border`
- `.actividad--empty` — estado vacío centrado con icono `info`
- `.actividad--error` — estado error con mensaje
- `.actividad-item` — tarjeta horizontal con badge + texto
- `.actividad-item__tipo` — badge de tipo de actividad
- `.actividad-item__descripcion` — texto principal
- `.actividad-item__fecha` — texto secundario en `--color-text-muted`

**Verificación**: Inspección visual. Los badges usan colores de `_badge_estado.html`. Sin hardcodear colores.

**Trazabilidad visual**: `[visual]` — nuevos estilos en sección Componentes.

---

## Fase 5: Polish e integración

### T5.1 [P1-P3] [visual] Reorganizar `dashboard.html` con orden vertical fijo

**Archivo**: `app/templates/dashboard.html`

**Cambios**:
- Sección de métricas (primero)
- Sección de accesos rápidos (segundo)
- Sección de actividad reciente (tercero)
- Cada sección recibe sus datos del contexto: `metricas`, `accesos`, `actividad`

**Verificación**: `curl -s http://localhost:8000/ | grep -o '<section'` muestra 3 secciones en el orden correcto.

**Trazabilidad visual**: `[visual]` — reorganización del template principal. Extiende `base.html` sin modificarlo.

---

### T5.2 [P1-P3] [visual] Ajustar CSS responsive para las 3 secciones

**Archivo**: `app/static/css/app.css` (sección Responsive)

**Cambios**:
- Desktop (> 1023px): métricas 3 columnas, accesos 4 columnas, actividad 1 columna
- Tablet (≤ 1023px): métricas 2 columnas, accesos 2 columnas, actividad 1 columna
- Móvil (≤ 767px): métricas 1 columna, accesos 2 columnas, actividad 1 columna

**Verificación**: Redimensionar viewport en DevTools. Sin overflow horizontal en 360px. Las 3 secciones son legibles en todos los breakpoints.

**Trazabilidad visual**: `[visual]` — ajustes en sección Responsive. Sin modificar tokens `:root`.

---

### T5.3 Integración: tests de la Home completa

**Archivo**: `app/tests/test_dashboard.py`

**Verificación**:
- `GET /` retorna 200
- El HTML contiene las 3 secciones en orden: `.metricas`, `.accesos-rapidos`, `.actividad`
- Las métricas incluyen tendencias (texto y dirección)
- Los accesos rápidos tienen 4 tarjetas cliqueables
- La actividad tiene 3 ítems con badge, descripción y fecha
- Los estados de carga y error son verificables manualmente

---

### T5.4 [visual] Validar gobernanza visual

**Comando**: `make visual-check`

**Verificación**: `make visual-check` retorna exit 0. Todas las tareas con cambios en archivos protegidos tienen el marcador `[visual]` correspondiente en este `tasks.md`.

**Trazabilidad visual**: confirmación de que los marcadores `[visual]`, `[visual][extension]` y `[visual][componente]` cubren todos los archivos afectados.

---

### T5.5 Verificar accesibilidad del nuevo componente

**Archivos**: `app/templates/components/_actividad_item.html`, `app/static/css/app.css`

**Verificación**:
- Badges tienen `aria-label` descriptivo (ej. `"Tipo: propiedad"`)
- Estados de carga/error tienen `role="status"`
- Contraste AA en texto sobre fondo de badges (`--color-accent`, `--color-warning`, `--color-success`, `--color-danger`)
- Los enlaces de accesos rápidos son navegables por teclado (foco visible)

---

## Resumen

| Fase | Tareas | User Stories | Marcadores visuales |
|------|--------|-------------|---------------------|
| Fase 1 (Setup) | T1.1, T1.2 | — | `[visual][extension]` |
| Fase 2 (Métricas) | T2.1–T2.3 | US1 (P1) | `[visual][extension]`, `[visual]` |
| Fase 3 (Accesos) | T3.1–T3.3 | US2 (P2) | `[visual]` |
| Fase 4 (Actividad) | T4.1–T4.3 | US3 (P3) | `[visual][componente]`, `[visual]` |
| Fase 5 (Polish) | T5.1–T5.5 | US1–US3 | `[visual]` |

**Total**: 16 tareas en 5 fases. Cada fase sigue TDD: prueba primero, implementación después, refactor al final.

### Tareas con trazabilidad visual

| Marcador | Tareas |
|----------|--------|
| `[visual][extension]` | T1.1, T2.2 |
| `[visual][componente]` | T4.2 |
| `[visual]` | T2.3, T3.2, T3.3, T4.3, T5.1, T5.2, T5.4 |

**Siguiente paso**: `/speckit.implement`

---

## Verificación de trazabilidad visual

- [X] T1.1 [visual][extension] Agregar iconos Lucide `clock` y `calendar` en `app/static/icons/`
- [X] T2.2 [visual][extension] Extender `_tarjeta_metrica.html` con estados de carga y error en `app/templates/components/`
- [X] T2.3 [visual] Agregar CSS para estados de carga y error en `app/static/css/app.css`
- [X] T3.2 [visual] Mejorar `_accesos_rapidos.html` con iconos 28px y espaciado en `app/templates/components/`
- [X] T3.3 [visual] Agregar CSS de mejora visual de accesos rápidos en `app/static/css/app.css`
- [X] T4.2 [visual][componente] Crear `_actividad_item.html` en `app/templates/components/`
- [X] T4.3 [visual] Agregar CSS de sección de actividad en `app/static/css/app.css`
- [X] T5.1 [visual] Reorganizar `dashboard.html` con orden vertical fijo en `app/templates/`
- [X] T5.2 [visual] Ajustar CSS responsive para las 3 secciones en `app/static/css/app.css`
- [X] T5.4 [visual] Validar gobernanza visual con `make visual-check`
