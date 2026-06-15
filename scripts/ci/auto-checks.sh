#!/bin/bash
set -euo pipefail

tmp_log="$(mktemp)"

cleanup() {
	rm -f "$tmp_log"
}

trap cleanup EXIT

if @uv run pre-commit run --all-files > "$tmp_log" 2>&1; then
	cat "$tmp_log"
	exit 0
fi

uv run pre-commit run --all-files
