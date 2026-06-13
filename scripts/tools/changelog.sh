#!/bin/bash
# ---------------------------------------------------------------------------
# changelog.sh — Recordatorio post-commit para curar el changelog
#
# Lee información del último commit y muestra un recordatorio para
# ejecutar /changelog. Ya no escribe en ningún buffer intermedio.
#
# Invocado por: .git/hooks/post-commit (→ scripts/hooks/post-commit.changelog)
# ---------------------------------------------------------------------------
set -euo pipefail

HASH_SHORT=$(git show --format=%h --no-patch HEAD 2>/dev/null || echo "???????")
COMMIT_MSG=$(git show --format=%s --no-patch HEAD 2>/dev/null || echo "sin mensaje")

echo "[changelog] Commit detectado: $HASH_SHORT — $COMMIT_MSG"
echo "[changelog] Ejecutá /changelog para curar el changelog."
