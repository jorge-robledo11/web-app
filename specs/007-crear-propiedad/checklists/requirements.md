# Requirements Quality Checklist — Spec 007-crear-propiedad

**Feature**: 007-crear-propiedad
**Spec**: [spec.md](./spec.md)
**Created**: 2026-06-20

## Cobertura funcional

- [x] Cada User Story (P1, P2, P3, P4) tiene criterios de aceptación
  verificables.
- [x] Cada requisito funcional (FR-001 a FR-020) está trazado a al menos
  una User Story o criterio de éxito.
- [x] Cada Success Criteria (SC-001 a SC-011) es medible y verificable
  mediante test.
- [x] Los edge cases obligatorios del prompt están listados en la sección
  "Casos límite" y cubiertos por FR-XXX.

## Arquitectura y vertical slice

- [x] La feature extiende el vertical slice de propiedades existente
  (`app/modules/propiedades/`).
- [x] No se crean módulos nuevos (rentas, pagos, inquilinos, contratos).
- [x] `routes.py`, `service.py`, `repository.py`, `templates/` siguen la
  separación vigente.
- [x] Se reutiliza `service.crear_propiedad()` y `repository.crear()`
  existentes.

## Gobernanza visual

- [x] La sección VTG-XXX declara todos los puntos de contacto visual
  (CSS, navbar, iconografía, layout).
- [x] Marcador `[visual][extension]` para extensiones permitidas
  (VTG-002, VTG-004).
- [x] VTG-001 garantiza que NO se modifican tokens canónicos.
- [x] VTG-007 exige marcador `[visual]` en `tasks.md` si se modifica
  algún token canónico.

## Calidad y testing

- [x] Tests unitarios del servicio con mocks (FR-017, NFR-QA-002).
- [x] Tests de integración con Testcontainers y seed real (NFR-QA-003).
- [x] ruff, mypy strict, pre-commit aplicables (NFR-QA-001).

## Async-first

- [x] Todas las funciones con I/O son `async def` (NFR-ASYNC-001).
- [x] Formato y mapeo pueden ser `def` síncrono (NFR-ASYNC-002).

## Dependencias externas

- [x] `https://picsum.photos` es la única dependencia externa nueva
  (servicio público sin paquete).
- [x] Política de fallback definida para falla de picsum (FR-009).
- [x] No se introducen paquetes Python nuevos (NFR-ARCH-005).

## Pendientes para clarificación

- [x] Campo `area` → opcional con default 0 en `service.py`.
- [x] Campo `ciudad` → omitido del formulario.
- [x] Mecanismo de envío → POST tradicional con redirect 303 a `/propiedades`.
- [x] Fallback de picsum → string vacío en `imagen`.
- [x] Icono del botón → texto + `plus` de Lucide (vendorear
  `app/static/icons/plus.svg`) con `[visual][extension]`.
- [x] Rango habitaciones/banos → `habitaciones <= 20`, `banos <= 10`.
- [x] Manejo de duplicados → capturar `IntegrityError` en `service.py`.
- [x] Redirección post-creación → `/propiedades` (listado).

## Criterios de aceptación para considerar la spec cerrada

- [ ] Todas las preguntas de clarificación resueltas.
- [ ] Trazabilidad completa entre User Stories, FR-XXX, SC-XXX y tests.
- [ ] `plan.md` y `tasks.md` generados sin hallazgos críticos en
  `report.md` del analyze.
