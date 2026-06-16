---
name: 005-dashboard-datos-reales-tasks
description: >
  Genera tasks.md con tareas secuenciales, accionables y verificables para
  005-dashboard-datos-reales.
spec_kit_command: "/speckit.tasks"
usage: "/speckit.tasks @.opencode/prompts/005-dashboard-datos-reales.tasks.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

Genera `tasks.md` para la feature activa `005-dashboard-datos-reales` usando el
workflow canónico de Spec Kit.

Usa la feature activa resuelta por Spec Kit. No asumas rutas fijas si el comando
ya puede resolverlas.

## Reglas

- Mantén todo en español.
- No implementes código.
- No modifiques `spec.md` ni `plan.md`.
- Respeta la constitución, `AGENTS.md`, `report.md` y las instrucciones activas.
- Respeta la gobernanza visual vigente definida por `002-blindar-tokens-visuales`.
- Si existen hallazgos críticos o advertencias pendientes en `report.md`, pausa
  e infórmalos antes de generar tareas.
- Agrupa las tareas por fases del `plan.md`.
- Cada tarea debe ser accionable y verificable.
- Toda tarea que afecte archivos visuales protegidos debe incluir trazabilidad
  explícita según la spec.
- Toda tarea visual debe indicar si reutiliza tokens existentes o si requiere
  trazabilidad por desviación visual.
- No generes tareas que amplíen el alcance funcional definido en `spec.md`.

## Alcance esperado

Las tareas deben cubrir, cuando aplique:

- Lectura del contexto actual de la home: endpoint `GET /` en `app/main.py`,
  template `dashboard.html`, contrato `dashboard.yaml`.
- Localización precisa de valores hardcodeados a reemplazar.
- Creación del módulo `app/modules/dashboard/` con:
  `__init__.py`, `routes.py`, `schemas.py`, `service.py`, `repository.py`.
- Implementación del repositorio de dashboard con funciones de conteo por
  estado (`contar_disponibles`, `contar_rentadas`, `contar_total`).
- Implementación del servicio de dashboard que orquesta conteos y construye el
  contexto para el template.
- Construcción del contexto de métricas conservando el contrato actual, con
  orden: disponibles (real), rentadas (real), ingresos (no operativo), vencidos
  (no operativo).
- Integración de métricas reales con el contexto del template.
- Estado vacío del dashboard basado en conteo total de propiedades.
- Crear o actualizar `app/modules/dashboard/routes.py` para exponer `GET /`.
- Mover la construcción del contexto de la home fuera de `app/main.py`.
- Dejar `app/main.py` limitado al registro del router del slice dashboard si
  corresponde.
- Actualización de `dashboard.html` para reflejar métricas reales y no
  operativas conservando el contrato de contexto existente.
- Actualización del contrato `dashboard.yaml` si el plan lo requiere.
- Pruebas unitarias del servicio de dashboard (mocked repository).
- Pruebas de integración: seed → métricas → render de home.
- Pruebas de estado vacío.
- Pruebas de métricas no operativas.
- Actualización de tests existentes en `tests/unit/test_dashboard.py`.
- Validaciones finales: ruff, mypy, pytest, pre-commit.

## Fuera de alcance

Las tareas NO deben incluir:

- Creación de módulos de rentas, pagos o contratos.
- Cálculo real de ingresos o vencidos.
- Rediseño visual de la home.
- Cambios en CSS, tokens visuales, iconografía o componentes compartidos.
- Nuevos endpoints HTTP adicionales.
- Nuevas dependencias de paquetes Python.
- Cambios en `base.html`, sidebar, navbar o cualquier componente compartido.
- Servicios genéricos fuera del slice `app/modules/dashboard/`.
- Lógica de dashboard fuera de `app/modules/dashboard/`.

## Formato de numeración

Usa este formato para los identificadores de tareas:

```text
T<fase>.<orden>
```

Ejemplos:

```text
T1.1
T1.2
T2.1
T2.2
```

## Formato de cada tarea

Cada tarea debe incluir:

- Identificador.
- Descripción accionable.
- Archivo o ruta afectada, cuando aplique.
- Criterio de verificación.
- Trazabilidad visual, si aplica.

Ejemplo:

```text
T2.1 Implementar repositorio de dashboard con conteo por estado
Archivo: app/modules/dashboard/repository.py
Verificación: las funciones contar_disponibles y contar_rentadas retornan enteros correctos
Trazabilidad visual: no aplica
```

## Salida esperada

Al finalizar, informa:

- Ruta de `tasks.md`.
- Número total de tareas.
- Fases generadas.
- Si detectaste bloqueos.
- Si hay tareas con trazabilidad visual.
- Siguiente comando recomendado.
