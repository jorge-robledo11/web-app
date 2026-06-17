# Tasks: Página de propiedades con cards

**Feature**: 006-pagina-propiedades-cards
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)
**Created**: 2026-06-16

## Fase 0: Contexto

- [x] **T0.1**: Leer `spec.md`, `plan.md` y `report.md` para entender alcance completo, decisiones de clarificación y contrato de contexto.
- [x] **T0.2**: Leer instrucciones vigentes: `backend.instructions.md`, `frontend.instructions.md`, `database.instructions.md`, `tests.instructions.md`.

## Fase 1: Extender componente `_card_propiedad.html` [visual][extension]

- [x] **T1.1** [visual][extension]: Extender `app/templates/components/_card_propiedad.html` con los 8 campos requeridos: imagen, título, dirección, habitaciones, baños, área, precio y estado. Usar badge `_badge_estado.html` para el estado. El componente debe aceptar todos los campos como parámetros opcionales para mantener retrocompatibilidad. Traza a: FR-004, FR-013.
- [x] **T1.2** [visual][extension]: Agregar placeholder visual para imagen faltante: div con fondo `--color-surface` e icono `building-2` centrado. Activar cuando `imagen` está vacía o es `None`. Traza a: FR-009.
- [x] **T1.3**: Agregar ellipsis CSS (`text-overflow: ellipsis; overflow: hidden; white-space: nowrap`) en clases de título y dirección. Traza a: FR-010.

## Fase 2: Crear template y CSS [visual][extension]

- [x] **T2.1** [visual][extension]: Crear `app/modules/propiedades/templates/propiedades.html`. Extender `base.html`. Iterar `propiedades` del contexto con `{% for %}` renderizando `_card_propiedad.html` por cada item. Si `vacio` es `True`, mostrar estado vacío con mensaje "No hay propiedades registradas" e icono `info`. Traza a: FR-003, FR-007, FR-008, FR-015.
- [x] **T2.2** [visual][extension]: Agregar CSS para `.propiedades-grid`: `display: grid; gap: var(--space-6); grid-template-columns: repeat(3, 1fr)`. Media queries: `max-width: 1023px` → 2 columnas, `max-width: 767px` → 1 columna. Usar tokens existentes. Traza a: FR-005.
- [x] **T2.3** [visual][extension]: Agregar CSS para cards extendidas: `.card-propiedad__imagen` (aspect-ratio, object-fit), `.card-propiedad__imagen-placeholder`, `.card-propiedad__datos` (padding, flex), `.card-propiedad__precio` (font-weight, color), `.card-propiedad__area`. Traza a: FR-004.

## Fase 3: Lógica de servicio

- [x] **T3.1**: Agregar función async `listar_propiedades(session: AsyncSession) -> list[dict[str, object]]` en `app/modules/propiedades/service.py`. Invoca `repository.listar(session)`. Traza a: FR-002, FR-014.
- [x] **T3.2**: Formatear cada propiedad: precio como `$X,XXX.00` (usar `locale` o `Decimal.quantize`), área como `X,XXX m²`. Mapear entidad a dict con los 8 campos requeridos. Traza a: FR-011, FR-012.

## Fase 4: Endpoint `GET /propiedades`

- [x] **T4.1**: Reemplazar placeholder en `app/modules/propiedades/routes.py`. Eliminar `# pragma: no cover`. Definir `Jinja2Templates` con `get_paths()` del path manager. Agregar `@router.get('', response_class=HTMLResponse)`. Inyectar `AsyncSession`, llamar `service.listar_propiedades()`, renderizar `propiedades.html` con contexto `{'propiedades': [...], 'request': request, 'vacio': len == 0}`. Traza a: FR-001, FR-014.
- [x] **T4.2**: Verificar que `app/main.py` ya incluye `app.include_router(propiedades_router)`. Si no, agregarlo. Traza a: FR-001.

## Fase 5: Navegación lateral y canónica

- [x] **T5.1**: Cambiar `href="#"` → `href="/propiedades"` en el enlace "Propiedades" de `app/templates/components/_sidebar.html`. Un solo atributo; sin modificar estructura ni estilos. Traza a: FR-006.
- [x] **T5.2** [visual][extension]: Corregir y documentar estado activo dinámico del sidebar y breadcrumb del navbar desde `request.url.path`; separar Inquilinos y Contratos en anchors independientes. Actualizar `.opencode/instructions/frontend.instructions.md` para reflejar los patrones canónicos y eliminar la excepción de estilos inline obsoleta.

## Fase 6: Tests unitarios

- [x] **T6.1**: Crear `tests/unit/propiedades/test_service_listar.py`. Test de `listar_propiedades()` mockeando `repository.listar()` con 2 propiedades de prueba. Verificar que retorna lista de dicts con los 8 campos requeridos. Traza a: SC-009, NFR-QA-002.
- [x] **T6.2**: Test de formato: verificar que el precio se formatea como `$1,500.00` y el área como `1,000 m²`. Verificar que lista vacía del repo retorna `[]`. Traza a: FR-011, FR-012, SC-009.

## Fase 7: Tests de integración

- [x] **T7.1**: Crear `tests/integration/propiedades/test_routes.py`. Test de `GET /propiedades` con datos reales (Testcontainers + seed de 10 propiedades). Verificar 200, HTML con layout base, `.card-propiedad` × 10. Traza a: SC-001, SC-002, SC-010.
- [x] **T7.2**: Test de render HTML: verificar que cada card contiene título, dirección, precio formateado, área formateada, habitaciones, baños, badge de estado e imagen. Verificar grid con clase `.propiedades-grid`. Traza a: SC-003, SC-004.
- [x] **T7.3**: Test de estado vacío: truncar `propiedades`, verificar `GET /propiedades` muestra "No hay propiedades registradas" y 0 cards. Traza a: SC-006.
- [x] **T7.4**: Test de placeholder de imagen: crear propiedad con `imagen=''`, verificar que el HTML contiene `.card-propiedad__imagen-placeholder` o el icono `building-2`. Traza a: SC-007.
- [x] **T7.5**: Test de navegación: verificar que `GET /` contiene `href="/propiedades"` en el sidebar. Traza a: SC-005.

## Fase 8: Calidad

- [x] **T8.1**: Ejecutar `uv run ruff check .` y `uv run ruff format --check .`. Cero hallazgos.
- [x] **T8.2**: Ejecutar `uv run mypy --strict app/modules/propiedades/`. Cero errores.
- [x] **T8.3**: Ejecutar `uv run pytest tests/unit/propiedades tests/integration/propiedades -q`. Todos verdes. `uv run pytest --cov=app/modules/propiedades --cov-fail-under=80`.

---

**Total tareas**: 23 (T0.1–T8.3)
**Marcadores visuales**: 6 tareas con `[visual][extension]` (T1.1, T1.2, T2.1, T2.2, T2.3, T5.2)
**Fases**: 9 (Fase 0 a Fase 8)
