# Convenciones del proyecto Realtor

Este archivo consolida todas las convenciones de nomenclatura, formato y
estándares del proyecto. Es una referencia unificada derivada de las fuentes
canónicas: `AGENTS.md`, `.specify/memory/constitution.md`,
`.opencode/instructions/` y los prompts de changelog.

En caso de conflicto, las fuentes originales prevalecen sobre este resumen.

---

## 1. Idioma

- Todo el contenido `.md`, comentarios, docstrings y mensajes de commit DEBEN
  estar en español.
- Nunca mezclar idiomas dentro de un mismo archivo.
- Única excepción: los tipos de Conventional Commits van en inglés
  (`feat`, `fix`, `docs`, etc.).

---

## 2. Commits (Conventional Commits)

### Formato

```
<type>(<optional scope>): <description>
```

### Tipos permitidos

| Tipo | Uso |
|------|-----|
| `feat` | Cambios que agregan, ajustan o eliminan una feature visible para API o UI |
| `fix` | Correcciones de bugs en comportamiento existente |
| `docs` | Cambios exclusivamente documentales, specs, prompts, AGENTS, instrucciones o constitución |
| `test` | Cambios exclusivamente de pruebas |
| `refactor` | Reestructura interna sin cambiar comportamiento visible |
| `perf` | Mejora de rendimiento |
| `style` | Formato o estilo de código sin cambio funcional |
| `build` | Dependencias, build tools o empaquetado |
| `ops` | Docker, infraestructura, CI/CD, despliegue, scripts operacionales |
| `chore` | Tareas auxiliares que no encajan en otra categoría |

### Regla de tipo automático

Si un commit solo cambia `specs/`, `.opencode/`, `AGENTS.md`, `.specify/`,
`docs/` o instrucciones, normalmente debe usar `docs(...)`, no `feat(...)`.

### Reglas de descripción

- Usar imperativo o presente.
- Escribir en español.
- No iniciar con mayúscula.
- No terminar con punto.
- Ser específica y trazable.
- Evitar frases genéricas: `update`, `changes`, `fix`, `wip`, `arreglo`,
  `avance`, `cosas`.

### Reglas de scope

- Usar scope cuando ayude a entender el área afectada.
- Preferir scopes de feature o área real del repo.
- No usar identificadores de issue como scope.
- Para specs, usar el número de spec como scope cuando aplique.

### Scopes sugeridos

```
001, 002, 003, specs, opencode, agents, changelog, frontend, backend,
database, tests, health, home, visual-governance, docker, docs, setup
```

### Breaking changes

```text
feat(api)!: eliminar forma legacy de respuesta health

BREAKING CHANGE: las respuestas de health ya no exponen el valor anterior.
```

---

## 3. Ramas

- Las ramas usan el mismo nombre lógico que la spec, sin prefijo `feat/`.
- Ejemplos: `001-bootstrap-proyecto`, `002-blindar-tokens-visuales`,
  `003-redisenar-home`, `main`.

---

## 4. Schemas Pydantic

- Sufijos: `In`, `Out`, `Update`, `Filter`.
- Todos con `model_config = ConfigDict(frozen=True)`.

---

## 5. Tests

### Nomenclatura

| Elemento | Formato | Ejemplo |
|----------|---------|---------|
| Archivo | `test_<módulo>.py` | `test_routes.py` |
| Clase | `Test<Entidad>` | `TestPropiedad` |
| Función | `test_<acción>_<resultado>` | `test_crear_propiedad_retorna_schema` |

---

## 6. Base de datos

### Nomenclatura

| Elemento | Formato | Ejemplo |
|----------|---------|---------|
| Tablas | plural, snake_case | `propiedades`, `inquilinos` |
| Columnas | snake_case | `fecha_inicio`, `monto_mensual` |
| FKs | `<tabla_singular>_id` | `propietario_id` |
| Índices | `ix_<tabla>_<columna>` | `ix_propiedades_direccion` |
| Constraints | `uq_<tabla>_<columna>` | `uq_propiedades_direccion` |

### Migraciones (Alembic)

- Nombres descriptivos en español.

---

## 7. CSS / Frontend

### Sistema de diseño (tokens canónicos)

```css
:root {
  --color-bg: #ffffff;
  --color-surface: #fafafa;
  --color-text: #1a1a1a;
  --color-text-muted: #6b7280;
  --color-border: #e5e7eb;
  --color-accent: #2563eb;
  --color-accent-hover: #1d4ed8;
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-danger: #ef4444;
  --color-info: #3b82f6;

  --space-1: 4px;   --space-2: 8px;   --space-3: 12px;
  --space-4: 16px;  --space-6: 24px;  --space-8: 32px;
  --space-12: 48px;

  --radius-sm: 6px;  --radius-md: 10px;  --radius-lg: 16px;

  --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
  --shadow-lg: 0 10px 24px rgba(0,0,0,0.10);

  --font-sans: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-size-base: 15px;
  --line-height-base: 1.55;

  --sidebar-width: 260px;
  --navbar-height: 56px;
}
```

### Nomenclatura CSS

- Clases en **kebab-case**: `.card-propiedad`, `.tarjeta-metrica`.
- Modificadores con **doble guion**: `.btn--primary`, `.alerta--danger`.
- Custom properties: `--categoria-nombre`.
- Prohibidos estilos inline excepto estados HTMX.

### Breakpoints

- **1023px** (`max-width`): tablet, sidebar overlay, grid 1 columna.
- **767px** (`max-width`): móvil, métricas 1 columna, accesos 2 columnas.

### Organización de `app.css`

```
1. Reset y base
2. Variables (tokens)
3. Tipografía
4. Layout (sidebar + main)
5. Componentes
6. Utilidades
7. Responsive (media queries)
```

---

## 8. Templates y componentes

### Estructura

```
app/templates/
  base.html                    → layout base: sidebar + main + flash-zone
  components/                  → parciales Jinja2 reutilizables
  macros/                      → macros Jinja2 compartidas
app/modules/<feature>/templates/
  *.html                       → vistas del módulo
  _*.html                      → parciales HTMX
```

### Componentes compartidos

| Componente | Archivo |
|-----------|---------|
| Sidebar | `_sidebar.html` |
| Navbar | `_navbar.html` |
| Card de propiedad | `_card_propiedad.html` |
| Tarjeta de métrica | `_tarjeta_metrica.html` |
| Accesos rápidos | `_accesos_rapidos.html` |
| Badge de estado | `_badge_estado.html` |
| Alerta / flash | `_alerta.html` |
| Campo de formulario | `_form_field.html` |

---

## 9. Iconografía

- SVG outline de Lucide, vendoreados en `app/static/icons/<nombre>.svg`.
- Tamaño base: 20×20 o 24×24, trazo 2px.
- Color: `currentColor` heredado. Nunca hardcodear `fill` o `stroke`.
- Uso: macro `{{ icon("nombre") }}` en `app/templates/macros/icons.html`.
- Prohibidos: webfonts, emojis, Unicode como íconos funcionales.

---

## 10. Gobernanza visual

### Marcadores en `tasks.md`

| Marcador | Cuándo se usa |
|----------|---------------|
| `[visual]` | Modifica tokens CSS, componentes compartidos, layout base, macros o iconos |
| `[visual][extension]` | Agrega nuevos tokens o componentes sin modificar existentes |
| `[visual][bugfix]` | Corrige bugs visuales (contraste, accesibilidad, regresión) |
| `[visual][componente]` | Agrega nuevo componente a `app/templates/components/` |
| `[visual][instrucción]` | Modifica `.opencode/instructions/frontend.instructions.md` |

### Archivos protegidos

- `app/static/css/app.css` (secciones `:root`, variables, tipografía, layout, responsive)
- `app/templates/base.html`
- `app/templates/components/_*.html`
- `app/templates/macros/*.html`
- `app/static/icons/`
- `.opencode/instructions/frontend.instructions.md`
- `app/static/vendor/htmx.min.js`

---

## 11. Changelog

### Categorías

Solo estas seis: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

### Reglas de entrada

- Agrupar cambios por intención, no por commit.
- Cada entrada: frase en español, pretérito perfecto o presente descriptivo.
- Omitir ruido: commits de merge, cambios mecánicos sin impacto.
- Relacionar con specs cuando sea posible: `(spec 003)`.

### Marca de último commit procesado

```html
<!-- changelog:last-processed-commit=<hash> -->
```

---

> **Fuentes**: `AGENTS.md`, `.specify/memory/constitution.md` (v1.2.0),
> `.opencode/instructions/backend.instructions.md`,
> `.opencode/instructions/database.instructions.md`,
> `.opencode/instructions/frontend.instructions.md`,
> `.opencode/instructions/tests.instructions.md`,
> `.opencode/prompts/000-changelog.prompt.md`,
> `specs/002-blindar-tokens-visuales/spec.md`.
