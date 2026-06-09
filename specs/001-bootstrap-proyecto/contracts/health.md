# Contrato: Health Check

**Endpoint**: `GET /health` | **Feature**: `001-bootstrap-proyecto`

## Request

```
GET /health HTTP/1.1
Accept: application/json
```

Sin parámetros, sin body, sin autenticación.

## Response — Éxito (200 OK)

**Condición**: PostgreSQL responde a `SELECT 1` en menos de 2 segundos.

```json
{
  "status": "ok",
  "database": "ok"
}
```

| Campo | Tipo | Valor |
|---|---|---|
| `status` | `string` | `"ok"` |
| `database` | `string` | `"ok"` |

## Response — Fallo (503 Service Unavailable)

**Condición**: Timeout (> 2s) o error de conexión al ejecutar `SELECT 1`.

```json
{
  "status": "error",
  "database": "unavailable",
  "detail": "timeout after 2s"
}
```

| Campo | Tipo | Descripción |
|---|---|---|
| `status` | `string` | `"error"` |
| `database` | `string` | `"unavailable"` |
| `detail` | `string` | Descripción legible del fallo |

## Comportamiento

1. Obtiene `AsyncSession` vía `Depends(get_session)`.
2. Envuelve `await session.execute(text("SELECT 1"))` en `asyncio.timeout(2)`.
3. Éxito → `200` con body de éxito.
4. `TimeoutError` o `SQLAlchemyError` → `503` con body de error.
5. En fallo: `logger.warning("health.database_unavailable", extra={"detail": str(exc)})`.
6. En éxito: sin logs propios (solo acceso HTTP de uvicorn).
