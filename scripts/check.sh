#!/bin/bash
set -euo pipefail
echo "=== Verificaciones de calidad ==="
bash scripts/lint.sh
bash scripts/typecheck.sh
bash scripts/test.sh
echo "=== Todas las verificaciones pasaron ==="
