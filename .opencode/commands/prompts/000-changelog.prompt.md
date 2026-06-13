---
name: 000-changelog
description: >
  Configura el sistema de changelog dual del proyecto: buffer técnico post-commit,
  changelog curado, subagente de auditoría y comando /changelog.
---

Implementa el sistema base de changelog dual y auditoría de mensajes de commit
para el repositorio.

Este prompt funciona como setup inicial del proyecto para dejar instalado el flujo
de documentación histórica del repositorio.

## Naturaleza del cambio

Este prompt implementa infraestructura operativa de tooling para el repositorio.

No es una feature de dominio ni una feature de aplicación.

No debe crear ni modificar código bajo `app/`, `app/modules/`, `alembic/` ni
templates de aplicación.

Puede crear o modificar únicamente archivos de soporte operativo:

```text
docs/context/
scripts/
scripts/hooks/
.opencode/agents/
.opencode/commands/prompts/
.gitignore
.repomixignore
```

Si detectas que la constitución exige una spec para este cambio de tooling, pausa
e informa antes de continuar.

## Objetivo

Crear un flujo que transforme el historial Git en dos niveles de documentación:

1. Un buffer técnico y mecánico generado después de cada commit.
2. Un changelog curado, humano y estable siguiendo Keep a Changelog.

Además, el flujo debe detectar commits con mensajes pobres, genéricos o poco
trazables y sugerir mensajes mejorados siguiendo Conventional Commits.

## Archivos a crear

Crea estos archivos si no existen:

```text
docs/context/.changelog-pending.md
docs/context/CHANGELOG.md
scripts/changelog.sh
scripts/hooks/post-commit.changelog
scripts/install-git-hooks.sh
.opencode/agents/changelog.md
```

## Archivo de comando existente

Este archivo ya existe y contiene este prompt:

```text
.opencode/commands/prompts/000-changelog.prompt.md
```

No lo recrees, no lo dupliques y no lo sobreescribas.

Usa este archivo como definición operativa del comando `/changelog`.

## Comando de OpenCode

El comando de OpenCode debe ser:

```text
/changelog
```

El comando debe llamarse:

```text
changelog
```

## Reglas de ramas

El proyecto usa ramas con el mismo nombre lógico que la spec.

Ejemplo:

```text
001-bootstrap-proyecto
002-blindar-tokens-visuales
003-redisenar-home
main
```

No asumas ramas con prefijo `feat/`.

## Diseño esperado

El flujo debe ser:

```text
git commit manual
  -> .git/hooks/post-commit
  -> scripts/changelog.sh
  -> docs/context/.changelog-pending.md
  -> /changelog
  -> docs/context/CHANGELOG.md
```

El hook y el script solo capturan información mecánica.

El subagente `/changelog` interpreta, agrupa y cura los cambios.

El subagente también audita mensajes de commit y sugiere mejoras cuando detecte
mensajes pobres o poco trazables.

## Archivo técnico pendiente

Crea `docs/context/.changelog-pending.md` como buffer técnico.

Debe contener entradas por commit con información como:

* Hash corto.
* Fecha ISO.
* Rama actual.
* Mensaje del commit.
* Archivos cambiados.
* Diff stat.
* Categoría sugerida.
* Entrada sugerida para el changelog curado.
* Evaluación del mensaje de commit.
* Mensaje de commit sugerido, si aplica.
* Notas técnicas.

Ejemplo de formato:

````markdown
# Changelog pending

Este archivo contiene entradas mecánicas generadas por el hook `post-commit`.

No es el changelog final del proyecto.

El changelog curado vive en:

```text
docs/context/CHANGELOG.md
```

---

## Pending

### 451fc95 — 2026-06-10T11:40:00-05:00

- Branch: `003-redisenar-home`.
- Message: `feat: nuevo prompt de clarify`.
- Files:
  - `M .opencode/commands/prompts/003-redisenar-home.clarify.prompt.md`
- Stat: `1 file changed, 42 insertions(+)`.
- Suggested category: `Added`.
- Suggested entry: Agregado el prompt de clarificación para la spec `003-redisenar-home`.
- Commit message quality: `Mejorable`.
- Suggested commit message: `docs(003): añadir prompt de aclaración para la spec de rediseño del inicio`.
- Notes:
  - Cambio documental de Spec Kit.
  - El mensaje original usa `feat`, pero el cambio afecta prompts/documentación, no funcionalidad de aplicación.
  - Relacionado con `specs/003-redisenar-home`.
````

## Changelog curado

Crea `docs/context/CHANGELOG.md`.

Debe seguir esta estructura:

```markdown
# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en Keep a Changelog y este proyecto sigue versionado
SemVer cuando aplique.

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

<!-- changelog:last-processed-commit= -->
```

Reglas:

* No copiar commits directamente.
* No listar cada commit como entrada final.
* Agrupar cambios por intención.
* Mantener lenguaje humano.
* Mantener la sección `[Unreleased]`.
* Usar solo estas categorías:

  * `Added`.
  * `Changed`.
  * `Deprecated`.
  * `Removed`.
  * `Fixed`.
  * `Security`.

## Versionado del changelog

`docs/context/CHANGELOG.md` debe ser versionado en el repositorio.

Motivo:

* Es contexto curado y estable.
* Sirve como memoria histórica del proyecto.
* Puede entrar en Repomix.
* Ayuda a agentes futuros a entender la evolución del repo sin leer `.git/`.

`docs/context/.changelog-pending.md` no debe versionarse.

Motivo:

* Es buffer mecánico.
* Puede contener ruido.
* Se regenera después de commits.
* No representa el changelog final.

## Marca de último commit procesado

`docs/context/CHANGELOG.md` debe incluir una marca HTML al final del archivo:

```html
<!-- changelog:last-processed-commit=<hash> -->
```

Reglas:

* Si ya existe, actualízala cuando `/changelog` procese commits.
* Si no existe, créala al final del archivo.
* El comentario no debe afectar la lectura humana del changelog.
* El hash debe corresponder al último commit incluido o revisado por el changelog curado.
* No uses esta marca para modificar historial Git.

## Alcance de auditoría de commits

Para evitar ruido y consumo excesivo de contexto, el subagente no debe auditar
todo el historial por defecto.

Debe aplicar este orden:

1. Si `docs/context/CHANGELOG.md` contiene una marca `changelog:last-processed-commit`,
   audita solo commits posteriores a esa marca.
2. Si no existe marca de último commit procesado, audita como máximo los últimos
   20 commits.
3. Si el usuario solicita explícitamente una auditoría completa, puede revisar más
   commits, pero debe pedir confirmación antes.

Comandos de lectura sugeridos para este alcance:

```bash
git log --oneline --decorate --max-count=20
git log --oneline --decorate <last-processed-commit>..HEAD
git diff --stat <last-processed-commit>..HEAD
git diff --name-status <last-processed-commit>..HEAD
```

Si la marca existe pero el commit ya no está disponible en el historial local,
informa la situación y usa como fallback los últimos 20 commits.

## Convención de commits

Usa como referencia esta forma de Conventional Commits:

```text
<type>(<optional scope>): <description>
```

Ejemplos válidos para este proyecto:

```text
feat(home): añadir sección hero de búsqueda
fix(health): reportar estado de base de datos no disponible
docs(003): añadir prompt de aclaración para la spec de rediseño del inicio
chore(opencode): cargar instrucciones del proyecto desde la configuración del repo
refactor(properties): separar rutas por operación
test(health): cubrir respuesta con base de datos no disponible
build(deps): añadir ruff como dependencia de desarrollo
ops(docker): configurar servicio postgres en compose
```

Tipos permitidos:

```text
feat
fix
refactor
perf
style
test
docs
build
ops
chore
```

Reglas de descripción:

* Usar imperativo o presente.
* Escribir en español para el commit sugerido.
* No iniciar con mayúscula.
* No terminar con punto.
* Ser específica y trazable.
* Evitar frases genéricas como `update`, `changes`, `fix`, `wip`, `arreglo`, `avance` o `cosas`.

Reglas de scope:

* Usar scope cuando ayude a entender el área.
* Preferir scopes de feature o área real del repo.
* No usar identificadores de issue como scope.
* Para specs, usar el número de spec como scope cuando aplique.

Scopes sugeridos para este repo:

```text
001
002
003
specs
opencode
agents
changelog
frontend
backend
database
tests
health
home
visual-governance
docker
docs
setup
```

## Auditoría de mensajes de commit

El subagente debe revisar commits recientes y detectar mensajes pobres, genéricos,
ambiguos o incorrectamente tipados.

Debe usar el diff real para sugerir mensajes mejores.

Ejemplos de mensajes pobres tomados del historial actual:

```text
feat: nuevo prompt de clarify
chore: agrega prompt y activa spec rediseñar home
feat: se crean los prompts
feat: se implementó gobernanza visual
feat: se implementó analyze
chore: actualización de prompts, reglas, constitución, entre otros
feat: creación de los nuevos prompts de la spec
chore: cambios en el directorio instructions y usar opencode.json en el repo
chore: cambio de parámetro
chore: fix de los scripts
chore: actualización de cambios de ficheros
feat: se implementó la spec
feat: se crea el prompt para la implementación
feat: se aplica tasks
feat: se aplicó la spec de analyze
fix: de errores críticos
feat: prompt para analyze
feat: se ejecutó spec y clarify
fix: cambios en el prompt de spec
setup correcto
docs: fix de la constitución
feat: levantamiento de la db
```

El subagente debe marcarlos como mejorables cuando corresponda y sugerir
alternativas basadas en el diff.

Ejemplos de transformación esperada:

```text
feat: nuevo prompt de clarify
```

Sugerencia:

```text
docs(003): añadir prompt de aclaración para la spec de rediseño del inicio
```

```text
feat: se crean los prompts
```

Sugerencia posible:

```text
docs(opencode): añadir prompts de comandos de Spec Kit
```

```text
feat: se implementó la gobernanza visual
```

Sugerencia posible:

```text
docs(002): añadir reglas de gobernanza para tokens visuales
```

```text
chore: actualización de prompts, reglas, constitución, entre otros
```

Sugerencia posible:

```text
docs(governance): alinear prompts, reglas y constitución
```

```text
setup correcto
```

Sugerencia posible:

```text
chore(setup): alinear la configuración inicial del proyecto
```

La sugerencia final debe basarse siempre en los archivos y cambios reales del
commit, no solo en el mensaje original.

## Reglas para detectar tipo correcto

Usa estas reglas:

* `feat`: cambios que agregan, ajustan o eliminan una feature visible para API o UI.
* `fix`: correcciones de bugs en comportamiento existente.
* `docs`: cambios exclusivamente documentales, specs, prompts, AGENTS, instrucciones o constitución.
* `test`: cambios de pruebas.
* `refactor`: reestructura interna sin cambiar comportamiento visible.
* `perf`: mejora de rendimiento.
* `style`: formato o estilo de código sin cambio funcional.
* `build`: dependencias, build tools o empaquetado.
* `ops`: Docker, infraestructura, CI/CD, despliegue, scripts operacionales.
* `chore`: tareas auxiliares que no encajan mejor en otra categoría.

Regla importante:

* Si un commit solo cambia `specs/`, `.opencode/`, `AGENTS.md`, `.specify/`,
  `docs/` o instrucciones, normalmente debe sugerirse como `docs(...)`, no como
  `feat(...)`.

## Cambios incompatibles

Si el diff sugiere un cambio incompatible, el subagente debe recomendar `!` o
footer `BREAKING CHANGE:`.

Ejemplo:

```text
feat(api)!: eliminar forma legacy de respuesta health

BREAKING CHANGE: las respuestas de health ya no exponen el valor anterior `database: error`.
```

No debe marcar breaking changes sin evidencia clara.

## Política sobre reescritura de historial

El subagente puede sugerir comandos, pero no ejecutarlos.

Permitido sugerir:

```bash
git commit --amend -m "docs(003): añadir prompt de aclaración para la spec de rediseño del inicio"
```

Solo si el commit es local y no publicado.

Para varios commits locales, puede sugerir una estrategia con rebase interactivo:

```bash
git rebase -i main
```

Pero no debe ejecutarla.

Debe advertir:

* Renombrar commits ya publicados puede requerir `push --force-with-lease`.
* Reescribir historial compartido puede afectar a otras personas.
* Antes de reescribir, el usuario debe confirmar que la rama no fue compartida.

## Script `scripts/changelog.sh`

Crea un script Bash seguro que:

* Use `set -euo pipefail`.
* Cree `docs/context/` si no existe.
* Lea el último commit.
* Agregue una entrada técnica a `docs/context/.changelog-pending.md`.
* No modifique Git.
* No haga commits.
* No invoque IA.
* No falle el commit si no puede escribir la bitácora.

Puede usar comandos Git de solo lectura:

```bash
git branch --show-current
git status --short
git show --format=%H --no-patch HEAD
git show --format=%h --no-patch HEAD
git show --format=%s --no-patch HEAD
git show --format=%ad --date=iso-strict --no-patch HEAD
git show --name-status --format= HEAD
git show --stat --format= HEAD
```

No debe usar comandos destructivos.

## Hook versionado

Crea:

```text
scripts/hooks/post-commit.changelog
```

Debe ejecutar:

```bash
scripts/changelog.sh
```

Reglas:

* No bloquear el commit si falla.
* No modificar Git.
* No invocar OpenCode.
* No hacer commits automáticos.
* Debe ser rápido y seguro.

## Instalador de hook

Crea:

```text
scripts/install-git-hooks.sh
```

Debe:

* Copiar `scripts/hooks/post-commit.changelog` a `.git/hooks/post-commit`.
* Hacer backup si ya existe `.git/hooks/post-commit`.
* Marcar el hook como ejecutable.
* Informar qué hizo.
* No sobrescribir silenciosamente hooks existentes.
* No intentar combinar hooks existentes automáticamente.

Si ya existe `.git/hooks/post-commit`, debe:

1. Crear backup con timestamp.
2. Informar la ruta del backup.
3. Instalar el nuevo hook solo si puede hacerlo sin pérdida silenciosa.
4. Recomendar revisión manual si detecta contenido previo relevante.

## Subagente

Crea:

```text
.opencode/agents/changelog.md
```

El subagente debe:

* Leer `docs/context/.changelog-pending.md`.
* Leer `docs/context/CHANGELOG.md`.
* Revisar contexto Git reciente con comandos de solo lectura.
* Actualizar `docs/context/CHANGELOG.md`.
* Agrupar cambios según Keep a Changelog.
* Omitir ruido.
* Conservar solo cambios notables.
* Relacionar cambios con specs cuando sea posible.
* Detectar cambios visuales protegidos y advertir si falta trazabilidad.
* Auditar mensajes de commit recientes.
* Detectar commits con mensajes pobres, genéricos, ambiguos o mal tipados.
* Sugerir mensajes mejorados siguiendo la convención definida en este prompt.
* Incluir sugerencias de renombrado en la respuesta final.
* Respetar el alcance máximo de auditoría definido en este prompt.
* Actualizar la marca `changelog:last-processed-commit` cuando corresponda.
* No modificar historial Git.
* No ejecutar comandos destructivos.
* No ejecutar `git commit`, `git reset`, `git rebase`, `git push`, `git pull`,
  `git merge`, `git switch`, `git checkout`, `git restore`, `git stash`,
  `git clean`.

Puede sugerir comandos al usuario, pero no ejecutarlos.

## Prompt de comando

Este archivo es el prompt del comando `/changelog`.

No lo recrees ni lo dupliques.

El prompt del comando debe invocar al subagente de changelog y pedirle que
actualice `docs/context/CHANGELOG.md` usando el buffer pendiente y el historial
Git reciente.

El comando debe pedir explícitamente:

* Actualizar `docs/context/CHANGELOG.md`.
* Leer `docs/context/.changelog-pending.md`.
* Auditar commits recientes respetando el alcance definido.
* Sugerir renombres para commits pobres.
* No ejecutar reescrituras de historial.
* No ejecutar comandos destructivos.
* Reportar entradas omitidas por ruido.
* Reportar riesgos detectados.
* Actualizar la marca `changelog:last-processed-commit` cuando corresponda.

## Actualización segura de `.gitignore`

Actualiza `.gitignore` para ignorar el buffer técnico:

```gitignore
docs/context/.changelog-pending.md
```

Reglas:

* Si `.gitignore` ya contiene esa entrada, no la dupliques.
* Si `.gitignore` no existe, créalo.
* Si existe, agrega la entrada al final bajo esta sección solo si falta:

```gitignore
# Changelog local buffer
docs/context/.changelog-pending.md
```

## Actualización segura de `.repomixignore`

Si `.repomixignore` existe, revisa si ya contiene:

```gitignore
.git/
docs/context/.changelog-pending.md
```

Reglas:

* No dupliques entradas existentes.
* Si `.repomixignore` no existe, no lo crees automáticamente salvo que el usuario lo haya pedido explícitamente.
* Si existe, agrega las entradas faltantes bajo esta sección:

```gitignore
# Git internals and local changelog buffer
.git/
docs/context/.changelog-pending.md
```

No ignores:

```text
docs/context/CHANGELOG.md
```

## Reglas obligatorias

* Mantén todo en español.
* Trata este cambio como setup/tooling, no como feature de dominio.
* No modifiques código de aplicación.
* No modifiques specs existentes salvo que sea estrictamente necesario y lo informes antes.
* No cambies la constitución.
* No uses comandos destructivos de Git.
* No automatices commits.
* No hagas push.
* Respeta `AGENTS.md` y `.opencode/instructions/*.instructions.md`.
* Si hay conflicto con alguna regla del proyecto, pausa e informa antes de continuar.

## Verificaciones esperadas

Al finalizar, ejecuta o indica cómo ejecutar:

```bash
bash -n scripts/changelog.sh
bash -n scripts/hooks/post-commit.changelog
bash -n scripts/install-git-hooks.sh
```

Si es seguro, ejecuta también:

```bash
scripts/changelog.sh
```

para generar una entrada inicial de prueba en `.changelog-pending.md`.

No hagas commit automáticamente.

## Salida esperada

Al finalizar informa:

* Archivos creados.
* Archivos modificados.
* Comandos ejecutados.
* Si el cambio fue tratado como setup/tooling y no como feature de dominio.
* Si el hook quedó instalado o solo preparado.
* Cómo instalar el hook.
* Cómo ejecutar `/changelog`.
* Si `docs/context/CHANGELOG.md` quedó listo y versionable.
* Si `docs/context/.changelog-pending.md` quedó ignorado.
* Cantidad máxima de commits que auditará el subagente por defecto.
* Si se agregó o detectó la marca `changelog:last-processed-commit`.
* Commits revisados.
* Entradas agregadas al changelog curado.
* Entradas omitidas por ruido.
* Commits con mensajes pobres detectados.
* Mensajes de commit sugeridos.
* Riesgos o advertencias.
* Pendientes.
