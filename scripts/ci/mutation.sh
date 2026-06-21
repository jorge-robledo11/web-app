#!/bin/bash
# Ejecuta mutation testing focalizado con mutmut.
# Política: corre primero la suite de tests para confirmar verde, luego
# genera mutantes. No elimina tests ni aplica mutantes automáticamente.
# Las salidas viven en `mutants/` (declarado en `.gitignore`).
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"
mkdir -p mutants
uv run pytest -q
uv run mutmut run "$@"
