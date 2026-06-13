# Quickstart: Rediseñar Home principal

**Feature**: `003-redisenar-home` | **Phase**: 1

## Verificación rápida

### 1. Arrancar el backend

```bash
cd web-app
uv sync
make backend
```

### 2. Verificar la Home

```bash
curl -s http://localhost:8000/ | head -50
```

Debe contener las 3 secciones en orden:
1. `<section class="metricas">` con 3 tarjetas de métrica
2. `<section class="accesos-rapidos">` con 4 tarjetas de acceso
3. `<section class="actividad">` con 3 ítems de actividad

### 3. Verificar estados visuales

Los estados se prueban manualmente cambiando el campo `estado` en los datos
hardcodeados de `app/main.py` y verificando el HTML resultante:

```python
# Para probar estado de carga en métricas:
metrica["estado"] = "carga"

# Para probar estado de error:
metrica["estado"] = "error"

# Para probar estado vacío en actividad:
actividad = []
actividad_estado = "vacio"
```

Clases CSS esperadas en cada estado:
- Carga: `.tarjeta-metrica.is-loading`
- Error: `.tarjeta-metrica.is-error`
- Vacío: `.actividad--empty`
- Datos: clases normales sin modificadores de estado

### 4. Verificar responsive

```bash
# Desktop (> 1024px): 3 cols métricas, 4 cols accesos
# Tablet (768-1023px): 2 cols métricas, 2 cols accesos
# Móvil (< 768px): 1 col métricas, 2 cols accesos
```

Usar DevTools del navegador para cambiar viewport.

### 5. Ejecutar tests

```bash
uv run pytest app/tests/ -v
```

### 6. Verificar gobernanza visual

```bash
make visual-check
```

Debe retornar exit 0 (todos los cambios visuales trazados en tasks.md).

### 7. Verificar calidad

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict app/modules/
```
