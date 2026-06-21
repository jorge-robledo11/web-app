# Auditoría de valor de tests

Auditoría inicial del estado de los tests del proyecto al cierre de la
enmienda v1.6.0 de la constitución. Sirve como línea base para aplicar la
política de conservación y poda de la sección X.4.

## Contexto

* Total de tests collected: 136 (a partir de `uv run pytest --collect-only -q`).
* 113 tests pasan sin Docker (suite unitaria).
* 23 tests adicionales viven en `tests/integration/` y requieren
  Testcontainers con `postgres:16-alpine` y Docker.
* mutmut 3.6.0 está instalado como dependencia de desarrollo y
  configurado en `[tool.mutmut]` con `source_paths = ["app/"]`,
  `do_not_mutate` para `__init__.py`, `routes.py`, `main.py`,
  `infra/`, `config/` y `health/`, y `also_copy = ["config/"]`.
* Ejecución verificada sobre un subconjunto reducido (`--max-children 1`):
  la cobertura se recolecta correctamente y mutmut detecta el primer
  mutante. Hay un caveat conocido documentado en la sección
  [Limitaciones detectadas](#limitaciones-detectadas).

## Limitaciones detectadas

1. **mutmut + Pydantic v2 + `Decimal`**: al ejecutar la cobertura sobre
   `tests/unit/propiedades/test_schemas_form.py::test_acepta_datos_validos_completos`,
   mutmut reporta un falso positivo en la validación `Decimal` del DTO.
   El test pasa en `uv run pytest` y al correr pytest desde `mutants/`
   con el venv del padre, pero mutmut (que usa `pytest.main()` in-process
   y aplica su `wrap_in_trampoline` sobre los métodos de las clases
   Pydantic) genera un error de validación que no se reproduce fuera de
   mutmut. Esto sugiere una interacción entre el trampoline de mutmut y
   `BaseModel.__init__` de Pydantic v2 cuando se le pasa `Decimal` como
   valor de campo. Workaround tentativo: usar `only_mutate` para
   restringir mutmut a archivos que no contengan DTOs Pydantic
   problemáticos, o agregar `# pragma: no mutate` en los `Field` con
   `Decimal`. No se ha aplicado workaround en esta primera versión.

2. **Tests de integración requieren copiar más archivos**:
   `pytest_add_cli_args_test_selection` se limita a `["tests/unit/"]` en
   esta primera versión. Para incluir `tests/integration/`, los conftests
   invocan `alembic` y `scripts/dev/seed_propiedades.py` como subprocess
   con `cwd=mutants/`, lo que requiere copiar `alembic/`, `alembic.ini`
   y `scripts/` a `mutants/` (agregar a `also_copy`). Sin esos archivos,
   el subprocess de alembic falla con código 255.

3. **Baseline cuantitativo no generado**: la primera ejecución real de
   `make mutation` con alcance completo tarda horas. Esta primera versión
   valida la instalación, la configuración y la viabilidad del flujo, no
   el score cuantitativo. El baseline se obtendrá en una iteración
   posterior.

## Inventario por archivo

### `tests/unit/test_health.py`

* `test_health_ok` → smoke test del módulo `health/`. Protege contrato
  HTTP mínimo: el endpoint responde 200 y JSON con `status: "ok"`.
  **Conservar.** Smoke crítico, no mata mutantes pero protege contrato.
* `test_health_db_unavailable` → verifica que el endpoint maneja DB caída
  con status 503. Protege un camino de fallo.
  **Conservar.** Cubre comportamiento observable ante fallo de
  infraestructura.

### `tests/unit/dashboard/test_repository.py`

* `test_obtener_metricas_con_datos` → mockea `contar_por_estado` y
  `contar_total`, verifica que `obtener_metricas` retorna el dict con los
  conteos. **Conservar.** Cubre la lógica de agregación de métricas
  (rama de negocio).
* `test_obtener_metricas_sin_datos` → verifica que retorna ceros cuando
  no hay propiedades. **Conservar.** Edge case importante (lista vacía
  → no debe romper la UI).

### `tests/unit/dashboard/test_service.py`

* `test_construir_contexto_con_datos` → mockea el repo, verifica que el
  contexto se construye con valores correctos y formato de métricas
  (label, valor, icono). **Conservar.** Protege reglas de presentación
  (mapeo de estado → icono, formato de label).
* `test_construir_contexto_sin_propiedades` → verifica `vacio is True`
  cuando no hay datos. **Conservar.** Edge case UI (estado vacío).
* `test_construir_contexto_solo_disponibles` → verifica que `vacio` no
  se activa con solo disponibles. **Conservar.** Edge case de borde.
* `test_construir_contexto_solo_rentadas` → simétrico al anterior.
  **Conservar.** Edge case de borde.

### `tests/unit/dashboard/test_routes.py`

* `test_dashboard_route_renderiza_html_con_metricas` → usa ASGITransport
  y verifica que GET / renderiza HTML con strings clave. **Conservar.**
  Smoke test de wiring de rutas + render server-side.
* `test_dashboard_route_actividad_*` (varios) → verifican render de
  sección "actividad reciente" con distintos estados. **Conservar.**
  Cubre render condicional según estado.

### `tests/unit/propiedades/test_models.py`

* `TestEstadoPropiedad`:
  * `test_es_str_enum` → verifica que `EstadoPropiedad` es `StrEnum`.
    **Conservar.** Protege requisito de catálogo cerrado.
  * `test_cuatro_valores` → verifica cardinalidad.
    **Candidato a fusionar** con `test_valores_esperados`: ambos
    verifican el catálogo. Podrían ser un único test que verifique
    contenido y cardinalidad juntos.
  * `test_valores_esperados` → verifica los 4 valores literales.
    **Candidato a fusionar** con `test_cuatro_valores`.

  **Acción recomendada:** fusionar `test_cuatro_valores` y
  `test_valores_esperados` en un único test
  `test_catalogo_tiene_cuatro_valores_esperados`. La fusión no reduce
  cobertura; ambos asserts verifican el mismo objeto.

* `TestPropiedad`:
  * `test_tabla_es_propiedades` → verifica `__tablename__`.
    **Conservar.** Convención de nombres de la constitución (XIII).
  * `test_once_atributos_minimos` → verifica ≥11 columnas. Mapea a FR-001.
    **Conservar.** Trazado a spec, valida requisito de columnas.
  * Resto de tests de atributos → verifican tipos, nulabilidad, defaults
    y unique constraint. **Conservar.** Protegen invariantes del modelo.

### `tests/unit/propiedades/test_schemas.py`

* `TestPropiedadIn`:
  * `test_es_frozen` → verifica inmutabilidad del DTO.
    **Conservar.** Constitución XIV exige `ConfigDict(frozen=True)`.
  * `test_estado_invalido_rechazado` → verifica rechazo de estado fuera
    del catálogo (FR-003). **Conservar.** Protege contrato público.
  * Tests recientes de `area` (`test_area_cero_valido`,
    `test_area_default_cero`) introducidos en spec 007. **Conservar.**
    Cubren la modificación `gt=0` → `ge=0, default=0`.

* `TestPropiedadOut`:
  * Verificaciones de shape y tipos. **Conservar.** Protege DTO público.

### `tests/unit/propiedades/test_schemas_form.py` (spec 007)

* `TestPropiedadFormIn` con 12 tests. Verifican:
  * Defaults (`ciudad=Miami`, `estado=disponible`).
  * Validación de campos requeridos.
  * Conversión de strings numéricos vacíos.
  * Edge cases del DTO de formulario.

  **Conservar.** Trazado a spec 007 FR/SC. Protegen el contrato del
  formulario que es la entrada del feature.

### `tests/unit/propiedades/test_service_listar.py`

* `TestFormatPrecio` (4 tests) → verifican formato de precio con
  distintos tipos de entrada (int, decimal, float, miles).
  **Conservar.** Edge cases de formato.
* `TestFormatArea` (3 tests) → verifican formato de área (pequeño, miles,
  grande). **Conservar.** Edge cases de formato.
* `TestListarPropiedades` (3 tests) → verifican la función de listado
  (dict con campos correctos, lista vacía, decimales).
  **Conservar.** Protege la función principal de lectura.

### `tests/unit/propiedades/test_service_crear_formulario.py` (spec 007)

* `TestGenerarUrlImagen` (3 tests) → verifican formato de URL picsum,
  fallback a string vacío cuando no se genera, y helper
  `_formatear_url_picsum` mockable. **Conservar.** Protege la lógica
  de generación de imagen.
* `TestCrearPropiedadDesdeFormulario` (6 tests) → verifican:
  * Aplicación de defaults (`ciudad=Miami`, `estado=disponible`).
  * Propagación de `area=0`.
  * Detección de duplicados (retorna `None`).
  * Retorno de DTO en éxito.
  * Imagen no vacía.

  **Conservar.** Trazado a spec 007 FR-002, FR-003, FR-004, FR-008.

### `tests/integration/dashboard/test_dashboard.py`

* Smoke test del endpoint dashboard con Testcontainers.
  **Conservar.** Smoke + render real + DB real. Cubre FR-002, SC-001.

### `tests/integration/propiedades/test_migration.py`

* `TestMigracionPropiedades.test_upgrade_head_crea_tabla` → verifica
  que la migración aplica y el head es el esperado. **Conservar.**
  Protección de migración + smoke del head hash.

### `tests/integration/propiedades/test_repository.py`

* `TestRepositorioPropiedades` con varios tests contra PostgreSQL real.
  **Conservar.** Integración real con DB; valida queries, paginación,
  filtros.

### `tests/integration/propiedades/test_routes.py`

* `TestPropiedadesRoutes` con tests de GET /propiedades, render,
  paginación. **Conservar.** Integración real (HTTP + DB + templates).

### `tests/integration/propiedades/test_routes_crear.py` (spec 007)

* 15 tests de los endpoints `GET /propiedades/nueva` y `POST /propiedades`.
  Incluyen:
  * Render del formulario.
  * Validación de campos (precio, habitaciones, baños, área, título,
    dirección).
  * Redirección 303 al éxito.
  * Flash firmado HMAC en cookie.
  * Re-render con errores inline.
  * Detección de duplicados.

  **Conservar.** Trazado a spec 007. Protege contratos HTTP, DTOs,
  validaciones y edge cases del feature.

### `tests/integration/propiedades/test_seed.py`

* `TestSeedPropiedades` (4 tests) → verifican:
  * Primera ejecución deja 10 propiedades (SC-002).
  * Segunda ejecución mantiene cardinalidad (SC-003).
  * Estados válidos en el seed (SC-004).
  * Idempotencia del seed.

  **Conservar.** Protección de seed + contrato observable.

### `tests/integration/propiedades/test_service.py`

* `TestServicioPropiedades` con tests del service contra DB real.
  **Conservar.** Integración real con DB; valida queries y mapeos.

## Resumen por categoría

| Categoría                                                          | Tests | Archivos                                                                                |
|--------------------------------------------------------------------|-------|-----------------------------------------------------------------------------------------|
| Tests que protegen reglas de negocio                                | ~30   | `test_service.py` (dashboard), `test_service_listar.py`, `test_service_crear_formulario.py`, `test_repository.py` (dashboard) |
| Tests que protegen contratos HTTP o DTOs públicos                   | ~25   | `test_schemas.py`, `test_schemas_form.py`, `test_routes.py` (dashboard), `test_routes_crear.py` |
| Tests que protegen migraciones, seeds o integración con base de datos| ~12  | `test_migration.py`, `test_seed.py`, `tests/integration/propiedades/test_repository.py`, `tests/integration/propiedades/test_service.py`, `tests/integration/dashboard/test_dashboard.py` |
| Tests que protegen render server-side o wiring de rutas            | ~6    | `test_dashboard_route_renderiza_html_con_metricas`, varios en `test_routes_crear.py`    |
| Tests de smoke críticos                                            | ~2    | `test_health_ok`, `test_dashboard_route_renderiza_html_con_metricas`                     |
| Tests de regresión histórica                                       | 0     | (No hay regresiones documentadas aún; el primer bug reproducido con test se considera)   |
| Tests redundantes candidatos a fusionar                            | 2     | `test_cuatro_valores` y `test_valores_esperados` en `test_models.py`                     |
| Tests superficiales candidatos a eliminar                          | 0     | (No se identificaron superficiales)                                                     |
| Tests con assertions débiles candidatos a mejorar                  | 0     | (Pendiente de mutmut run; sin baseline cuantitativo)                                     |
| Mutantes sobrevivientes que revelan falta de test                  | TBD   | Requiere primera ejecución de `make mutation`                                            |
| Mutantes sobrevivientes equivalentes o irrelevantes                 | TBD   | Requiere primera ejecución de `make mutation`                                            |

## Decisiones aplicadas en esta auditoría

* **Fusionar 2 tests en `test_models.py`**:
  * `test_cuatro_valores` y `test_valores_esperados` se fusionan en un
    único `test_catalogo_tiene_cuatro_valores_esperados`. Razón:
    duplicación directa; ambos asserts verifican el mismo objeto.

* **No se eliminan tests en esta primera iteración**. La política de
  poda de la sección X.4 exige:

  1. No matar mutantes relevantes.
  2. No trazado a spec, contrato, bug o integración.
  3. Duplicado por otro test más expresivo.
  4. Solo detalle de implementación interna.
  5. Assertions triviales.
  6. Sin reducción de cobertura de requisitos ni mutation score.

  La auditoría cualitativa no encontró ningún test que cumpla las 6
  condiciones simultáneamente. La auditoría cuantitativa (con
  `make mutation`) puede revelar otros candidatos.

## Baseline mutmut inicial

Resultado:

- Mutantes evaluados: 341
- Matados: 313
- Sobrevivientes: 28
- Score aproximado: 91.8 %

Clasificación de sobrevivientes:

- 27 sobrevivientes corresponden a mutaciones de logging (`logger.info`,
  `logger.warning`, `logger.exception` y sus `extra`). Se aceptan como
  mutaciones irrelevantes para comportamiento observable en esta iteración.
- 1 sobreviviente elimina `ciudad='Miami'` en
  `crear_propiedad_desde_formulario`. Se clasifica como mutante equivalente
  porque `PropiedadIn` mantiene el mismo default observable. Se conserva el
  código explícito por trazabilidad con spec 007.
- El problema de mutmut + Pydantic v2 + Decimal fue mitigado en tests de formulario usando inputs tipo string y assertions estables.
- El baseline cuantitativo inicial ya existe para el scope unitario actual: 341 mutantes evaluados, 313 matados, 28 sobrevivientes, score aproximado 91.8%.
- Los 28 sobrevivientes actuales fueron clasificados como logging operacional o mutante equivalente/de bajo valor funcional.

Decisión:

No se agregan tests adicionales para logs. No se persigue 100% mutation score.
El baseline queda aceptado para el scope unitario actual.
