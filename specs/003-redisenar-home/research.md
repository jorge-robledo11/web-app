# Research: Rediseñar Home principal

**Feature**: `003-redisenar-home` | **Phase**: 0

## 1. Estados visuales en componentes server-rendered

### Problema

La spec exige estados de carga, error y vacío para las secciones de la Home,
pero los datos son hardcodeados y el renderizado es server-side síncrono.
No hay operaciones asíncronas que produzcan estados intermedios reales.

### Solución adoptada

Implementar los estados como **clases CSS estructurales** en los templates,
no como comportamiento asíncrono real:

```jinja2
<div class="tarjeta-metrica is-loading">
  <!-- skeleton/spinner visible -->
</div>
<div class="tarjeta-metrica is-error">
  <!-- mensaje de error visible -->
</div>
```

Los tests verifican la presencia de las clases en el HTML renderizado,
no su activación dinámica. Esto es preparación para specs futuras cuando
los datos sean reales.

### Patrón CSS

```css
.tarjeta-metrica__estado-carga { display: none; }
.tarjeta-metrica__estado-error { display: none; }
.tarjeta-metrica__estado-datos { display: block; }

.tarjeta-metrica.is-loading .tarjeta-metrica__estado-carga { display: flex; }
.tarjeta-metrica.is-loading .tarjeta-metrica__estado-datos { display: none; }
.tarjeta-metrica.is-error .tarjeta-metrica__estado-error { display: flex; }
.tarjeta-metrica.is-error .tarjeta-metrica__estado-datos { display: none; }
```

## 2. Componente `_tarjeta_metrica.html` — extensión

### Estado actual

Ya soporta tendencia opcional (`tendencia.direccion`, `tendencia.texto`).

### Extensión requerida

Agregar estructura de template para estados de carga y error:

- Nuevo bloque condicional `.tarjeta-metrica__estado-carga` con skeleton
- Nuevo bloque condicional `.tarjeta-metrica__estado-error` con mensaje e icono
- Clase modificadora `.is-loading` / `.is-error` en el wrapper

### Props actuales

```jinja2
{ label, valor, icono, tendencia: { direccion, texto } }
```

### Props después de la extensión

```jinja2
{ label, valor, icono, tendencia: { direccion, texto }, estado: "datos"|"carga"|"error" }
```

## 3. Componente `_accesos_rapidos.html` — mejora visual

### Estado actual

Grid de tarjetas con icono, label y URL. Sin estados.

### Mejora requerida

- Iconos más prominentes (24px → 28px)
- Mejor jerarquía visual (espaciado entre icono y label)
- Sin cambios de estructura ni estados (datos hardcodeados)

## 4. Componente `_actividad_item.html` — nuevo

### Diseño

Cada ítem muestra:
- Badge de tipo (Propiedad → accent, Contrato → warning/danger, Pago → success)
- Descripción corta
- Fecha relativa
- Icono opcional por tipo

### Props

```jinja2
{ tipo: "propiedad"|"contrato"|"pago", descripcion: str, fecha: str, badge_variante: str }
```

### Estados

- Datos: render normal
- Vacío: mensaje «Aún no hay actividad registrada» con icono
- Error: mensaje «No se pudo cargar la actividad reciente»

## 5. Iconos Lucide nuevos

Se requieren 2 iconos adicionales para la sección de actividad reciente:

| Icono | Uso | Archivo |
|-------|-----|---------|
| `clock` | Fecha/hora en items de actividad | `clock.svg` |
| `calendar` | Sección de actividad (encabezado) | `calendar.svg` |

**Estrategia**: descargar de https://lucide.dev/icons o crear manualmente si la API falla
(patrón usado en spec 001 para `check-circle-2`, `alert-triangle`, `alert-circle`).

## 6. CSS — cambios en `app.css`

### Sección Componentes (nuevo)

- `.tarjeta-metrica.is-loading` / `.is-error` — estados de carga y error
- `.tarjeta-metrica__estado-carga` — skeleton/spinner
- `.tarjeta-metrica__estado-error` — mensaje + icono de error
- `.tarjeta-metrica__tendencia--up` / `--down` / `--neutral` — colores de tendencia
- `.acceso-rapido__icono` — tamaño 28px
- `.actividad` — grilla de items de actividad
- `.actividad-item` — tarjeta de actividad con badge + descripción + fecha
- `.actividad-item__tipo` — badge por tipo de actividad
- `.actividad--empty` / `.actividad--error` — estados vacío y error

### Sección Responsive (actualizar)

- `.metricas` — grid: 3 cols desktop, 2 cols ≤1023px, 1 col ≤767px
- `.accesos-rapidos__grid` — grid: 4 cols desktop, 2 cols ≤1023px, 2 cols ≤767px
- `.actividad` — grid: 1 col siempre, items en fila

### Reglas de gobernanza

- Todos los colores de `currentColor` o tokens `--color-*` de `:root`
- Sin nuevos tokens en `:root` (solo extensión de clases)
- Sin modificar valores existentes de tokens
