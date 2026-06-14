#!/bin/bash 
set -euo pipefail 
uv run pytest \ 
    --cov=app \ 
    --cov-report=term-missing \ 
    --cov-report=html \ 
    --cov-fail-under=80 \ 
    "$@"