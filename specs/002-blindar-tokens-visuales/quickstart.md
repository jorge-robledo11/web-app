# Guía de Validación Rápida: Blindar tokens visuales canónicos del frontend

**Feature**: `002-blindar-tokens-visuales` | **Date**: 2026-06-10

## Prerrequisitos

- Git (ya instalado)
- Bash
- Proyecto Realtor clonado con al menos la spec `001-bootstrap-proyecto` en `main`

## Setup

```bash
# Verificar que estamos en la rama de la feature
git branch --show-current
# Esperado: 002-blindar-tokens-visuales
```

## Validación del script

```bash
# 1. Verificar que el script existe y es ejecutable
ls -l scripts/check-visual-trace.sh
# Esperado: permisos -rwxr-xr-x

# 2. Ejecutar en una feature sin cambios visuales (esta misma)
bash scripts/check-visual-trace.sh
echo "Código de salida: $?"
# Esperado: 0 (esta spec no modifica archivos visuales)

# 3. Simular un cambio visual sin trazabilidad
echo "/* test */" >> app/static/css/app.css
bash scripts/check-visual-trace.sh
echo "Código de salida: $?"
# Esperado: 1 (app.css modificado sin tareas [visual])

# 4. Restaurar
git checkout app/static/css/app.css
```

## Validación de artefactos de gobernanza

```bash
# Verificar que la constitución tiene la regla de blindaje
grep -c "Blindaje de tokens" .specify/memory/constitution.md
# Esperado: 1

# Verificar que AGENTS.md referencia los tokens protegidos
grep -c "tokens visuales canónicos" AGENTS.md
# Esperado: 1

# Verificar que el template de specs tiene la sección de impacto visual
grep -c "Impacto visual" .specify/templates/spec-template.md
# Esperado: 1
```

## Validación de calidad

```bash
# El script debe pasar shellcheck (si está instalado)
shellcheck scripts/check-visual-trace.sh || echo "shellcheck no instalado, omitiendo"

# ruff no debe encontrar problemas nuevos
uv run ruff check .
```

## Limpieza

No requiere limpieza. Esta spec no crea contenedores, volúmenes ni archivos
temporales.
