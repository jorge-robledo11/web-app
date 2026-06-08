#!/bin/bash
set -euo pipefail
uv run alembic revision --autogenerate -m "$1"
