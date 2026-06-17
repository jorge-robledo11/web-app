---
name: 006-pagina-propiedades-cards-analyze
description: >
  Analiza consistencia de spec.md y plan.md para 006-pagina-propiedades-cards.
spec_kit_command: "/speckit.analyze"
usage: "/speckit.analyze @.opencode/prompts/006-pagina-propiedades-cards.analyze.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

## Prompt para `speckit.analyze`

Analiza consistencia entre `spec.md`, `plan.md`, constitución, `AGENTS.md` y las
instrucciones del proyecto para `006-pagina-propiedades-cards`.

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

## Referencias obligatorias

* `.specify/memory/constitution.md`
* `AGENTS.md`
* `.opencode/instructions/backend.instructions.md`
* `.opencode/instructions/frontend.instructions.md`
* `.opencode/instructions/database.instructions.md`
* `.opencode/instructions/tests.instructions.md`
* `specs/006-pagina-propiedades-cards/spec.md`
* `specs/006-pagina-propiedades-cards/plan.md`

## Reglas

* No modifiques archivos.
* Genera `report.md` con hallazgos, warnings y recomendaciones.
* Si hay hallazgos críticos, el siguiente paso es `fix-report`.
* Si no hay hallazgos, el siguiente paso es `tasks`.
* Mantén todo en español.

## Salida esperada

```
Archivo actualizado: specs/006-pagina-propiedades-cards/report.md
Hallazgos: N críticos, M warnings
Siguiente comando:
  - Si hay hallazgos: /speckit.fix-report @.opencode/prompts/006-pagina-propiedades-cards.fix-report.prompt.md
  - Si 0 hallazgos: /speckit.tasks @.opencode/prompts/006-pagina-propiedades-cards.tasks.prompt.md
```
