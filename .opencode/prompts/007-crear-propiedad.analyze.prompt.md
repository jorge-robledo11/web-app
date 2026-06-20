---
name: 007-crear-propiedad-analyze
description: >
  Analiza consistencia de spec.md y plan.md para 007-crear-propiedad.
spec_kit_command: "/speckit.analyze"
usage: "/speckit.analyze @.opencode/prompts/007-crear-propiedad.analyze.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

## Prompt para `speckit.analyze`

Analiza consistencia entre `spec.md`, `plan.md`, constitución, `AGENTS.md` y las
instrucciones del proyecto para `007-crear-propiedad`.

## Áreas a validar

1. **Cobertura funcional**: ¿cada requisito funcional de la spec tiene una
   fase o tarea correspondiente en el plan?
2. **Consistencia arquitectónica**: ¿el plan respeta vertical slice? ¿No crea
   módulos innecesarios?
3. **Gobernanza visual**: ¿las tareas que tocan componentes compartidos o CSS
   tienen marcador `[visual]` o `[visual][extension]`?
4. **Constitución**: ¿hay violaciones de stack, prohibiciones o estructura
   obligatoria?
5. **Dependencias**: ¿las dependencias entre fases son correctas?
6. **Cobertura de tests**: ¿el plan incluye tests unitarios y de integración?
7. **Edge cases**: ¿el plan cubre los edge cases listados en la spec?
   (precio_mensual inválido, habitaciones/banos fuera de rango, falla de
   picsum, campos con solo espacios, duplicados).
8. **Validaciones**: ¿las validaciones del formulario están correctamente
   mapeadas a Pydantic o a lógica de servicio?
9. **Fallback de imagen**: ¿la política de fallback está claramente definida
   y testeable?
10. **DTO de formulario**: ¿se necesita un DTO específico para el formulario
    o se reutiliza `PropiedadIn`?

## Referencias obligatorias

* `.specify/memory/constitution.md`
* `AGENTS.md`
* `.opencode/instructions/backend.instructions.md`
* `.opencode/instructions/frontend.instructions.md`
* `.opencode/instructions/database.instructions.md`
* `.opencode/instructions/tests.instructions.md`
* `specs/007-crear-propiedad/spec.md`
* `specs/007-crear-propiedad/plan.md`

## Reglas

* No modifiques archivos.
* Genera `report.md` con hallazgos, warnings y recomendaciones.
* Si hay hallazgos críticos, el siguiente paso es `fix-report`.
* Si no hay hallazgos, el siguiente paso es `tasks`.
* Mantén todo en español.

## Salida esperada

```
Archivo actualizado: specs/007-crear-propiedad/report.md
Hallazgos: N críticos, M warnings
Siguiente comando:
  - Si hay hallazgos: /speckit.fix-report @.opencode/prompts/007-crear-propiedad.fix-report.prompt.md
  - Si 0 hallazgos: /speckit.tasks @.opencode/prompts/007-crear-propiedad.tasks.prompt.md
```
