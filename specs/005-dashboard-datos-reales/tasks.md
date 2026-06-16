# Tasks: Dashboard con datos reales

**Feature**: `005-dashboard-datos-reales`
**Basado en**: [plan.md](./plan.md) — Fases 0 a 6
**Reporte de análisis**: [report.md](./report.md) — 0 hallazgos

---

## Fase 0 — Preparación y lectura de contexto

### T0.1 Leer el endpoint `GET /` en `app/main.py`
Archivo: `app/main.py`
Verificación: identificados todos los valores hardcodeados (3 métricas, 4 accesos, 3 items de actividad) y la construcción del contexto en `dashboard()`
Trazabilidad visual: no aplica

### T0.2 Confirmar que `_tarjeta_metrica.html` soporta `tendencia` opcional
Archivo: `app/templates/components/_tarjeta_metrica.html`
Verificación: el template usa `{% if tendencia %}` y omite el bloque de tendencia cuando no se pasa el campo
Trazabilidad visual: no aplica

---

## Fase 1 — Extender repositorio de propiedades

### T1.1 Agregar `contar_por_estado(session, estado: EstadoPropiedad) -> int`
Archivo: `app/modules/propiedades/repository.py`
Verificación: la función ejecuta `select(func.count()).select_from(Propiedad).where(Propiedad.estado == estado)`, retorna `int` vía `.scalar_one()`, es `async def`
Trazabilidad visual: no aplica

### T1.2 Agregar `contar_total(session) -> int`
Archivo: `app/modules/propiedades/repository.py`
Verificación: la función ejecuta `select(func.count()).select_from(Propiedad)`, retorna `int` vía `.scalar_one()`, es `async def`
Trazabilidad visual: no aplica

---

## Fase 2 — Crear módulo dashboard

### T2.1 Crear `app/modules/dashboard/__init__.py`
Archivo: `app/modules/dashboard/__init__.py`
Verificación: el archivo existe con docstring del módulo en español
Trazabilidad visual: no aplica

### T2.2 Crear `app/modules/dashboard/repository.py`
Archivo: `app/modules/dashboard/repository.py`
Verificación: expone `obtener_metricas(session: AsyncSession) -> dict` que invoca `contar_por_estado(DISPONIBLE)`, `contar_por_estado(RENTADA)` y `contar_total()` del repo de `propiedades`. Retorna `{"disponibles": int, "rentadas": int, "total": int}`. Es `async def`. No importa `Propiedad` directamente.
Trazabilidad visual: no aplica

### T2.3 Crear `app/modules/dashboard/service.py`
Archivo: `app/modules/dashboard/service.py`
Verificación: expone `construir_contexto(session: AsyncSession) -> dict` que invoca al repo de dashboard y construye:
- `metricas`: lista de 4 dicts en orden fijo con `label`, `valor`, `icono`, `estado`, más `marcador` en métricas no operativas. Sin campo `tendencia` en disponibles ni rentadas.
- `accesos`: 4 dicts hardcodeados idénticos al dashboard actual
- `actividad`: 3 dicts hardcodeados de demo
- `actividad_estado`: `"datos"`
- `vacio`: `True` si `total == 0`
Trazabilidad visual: no aplica

### T2.4 Crear `app/modules/dashboard/schemas.py`
Archivo: `app/modules/dashboard/schemas.py`
Verificación: Si se crean DTOs Pydantic, usan `model_config = ConfigDict(frozen=True)`. Si no se justifica tipado estático adicional, puede quedar sin schemas o con un docstring explicando que el contexto es un dict simple compatible con Jinja2.
Trazabilidad visual: no aplica

### T2.5 Crear `app/modules/dashboard/routes.py` con `GET /`
Archivo: `app/modules/dashboard/routes.py`
Verificación: define `router = APIRouter(tags=["dashboard"])`, endpoint `@router.get("/", response_class=HTMLResponse)`, `async def dashboard(request: Request, session: SessionDep)` que invoca `construir_contexto(session)` y renderiza `dashboard.html`. Si `vacio` es `True`, renderiza estado vacío (condicional en template o mensaje directo).
Trazabilidad visual: no aplica

---

## Fase 3 — Migrar `GET /` fuera de `app/main.py`

### T3.1 Eliminar lógica de dashboard de `app/main.py`
Archivo: `app/main.py`
Verificación: la función `dashboard()` y los datos hardcodeados (métricas, accesos, actividad) son eliminados. Se conservan `health()`, `lifespan`, `StaticFiles`, `templates`, `engine`, `SessionDep`.
Trazabilidad visual: no aplica

### T3.2 Registrar router del dashboard en `app/main.py`
Archivo: `app/main.py`
Verificación: `from app.modules.dashboard.routes import router as dashboard_router` + `app.include_router(dashboard_router)`. `GET /` responde 200 y renderiza el dashboard con métricas reales.
Trazabilidad visual: no aplica

---

## Fase 4 — Estado vacío del dashboard

### T4.1 Implementar lógica de estado vacío en el servicio
Archivo: `app/modules/dashboard/service.py`
Verificación: `construir_contexto()` retorna `vacio: True` cuando `contar_total() == 0`. Con datos, retorna `vacio: False`.
Trazabilidad visual: no aplica

### T4.2 Renderizar estado vacío en `dashboard.html`
Archivo: `app/templates/dashboard.html`
Verificación: el template incluye `{% if vacio %}` al inicio del bloque `content` que muestra un mensaje descriptivo centrado. Si `vacio` es `False`, renderiza las 3 secciones normalmente. El mensaje de estado vacío usa icono `info` existente y texto descriptivo, sin modificar CSS ni componentes compartidos.
Trazabilidad visual: reutiliza tokens existentes; no modifica CSS, iconos ni componentes

---

## Fase 5 — Actualizar template para métricas reales

### T5.1 Agregar render del marcador "No disponible" en métricas
Archivo: `app/templates/dashboard.html`
Verificación: el loop `{% for metrica in metricas %}` incluye `{% if metrica.marcador %}` que renderiza el texto del marcador debajo del valor. Las métricas de ingresos y vencidos muestran "No disponible".
Trazabilidad visual: reutiliza tokens existentes; no modifica componentes compartidos

### T5.2 Verificar que el template renderiza métricas dinámicas del contexto
Archivo: `app/templates/dashboard.html`
Verificación: las métricas ya no contienen valores hardcodeados en el template. El bucle itera sobre `metricas` del contexto. Los accesos rápidos y la actividad reciente permanecen idénticos (hardcodeados en el template como demo).
Trazabilidad visual: reutiliza tokens existentes

---

## Fase 6 — Pruebas

### T6.1 Crear `tests/unit/dashboard/` con `__init__.py`
Archivos: `tests/unit/dashboard/__init__.py`, `tests/unit/dashboard/test_service.py`
Verificación: el directorio existe con `__init__.py` vacío y `test_service.py`
Trazabilidad visual: no aplica

### T6.2 Implementar pruebas unitarias del servicio de dashboard
Archivo: `tests/unit/dashboard/test_service.py`
Pruebas:
- `test_construir_contexto_con_datos`: mockea `obtener_metricas` con `{"disponibles": 4, "rentadas": 3, "total": 7}`, verifica que `metricas[0]["valor"] == 4`, `metricas[1]["valor"] == 3`, `vacio == False`
- `test_construir_contexto_sin_propiedades`: mockea `obtener_metricas` con `{"disponibles": 0, "rentadas": 0, "total": 0}`, verifica `vacio == True`
- `test_construir_contexto_solo_disponibles`: mockea con `{"disponibles": 4, "rentadas": 0, "total": 4}`, verifica `metricas[0]["valor"] == 4`, `metricas[1]["valor"] == 0`, `vacio == False`
- `test_construir_contexto_solo_rentadas`: mockea con `{"disponibles": 0, "rentadas": 3, "total": 3}`, verifica `metricas[1]["valor"] == 3`, `vacio == False`
- `test_metricas_no_operativas`: verifica `metricas[2]["label"] == "Ingresos"`, `metricas[2]["valor"] == 0`, `metricas[2]["marcador"] == "No disponible"`, ídem para vencidos
- `test_orden_metricas`: verifica `metricas[0]["label"]`, `metricas[1]["label"]`, `metricas[2]["label"]`, `metricas[3]["label"]` en orden fijo
- `test_metricas_reales_sin_tendencia`: verifica que `"tendencia" not in metricas[0]` y `"tendencia" not in metricas[1]`
Trazabilidad visual: no aplica

### T6.3 Crear `tests/integration/dashboard/` con `__init__.py`
Archivos: `tests/integration/dashboard/__init__.py`, `tests/integration/dashboard/test_dashboard.py`
Verificación: el directorio existe con `__init__.py` vacío y `test_dashboard.py`
Trazabilidad visual: no aplica

### T6.4 Implementar pruebas de integración del dashboard
Archivo: `tests/integration/dashboard/test_dashboard.py`
Requisito: PostgreSQL vía Testcontainers (`postgres:16-alpine`) + seed de propiedades aplicado
Pruebas:
- `test_dashboard_metricas_reales`: ejecuta seed → `GET /` → verifica HTML contiene "Propiedades disponibles", "Propiedades rentadas", `>4<` en el valor de disponibles, `>3<` en el valor de rentadas
- `test_dashboard_estado_vacio`: BD sin propiedades → `GET /` → verifica HTML contiene mensaje de estado vacío
- `test_dashboard_metricas_no_operativas`: verifica HTML contiene `>0<` junto a "Ingresos", `>0<` junto a "Vencidos", y "No disponible" aparece 2 veces
- `test_dashboard_orden_secciones`: verifica que `.metricas` aparece antes que `.accesos-rapidos` y esta antes que `.actividad` en el HTML
- `test_dashboard_accesos_rapidos`: verifica 4 elementos con clase `acceso-rapido` y labels "Propiedades", "Inquilinos", "Contratos", "Pagos"
- `test_dashboard_responde_200`: verifica `GET /` retorna HTTP 200 con `text/html`
Trazabilidad visual: no aplica

### T6.5 Actualizar `tests/unit/test_dashboard.py`
Archivo: `tests/unit/test_dashboard.py`
Verificación: los asserts que esperaban valores hardcodeados (`124`, `87`, `53`, "Propiedades activas", "+8%", "-5%") son reemplazados o eliminados. Los tests de estructura (sidebar, navbar, secciones, accesos rápidos) se conservan. Se agregan tests de estado vacío simulando `vacio: True` en el contexto.
Trazabilidad visual: no aplica

### T6.6 Ejecutar validaciones de calidad
Comandos:
```bash
uv run ruff check app/modules/dashboard/ app/modules/propiedades/repository.py
uv run mypy --strict app/modules/dashboard/
uv run ruff format --check app/modules/dashboard/
```
Verificación: todos los comandos finalizan con código de salida 0 sin hallazgos
Trazabilidad visual: no aplica

### T6.7 Ejecutar suite de pruebas completa
Comandos:
```bash
uv run pytest tests/unit/dashboard/ tests/integration/dashboard/ tests/unit/test_dashboard.py -q
```
Verificación: todos los tests pasan en verde. Cobertura de reglas de negocio del servicio de dashboard.
Trazabilidad visual: no aplica

---

## Resumen

| Fase | Tareas | Descripción |
|------|--------|-------------|
| Fase 0 | T0.1 – T0.2 | Lectura de contexto actual |
| Fase 1 | T1.1 – T1.2 | Extender repo de propiedades |
| Fase 2 | T2.1 – T2.5 | Crear slice vertical dashboard |
| Fase 3 | T3.1 – T3.2 | Migrar `GET /` a dashboard, limpiar `main.py` |
| Fase 4 | T4.1 – T4.2 | Estado vacío del dashboard |
| Fase 5 | T5.1 – T5.2 | Template con métricas reales y marcador |
| Fase 6 | T6.1 – T6.7 | Pruebas unitarias, integración y calidad |

**Total**: 7 fases, 23 tareas
**Trazabilidad visual**: 0 tareas con marcador `[visual]` (los cambios en `dashboard.html` son de contenido dentro del contrato, sin alterar tokens ni componentes)
**Siguiente fase**: `/speckit.implement @.opencode/prompts/005-dashboard-datos-reales.implement.prompt.md`
