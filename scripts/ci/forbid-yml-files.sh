#!/bin/bash
set -euo pipefail

files="$(git ls-files '*.yml' ':(exclude).specify/**')"

if [ -n "$files" ]; then
    echo "$files"
    echo 'Usa .yaml, no .yml'
    exit 1
fi
