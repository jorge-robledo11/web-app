#!/bin/bash
set -euo pipefail
mkdir -p docs/context
npx repomix@latest --output docs/context/repo-state.xml
