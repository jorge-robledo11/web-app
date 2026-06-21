<!--
Informe de impacto de sincronización
- Cambio de versión: 1.6.0 -> 1.7.0
- Secciones agregadas:
  - X.7 Responsabilidad operativa de métricas de tests: precisa quién opera las
    métricas de calidad de tests. Declara que la operación es responsabilidad del
    desarrollador humano. Enumera los targets de Makefile mínimos obligatorios
    (tests, coverage, mutation, mutation-results, mutation-clean). Lista las
    prohibiciones explícitas para los agentes de IA (no ejecutar ciclos
    exploratorios, no cambiar umbrales, no agregar tests artificiales, no eliminar
    tests por score, no usar score global como objetivo, no marcar
    `# pragma: no mutate` sin aprobación, no convertir mutation testing en gate
    obligatorio de CI). Lista las acciones permitidas (proponer tests con
    evidencia, endurecer asserts, fusionar redundantes, explicar clasificación,
    documentar decisiones del desarrollador). Reserva al desarrollador la
    clasificación final, aceptación de mutantes equivalentes, baselines, poda
    de tests e interpretación de métricas.
- Secciones modificadas:
  - XIX. Historial de versiones: agregada entrada v1.7.0; versión y fecha de
    última enmienda actualizadas.
- Artefactos relacionados revisados:
  - .opencode/instructions/tests.instructions.md ✅ agregada subsección
    «Responsabilidad operativa de métricas de tests» alineada con X.7
  - docs/testing/mutation-testing.md ✅ agregada sección sobre responsabilidad
    operativa
  - Makefile ✅ agregado target `mutation-clean` para limpiar `mutants/`
- Sin cambios al stack, arquitectura, flujo SDD ni a los principios ya
  establecidos en la sección X. La nueva subsección X.7 refina la responsabilidad
  operativa, no modifica la política de calidad de tests ni las reglas de
  conservación y poda.
- Pendientes de seguimiento:
  - Baseline de mutation score por definir tras primera ejecución real con
    `make mutation` sobre `app/modules/` (heredado de v1.6.0).
  - Umbrales por slice crítico: aún no definidos; se introducirán de forma
    evolutiva.
-->

# Constitución del Proyecto Realtor

Esta constitución es la fuente de verdad superior del proyecto. Toda decisión
técnica, arquitectónica o de proceso debe ser consistente con los principios aquí
declarados. Ante cualquier conflicto entre documentos, esta constitución
prevalece.

## I. Idioma

Todo el contenido `.md`, los comentarios, los docstrings y los mensajes de
commit DEBEN estar en español. NUNCA mezclar idiomas dentro de un mismo archivo.

## II. Stack obligatorio inmutable

El proyecto es un monolito Python con los siguientes componentes fijos. Ningún
componente del stack puede ser reemplazado sin una enmienda formal a esta
constitución.

| Componente       | Herramienta                                                                          |
| ---------------- | ------------------------------------------------------------------------------------ |
| Runtime          | Python 3.13.13, gestionado con `uv`                                                   |
| Empaquetado      | `pyproject.toml` + `uv.lock`                                                         |
| HTTP             | FastAPI                                                                              |
| Vistas           | Jinja2 server-rendered + HTMX                                                        |
| ORM              | SQLAlchemy 2.x async con `Mapped[...]`, `mapped_column`, `select()` y `AsyncSession` |
| Validación       | Pydantic v2 con `model_config = ConfigDict(frozen=True)`                             |
| Base de datos    | PostgreSQL vía asyncpg, local con Docker o Docker Compose                            |
| Migraciones      | Alembic como única herramienta permitida                                             |
| Tests            | pytest + pytest-asyncio + httpx.AsyncClient                                          |
| Integración      | Testcontainers cuando se requiera infraestructura real                               |
| Calidad estática | Ruff + mypy `--strict` mínimo en `app/modules/`                                      |
| Pre-commit       | pyupgrade, ruff (lint + format), format-docstrings, pydocstyle, check-yaml, check-toml     |
| Automatización   | `.pre-commit-config.yaml` como entry point unificado de calidad                      |
| Iconografía      | SVG outline de Lucide vendoreados en `app/static/icons/`                             |

## III. Prohibiciones absolutas

Las siguientes herramientas, prácticas y patrones están PROHIBIDOS en todo el
proyecto:

* `pip`, `poetry`, `conda`, `pipenv`, `requirements.txt`, `setup.py`.
* Bootstrap, Tailwind, Bulma, Foundation o cualquier framework CSS.
* Cargar HTMX o cualquier JS de terceros desde CDN en runtime.
* Iconos como webfont, Bootstrap Icons, Font Awesome, Material Icons font,
  emojis o caracteres Unicode como íconos funcionales.
* Estilo legacy de SQLAlchemy: `Column(...)` en clase, `Query` o sesiones
  síncronas.
* Funciones `def` síncronas en `routes.py`, `service.py` o `repository.py`
  cuando realicen I/O.
* Carpetas globales por capa técnica: `controllers/`, `services/`,
  `repositories/`, `handlers/`, `managers/` fuera de un módulo.
* Exponer entidades SQLAlchemy como respuesta HTTP.
* Retornar `dict` libres en errores.
* Strings mágicos para estados de dominio.
* Usar Supabase en producción o desarrollo.
* Usar extensión `.yml` para archivos YAML; usar siempre `.yaml`.
* Separar frontend y backend en aplicaciones o repositorios independientes.
* Crear microservicios sin una enmienda formal a esta constitución.

## IV. Arquitectura: Vertical Slice

El proyecto sigue una arquitectura de Vertical Slice. Cada feature vive en su
propio módulo bajo `app/modules/<feature>/`.

Cada módulo DEBE contener estos artefactos:

* `routes.py` — capa delgada: parsea entrada, llama al servicio y retorna
  respuesta.
* `schemas.py` — DTOs Pydantic v2 con `frozen=True`.
* `models.py` — entidades SQLAlchemy 2.x async con `Mapped[...]` y
  `mapped_column`.
* `repository.py` — solo acceso a datos.
* `service.py` — lógica de negocio del módulo.
* `templates/` — plantillas Jinja2 del módulo.

La lógica de negocio reside en `service.py`. `routes.py` y `repository.py` son
capas de entrada e infraestructura sin reglas de negocio. La lógica compartida
solo se extrae cuando exista duplicación real demostrable, nunca por anticipación.

Las pruebas del proyecto viven fuera del módulo, en la raíz del repositorio,
según la estructura obligatoria definida en la sección IX.5 y en la sección XIV.

## V. Spec-Driven Development

No se implementa NADA que no esté descrito en un `spec.md` aprobado.

Las specs deben crearse exclusivamente mediante los comandos de Spec Kit. No se
deben crear, mover o duplicar specs manualmente fuera de la ruta que resuelvan
esos comandos.

Cada `spec.md` aprobado es la fuente de verdad funcional de su feature, siempre
que no contradiga esta constitución.

La ruta de specs no es una decisión de arquitectura de aplicación. Si una versión
futura de Spec Kit cambia la ruta generada por sus comandos, deben actualizarse
solo los documentos derivados o el puntero operativo correspondiente, sin
modificar la arquitectura del proyecto.

Cada spec debe contener, **todos obligatorios sin excepción**:

```text
spec.md
plan.md
tasks.md
data-model.md
contracts/<feature>.yaml
quickstart.md
research.md
```

Donde:

* `spec.md` — fuente de verdad funcional de la feature (qué).
* `plan.md` — decisiones técnicas, fases, contrato de contexto, gobernanza
  visual y Complexity Tracking (cómo).
* `tasks.md` — tareas pequeñas, ordenadas, verificables y trazables a
  requisitos funcionales (cuándo).
* `data-model.md` — entidades, columnas, índices, migraciones, flujo de datos
  entre módulos y DTOs Pydantic. Si la spec no introduce cambios al modelo,
  referenciar el spec del que se hereda y declarar "Sin cambios".
* `contracts/<feature>.yaml` — contrato formal de los endpoints HTTP expuestos
  por la feature: método, path, request, response, contexto de template,
  gobernanza visual y consideraciones de seguridad. El nombre del archivo es
  el slug de la feature. Formato YAML para permitir parseo programático.
* `quickstart.md` — pasos manuales reproducibles para validar la feature
  end-to-end con `curl`, navegador o scripts. Incluye reset completo para
  entorno limpio.
* `research.md` — decisiones técnicas investigadas con alternativas
  evaluadas y fundamento. Las decisiones tomadas en la fase `clarify` se
  referencian aquí.

Toda spec nueva o retroactiva debe generar los 7 archivos. Ningún archivo es
opcional. La ausencia de cualquiera de ellos bloquea la transición a
`implement`. Los archivos pueden tener contenido mínimo (p. ej.
`data-model.md` con "Sin cambios") pero no pueden estar ausentes.

El orden de implementación lo define el prefijo numérico de cada spec. Toda tarea
de implementación debe rastrear a un `tasks.md` generado desde la spec.

## VI. Flujo Spec Kit obligatorio

Toda feature debe seguir este flujo obligatorio:

```text
/speckit.specify
/speckit.clarify
/speckit.plan
/speckit.analyze
fix-report (solo si analyze encuentra hallazgos)
/speckit.analyze (confirma 0 hallazgos antes de tasks)
/speckit.tasks
/speckit.implement
```

Ninguna fase puede saltarse. Cada fase depende de los artefactos generados por la
fase anterior. El loop `analyze → fix-report → analyze` garantiza que `tasks.md`
se genere sobre artefactos limpios.

Reglas del flujo:

* `specify` crea o actualiza `spec.md`.
* `clarify` resuelve ambigüedades antes del plan.
* `plan` crea `plan.md` con decisiones técnicas y dependencias.
* `analyze` valida consistencia entre spec, plan y restricciones. Genera
  `report.md`.
* `fix-report` corrige hallazgos críticos y advertencias detectados por
  `analyze`. Se ejecuta solo si `report.md` contiene hallazgos.
* `analyze` se re-ejecuta tras `fix-report` para confirmar cero hallazgos.
* `tasks` crea `tasks.md` con tareas pequeñas, ordenadas y verificables.
* `implement` modifica código real solo después de existir spec, plan, report
  limpio y tasks.

Los comandos `speckit.specify` y `speckit.clarify` deben operar en modo
interactivo cuando existan decisiones abiertas. El comando `speckit.plan` puede
operar en modo interactivo solo cuando detecte decisiones estructurales no
resueltas que afecten la implementación o specs futuras.

## VII. Modo interactivo de preguntas

Cuando un comando o prompt opere en modo interactivo, DEBE hacer una sola
pregunta a la vez y esperar respuesta antes de continuar. Está prohibido lanzar
una lista completa de preguntas cuando la decisión requiera interacción guiada.

### 1. Cuándo usar modo interactivo

El modo interactivo debe usarse cuando existan:

- Ambigüedades funcionales en una spec.
- Decisiones técnicas que afecten el plan o la implementación.
- Criterios de aceptación incompletos.
- Gaps que puedan generar retrabajo durante `plan`, `tasks` o `implement`.
- Decisiones con más de una opción razonable y efectos distintos en código,
  pruebas, infraestructura o experiencia de usuario.

### 2. Formato de pregunta con opciones

Cada pregunta con opciones debe usar exactamente este formato:

```text
Pregunta [N de TOTAL] — [tema corto]
─────────────────────────────────────
[Enunciado claro de la pregunta]

Por qué importa: [1 línea explicando el impacto de decidir mal]

A) [opción concreta con valor específico]
B) [opción concreta con valor específico] ← Recomendado
C) [opción concreta con valor específico]
D) Otro — escribe tu respuesta

> Responde con la letra (A, B, C o D) o escribe tu respuesta libre.
```

Reglas de las opciones:

- Cada opción debe ser concreta, verificable y accionable.
- Las opciones deben ser mutuamente excluyentes.
- Cada opción debe llevar a un resultado distinto en spec, plan, tareas,
  implementación, pruebas o configuración.
- La opción marcada con `← Recomendado` debe ser la más alineada con FastAPI,
  PostgreSQL local, SQLAlchemy async, Docker o Docker Compose, `uv`,
  Python 3.13.13 y esta constitución.
- La opción `D) Otro` siempre debe estar presente cuando existan alternativas
  personalizadas razonables.

Ejemplo correcto:

```text
A) Colapsar sidebar por debajo de 768px.
B) Colapsar sidebar por debajo de 1024px. ← Recomendado
C) Colapsar sidebar por debajo de 1280px.
D) Otro — escribe tu respuesta
```

Ejemplo prohibido:

```text
A) Usar un breakpoint pequeño.
B) Usar un breakpoint estándar.
C) Usar un breakpoint grande.
```

### 3. Formato de pregunta Sí/No

Cuando la decisión sea binaria, debe usarse este formato:

```text
Pregunta [N de TOTAL] — [tema corto]
─────────────────────────────────────
[Enunciado de la pregunta]

Por qué importa: [1 línea]

S) Sí ← Recomendado
N) No

> Responde S o N.
```

La opción recomendada puede ser `S` o `N`, según la opción más consistente con
esta constitución y con la spec vigente.

### 4. Reglas de respuesta

Si el usuario responde con una letra (`A`, `B`, `C`, `S` o `N`), el agente debe:

1. Confirmar la elección en una línea con el valor concreto elegido.
2. Registrar la decisión para el resumen final.
3. Pasar inmediatamente a la siguiente pregunta.

Si el usuario responde `D` o escribe texto libre, el agente debe:

1. Aceptar la respuesta.
2. Confirmarla en una línea.
3. Registrar la decisión para el resumen final.
4. Pasar a la siguiente pregunta.

El agente no debe debatir la elección salvo que contradiga la constitución. Si
la respuesta contradice la constitución, debe pausar, explicar el conflicto y
pedir una alternativa válida.

### 5. Cierre del modo interactivo

Después de la última pregunta, el agente debe mostrar un resumen de decisiones
tomadas.

Según el comando en ejecución, debe actualizar el artefacto correspondiente:

- `speckit.specify`: integrar las decisiones en `spec.md`.
- `speckit.clarify`: añadir o actualizar la sección `Clarificaciones` en
  `spec.md`.
- `speckit.plan`: integrar las decisiones en `plan.md`.
- Prompts custom de clarificación: seguir el comportamiento declarado en el
  prompt, siempre que no contradiga esta constitución.

## VIII. Test-Driven Development

El ciclo Red-Green-Refactor es obligatorio:

1. **Red**: escribir primero una prueba que falle por el motivo correcto.
2. **Green**: implementar el código mínimo necesario para que la prueba pase.
3. **Refactor**: mejorar el diseño sin cambiar el comportamiento observable.

Reglas complementarias:

* No se escribe código de producción sin una prueba asociada.
* Toda regla de negocio debe estar cubierta por pruebas.
* Toda corrección de bug comienza con una prueba que reproduzca el fallo.
* Refactorizar solo con la suite de tests en verde.
* No se elimina ni debilita una prueba para hacer pasar la suite.

## IX. Calidad y validación

Toda implementación debe poder validarse localmente con comandos reproducibles.

El entry point unificado de calidad es el pre-commit, configurado en
`.pre-commit-config.yaml`. Los comandos equivalentes son:

```bash
make auto-checks          # pre-commit run --all-files (hooks automáticos)
make ci                   # auto-checks + tests + coverage + clean
```

Comandos individuales de referencia (ya cubiertos por pre-commit):

```bash
uv sync
uv run ruff check .       # cubierto por ruff-check hook
uv run ruff format .      # cubierto por ruff-format hook
uv run mypy --strict app/modules/  # cubierto por typecheck hook
```

Reglas de testing:

* Las pruebas unitarias usan pytest.
* Las pruebas asíncronas usan pytest-asyncio.
* Las pruebas HTTP usan httpx.AsyncClient.
* Las pruebas de integración que requieran PostgreSQL usan Testcontainers.
* La base de datos de pruebas debe estar aislada.
* Las pruebas deben ser deterministas y enfocadas en comportamiento observable.

### Organización de tests

La estructura de directorios de tests es obligatoria y no negociable:

```text
tests/
├── conftest.py          # Fixtures compartidas (cliente HTTP, etc.)
├── unit/                # Pruebas unitarias puras
│   └── <feature>/       # Sin dependencias externas de ningún tipo
└── integration/         # Pruebas de integración con infraestructura real
    └── <feature>/       # PostgreSQL vía Testcontainers
```

Reglas obligatorias:

* Los tests unitarios viven en `tests/unit/<feature>/`. Está PROHIBIDO que
  dependan de base de datos, red, sistema de archivos o cualquier
  infraestructura externa.
* Los tests de integración viven en `tests/integration/<feature>/`. DEBEN
  usar Testcontainers para PostgreSQL. Está PROHIBIDO conectarse a la base
  de datos de desarrollo.
* El directorio `tests/unit/` y `tests/integration/` son obligatorios en la
  raíz del repositorio. No se aceptan tests dentro de `app/modules/`.
* Las fixtures de infraestructura (conexión a BD, contenedores) solo pueden
  definirse en `tests/integration/conftest.py`. Está PROHIBIDO definirlas en
  `tests/conftest.py` raíz.
* El contenedor PostgreSQL de Testcontainers debe ser `postgres:16-alpine`,
  coherente con la imagen de desarrollo.

## X. Calidad de tests, mutation testing y poda de tests

La calidad de los tests no se mide por la cantidad ni por la cobertura de
líneas: se mide por su capacidad de detectar cambios incorrectos en el
comportamiento observable del sistema.

### 1. Principios

* La calidad de tests se mide por capacidad de detectar cambios incorrectos,
  no por cantidad de tests ni por cobertura de líneas.
* Toda regla de negocio nueva debe tener tests capaces de matar mutantes
  relevantes.
* La cobertura de líneas es señal secundaria; mutation testing es señal
  fuerte para reglas de negocio y validaciones.
* Está prohibido agregar tests triviales, duplicados o sin asserts útiles
  solo para aumentar métricas.
* Está permitido eliminar o fusionar tests de bajo valor cuando cumplan la
  política de poda de la sección X.4.
* Está prohibido eliminar tests únicamente para subir el mutation score o
  para hacer pasar la suite.
* Un test puede conservarse aunque no mate mutantes si protege un
  comportamiento valioso: smoke test crítico, contrato HTTP, DTO público,
  migración, seed, integración con base de datos, render server-side,
  wiring de rutas o templates, regresión documentada o gobernanza visual o
  estructural.
* Mutation testing debe aplicarse de forma focalizada por slice o módulo
  crítico, no obligatoriamente a todo el repositorio en cada cambio.

### 2. Herramienta

* `mutmut` es la herramienta de mutation testing declarada en el stack.
* Se declara como dependencia de desarrollo en `pyproject.toml`.
* Se configura mediante el bloque `[tool.mutmut]` en `pyproject.toml`,
  apuntando a `app/modules/` como código a mutar y a `tests/unit/` y
  `tests/integration/` como selección de tests para matar mutantes.
* Las ejecuciones por defecto son manuales y focalizadas; no forman parte
  del gate obligatorio de CI en esta enmienda.

### 3. Clasificación de mutantes sobrevivientes

Todo mutante que sobreviva a la suite debe clasificarse antes de actuar.
Las categorías mínimas son:

1. Falta de test valioso: existe una rama o camino no cubierto.
2. Test con assertion débil: existe el test pero su assert no detecta el
   cambio.
3. Mutante equivalente: el cambio no produce diferencia observable en
   comportamiento.
4. Código muerto o innecesario: la rama mutada no aporta valor.
5. Mutación irrelevante: el cambio no afecta comportamiento observable
   documentado.

### 4. Política de conservación y poda de tests

#### 4.1. Un test se conserva si cumple al menos una condición

* Mata mutantes no equivalentes en código de negocio.
* Cubre un requisito `FR`/`SC` o edge case de una `spec.md` aprobada.
* Protege un contrato HTTP o un DTO público.
* Protege una migración, un seed o una integración con base de datos.
* Protege render server-side o el wiring de rutas y templates.
* Reproduce una regresión histórica documentada.
* Es el smoke test mínimo de una capability crítica.
* Protege gobernanza visual, estructural o de configuración.

#### 4.2. Un test se puede eliminar o fusionar si cumple todas estas condiciones

* No mata mutantes relevantes del comportamiento que dice proteger.
* No está trazado a spec, contrato, bug o integración.
* Está duplicado por otro test más expresivo.
* Solo verifica detalle de implementación interna.
* Sus assertions son triviales o no validan comportamiento observable.
* Su eliminación no reduce la cobertura de requisitos ni el mutation score
  relevante.

#### 4.3. Reglas para borrar o fusionar tests

* Nunca borrar tests en bloque.
* Borrar o fusionar tests en cambios pequeños y revisables, idealmente
  dentro del mismo PR que ajusta la regla de negocio o el test más
  expresivo que lo sustituye.
* Después de eliminar o fusionar tests, ejecutar la suite normal y, si
  aplica, un ciclo focalizado de mutation testing sobre el módulo
  afectado.
* Todo test eliminado o fusionado debe dejar explícito cuál de las
  siguientes razones aplica:

  * El comportamiento queda cubierto por otro test más expresivo.
  * El test no era trazable a spec, contrato, bug o integración.
  * El test solo verificaba detalle interno.
  * El test tenía assertions triviales sin protección observable.
  * Existía duplicación directa con otro test.
  * El código asociado fue eliminado o simplificado en la misma
    enmienda.
* Si hay duda razonable, conservar el test o fusionarlo en lugar de
  eliminarlo.

### 5. Acción preferida ante un mutante sobreviviente

Ante un mutante que sobrevive a la suite, la acción se elige en este
orden de preferencia:

1. Mejorar un test existente para que su assert detecte el cambio.
2. Agregar un test mínimo y valioso si cubre un comportamiento de negocio
   real.
3. Fusionar tests redundantes.
4. Eliminar tests superficiales según la política de la sección X.4.
5. Simplificar o eliminar código innecesario.
6. Marcar el mutante como excluido con `# pragma: no mutate` solo si hay
   justificación explícita registrada en `tasks.md` o en `plan.md`.

### 6. Umbrales y cobertura

* No se exige una meta global del 100 % de mutation score.
* El baseline informativo se obtiene en la primera ejecución real.
* Los umbrales futuros, si los hubiera, deben ser por slice crítico,
  evolutivos y nunca deben bloquear por mutantes equivalentes
  documentados.
* La cobertura de líneas se mantiene como señal secundaria, con el mismo
  umbral del 80 % declarado en `scripts/ci/coverage.sh`.

### 7. Responsabilidad operativa de métricas de tests

La operación de métricas de calidad de tests es responsabilidad del
desarrollador humano. Mutation testing es una herramienta de auditoría y
aprendizaje, no una tarea automática delegable al agente ni una métrica
vanity.

#### 7.1. Interfaces oficiales

Las interfaces oficiales para ejecutar verificaciones de calidad de tests
DEBEN permanecer expuestas mediante el `Makefile`. Como mínimo el
proyecto DEBE conservar targets para:

* Ejecutar la suite de tests.
* Ejecutar coverage.
* Ejecutar mutation testing.
* Consultar resultados de mutation testing.
* Limpiar artefactos temporales de mutation testing.

#### 7.2. Alcance de responsabilidad de los agentes de IA

Los agentes de IA PUEDEN escribir, modificar o endurecer tests cuando
una tarea funcional lo requiera, pero NO son responsables de operar,
optimizar ni perseguir métricas globales de coverage o mutation testing
salvo instrucción explícita del desarrollador.

#### 7.3. Prohibiciones explícitas para los agentes de IA

Está PROHIBIDO que los agentes de IA, por iniciativa propia:

* Ejecuten ciclos exploratorios de mutation testing para maximizar
  score.
* Cambien umbrales, configuración o scope de mutation testing.
* Agreguen tests artificiales solo para matar mutantes.
* Eliminen tests únicamente porque no mejoran coverage o mutation
  score.
* Usen el mutation score global como objetivo de implementación.
* Marquen mutantes con `# pragma: no mutate` sin justificación
  aprobada por el desarrollador.
* Conviertan mutation testing en gate obligatorio de CI sin
  aprobación explícita.

#### 7.4. Acciones permitidas para los agentes de IA

Los agentes de IA SÍ PUEDEN:

* Proponer tests mínimos y valiosos cuando el desarrollador
  proporcione evidencia concreta, como un mutante sobreviviente, bug
  reproducible, requisito de spec o contrato roto.
* Endurecer assertions débiles en tests existentes.
* Fusionar tests redundantes cuando el comportamiento protegido
  permanezca cubierto.
* Explicar la clasificación de mutantes sobrevivientes.
* Documentar decisiones tomadas por el desarrollador sobre mutantes
  equivalentes, irrelevantes o aceptados.

#### 7.5. Responsabilidad reservada al desarrollador

La clasificación final de sobrevivientes, la aceptación de mutantes
equivalentes, la actualización de baselines, la poda de tests y la
interpretación de métricas quedan bajo criterio exclusivo del
desarrollador humano.

## XI. Base de datos

* PostgreSQL se ejecuta localmente con Docker o Docker Compose.
* La base de datos de producción no usará Supabase.
* Las migraciones se gestionan exclusivamente con Alembic.
* Las sesiones de base de datos se manejan mediante dependencias controladas con
  inyección de `AsyncSession`.
* `config/app.yaml` nunca debe versionarse con secretos reales.
* `config/app.example.yaml` debe existir como plantilla de configuración.
* La infraestructura local debe usar archivos `.yaml`, nunca `.yml`.

## XII. Async-First

Todo I/O del sistema debe ser asíncrono cuando forme parte del flujo web,
persistencia o integración externa.

Esto incluye:

* Base de datos.
* HTTP saliente.
* Colas.
* Storage remoto.
* Servicios externos.
* Operaciones de infraestructura.

Solo se permite `def` síncrono para puro cómputo en memoria, mapeos, cálculos o
validaciones sin I/O.

## XIII. Frontend y sistema visual

La interfaz será server-rendered con Jinja2 y mejorada progresivamente con HTMX.
No se debe convertir la aplicación en una SPA.

Reglas obligatorias:

* HTMX vive vendoreado en `app/static/vendor/htmx.min.js`.
* El CSS propio vive en `app/static/css/app.css`.
* Los iconos SVG outline viven en `app/static/icons/`.
* La librería estándar de iconografía es Lucide.
* Las plantillas compartidas viven en `app/templates/`.
* Las plantillas específicas viven dentro del módulo correspondiente.
* Los componentes compartidos viven en `app/templates/components/`.
* Las macros compartidas viven en `app/templates/macros/`.

### Blindaje de tokens visuales canónicos

Los tokens visuales canónicos definidos en
`.opencode/instructions/frontend.instructions.md` y en `app/static/css/app.css`
están protegidos contra modificaciones no autorizadas.

* Cualquier cambio en tokens visuales canónicos (colores, sombras, radios,
  espaciados, tipografía, breakpoints, layout base, componentes compartidos,
  macros de iconos o patrones visuales de estados) requiere autorización
  explícita, justificación y trazabilidad en `tasks.md` con el marcador
  `[visual]`.
* Las extensiones (nuevos tokens que no modifican los existentes) se permiten
  con marcador `[visual][extension]`.
* Las correcciones de bugs visuales se permiten con marcador
  `[visual][bugfix]`.
* Toda modificación de un token existente debe registrarse en
  `Complexity Tracking` de `plan.md` con justificación.
* La fuente operativa de los tokens es
  `.opencode/instructions/frontend.instructions.md`.
* La spec `002-blindar-tokens-visuales` define el proceso completo de
  gobernanza visual.

### Sistema visual canónico

Para todo trabajo frontend, la definición canónica de tokens visuales vive en
`.opencode/instructions/frontend.instructions.md`.

La implementación en `app/static/css/app.css`, templates Jinja, componentes,
macros e iconografía DEBE respetar exactamente esos tokens visuales.

No se aceptan cambios implícitos de color, sombra, radio, espaciado, tipografía,
breakpoints, layout base o patrones visuales compartidos por criterio estético
durante la implementación.

Toda variación de tokens visuales canónicos requiere:

- Spec aprobada.
- Autorización explícita.
- Actualización de las instrucciones frontend, si corresponde.
- Trazabilidad en `tasks.md`.
- Registro en `Complexity Tracking` cuando implique una desviación visual global.

El incumplimiento de esta regla invalida la implementación de la spec en revisión.

## XIV. Estructura obligatoria del repositorio

La estructura base del proyecto debe respetar esta organización:

```text
app/
  __init__.py
  main.py
  config/
    __init__.py
    settings.py
    paths.py
  infra/
    database.py
  modules/
    <feature>/
      routes.py
      schemas.py
      models.py
      repository.py
      service.py
      templates/
        *.html
    health/
      __init__.py
      routes.py
      schemas.py
  static/
    css/
      app.css
    vendor/
      htmx.min.js
    icons/
      *.svg
  templates/
    base.html
    components/
      _*.html
    macros/
      *.html
alembic/
  env.py
  versions/
config/
  app.example.yaml
tests/
  conftest.py
  unit/
    <feature>/
      test_*.py
  integration/
    conftest.py
    <feature>/
      test_*.py
.pre-commit-config.yaml
.repomixignore
pyproject.toml
uv.lock
docker-compose.yaml
```

Cualquier desviación debe justificarse en `plan.md`.

## XV. Contratos de dominio

* Las entidades SQLAlchemy no se exponen como respuesta HTTP.
* Las respuestas HTTP se mapean a DTOs Pydantic.
* Todos los DTOs Pydantic deben usar `model_config = ConfigDict(frozen=True)`.
* Los estados de dominio se modelan con `Enum` o tipos explícitos.
* Los errores usan `HTTPException` o modelos de error tipados.
* Los límites del sistema validan entradas antes de ejecutar lógica de negocio.

## XVI. Complexity Tracking

Toda desviación del stack, arquitectura, estructura, flujo obligatorio o reglas
de esta constitución debe registrarse explícitamente en la sección
`Complexity Tracking` de `plan.md`.

Debe incluir:

* Qué regla se desvía.
* Por qué la desviación es necesaria.
* Alternativas consideradas.
* Riesgos introducidos.
* Cómo se mitigarán esos riesgos.
* Cómo se validará que la desviación no rompe el sistema.

En ausencia de justificación, la desviación debe rechazarse.

## XVII. Jerarquía de autoridad

Durante la implementación de una spec, aplica el siguiente orden de prioridad
ante cualquier conflicto:

```text
constitución > spec > AGENTS.md > instructions > comando
```

Si hay conflicto entre capas, se debe pausar, advertir el conflicto
explícitamente y seguir la capa de mayor autoridad.

## XVIII. Gobernanza

* Esta constitución es la fuente de verdad suprema del proyecto. Ninguna
  decisión, spec o implementación puede contradecirla.
* Toda modificación a esta constitución requiere una enmienda documentada con
  justificación, impacto evaluado y plan de migración si aplica.
* Las enmiendas se versionan siguiendo el esquema semántico
  `MAJOR.MINOR.PATCH`.
* **MAJOR**: cambios incompatibles en stack, arquitectura, flujo obligatorio o
  principios.
* **MINOR**: nuevas secciones, nuevos principios o ampliaciones materiales.
* **PATCH**: correcciones de redacción, aclaraciones o cambios no semánticos.
* El cumplimiento de esta constitución se verifica en cada code review y en cada
  etapa del flujo Spec-Driven.
* La complejidad introducida debe justificarse explícitamente. Ante la duda,
  elegir la opción más simple.

## XIX. Historial de versiones

* **v1.0.0** — Versión inicial de la constitución del proyecto Realtor.
* **v1.1.0** — Agregado el protocolo de modo interactivo de preguntas para
  `speckit.specify`, `speckit.clarify`, `speckit.plan` y prompts custom de
  clarificación.
* **v1.2.0** — Agregada la regla de blindaje de tokens visuales canónicos en
  la sección XIII, exigiendo autorización explícita, justificación y trazabilidad
  en `tasks.md` con marcador `[visual]`.
* **v1.3.0** — Agregada la subsección «Organización de tests» en la sección IX
  con estructura obligatoria `tests/unit/` y `tests/integration/`, prohibición
  de dependencias externas en tests unitarios, obligatoriedad de Testcontainers
  en tests de integración, y prohibición de tests dentro de `app/modules/`.
  Actualizada la estructura del repositorio en la sección XIV para reflejar
  la nueva ubicación de tests. Corregido el nivel jerárquico de la
  subsección «Sistema visual canónico».
* **v1.3.1** — Documentado `.pre-commit-config.yaml` como entry point unificado
  de calidad en las secciones II, IX y XIV. Agregados pyupgrade, ruff-format y
  pydocstyle al stack. Actualizados los comandos de validación para referenciar
  `make auto-checks`/`make ci`. Corregida la instrucción `backend.instructions.md`
  para eliminar `tests/` de los artefactos del módulo. Sincronizados `AGENTS.md`
  y `conventions.instructions.md` con estos cambios.
* **v1.3.2** — Actualizado el informe de impacto de sincronización. Agregado
  `format-docstrings` a la fila Pre-commit del stack. Agregado `.repomixignore`
  a la estructura obligatoria del repositorio.
* **v1.4.0** — Consolidada la configuración en `config/app.yaml` como fuente
  única (eliminado `.env`). Extraído `GET /health` a `app/modules/health/`.
  Registrados todos los routers en `app/main.py`. Corregida la estructura del
  repositorio: `app/config.py` → `app/config/`, `app/database.py` →
  `app/infra/database.py`, `.env.example` → `config/app.example.yaml`.
  Sincronizados `AGENTS.md`, instrucciones y `db_preflight.py`.
* **v1.5.0** — El mínimo de cada spec pasa de 3 a 7 archivos obligatorios en la
  sección V: `data-model.md`, `contracts/<feature>.yaml`, `quickstart.md` y
  `research.md` se suman a `spec.md`, `plan.md` y `tasks.md`. La regla aplica
  consistentemente a toda spec nueva (≥ 008) y se hizo backfill de la spec 007
  en la enmienda. Las specs 001-006 ya contaban con estos archivos por
  convención previa. Sin cambios al stack, arquitectura ni flujo SDD
  existente.
* **v1.6.0** — Agregada la sección X «Calidad de tests, mutation testing y
  poda de tests». Se declara `mutmut` como herramienta de mutation testing,
  se prohíbe agregar tests triviales o duplicados solo para subir métricas,
  se permite eliminar o fusionar tests de bajo valor con justificación
  explícita y se prohíbe eliminar tests únicamente para subir el mutation
  score. Mutation testing entra como práctica focalizada y manual, sin meta
  global del 100 % de coverage de mutación y sin formar parte obligatoria
  del gate de CI. Renumeradas las secciones X-XVIII a XI-XIX para abrir
  espacio a la nueva sección X. Actualizadas las referencias cruzadas en
  `AGENTS.md`, `.opencode/instructions/frontend.instructions.md` y
  `.specify/templates/spec-template.md` para apuntar a la nueva sección
  XIII (Frontend). Sincronizados `pyproject.toml` (dependencia de
  desarrollo `mutmut` y bloque `[tool.mutmut]`), `.gitignore` (salidas de
  mutmut), `Makefile` (targets `mutation`, `mutation-browse`,
  `mutation-results`) y `scripts/ci/mutation.sh` (nuevo script bajo el
  mismo patrón que `test.sh` y `coverage.sh`). Creados
  `docs/testing/mutation-testing.md` (guía de uso) y
  `docs/testing/test-value-audit.md` (auditoría inicial de valor de
  tests). Actualizadas `.opencode/instructions/tests.instructions.md`
  para incorporar `mutmut` y la política de poda. Sin cambios al stack,
  arquitectura ni flujo SDD existente.
* **v1.7.0** — Agregada la subsección X.7 «Responsabilidad operativa de
  métricas de tests» dentro de la sección X. Se precisa que la operación
  de métricas de calidad de tests es responsabilidad del desarrollador
  humano. Se declaran los targets de Makefile mínimos obligatorios:
  tests, coverage, mutation, mutation-results y mutation-clean. Se
  enumeran las prohibiciones explícitas para los agentes de IA
  (prohibido ejecutar ciclos exploratorios para maximizar score, cambiar
  umbrales o scope por iniciativa propia, agregar tests artificiales,
  eliminar tests por score, usar mutation score como objetivo, marcar
  `# pragma: no mutate` sin aprobación del desarrollador y convertir
  mutation testing en gate obligatorio de CI sin aprobación). Se
  enumeran las acciones permitidas (proponer tests con evidencia
  concreta, endurecer asserts débiles, fusionar redundantes, explicar
  clasificación de sobrevivientes, documentar decisiones del
  desarrollador). Se reserva al desarrollador la clasificación final de
  sobrevivientes, la aceptación de mutantes equivalentes, la
  actualización de baselines, la poda de tests y la interpretación de
  métricas. Sincronizados `.opencode/instructions/tests.instructions.md`
  y `docs/testing/mutation-testing.md` con la nueva subsección, y
  agregado el target `mutation-clean` al `Makefile` para limpiar el
  directorio `mutants/`. Sin cambios al stack, arquitectura, flujo SDD
  ni a los principios ya establecidos en la sección X.

**Versión**: 1.7.0 | **Ratificada**: 2026-06-08 | **Última enmienda**: 2026-06-20
