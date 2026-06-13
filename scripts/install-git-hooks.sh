#!/bin/bash
# ---------------------------------------------------------------------------
# install-git-hooks.sh — Instala hooks versionados en .git/hooks/
#
# Copia los hooks desde scripts/hooks/ a .git/hooks/ y hace backup
# de cualquier hook existente con timestamp.
# ---------------------------------------------------------------------------
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOKS_SRC="$REPO_ROOT/scripts/hooks"
HOOKS_DST="$REPO_ROOT/.git/hooks"

echo "Instalador de hooks Git para Realtor"
echo "------------------------------------"
echo ""

installed=0
skipped=0

install_hook() {
  local name="$1"
  local src="$HOOKS_SRC/$name"
  local dst="$HOOKS_DST/${name%%.changelog}"

  if [[ ! -f "$src" ]]; then
    echo "  [❌] $name: fuente no encontrada en $src"
    return
  fi

  if [[ -f "$dst" ]]; then
    if cmp -s "$src" "$dst"; then
      echo "  [⏭]  $name: ya instalado, mismo contenido"
      skipped=$((skipped + 1))
      return
    fi
    local backup="${dst}.backup.$(date +%Y%m%d-%H%M%S)"
    cp "$dst" "$backup"
    echo "  [⚠️]  $name: hook existente respaldado en $(basename "$backup")"
  fi

  cp "$src" "$dst"
  chmod +x "$dst"
  echo "  [✅] $name: instalado"
  installed=$((installed + 1))
}

for hook_file in "$HOOKS_SRC"/*; do
  if [[ -f "$hook_file" ]]; then
    hook_name=$(basename "$hook_file")
    install_hook "$hook_name"
  fi
done

echo ""
echo "Resumen: $installed hook(s) instalado(s), $skipped omitido(s)."
echo ""

if [[ -f "$HOOKS_DST/post-commit" ]]; then
  echo "Para revisar el hook instalado:"
  echo "  cat .git/hooks/post-commit"
fi
