---
name: 007-crear-propiedad-fix-report
description: >
  Corrige hallazgos del analyze de 007-crear-propiedad.
spec_kit_command: "/speckit.fix-report"
usage: "/speckit.fix-report @.opencode/prompts/007-crear-propiedad.fix-report.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

## Prompt para `speckit.fix-report`

Corrige los hallazgos detectados en `specs/007-crear-propiedad/report.md`.

## Procedimiento

1. Leer `report.md` completo.
2. Para cada hallazgo, determinar si afecta `spec.md`, `plan.md` o ambos.
3. Aplicar la corrección mínima necesaria.
4. No introducir cambios no solicitados.
5. No modificar archivos fuera de `specs/007-crear-propiedad/`.

## Reglas

* Solo actuar sobre hallazgos críticos y warnings del report.
* No cambiar el alcance funcional de la spec.
* No modificar la constitución.
* Mantener todo en español.
* Si un hallazgo requiere decisión del usuario, preguntar en modo interactivo.

## Salida esperada

```
Hallazgos corregidos: N
Archivos modificados: specs/007-crear-propiedad/spec.md, plan.md
Siguiente comando: /speckit.analyze @.opencode/prompts/007-crear-propiedad.analyze.prompt.md
```
