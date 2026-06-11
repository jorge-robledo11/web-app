# Investigación: Blindar tokens visuales canónicos del frontend

**Feature**: `002-blindar-tokens-visuales` | **Date**: 2026-06-10

## 1. Detección de cambios: git diff + archivos no trackeados

- **Decisión**: Combinar `git diff main...HEAD --name-only` (cambios commiteados)
  con `git ls-files --others --exclude-standard` (archivos nuevos no trackeados).
- **Fundamento**: `git diff main...HEAD` solo detecta diferencias entre commits.
  Archivos nuevos no commiteados en carpetas protegidas (ej. un icono agregado en
  `app/static/icons/` sin commit) no serían detectados por diff solo. La unión de
  ambos comandos cubre todos los escenarios. Decisión de las clarificaciones
  ampliada para cubrir el caso de archivos no trackeados.
- **Alternativas descartadas**: `git diff` solo (no detecta archivos nuevos),
  `git status --porcelain` (más verboso, requiere parseo adicional).

## 2. Búsqueda de marcadores en tasks.md

- **Decisión**: Buscar `[visual]` solo en líneas que comienzan con `- [ ]` o `- [X]`.
- **Fundamento**: Decisión de las clarificaciones. Evita falsos positivos en
  comentarios o notas. `grep -E '^- \[[ X]\] .*\[visual\]'` es suficiente.
- **Alternativas descartadas**: Búsqueda en todo el archivo (falsos positivos en
  documentación), búsqueda en encabezados (demasiado permisivo).

## 3. Lista de archivos protegidos

- **Decisión**: El script tiene una lista hardcodeada de patrones de archivos
  visuales sensibles, derivada de la tabla "Definición de cambio visual global"
  en `spec.md`.
- **Fundamento**: La lista es finita y conocida: `app/static/css/app.css`,
  `app/templates/base.html`, `app/templates/components/_*.html`,
  `app/templates/macros/*.html`, `app/static/icons/`,
  `app/static/vendor/htmx.min.js`, `.opencode/instructions/frontend.instructions.md`.
  Un array bash es suficiente sin dependencias externas.
- **Alternativas descartadas**: Archivo de configuración externo (sobre-ingeniería
  para 7 patrones), detección por secciones CSS (requiere parser).

## 4. Comportamiento sin tasks.md

- **Decisión**: Si `tasks.md` no existe, el script retorna 1 con mensaje
  "tasks.md no encontrado. Esta feature no tiene tareas declaradas."
- **Fundamento**: Si no hay `tasks.md`, no puede haber tareas `[visual]`. El
  script debe advertir que la feature está incompleta o en fase temprana.
- **Alternativas descartadas**: Retornar 0 (ignoraría features sin plan),
  advertir sin fallar (no fuerza trazabilidad).

## 5. Formato de salida del script

- **Decisión**: Salida legible con una línea por archivo problemático, más un
  resumen final. Código de salida 0 si todo OK, 1 si hay problemas.
- **Fundamento**: Compatible con uso manual y con integración futura en CI.
  Cada línea muestra el archivo modificado y el marcador esperado.
- **Alternativas descartadas**: Salida JSON (sobre-ingeniería para script manual),
  solo código de salida (no informa qué archivos fallan).

## 6. Integración con make check

- **Decisión**: No integrar en `make check`.
- **Fundamento**: Decisión de las clarificaciones. `make check` ejecuta
  verificaciones de calidad del código actual; `check-visual-trace.sh` audita
  trazabilidad de planificación. Son dominios distintos.
- **Alternativas descartadas**: Integración en `make check` (falsos fallos en
  features sin `tasks.md` completo).
