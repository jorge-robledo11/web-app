---
name: 001-bootstrap-proyecto-plan
description: Prompt fuente para generar el plan técnico de la spec 001-bootstrap-proyecto.
---

/speckit.plan

Genera el `plan.md` de la spec `001-bootstrap-proyecto`.

Usa la feature actual resuelta por Spec Kit. Si existe `.specify/feature.json`,
respeta su `feature_directory`.

No asumas una ruta fija para la spec; usa la ruta activa que resuelvan los
comandos de Spec Kit.

## Instrucciones

- Lee `.specify/memory/constitution.md`.
- Lee `AGENTS.md`.
- Lee `spec.md` de la feature actual.
- Lee la sección `Clarificaciones` de `spec.md`, si existe.
- Respeta las instrucciones aplicables en `.opencode/instructions/`.
- No implementes código.
- No modifiques `tasks.md`.
- Mantén todo el contenido en español.
- No uses Supabase.
- No uses `.yml`; usa siempre `.yaml`.
- Si hay conflicto, prevalece la constitución.

## Modo interactivo

Haz preguntas solo si falta una decisión necesaria para crear el plan.

Si preguntas, sigue el modo interactivo definido en la constitución:

- una sola pregunta a la vez;
- opciones concretas;
- una opción marcada como `← Recomendado`;
- resumen final de decisiones.

No preguntes por decisiones ya resueltas en la spec o en las clarificaciones.

## Salida esperada

Actualiza `plan.md` en la carpeta de la feature actual resuelta por Spec Kit.

El plan debe quedar listo para continuar con:

```text
/speckit.analyze
```

Al terminar, indica:

- ruta del `plan.md`;
- si hubo preguntas;
- si hubo desviaciones en `Complexity Tracking`;
- siguiente comando sugerido.