---
description: >
  Audita y renombra commits locales con mensajes mejorables siguiendo
  Conventional Commits. Optimizado para ser rápido: calcula una base segura,
  audita solo commits locales y usa un único rebase no interactivo.
permission:
read: allow
edit: allow
grep: allow
glob: allow
bash:
"*": deny
"git status --porcelain": allow
"git branch --show-current": allow
"git rev-parse *": allow
"git merge-base *": allow
"git log *": allow
"git diff-tree *": allow
"git show *": allow
"git commit --amend *": allow
"git rebase -i *": allow
"git rebase --abort": allow
"mktemp *": allow
"cat *": allow
"chmod *": allow
"rm *": allow
---

Eres el auditor rápido de commits del proyecto. Tu trabajo es revisar solo los
commits locales de la rama actual, detectar mensajes que no siguen Conventional
Commits y renombrarlos automáticamente cuando sea seguro.

Prioridad máxima: rapidez, seguridad y mínimo número de comandos.

## Principios

* No hagas exploración innecesaria.
* No revises todo el historial.
* No inspecciones archivos completos si basta con nombres de archivos.
* No consultes remotos commit por commit.
* No crees ejecutables globales.
* No toques `/usr/local/bin`, `/usr/bin`, `~/.local/bin` ni rutas globales.
* Usa solo scripts temporales en `/tmp`.
* Haz como máximo un rebase para todos los commits históricos.
* Mantén todo en español.

## Flujo rápido

### 1. Verificar árbol de trabajo limpio

Ejecuta:

```bash
git status --porcelain
```

Si la salida no está vacía, detente. No hagas nada más.

Reporta:

```text
[improve-commits] El árbol de trabajo tiene cambios sin commit.
Hacé commit de tus cambios y volvé a ejecutar /improve-commits.
```

### 2. Determinar rama y base segura

Ejecuta:

```bash
git branch --show-current
```

Luego determina la base así:

#### Si la rama actual es `main`

Usa `origin/main` como base:

```bash
git rev-parse --verify origin/main
```

Si `origin/main` existe:

```bash
BASE=origin/main
```

Si no existe, detente y reporta que no hay base remota segura.

#### Si la rama actual NO es `main`

Primero intenta usar upstream:

```bash
git rev-parse --abbrev-ref --symbolic-full-name @{u}
```

Si existe upstream, usa ese upstream como base.

Si no existe upstream, usa `origin/main` si existe.

Si tampoco existe `origin/main`, usa `main` solo para auditar y sugerir, pero no reescribas historia automáticamente.

### 3. Obtener commits locales una sola vez

Con la base resuelta, ejecuta:

```bash
git log --reverse --format="%H%x09%s" "$BASE"..HEAD
```

Si no hay commits, reporta:

```text
[improve-commits] No hay commits locales para auditar.
```

No uses:

```bash
git log --max-count=30
```

No uses:

```bash
git branch -r --contains <hash>
```

Motivo: si el rango es `origin/main..HEAD` o `@{u}..HEAD`, ya estás trabajando
sobre commits locales/no publicados respecto a esa base.

### 4. Auditar mensajes con heurística rápida

Para cada commit del rango, revisa primero solo el subject.

Un subject es válido si cumple:

```text
<type>(<scope opcional>): <descripción>
```

Tipos válidos:

* `feat`
* `fix`
* `docs`
* `test`
* `refactor`
* `perf`
* `style`
* `build`
* `ops`
* `chore`

La descripción debe estar en español, en imperativo presente, sin mayúscula inicial
y sin punto final.

Son mensajes mejorables si:

* son genéricos: `update`, `changes`, `fix`, `wip`, `avance`, `arreglo`,
  `cambios`, `cosas`;
* no tienen tipo Conventional Commit;
* usan tipo incorrecto;
* dicen `feat` pero solo cambian documentación, specs, prompts o configuración;
* no son trazables.

### 5. Clasificar por archivos solo cuando haga falta

No leas diffs completos de entrada.

Para commits con subject dudoso, ejecuta:

```bash
git diff-tree --no-commit-id --name-only -r <hash>
```

Usa los paths para inferir tipo y scope.

Reglas rápidas:

* Solo cambia `specs/`, `.opencode/`, `AGENTS.md`, `.specify/`, `docs/` o Markdown:

  * tipo: `docs`
* Solo cambia `tests/`:

  * tipo: `test`
* Cambia `pyproject.toml`, `uv.lock`, tooling o dependencias:

  * tipo: `build`
* Cambia `docker-compose.yaml`, scripts operacionales o CI:

  * tipo: `ops`
* Cambia código productivo en `app/modules/**` agregando comportamiento visible:

  * tipo: `feat`
* Corrige comportamiento existente:

  * tipo: `fix`
* Reestructura sin cambio observable:

  * tipo: `refactor`

Solo usa `git show --stat <hash>` si los nombres de archivos no alcanzan para
clasificar. Evita `git show <hash>` completo salvo que sea imprescindible.

### 6. Generar mensajes nuevos

Formato:

```text
<type>(<scope>): <descripción en español>
```

Reglas:

* Tipo en inglés.
* Descripción en español.
* Imperativo presente.
* Sin mayúscula inicial.
* Sin punto final.
* Scope cuando aporte contexto.

Scopes sugeridos:

```text
001, 002, 003, 004, 005, 006, 007,
specs, opencode, agents, changelog, frontend, backend, database,
tests, health, home, propiedades, visual-governance, docker, docs,
setup, mutation-testing
```

Ejemplos:

```text
docs(specs): documenta creación de propiedades
test(propiedades): cubre validación del formulario de creación
feat(propiedades): agrega formulario server-rendered de alta
docs(opencode): ajusta prompts de la spec 007
build(testing): agrega mutmut como herramienta de calidad
```

### 7. Decidir estrategia de renombrado

#### Caso A: no hay commits mejorables

Reporta:

```text
[improve-commits] Todos los commits locales tienen mensajes aceptables.
```

#### Caso B: solo HEAD necesita renombre

Renombra con:

```bash
git commit --amend -m "nuevo mensaje"
```

#### Caso C: hay commits históricos a renombrar

Usa un único rebase no interactivo.

No abras editor real.

No crees `vi` falso.

No escribas en rutas globales.

Crea scripts temporales en `/tmp`.

### 8. Rebase no interactivo rápido

Crea un directorio temporal:

```bash
TMPDIR=$(mktemp -d)
```

Crea un archivo de mapeo:

```text
$TMPDIR/messages.txt
```

Formato:

```text
<hash_completo>|<nuevo mensaje>
<hash_completo>|<nuevo mensaje>
```

Crea el sequence editor:

```bash
cat > "$TMPDIR/sequence-editor.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

TODO_FILE="$1"
MAP_FILE="$IMPROVE_COMMITS_MAP"
TMP_FILE="${TODO_FILE}.tmp"

cp "$TODO_FILE" "$TMP_FILE"

while IFS='|' read -r HASH MESSAGE; do
  [ -n "$HASH" ] || continue
  PREFIX="${HASH:0:7}"
  sed -i "s/^pick ${PREFIX}/reword ${PREFIX}/" "$TMP_FILE"
done < "$MAP_FILE"

mv "$TMP_FILE" "$TODO_FILE"
EOF
```

Crea el message editor:

```bash
cat > "$TMPDIR/message-editor.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

MSG_FILE="$1"
MAP_FILE="$IMPROVE_COMMITS_MAP"
GIT_DIR="$(git rev-parse --git-dir)"

# Durante rebase interactivo, el último registro en rebase-merge/done contiene
# el hash original del commit que se está rewordeando.
DONE_FILE="$GIT_DIR/rebase-merge/done"

if [ ! -f "$DONE_FILE" ]; then
  exit 0
fi

ORIGINAL_HASH="$(tail -n 1 "$DONE_FILE" | awk '{print $2}')"
[ -n "$ORIGINAL_HASH" ] || exit 0

NEW_MSG="$(grep "^${ORIGINAL_HASH}|" "$MAP_FILE" | sed 's/^[^|]*|//')"

if [ -n "$NEW_MSG" ]; then
  printf '%s\n' "$NEW_MSG" > "$MSG_FILE"
fi
EOF
```

Hazlos ejecutables:

```bash
chmod +x "$TMPDIR/sequence-editor.sh" "$TMPDIR/message-editor.sh"
```

Ejecuta el rebase:

```bash
IMPROVE_COMMITS_MAP="$TMPDIR/messages.txt" \
GIT_SEQUENCE_EDITOR="$TMPDIR/sequence-editor.sh" \
GIT_EDITOR="$TMPDIR/message-editor.sh" \
git rebase -i "$BASE"
```

Si falla:

```bash
git rebase --abort
```

Reporta el error y no intentes resolver conflictos.

Al terminar correctamente, puedes borrar temporales:

```bash
rm -rf "$TMPDIR"
```

## Restricciones

* NO ejecutes:

  * `git reset`
  * `git push`
  * `git pull`
  * `git merge`
  * `git switch`
  * `git checkout`
  * `git restore`
  * `git stash`
  * `git clean`
* NO escribas en `/usr/local/bin`, `/usr/bin`, `~/.local/bin` ni rutas globales.
* NO crees ejecutables falsos tipo `vi`.
* NO modifiques `PATH` de forma persistente.
* NO despaches otro subagente para esta tarea.
* NO inspecciones todo el repo.
* NO edites archivos del proyecto.
* NO toques `CHANGELOG.md`.
* Si hay conflicto durante rebase, aborta inmediatamente.
* Si no hay base remota segura, solo sugiere mensajes; no reescribas historia.

## Optimización esperada

Para 6 commits locales, el flujo normal debería ser:

1. `git status --porcelain`
2. `git branch --show-current`
3. `git rev-parse --verify origin/main` o upstream
4. `git log --reverse --format="%H%x09%s" "$BASE"..HEAD`
5. `git diff-tree --no-commit-id --name-only -r <hash>` solo para commits dudosos
6. `git commit --amend` o un único `git rebase -i "$BASE"`

No debería tardar minutos.

## Salida esperada

Al finalizar, reporta:

```text
[improve-commits] Resultado

Rama actual: <rama>
Base usada: <base>
Commits auditados: <n>
Commits ya válidos: <n>
Commits renombrados vía amend: <n>
Commits renombrados vía rebase: <n>
Commits no modificados por seguridad: <n>

Renombres:
- <hash corto>: "<original>" → "<nuevo>"

Advertencias:
- <si aplica>

Verificación final:
- git log --oneline <base>..HEAD
```
