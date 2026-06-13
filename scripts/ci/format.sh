#!/bin/bash
set -euo pipefail
echo "=== Formateando código ==="
uv run ruff format .
uv run ruff check --fix .
echo "=== Formato OK ==="
