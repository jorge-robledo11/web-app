#!/bin/bash
# ---------------------------------------------------------------------------
# sync-agent-models.sh — Sincroniza modelos de agentes desde config/models.yaml
#
# Lee el catálogo de modelos en config/models.yaml y actualiza los campos
# `model:` en el frontmatter de cada agente listado en la sección `usage:`.
# ---------------------------------------------------------------------------
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
YAML_FILE="$REPO_ROOT/config/models.yaml"
AGENTS_DIR="$REPO_ROOT/.opencode/agent"

echo "Sincronizando modelos de agentes desde config/models.yaml"
echo "----------------------------------------------------------"
echo ""

python3 -c "
import yaml
import os
import re
import sys

yaml_file = os.environ.get('YAML_FILE', '$YAML_FILE')
agents_dir = os.environ.get('AGENTS_DIR', '$AGENTS_DIR')

with open(yaml_file) as f:
    data = yaml.safe_load(f)

# Construir diccionario de alias: 'opencode_go.flash' → 'opencode-go/deepseek-v4-flash'
aliases = {}
for provider, models in data.items():
    if provider == 'usage':
        continue
    for alias, model_id in models.items():
        aliases[f'{provider}.{alias}'] = model_id

if not aliases:
    print('[❌] No se encontraron definiciones de modelos en config/models.yaml')
    sys.exit(1)

updated = 0
skipped = 0
errors = 0

for agent_name, ref in data.get('usage', {}).items():
    model_id = aliases.get(ref)
    if not model_id:
        print(f'[❌] {agent_name}: referencia \\\"{ref}\\\" no resuelta en el catálogo')
        errors += 1
        continue

    agent_file = os.path.join(agents_dir, f'{agent_name}.md')
    if not os.path.exists(agent_file):
        print(f'[❌] {agent_name}: archivo \\\"{agent_file}\\\" no encontrado')
        errors += 1
        continue

    with open(agent_file) as f:
        content = f.read()

    new_content = re.sub(
        r'^model: .*$',
        f'model: {model_id}',
        content,
        count=1,
        flags=re.MULTILINE
    )

    if new_content == content:
        print(f'[⏭]  {agent_name}: ya actualizado ({model_id})')
        skipped += 1
    else:
        with open(agent_file, 'w') as f:
            f.write(new_content)
        print(f'[✅] {agent_name}: {model_id}')
        updated += 1

print()
print(f'Resumen: {updated} actualizado(s), {skipped} sin cambios, {errors} error(es).')

if errors > 0:
    sys.exit(1)
"
