#!/bin/bash
set -euo pipefail
if [[ -z "${1:-}" ]]; then
  echo "Uso: $0 <nombre-de-la-migración>" >&2
  exit 1
fi
uv run alembic revision --autogenerate -m "$1"
