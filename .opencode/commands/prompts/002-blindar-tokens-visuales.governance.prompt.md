---
name: 002-blindar-tokens-visuales-governance
description: >
  Actualiza la gobernanza del proyecto para blindar los tokens visuales
  canónicos antes de crear la spec 002-blindar-tokens-visuales.
---

/speckit.constitution

Actualiza los archivos de gobernanza necesarios para soportar la futura spec
`002-blindar-tokens-visuales`.

## Objetivo

Establecer Que Los Tokens Visuales Canónicos Del Frontend No Pueden Modificarse
Sin Autorización Explícita, Justificación Y Trazabilidad En `tasks.md`.

## Archivos A Revisar

- `.opencode/instructions/frontend.instructions.md`
- `.specify/memory/constitution.md`
- `AGENTS.md`
- `.specify/templates/spec-template.md`, si existe.

## Cambios Esperados

1. En `.opencode/instructions/frontend.instructions.md`, declarar que este
   archivo es la fuente operativa para:
   - Tokens De Color.
   - Espaciado.
   - Radios.
   - Sombras.
   - Tipografía.
   - Breakpoints.
   - Layout Base.
   - Componentes Visuales Compartidos.

2. En `.specify/memory/constitution.md`, agregar una regla global que indique que
   cualquier cambio en tokens visuales canónicos requiere:
   - Autorización Explícita.
   - Justificación.
   - Trazabilidad En `tasks.md`.
   - Registro En `Complexity Tracking` Si Implica Desviación Visual Global.

3. En `AGENTS.md`, reflejar la misma regla como instrucción operativa para
   agentes.

4. Si existe `.specify/templates/spec-template.md`, agregar una sección breve para
   que futuras specs declaren si tocan o no tokens visuales canónicos.

## Reglas

- No implementes código de aplicación.
- No crees la spec todavía.
- No generes `plan.md` ni `tasks.md`.
- Mantén todo en español.
- No dupliques reglas extensas si basta con referenciar la fuente operativa.
- No cambies el stack ni la arquitectura.
- No modifiques rutas de specs.
- Si una modificación a la constitución requiere subir versión, actualiza el
  historial de versiones de la constitución.

## Salida Esperada

Al finalizar, informa:

- Archivos Modificados.
- Regla Agregada A La Constitución.
- Si Se Actualizó El Template De Specs.
- Nueva Versión De La Constitución, Si Cambió.
- Siguiente Comando Recomendado.