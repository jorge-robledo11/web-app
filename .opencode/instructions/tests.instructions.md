---
applyTo: "app/modules/**/tests/**,app/tests/**"
---

# Tests — pytest + pytest-asyncio + httpx.AsyncClient + Testcontainers

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
- Ejecución: `uv run pytest`.

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
- La base de datos de pruebas DEBE estar aislada por sesión.
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

- Priorizar reglas de negocio sobre cobertura superficial de líneas.
- Toda regla de negocio debe tener al menos un test.
- Toda corrección de bug comienza con un test que reproduce el fallo.

## Prohibiciones

- Tests que dependen de orden de ejecución o estado compartido mutable.
- Tests que llaman servicios externos reales (APIs, Redis, etc.).
- Tests que usan la base de datos de desarrollo o producción.
- Eliminar tests para hacer pasar la suite.
- Marcar una tarea como terminada si sus tests no pasan.
