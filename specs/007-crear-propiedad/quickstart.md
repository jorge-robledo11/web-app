# Quickstart: Crear propiedad

**Feature**: 007-crear-propiedad
**Phase**: 1 — Design
**Date**: 2026-06-20

## Requisitos previos

- Docker y Docker Compose instalados y ejecutándose (`docker compose up -d`).
- `uv` instalado y dependencias sincronizadas (`uv sync`).
- Migraciones aplicadas (`uv run alembic upgrade head`).
- `config/app.yaml` con `session_secret` configurado (ver §0).
- Seed de propiedades opcional (`uv run python scripts/dev/seed_propiedades.py`).

### 0. Configurar `session_secret`

```bash
# Generar un secret único
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Copiar a config/app.yaml
cat >> config/app.yaml <<EOF
session_secret: <valor-generado-arriba>
EOF
```

Sin este valor, la app fallará al arrancar con `PydanticValidationError`.

## Pasos para validar la feature

### 1. Verificar el botón en el navbar

```bash
uv run fastapi dev app/main.py
```

Abrir `http://localhost:8000/` en el navegador. En la barra superior (navbar),
a la izquierda del indicador "Admin", debe aparecer el botón "Nueva propiedad"
con un icono `+` (plus) azul.

Hacer clic en el botón. Debe navegar a `http://localhost:8000/proiedades/nueva`
(verificar que la URL es correcta).

### 2. Verificar el formulario vacío (GET)

```bash
curl -s http://localhost:8000/proiedades/nueva | head -50
```

Salida esperada (fragmento relevante):

```html
<form method="post" action="/propiedades" class="formulario-crear">
  <div class="form-field">
    <label class="form-field__label" for="titulo">Título</label>
    <input class="form-field__input" id="titulo" name="titulo" type="text" value="" placeholder="" required>
  </div>
  ...
</form>
```

Verificaciones:
- Los 6 campos están presentes: `titulo`, `direccion`, `precio_mensual`,
  `habitaciones`, `banos`, `area`.
- El botón submit dice "Crear propiedad".
- El link "Cancelar" apunta a `/propiedades`.

### 3. Crear propiedad válida (POST con datos correctos)

```bash
curl -s -i -X POST http://localhost:8000/proiedades \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "titulo=Casa Test Quickstart&direccion=123 Test St&precio_mensual=1500&habitaciones=2&banos=1&area=80"
```

Salida esperada:

```text
HTTP/1.1 303 See Other
location: http://localhost:8000/proiedades
set-cookie: flash=<firma_hmac>; HttpOnly; SameSite=lax; Max-Age=60; Path=/
content-length: 0
```

Verificaciones:
- Status code `303 See Other`.
- Header `location` apunta a `/propiedades`.
- Header `set-cookie` contiene la cookie `flash` firmada.

### 4. Verificar el flash post-creación (GET con cookie)

```bash
# Capturar la cookie del paso anterior
COOKIE=$(curl -s -i -X POST http://localhost:8000/proiedades \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "titulo=Casa Test 2&direccion=456 Test Ave&precio_mensual=2000&habitaciones=3&banos=2" \
  | grep -i "set-cookie" | sed 's/.*flash=\([^;]*\).*/\1/')

# Usar la cookie en el siguiente GET
curl -s -i --cookie "flash=$COOKIE" http://localhost:8000/proiedades | head -30
```

Salida esperada:

- Status code `200 OK`.
- HTML contiene `<div class="alerta alerta--success">` con el mensaje de éxito.
- Header `set-cookie: flash=; ...; Max-Age=0` (cookie eliminada para
  one-shot).

### 5. Validar campos obligatorios vacíos (POST inválido)

```bash
curl -s -X POST http://localhost:8000/proiedades \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "titulo=&direccion=&precio_mensual=&habitaciones=&banos=&area="
```

Salida esperada:

- Status code `200 OK`.
- HTML contiene el formulario re-renderizado con mensajes de error inline
  junto a cada campo (`<span class="form-field__error">...`).
- Los valores vacíos se conservan (en este caso todos están vacíos).

### 6. Validar solo espacios en blanco (tratados como vacíos)

```bash
curl -s -X POST http://localhost:8000/proiedades \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "titulo=   &direccion=%20%20%20&precio_mensual=1500&habitaciones=2&banos=1&area=80"
```

Salida esperada:

- Status code `200 OK`.
- Errores inline en `titulo` y `direccion` (tratados como vacíos tras
  `.strip()`).

### 7. Validar precio_mensual inválido

```bash
# No numérico
curl -s -X POST http://localhost:8000/proiedades \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "titulo=X&direccion=Y&precio_mensual=abc&habitaciones=2&banos=1&area=80"

# <= 0
curl -s -X POST http://localhost:8000/proiedades \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "titulo=X&direccion=Y&precio_mensual=-100&habitaciones=2&banos=1&area=80"
```

Salida esperada:

- Status code `200 OK`.
- Error inline en `precio_mensual`.

### 8. Validar habitaciones/banos fuera de rango

```bash
# habitaciones > 20
curl -s -X POST http://localhost:8000/proiedades \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "titulo=X&direccion=Y&precio_mensual=1500&habitaciones=25&banos=1&area=80"

# banos > 10
curl -s -X POST http://localhost:8000/proiedades \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "titulo=X&direccion=Y&precio_mensual=1500&habitaciones=2&banos=11&area=80"
```

Salida esperada:

- Status code `200 OK`.
- Error inline en `habitaciones` o `banos`.

### 9. Validar duplicado (constraint único)

```bash
# Primer POST: crea
curl -s -i -X POST http://localhost:8000/proiedades \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "titulo=Duplicado Test&direccion=999 Dup St&precio_mensual=1500&habitaciones=2&banos=1" \
  | head -5

# Segundo POST con mismos datos: error
curl -s -X POST http://localhost:8000/proiedades \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "titulo=Duplicado Test&direccion=999 Dup St&precio_mensual=1500&habitaciones=2&banos=1" \
  | grep -A2 "alerta--danger"
```

Salida esperada:

- Primer POST: `303 See Other` con `Location: /propiedades`.
- Segundo POST: status `200 OK` con HTML que contiene
  `<div class="alerta alerta--danger">` con mensaje "Ya existe una
  propiedad con ese título y dirección en Miami".

### 10. Validar area opcional con default 0

```bash
# Sin campo area en el form
curl -s -i -X POST http://localhost:8000/proiedades \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "titulo=Sin Area&direccion=789 No Area St&precio_mensual=1000&habitaciones=1&banos=1"
```

Salida esperada:

- Status code `303 See Other` (creación exitosa).
- En la base de datos, la propiedad tiene `area=0`.

### 11. Validar cookie con firma inválida (seguridad)

```bash
# Cookie con firma alterada
curl -s -i --cookie "flash=abc.defghi" http://localhost:8000/proiedades | head -3
```

Salida esperada:

- Status code `200 OK`.
- Sin alerta de flash renderizada (firma inválida → cookie ignorada).
- Sin errores 500 (manejo silencioso).

## Validación con navegador (UX end-to-end)

1. Abrir `http://localhost:8000/proiedades/nueva` en el navegador.
2. Llenar todos los campos con datos válidos. Hacer clic en "Crear propiedad".
3. Verificar redirección a `/propiedades` con alerta verde "Propiedad creada
   exitosamente" (o mensaje equivalente) en la parte superior del listado.
4. Verificar que la nueva propiedad aparece en el grid de cards.
5. Hacer clic en "Nueva propiedad" de nuevo. Completar el form con el
   mismo titulo y direccion. Hacer clic en "Crear propiedad".
6. Verificar que el form se re-renderiza con error global "Ya existe una
   propiedad con ese título y dirección en Miami".
7. Hacer clic en "Cancelar". Verificar que vuelve a `/propiedades` sin
   crear nada.

## Ejecutar pruebas automatizadas

```bash
# Tests unitarios del nuevo DTO y servicio
uv run pytest tests/unit/propiedades/test_schemas_form.py -q
uv run pytest tests/unit/propiedades/test_schemas.py -q
uv run pytest tests/unit/propiedades/test_service_crear_formulario.py -q

# Tests de integración del endpoint
uv run pytest tests/integration/propiedades/test_routes_crear.py -q

# Toda la suite de propiedades
uv run pytest tests/unit/propiedades tests/integration/propiedades -q

# Cobertura mínima 80%
uv run pytest --cov=app/modules/propiedades --cov-fail-under=80
```

## Validaciones de calidad

```bash
# Lint
uv run ruff check .
uv run ruff format --check .

# Typecheck
uv run mypy --strict app/modules/propiedades/

# Trazabilidad visual
make visual-check
```

## Reset completo para entorno limpio

```bash
# Limpiar base de datos
docker compose exec db psql -U realtor_dev -d realtor_dev \
  -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Reaplicar migraciones
uv run alembic upgrade head

# Reaplicar seed
uv run python scripts/dev/seed_propiedades.py

# Reiniciar servidor
pkill -f "fastapi dev" || true
uv run fastapi dev app/main.py
```
