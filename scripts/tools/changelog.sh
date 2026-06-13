#!/bin/bash
# ---------------------------------------------------------------------------
# changelog.sh — Registro mecánico post-commit en el buffer técnico
#
# Captura hash, fecha, rama, mensaje, archivos y diff stat del último commit
# y agrega una entrada en docs/context/.changelog-pending.md.
#
# Invocado por: .git/hooks/post-commit (→ scripts/hooks/post-commit.changelog)
# ---------------------------------------------------------------------------
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
PENDING_FILE="$REPO_ROOT/docs/context/.changelog-pending.md"

# Asegurar que el directorio existe
mkdir -p "$(dirname "$PENDING_FILE")"

# Asegurar que el archivo existe con el encabezado mínimo
if [[ ! -f "$PENDING_FILE" ]]; then
  cat > "$PENDING_FILE" <<'HEADER'
# Changelog pending

Este archivo contiene entradas mecánicas generadas por el hook `post-commit`.

No es el changelog final del proyecto.

El changelog curado vive en:

```text
CHANGELOG.md
```

---

## Pending

HEADER
fi

# Leer información del último commit (solo lectura)
HASH_SHORT=$(git show --format=%h --no-patch HEAD 2>/dev/null || echo "???????")
COMMIT_MSG=$(git show --format=%s --no-patch HEAD 2>/dev/null || echo "sin mensaje")
COMMIT_DATE=$(git show --format=%ad --date=iso-strict --no-patch HEAD 2>/dev/null || echo "sin fecha")
BRANCH=$(git branch --show-current 2>/dev/null || echo "desconocida")

# Archivos cambiados y diff stat (solo si hay un commit padre)
FILES=""
STAT=""
if git rev-parse HEAD~1 >/dev/null 2>&1; then
  FILES=$(git show --name-status --format= HEAD 2>/dev/null | sed 's/^/  - `/; s/$/`/' || true)
  STAT=$(git show --stat --format= HEAD 2>/dev/null | tail -1 | sed 's/^[[:space:]]*//' || true)
else
  FILES="  - \`(commit inicial)\`"
  STAT="(commit inicial)"
fi

if [[ -z "$FILES" ]]; then
  FILES="  - \`(sin archivos detectados)\`"
fi

# Construir la entrada del changelog pendiente
write_entry() {
  printf '\n'
  printf '### %s — %s\n' "$HASH_SHORT" "$COMMIT_DATE"
  printf '\n'
  printf -- '- Branch: `%s`.\n' "$BRANCH"
  printf -- '- Message: `%s`.\n' "$COMMIT_MSG"
  printf -- '- Files:\n'
  printf '%s\n' "$FILES"
  printf -- '- Stat: `%s`.\n' "$STAT"
  printf -- '- Suggested category: _(pendiente de revisión)_.\n'
  printf -- '- Suggested entry: _(pendiente de revisión)_.\n'
  printf -- '- Commit message quality: _(pendiente de revisión)_.\n'
  printf -- '- Suggested commit message: _(pendiente de revisión)_.\n'
  printf -- '- Notes:\n'
  printf -- '  - Entrada mecánica generada por `scripts/tools/changelog.sh`.\n'
  printf -- '  - Revisar con `/changelog`.\n'
}

# Insertar entrada después del marcador "## Pending"
TEMP_FILE=$(mktemp)
inserted=false

while IFS= read -r line || [[ -n "$line" ]]; do
  printf '%s\n' "$line" >> "$TEMP_FILE"
  if [[ "$line" == "## Pending" ]] && [[ "$inserted" == false ]]; then
    write_entry >> "$TEMP_FILE"
    inserted=true
  fi
done < "$PENDING_FILE"

if [[ "$inserted" == false ]]; then
  printf '\n## Pending\n' >> "$TEMP_FILE"
  write_entry >> "$TEMP_FILE"
fi

mv "$TEMP_FILE" "$PENDING_FILE"

# Contar entradas pendientes y mostrar recordatorio
PENDING_COUNT=$(grep -c '^### ' "$PENDING_FILE" 2>/dev/null || echo "0")
PENDING_COUNT=$(echo "$PENDING_COUNT" | grep -oE '[0-9]+' | head -1)
PENDING_COUNT="${PENDING_COUNT:-0}"

echo "[changelog] Entrada registrada: $HASH_SHORT — $COMMIT_MSG"
if [[ "$PENDING_COUNT" -eq 1 ]]; then
  echo "[changelog] 1 commit pendiente de revisión. Ejecutá /changelog para curar."
else
  echo "[changelog] $PENDING_COUNT commits pendientes de revisión. Ejecutá /changelog para curar."
fi
