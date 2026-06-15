#!/bin/bash
set -euo pipefail

coverage_file="$(mktemp "${TMPDIR:-/tmp}/coverage.XXXXXX")"
export COVERAGE_FILE="$coverage_file"

trap 'rm -f "$coverage_file"' EXIT

uv run pytest \
    --cov=app \
    --cov-report=term-missing \
    --cov-fail-under=80 \
    "$@"
