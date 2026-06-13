#!/bin/bash
set -euo pipefail
uv run mypy --strict app/modules/
