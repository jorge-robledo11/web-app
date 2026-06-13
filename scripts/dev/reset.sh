#!/bin/bash
set -euo pipefail
read -r -p "¿Borrar volumen de datos de PostgreSQL y reiniciar? (s/N): " confirm
if [[ "$confirm" =~ ^[sS]$ ]]; then
  docker compose down -v
  docker compose up -d
  echo "Base de datos reiniciada (volumen eliminado)."
else
  echo "Cancelado."
fi
