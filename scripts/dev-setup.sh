#!/bin/bash
set -euo pipefail
echo "=== Levantando base de datos ==="
bash scripts/db/up.sh
echo "=== Instalando dependencias ==="
uv sync
echo "=== Ejecutando migraciones ==="
bash scripts/db/migrate.sh
echo "=== Setup completado ==="
