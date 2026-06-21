---
applyTo: "app/modules/**/tests/**,app/tests/**"
---

# Tests — pytest + pytest-asyncio + httpx.AsyncClient + Testcontainers + mutmut

## Ciclo TDD (Red-Green-Refactor)

1. Red: escribir primero una prueba que falle por el motivo correcto.
2. Green: implementar el código mínimo para que la prueba pase.
3. Refactor: mejorar el diseño con la suite en verde.

NUNCA escribir código de producción sin una prueba asociada.

## Tooling

- pytest como runner principal.
- pytest-asyncio para tests async (`@pytest.mark.asyncio` o modo auto).
- httpx.AsyncClient para tests de endpoints FastAPI.
- Testcontainers (postgres) para tests de integración con base de datos.
- mutmut como herramienta de mutation testing (sección X de la constitución).
- Ejecución: `uv run pytest`, `make mutation` para mutmut.

## Estructura de archivos de test

- Archivos: `test_<módulo>.py` dentro de `tests/` del módulo.
- Clases: `Test<Entidad>` cuando agrupa tests relacionados.
- Funciones: `test_<acción>_<resultado>`.

Ejemplo:

```text
app/modules/propiedades/tests/
  test_routes.py
  test_service.py
  test_repository.py
```

## Tests unitarios

- Aíslan la unidad bajo prueba; dependencias externas se mockean.
- Mock con `unittest.mock` o `pytest-mock` (`mocker` fixture).
- Cada test debe verificar comportamiento observable, no detalle interno
  de implementación.
- Está prohibido usar mocks que reproduzcan la implementación original
  en lugar de verificar el resultado.

Ejemplo de mock de repositorio:

```python
@pytest.mark.asyncio
async def test_crear_propiedad_retorna_schema(mocker):
    repo_mock = mocker.patch(
        "app.modules.propiedades.repository.crear",
        return_value=PropiedadFactory.build(),
    )
    result = await service.crear_propiedad(session, payload)
    assert isinstance(result, PropiedadOut)
    repo_mock.assert_called_once()
```

## Tests de endpoints (httpx.AsyncClient)

- Usar `httpx.AsyncClient` con `ASGITransport` apuntando a la app FastAPI.
- Preferir cliente asíncrono vía fixtures de sesión.

```python
@pytest.mark.asyncio
async def test_crear_propiedad_endpoint(async_client):
    payload = {"direccion": "Calle 123", "precio": 1500.00}
    response = await async_client.post("/api/propiedades/", json=payload)
    assert response.status_code == 201
    assert response.json()["direccion"] == "Calle 123"
```

## Tests de integración (Testcontainers)

- Usar Testcontainers para levantar PostgreSQL efímero.
- La base de datos de pruebas DEBE estar aislada.
- Aplicar migraciones con Alembic antes de cada sesión.
- Cada test limpia o revierte su estado (transacciones o truncate).

## Fixtures y fábricas

- Fixtures en `conftest.py` del módulo o raíz de tests.
- Usar fábricas (Factory Boy o helpers propios) para generar entidades
  de prueba.
- NUNCA usar datos de producción en tests.

```python
# conftest.py
@pytest.fixture
def async_client():
    transport = ASGITransport(app=app)
    return httpx.AsyncClient(transport=transport, base_url="http://test")
```

## Cobertura

- Cobertura de líneas es señal secundaria. Ver sección X de la constitución.
- Toda regla de negocio debe tener al menos un test capaz de matar
  mutantes relevantes.
- Toda corrección de bug comienza con un test que reproduce el fallo.

## Mutation testing (mutmut)

La herramienta oficial de mutation testing es `mutmut`. La política y los
criterios completos están en la sección X de la constitución. Esta
instrucción resume el flujo operativo.

### Flujo recomendado

1. Ejecutar la suite normal para confirmar verde:
   ```bash
   uv run pytest
   ```
2. Ejecutar mutation testing focalizado sobre el slice afectado:
   ```bash
   make mutation
   ```
   Equivalente directo: `bash scripts/ci/mutation.sh` o
   `uv run mutmut run`.
3. Revisar sobrevivientes con `make mutation-browse` o
   `uv run mutmut results`.
4. Clasificar cada sobreviviente (ver constitución X.3):

   * Falta de test valioso.
   * Test con assertion débil.
   * Mutante equivalente.
   * Código muerto o innecesario.
   * Mutación irrelevante para comportamiento observable.

5. Mejorar tests valiosos con assertion débil hasta que maten el mutante.
6. Agregar un test mínimo y valioso solo si protege comportamiento real.
7. Fusionar tests redundantes.
8. NO agregar tests triviales solo para subir el score.

### Configuración

- `mutmut` se configura en `[tool.mutmut]` dentro de `pyproject.toml`.
- `source_paths = ["app/modules/"]` limita el alcance al Vertical Slice.
- `pytest_add_cli_args_test_selection` apunta a `tests/unit/` y
  `tests/integration/`. La ejecución con `tests/integration/` requiere
  Docker disponible.
- `do_not_mutate` excluye `__init__.py`, `routes.py` y `health/*`
  (capas sin lógica de negocio o triviales).
- `mutate_only_covered_lines = true` evita perder tiempo en código no
  cubierto por la suite.

### Comandos disponibles

```bash
make mutation            # corre suite + mutmut run
make mutation-browse     # UI textual para revisar mutantes
make mutation-results    # resumen agregado
uv run mutmut show <id>  # detalle de un mutante concreto
uv run mutmut run        # solo mutación (sin suite previa)
```

## Política de conservación y poda de tests

La política completa está en la sección X.4 de la constitución. Esta
instrucción la resume en términos operativos.

### Cuándo conservar un test

Un test se conserva si cumple al menos una de estas condiciones:

* Mata mutantes no equivalentes en código de negocio.
* Cubre un requisito `FR`/`SC` o edge case de una `spec.md` aprobada.
* Protege un contrato HTTP o un DTO público.
* Protege una migración, un seed o una integración con base de datos.
* Protege render server-side o el wiring de rutas y templates.
* Reproduce una regresión histórica documentada.
* Es el smoke test mínimo de una capability crítica.
* Protege gobernanza visual, estructural o de configuración.

### Cuándo fusionar o eliminar un test

Un test solo puede eliminarse o fusionarse si cumple TODAS estas
condiciones:

1. No mata mutantes relevantes del comportamiento que dice proteger.
2. No está trazado a spec, contrato, bug o integración.
3. Está duplicado por otro test más expresivo.
4. Solo verifica detalle de implementación interna.
5. Sus assertions son triviales o no validan comportamiento observable.
6. Su eliminación no reduce la cobertura de requisitos ni el mutation
   score relevante.

### Reglas operativas para podar

* Nunca borrar tests en bloque.
* Borrar o fusionar tests en cambios pequeños y revisables.
* Después de podar, ejecutar `uv run pytest` y, si aplica,
  `make mutation` sobre el módulo afectado.
* Todo test eliminado debe dejar explícita la razón: cobertura por otro
  test más expresivo, no trazable, solo detalle interno, assertion
  trivial, duplicación directa o código asociado eliminado.
* Si hay duda razonable, conservar el test o fusionarlo en lugar de
  eliminarlo.
* Está prohibido eliminar tests únicamente para subir el mutation score
  o para hacer pasar la suite.
* Está prohibido agregar tests triviales, duplicados o sin asserts útiles
  solo para aumentar métricas.

### Mocks permisivos: señal de test débil

Un mock que reproduce la implementación original en lugar de verificar
el resultado es candidato a test de bajo valor. Reglas:

* Preferir pocos tests expresivos sobre muchos tests superficiales.
* Un test que solo verifica que una función llama a otra función interna
  es candidato a eliminación si no protege comportamiento observable.
* Un test que solo verifica detalles de implementación interna (formato
  exacto de logs, orden de llamadas sin relevancia funcional, etc.) es
  candidato a eliminación salvo que proteja un contrato explícito.

## Prohibiciones

- Tests que dependen de orden de ejecución o estado compartido mutable.
- Tests que llaman servicios externos reales (APIs, Redis, etc.).
- Tests que usan la base de datos de desarrollo o producción.
- Eliminar tests para hacer pasar la suite.
- Eliminar tests solo para subir el mutation score.
- Agregar tests triviales, duplicados o sin asserts útiles para subir
  métricas.
- Marcar una tarea como terminada si sus tests no pasan.
- Mocks que reproduzcan la implementación original en lugar de verificar
  el resultado.
