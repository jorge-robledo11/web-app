# Modelo de Datos: Blindar tokens visuales canónicos del frontend

**Feature**: `002-blindar-tokens-visuales` | **Date**: 2026-06-10

## Resumen

Esta spec de gobernanza no define entidades de base de datos. Los "datos" que
maneja son archivos del sistema de archivos y marcadores textuales en
documentos Markdown.

## 1. Archivos protegidos (entidades de gobernanza)

| Archivo | Categoría | Marcador requerido |
|---|---|---|
| `app/static/css/app.css` | Tokens CSS | `[visual]` |
| `app/templates/base.html` | Layout base | `[visual]` |
| `app/templates/components/_*.html` | Componentes compartidos | `[visual]` o `[visual][componente]` |
| `app/templates/macros/*.html` | Macros | `[visual]` |
| `app/static/icons/*.svg` | Iconografía | `[visual]` |
| `app/static/vendor/htmx.min.js` | HTMX vendoreado | `[visual]` |
| `.opencode/instructions/frontend.instructions.md` | Instrucciones visuales | `[visual][instrucción]` |

## 2. Marcadores visuales (valores del dominio)

| Marcador | Significado | Cuándo usarlo |
|---|---|---|
| `[visual]` | Cambio visual global genérico | Modificación de tokens, layout, macros |
| `[visual][extension]` | Nuevo token sin modificar existentes | Agregar variable CSS, componente, breakpoint |
| `[visual][bugfix]` | Corrección de bug visual | Contraste, accesibilidad, regresión |
| `[visual][componente]` | Nuevo componente compartido | Agregar archivo en `app/templates/components/` |
| `[visual][instrucción]` | Cambio en instrucciones visuales | Modificar `frontend.instructions.md` |

## 3. Script check-visual-trace.sh (flujo de datos)

```
git diff main...HEAD --name-only
        │
        ▼
┌─────────────────────────┐
│ Lista de archivos       │
│ modificados en la feature│
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│ ¿Hay archivos           │   │ Lista hardcodeada de    │
│ protegidos modificados? │──▶│ archivos sensibles      │
└───────────┬─────────────┘   └─────────────────────────┘
            │
      ┌─────┴─────┐
      ▼           ▼
     Sí          No
      │           │
      ▼           ▼
┌──────────┐  ┌──────────┐
│ ¿tasks.md│  │ exit 0   │
│ tiene    │  │ Sin      │
│ [visual]?│  │ cambios  │
└──┬───┬───┘  └──────────┘
   │   │
   ▼   ▼
  Sí   No
   │   │
   ▼   ▼
exit 0 exit 1
OK      FALLA
```

## 4. Notas

- Esta spec no crea tablas, modelos ni esquemas de base de datos.
- Los marcadores `[visual]` son texto plano en `tasks.md`, no requieren parser.
- El script es stateless: no persiste estado entre ejecuciones.
