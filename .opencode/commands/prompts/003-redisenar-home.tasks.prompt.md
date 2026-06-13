---
name: 003-redisenar-home-tasks
description: >
  Genera tasks.md con tareas secuenciales, accionables y verificables para
  003-redisenar-home.
---

/speckit.tasks

Genera `tasks.md` para la feature activa `003-redisenar-home` usando el
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

- Preparación de templates Jinja afectados.
- Reutilización o creación de componentes/partials.
- Ajustes en `app.css`.
- Validación de tokens visuales canónicos.
- Estados visuales: carga, vacío, error, éxito o navegación.
- Comportamiento responsive.
- Pruebas automatizadas.
- Verificación manual o quickstart.
- Revisión de gobernanza visual.
- Validación final antes de implementación.

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
T2.1 Actualizar estructura del hero en el template de la Home
Archivo: app/modules/home/templates/index.html
Verificación: el hero renderiza título, subtítulo y CTA definidos por la spec
Trazabilidad visual: reutiliza tokens existentes definidos en frontend.instructions.md
```

## Salida esperada

Al finalizar, informa:

- Ruta de `tasks.md`.
- Número total de tareas.
- Fases generadas.
- Si detectaste bloqueos.
- Si hay tareas con trazabilidad visual.
- Siguiente comando recomendado.
