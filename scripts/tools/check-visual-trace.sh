#!/bin/bash
set -euo pipefail

# ---------------------------------------------------------------------------
# check-visual-trace.sh — Auditoría de trazabilidad visual para features Realtor
#
# Verifica que los cambios en archivos visuales protegidos tengan tareas
# con marcador [visual] en tasks.md de la feature activa.
#
# Uso: bash scripts/tools/check-visual-trace.sh
# Salida: 0 si OK, 1 si hay archivos protegidos sin trazabilidad.
# ---------------------------------------------------------------------------

# Detectar el directorio de la feature activa desde feature.json o branch
REPO_ROOT="$(git rev-parse --show-toplevel)"
FEATURE_JSON="$REPO_ROOT/.specify/feature.json"
BRANCH="$(git branch --show-current)"

if [[ -f "$FEATURE_JSON" ]]; then
  FEATURE_DIR=$(python3 -c "
import json
with open('$FEATURE_JSON') as f:
    d = json.load(f)
print(d.get('feature_directory', ''))
" 2>/dev/null)
fi

if [[ -z "${FEATURE_DIR:-}" ]]; then
  FEATURE_DIR="specs/$BRANCH"
fi

TASKS_FILE="$REPO_ROOT/$FEATURE_DIR/tasks.md"

# Lista de archivos visuales protegidos (patrones compatibles con grep)
PROTECTED_PATTERNS=(
  "app/static/css/app.css"
  "app/templates/base.html"
  "app/templates/components/_.*.html"
  "app/templates/macros/_.*.html"
  "app/static/icons/.*\.svg"
  "app/static/vendor/htmx\.min\.js"
  ".opencode/instructions/frontend\.instructions\.md"
)

# Paso 1: listar cambios commiteados vs main
COMMITTED=$(git diff main...HEAD --name-only 2>/dev/null || true)

# Paso 2: listar archivos nuevos no trackeados
UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null || true)

# Paso 3: listar cambios no commiteados en el árbol de trabajo y en staging
WORKING=$(git diff --name-only HEAD 2>/dev/null || true)

# Unir las tres listas
ALL_CHANGES=$(printf '%s\n%s\n%s\n' "$COMMITTED" "$UNTRACKED" "$WORKING" | sort -u | sed '/^$/d')

# Paso 3: filtrar archivos protegidos
PROTECTED_FOUND=""
for pattern in "${PROTECTED_PATTERNS[@]}"; do
  while IFS= read -r file; do
    if echo "$file" | grep -qE "^${pattern}$"; then
      PROTECTED_FOUND+="$file"$'\n'
    fi
  done <<< "$ALL_CHANGES"
done

PROTECTED_FOUND=$(echo "$PROTECTED_FOUND" | sort -u | sed '/^$/d')

# Paso 4: si no hay archivos protegidos modificados, OK
if [[ -z "$PROTECTED_FOUND" ]]; then
  echo "Sin cambios en archivos visuales protegidos."
  exit 0
fi

# Paso 5: verificar que tasks.md existe
if [[ ! -f "$TASKS_FILE" ]]; then
  echo "tasks.md no encontrado en $FEATURE_DIR."
  echo "Esta feature no tiene tareas declaradas."
  echo ""
  echo "Archivos visuales modificados que requieren trazabilidad:"
  echo "$PROTECTED_FOUND" | while IFS= read -r f; do [[ -n "$f" ]] && echo "  - $f"; done
  exit 1
fi

# Paso 6: buscar marcador [visual] en líneas de tarea
VISUAL_COUNT=$(grep -cE '^- \[[ X]\] .*\[visual\]' "$TASKS_FILE" 2>/dev/null || true)
VISUAL_COUNT=$(echo "$VISUAL_COUNT" | grep -oE '[0-9]+' | head -1)
VISUAL_COUNT="${VISUAL_COUNT:-0}"

if [[ "$VISUAL_COUNT" -eq 0 ]]; then
  echo "Los siguientes archivos visuales fueron modificados sin tareas [visual] en tasks.md:"
  echo "$PROTECTED_FOUND" | while IFS= read -r f; do [[ -n "$f" ]] && echo "  - $f"; done
  echo ""
  echo "Agrega tareas con marcador [visual] en $FEATURE_DIR/tasks.md para cada cambio."
  exit 1
fi

echo "Verificación visual completada: todos los cambios tienen trazabilidad."
exit 0
