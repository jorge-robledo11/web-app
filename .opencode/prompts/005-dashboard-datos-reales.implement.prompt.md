---
name: 005-dashboard-datos-reales-implement
description: >
  Implementa 005-dashboard-datos-reales siguiendo tasks.md, una fase a la vez y
  con confirmación manual entre fases.
spec_kit_command: "/speckit.implement"
usage: "/speckit.implement @.opencode/prompts/005-dashboard-datos-reales.implement.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

Ejecuta `db-preflight` antes de `speckit.implement` sobre `005-dashboard-datos-reales`. Estamos en ambiente de desarrollo y autorizo reset destructivo solo cuando `db-preflight` detecte un estado que admita `--allow-reset`; en ese caso, intenta resolver por `reset --allow-reset`. Si `db-preflight` no admite reset para el estado detectado, detén el flujo y reporta el bloqueo sin continuar. Si el resultado de `db-preflight` deja `permite_implement=true` (incluyendo corrección automática si aplica), ejecuta inmediatamente el agente `speckit.implement` para implementar `specs/005-dashboard-datos-reales` siguiendo `specs/005-dashboard-datos-reales/tasks.md`.

Implementa la feature activa `005-dashboard-datos-reales` siguiendo `tasks.md`.

Usa la feature activa resuelta por Spec Kit. No asumas rutas fijas si el comando
ya puede resolverlas.

## Reglas

- Respeta `tasks.md`, `plan.md`, `spec.md`, `report.md`, `AGENTS.md` y la
  constitución.
- Respeta las instrucciones activas de `.opencode/instructions/*.instructions.md`.
- Respeta la gobernanza visual vigente definida por `002-blindar-tokens-visuales`.
- Trabaja una fase a la vez.
- Al terminar cada fase, pausa y espera mi confirmación antes de continuar.
- Mantén el intercambio en español.
- No agregues alcance no definido por los artefactos de la feature.
- No cambies tokens visuales canónicos sin trazabilidad explícita en `tasks.md`.
- Si detectas contradicciones, hallazgos críticos pendientes o bloqueos, pausa e
  informa antes de continuar.

## Restricciones específicas de esta feature

Durante la implementación, el agente NO debe:

- Crear módulos de rentas, pagos ni contratos.
- Inventar cálculos de ingresos ni vencidos. Las métricas no operativas deben
  hardcodearse con valor `0` y marcador "No disponible".
- Crear endpoints adicionales (FR-017).
- Modificar CSS, tokens visuales, iconografía ni componentes compartidos
  (VTG-001 a VTG-005).
- Rediseñar la home. Los cambios en `dashboard.html` deben limitarse a reflejar
  métricas reales y el estado vacío conservando el contrato de contexto, sin
  alterar layout, estilos ni estructura visual.
- Introducir nuevas dependencias de paquetes Python.
- Mover la arquitectura fuera de vertical slice.
- Exponer entidades SQLAlchemy como respuesta HTTP.
- Usar el estilo legacy de SQLAlchemy (`Column`, `Query`, sesiones síncronas).
- Dejar lógica de dashboard en `app/main.py`.

El agente DEBE:

- Implementar el dashboard dentro de `app/modules/dashboard/`.
- Definir `GET /` en `app/modules/dashboard/routes.py`.
- Mantener `app/main.py` sin lógica de dashboard; solo registrar router si
  corresponde.
- Mantener `repository.py` limitado a acceso a datos.
- Mantener `service.py` como lugar de cálculo y armado del contexto.
- Mantener `schemas.py` para DTOs o estructuras tipadas cuando aporten
  claridad.

## Verificaciones por fase

Al finalizar cada fase, ejecuta o informa las verificaciones indicadas por
`tasks.md`. Cuando aplique, considera:

- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run mypy app`
- `uv run pytest`
- Verificación manual o quickstart definido por la feature.
- Verificación de que `GET /` renderiza métricas reales.
- Verificación de que `GET /` muestra estado vacío cuando no hay propiedades.
- Verificación de trazabilidad visual cuando se afecten archivos protegidos.

## Cierre de cada fase

Al finalizar cada fase, informa brevemente:

- Fase completada.
- Tareas completadas.
- Archivos modificados.
- Verificaciones ejecutadas.
- Cambios visuales protegidos afectados, si aplica.
- Bloqueos, si existen.
- Siguiente fase pendiente.

## Salida final

Al completar todas las fases, informa:

- Tareas completadas.
- Archivos modificados.
- Verificaciones finales ejecutadas.
- Si hubo desviaciones de gobernanza visual.
- Siguiente comando recomendado.
