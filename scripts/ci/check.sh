#!/bin/bash
set -euo pipefail
echo "=== Verificaciones de calidad ==="
bash scripts/ci/lint.sh
bash scripts/ci/typecheck.sh
bash scripts/ci/test.sh
echo "=== Todas las verificaciones pasaron ==="
