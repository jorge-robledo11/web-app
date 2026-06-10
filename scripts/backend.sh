#!/bin/bash
set -euo pipefail
uv run fastapi dev app/main.py --no-reload
