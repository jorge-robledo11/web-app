# Mutation testing con `mutmut`

`mutmut` es la herramienta de mutation testing declarada en la sección X
de la constitución. Sirve para detectar tests de bajo valor, mocks
permisivos, asserts insuficientes y casos borde faltantes.

Este documento es la guía operativa de uso. La política completa (criterios
de conservación, poda y clasificación de sobrevivientes) vive en la
sección X de `.specify/memory/constitution.md`.

## Por qué mutation testing

La cobertura de líneas mide cuántas líneas se ejecutan durante los tests.
Eso NO garantiza que los tests detecten cambios incorrectos. Es facil
escribir tests que ejecutan el código pero no verifican nada relevante.

`mutmut` introduce mutaciones controladas en el código de producción
(cambiar un `>` por `>=`, eliminar un `return`, invertir una condición, etc.)
y vuelve a correr la suite. Si los tests siguen pasando con la mutación
activa, esa mutación "sobrevive" y el test no estaba protegiendo ese
camino.

Una mutación que sobrevive puede significar:

* Falta de un test para esa rama.
* Test con assertion débil que no detecta el cambio.
* Mutante equivalente (el cambio no produce diferencia observable).
* Código muerto o innecesario.

## Cuándo correrlo

Mutation testing se aplica de forma **focalizada por slice o módulo
crítico**, no obligatoriamente a todo el repositorio en cada cambio. Casos
de uso recomendados:

* Antes de cerrar una spec que introduce reglas de negocio nuevas.
* Después de una refactorización grande sobre un módulo.
* Cuando se sospecha que un test no protege lo que dice proteger.
* Periódicamente, sobre los slices más críticos del Vertical Slice
  (por ejemplo, `app/modules/propiedades/service.py`).

No se exige una meta global del 100 % de mutation score ni se usa como
gate obligatorio de CI. El baseline se obtiene en la primera ejecución
real y los umbrales por slice se introducen de forma evolutiva.

## Cómo correrlo

El entry point recomendado es el target de Makefile:

```bash
make mutation
```

Que internamente ejecuta `bash scripts/ci/mutation.sh`. El script:

1. Corre la suite normal con `uv run pytest -q` para confirmar verde.
2. Corre `uv run mutmut run` para generar y evaluar mutantes.

Comandos manuales equivalentes:

```bash
uv run mutmut run               # corre mutación sobre source_paths configurado
uv run mutmut results           # resumen agregado (vivos, muertos, timeout, skipped)
uv run mutmut results --all     # incluye sobrevivientes
uv run mutmut browse            # UI textual interactiva
uv run mutmut browse --show-killed
uv run mutmut show <mutant>     # detalle de un mutante concreto
uv run mutmut apply <mutant>    # aplica el cambio al repo (para reproducir)
uv run mutmut print-time-estimates
```

Las salidas viven en `mutants/` (declarado en `.gitignore`):

* `mutants/<path-mirrored>/<file>.py` con cada mutante.
* `mutants/mutmut-stats.json` con el resumen.

## Configuración

`mutmut` se configura en `[tool.mutmut]` dentro de `pyproject.toml`:

```toml
[tool.mutmut]
source_paths = ["app/modules/"]
do_not_mutate = [
    "app/modules/**/__init__.py",
    "app/modules/**/routes.py",
    "app/modules/health/*",
]
pytest_add_cli_args_test_selection = ["tests/unit/", "tests/integration/"]
max_stack_depth = 8
mutate_only_covered_lines = true
```

### Decisiones de configuración

* `source_paths = ["app/"]`: mutmut necesita todo `app/` en `mutants/`
  para que los conftests resuelvan `from app.main import app`. Excluimos
  explícitamente del mutado los archivos sin lógica de negocio con
  `do_not_mutate`.
* `do_not_mutate` excluye:
  * `app/**/__init__.py`: archivos vacíos, sin lógica.
  * `app/**/routes.py`: capas delgadas de FastAPI. Su mutación tiene
    bajo valor porque el contrato HTTP se valida con tests de
    integración. La lógica que mutar con valor vive en `service.py` y
    `schemas.py`.
  * `app/main.py`: entrypoint de la app, no contiene lógica de negocio.
  * `app/infra/**`: capa de infraestructura (engine, sesiones).
  * `app/config/**`: carga de settings.
  * `app/modules/health/*`: smoke test trivial, no es lógica de negocio.
* `pytest_add_cli_args_test_selection = ["tests/unit/"]`: en esta
  primera versión se ejecutan solo los tests unitarios para matar
  mutantes. La ejecución completa con `tests/integration/` es una
  evolución posterior: requiere copiar también `alembic/`, `alembic.ini`
  y `scripts/` a `mutants/` (los conftests de integración lanzan
  alembic y seed como subprocess con `cwd=mutants/`). Hasta que se
  habilite, los mutantes cuyo efecto solo se observa en integración
  pueden sobrevivir sin ser falsos positivos: el test de integración
  correspondiente es el que los mataría.
* `pytest_add_cli_args = ["-o", "pythonpath=mutants/.."]`: añade el
  cwd de pytest (`mutants/`) a `sys.path` para que los conftests
  resuelvan `from app.main import app` y `from app.infra.database
  import engine`.
* `also_copy = ["config/"]`: copia `config/app.yaml` (no versionado)
  y `config/app.example.yaml` a `mutants/config/` para que
  `pydantic_settings` valide al instanciar `Settings`.
* `mutate_only_covered_lines = true`: evita gastar tiempo mutando líneas
  no cubiertas por la suite.
* `max_stack_depth = 8`: limita la profundidad del AST analizado. Útil
  para funciones con muchas expresiones anidadas.

### Claves no soportadas en mutmut 3.6.0

Las claves `cache_invalidation_files` y `cache_invalidation_exclude`
propuestas en la propuesta inicial **no existen** en la versión instalada
(3.6.0). mutmut 3.x invalida la caché automáticamente comparando el
mtime de los archivos fuente. No hace falta declararlas.

## Cómo interpretar sobrevivientes

Después de `make mutation`, `uv run mutmut results` resume:

| Estado       | Significado                                                        |
|--------------|--------------------------------------------------------------------|
| `killed`     | Algún test detectó el cambio. El comportamiento está protegido.    |
| `survived`   | Ningún test detectó el cambio. Candidato a acción (ver abajo).     |
| `timeout`    | La mutación provocó un timeout (test colgado, loop infinito, etc.).|
| `no_tests`   | La línea mutada no está cubierta por ningún test seleccionado.     |
| `skipped`    | Línea excluida explícitamente o por `do_not_mutate`.               |
| `suspicious` | mutmut sospecha que el mutante es equivalente a un killed.         |

Para cada `survived`, clasificar antes de actuar (sección X.3):

1. **Falta de test valioso**: la rama no está cubierta. Mejorar test
   existente o agregar test mínimo.
2. **Test con assertion débil**: el test existe pero su assert no detecta
   el cambio. Endurecer el assert.
3. **Mutante equivalente**: el cambio no produce diferencia observable.
   Marcar como aceptado o simplificar el código.
4. **Código muerto o innecesario**: la rama mutada no aporta valor.
   Eliminar el código.
5. **Mutación irrelevante**: no afecta comportamiento observable
   documentado. Aceptar.

## Cuándo agregar, mejorar, fusionar o eliminar tests

* **Agregar test**: cuando la rama no está cubierta y protege un
  comportamiento de negocio real. Preferir un test mínimo y valioso sobre
  varios superficiales.
* **Mejorar test**: cuando existe el test pero su assert no detecta la
  mutación. Endurecer el assert para que cubra el caso.
* **Fusionar tests**: cuando varios tests verifican el mismo
  comportamiento con menos expresividad que uno solo consolidado.
* **Eliminar test**: cuando el test:
  * No mata mutantes relevantes.
  * No está trazado a spec, contrato, bug o integración.
  * Está duplicado por otro test más expresivo.
  * Solo verifica detalle de implementación interna.
  * Tiene assertions triviales.
  * Su eliminación no reduce la cobertura de requisitos ni el mutation
    score relevante.

## Cuándo usar `# pragma: no mutate`

Solo cuando hay justificación explícita registrada en `tasks.md` o en
`plan.md` y la mutación es equivalente o irrelevante. Es un último recurso
después de intentar mejorar test, agregar test mínimo, fusionar
redundantes y simplificar código. No usar para "ahorrar tiempo" en CI.

## Por qué no se exige 100 % mutation score

* Hay mutantes equivalentes cuyo cambio no produce diferencia observable
  pero que mutmut no detecta automáticamente.
* Hay mutaciones irrelevantes para comportamiento documentado.
* 100 % de score es una métrica vanity que fomenta agregar asserts
  artificiales para "matar" mutantes irrelevantes.
* El objetivo es detectar reglas de negocio desprotegidas, no maximizar
  un número.

## Por qué la cobertura no basta

Un test puede ejecutar el 100 % de las líneas de un módulo y aún así no
proteger nada. Ejemplos típicos:

* `assert result is not None` sin verificar contenido.
* Mock que reproduce la implementación original y verifica que se llamó
  con los mismos argumentos.
* Test que captura una excepción genérica sin verificar mensaje ni tipo.

Mutation testing detecta estos casos porque introduce cambios reales en
el código y observa si la suite los nota.

## Por qué un test que no mata mutantes puede seguir siendo valioso

Algunos tests son valiosos por lo que **representan**, no por su
contribución al mutation score:

* Smoke test mínimo de una capability crítica (el endpoint responde, el
  módulo importa sin error).
* Contrato HTTP: status code, headers, content-type.
* DTO público: shape del JSON expuesto, nombres de campos.
* Migración Alembic: aplicar y revertir sin error.
* Seed: idempotencia, datos mínimos.
* Render server-side: presencia de elementos clave en el HTML.
* Wiring de rutas: la ruta está registrada y responde.
* Regresión documentada: protege un bug que ya ocurrió.
* Gobernanza visual: tokens canónicos, responsive.

Estos tests no siempre "matan" mutantes de mutmut (porque mutan lógica
interna, no contratos externos), pero su ausencia podría romper la
aplicación de formas que mutation testing no detecta.

La sección X.4.1 de la constitución declara explícitamente estos casos
como motivos válidos para conservar un test aunque no mate mutantes.

## Responsabilidad operativa

La operación de métricas de calidad de tests es responsabilidad del
desarrollador humano. Mutation testing es una herramienta de auditoría
y aprendizaje, no una tarea automática delegable al agente ni una
métrica vanity. Esta sección resume operativamente la subsección X.7
de la constitución.

### Interfaces oficiales vía Makefile

Los targets mínimos obligatorios para operar las verificaciones de
calidad de tests son:

| Target                | Propósito                                              |
|-----------------------|--------------------------------------------------------|
| `make test`           | Ejecutar la suite de tests.                            |
| `make coverage`       | Ejecutar tests con coverage.                          |
| `make mutation`       | Ejecutar mutation testing focalizado con mutmut.       |
| `make mutation-results` | Consultar resumen de mutantes (vivos, muertos).      |
| `make mutation-clean` | Limpiar artefactos temporales (`mutants/`).            |

Adicionalmente, `make mutation-browse` y `make mutation-estimates` son
interfaces de exploración opcionales.

### Lo que un agente de IA NO debe hacer

Por iniciativa propia, un agente de IA tiene prohibido:

* Ejecutar ciclos exploratorios de mutation testing para maximizar
  score.
* Cambiar umbrales, configuración o scope de mutation testing.
* Agregar tests artificiales solo para matar mutantes.
* Eliminar tests únicamente porque no mejoran coverage o mutation
  score.
* Usar el mutation score global como objetivo de implementación.
* Marcar mutantes con `# pragma: no mutate` sin justificación
  aprobada por el desarrollador.
* Convertir mutation testing en gate obligatorio de CI sin
  aprobación explícita.

### Lo que un agente de IA sí puede hacer

Un agente de IA sí puede:

* Proponer tests mínimos y valiosos cuando el desarrollador
  proporcione evidencia concreta, como un mutante sobreviviente, bug
  reproducible, requisito de spec o contrato roto.
* Endurecer assertions débiles en tests existentes.
* Fusionar tests redundantes cuando el comportamiento protegido
  permanezca cubierto.
* Explicar la clasificación de mutantes sobrevivientes.
* Documentar decisiones tomadas por el desarrollador sobre mutantes
  equivalentes, irrelevantes o aceptados.

### Responsabilidad reservada al desarrollador

Quedan bajo criterio exclusivo del desarrollador humano:

* La clasificación final de mutantes sobrevivientes.
* La aceptación de mutantes equivalentes.
* La actualización de baselines.
* La poda de tests.
* La interpretación de métricas.

La política completa (incluyendo los criterios de conservación y poda
de la sección X.4 y la tabla de clasificación de sobrevivientes de la
sección X.3) está en `.specify/memory/constitution.md`.

## Responsabilidad operativa

El desarrollador opera mutation testing mediante los targets del `Makefile`.

Los agentes de IA pueden ayudar a interpretar resultados o proponer tests concretos a partir de evidencia proporcionada por el desarrollador, pero no deben ejecutar ciclos de optimización de mutation score ni modificar el scope de mutmut sin instrucción explícita.

La decisión de aceptar, justificar, excluir o corregir mutantes sobrevivientes corresponde al desarrollador.
