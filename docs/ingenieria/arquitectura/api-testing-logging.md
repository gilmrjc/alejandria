---
id: ARC-040
type: API Specification
rating: 9
rating-phase: document-editing
related:
  - target: ARC-005
    relationship_type: extends
    reason: Separa las estrategias de testing y logging de la especificación de endpoints para mejor organización
  - target: ARC-034
    relationship_type: references
    reason: Referencia las convenciones de API
  - target: ARC-035
    relationship_type: references
    reason: Referencia la especificación de endpoints
  - target: ADR-004
    relationship_type: references
    reason: Referencia la estrategia de jobs efímeros para retry strategy
---

# API Testing and Logging — Alejandria

Este documento define las estrategias de testing y logging para la API REST de Alejandria. Para la especificación de endpoints, ver [api-endpoints-specification.md](api-endpoints-specification.md). Para las convenciones generales, ver [api-conventions.md](api-conventions.md).

---

## Índice

1. [Error Handling](#1-error-handling)
2. [Testing](#2-testing)
3. [Logging](#3-logging)

---

## 1. Error Handling

### Formato de Errores

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": {
    "field": "Additional error details"
  }
}
```

### Códigos de Error Comunes

| Código                | Descripción                          |
|-----------------------|--------------------------------------|
| `validation_error`    | Validación de request falló          |
| `not_found`           | Recurso no encontrado                |
| `unauthorized`        | Autenticación fallida                |
| `forbidden`           | Permisos insuficientes               |
| `conflict`            | Conflicto (ej. duplicado)            |
| `rate_limit_exceeded` | Rate limit excedido (post-MVP)       |
| `internal_error`      | Error interno del servidor           |
| `service_unavailable` | Servicio temporalmente no disponible |

### Ejemplo de Error de Validación

Status: 422 Unprocessable Entity

```json
{
  "error": "validation_error",
  "message": "Validation failed",
  "details": {
    "email": "Invalid email format",
    "password": "Password must be at least 8 characters"
  }
}
```

### Edge Cases y Comportamiento de Error

#### Timeouts Configurados

- PostgreSQL queries: 30 segundos
- LLM providers: 60 segundos
- Redis operations: 5 segundos
- FastAPI endpoints: 120 segundos (default)

#### Fallback Behavior

Si un servicio externo falla (PostgreSQL, Redis, Qdrant, LLM providers), la API retorna 503 Service Unavailable con mensaje de error específico. No hay degradación graceful en MVP.

#### Retry Strategy

- Solo para jobs asíncronos (Celery) según ADR-004: backoff exponencial con jitter, máximo 5 reintentos, timeout 5 minutos
- Endpoints síncronos no tienen retry automático

#### Edge Cases Manejados

- Validaciones de Pydantic: 400 Bad Request para input inválido, 422 Unprocessable Entity para validación fallida
- Recurso no encontrado: 404 Not Found
- Conflicto (duplicados): 409 Conflict
- Autenticación fallida: 401 Unauthorized
- Permisos insuficientes: 403 Forbidden
- Rate limit excedido: 429 Too Many Requests (no implementado en MVP)

#### Circuit Breakers

No implementados en MVP. Post-MVP se evaluará pybreaker o resilience4py si se requiere resiliencia avanzada.

#### Health Check Endpoint

Endpoint /api/v1/health verifica estado de servicios (database, redis, qdrant, celery) y retorna 200 si todos healthy, 503 si alguno falla.

---

## 2. Testing

### Estrategia de Testing

#### Integration Tests

- 15-20% de coverage con DB real (bases de datos separadas en docker-compose: POSTGRES_TEST_DB, REDIS_TEST_URL)
- Mocks hacia otras capas (LLM providers, etc.)
- Testing de jobs asíncronos (Celery) con pytest-asyncio
- Mockear broker Redis para unit tests, usar Redis real (REDIS_TEST_URL) para integration tests
- Testing de MCP servers con FastMCP Client y pytest-asyncio

#### Cobertura de Testing Crítica

Los siguientes endpoints requieren 100% de coverage (happy path + edge cases):

- **Autenticación**: POST /api/v1/auth/login
- **Documents CRUD**:
  - POST /api/v1/documents (crear)
  - GET /api/v1/documents/{id} (leer)
  - GET /api/v1/documents (listar con paginación/filtros)
  - PUT /api/v1/documents/{id} (actualizar)
  - DELETE /api/v1/documents/{id} (eliminar)
- **Snapshots**:
  - GET /api/v1/documents/{id}/snapshots (listar)
  - POST /api/v1/documents/{id}/snapshots/{snapshot_id}/restore (restaurar)
- **Health**: GET /api/v1/health

Endpoints de jobs (admin/debugging) tienen prioridad de coverage baja.

#### Configuración Pytest

- asyncio_mode = "auto" en pyproject.toml

### Manual Testing

#### Swagger UI

Swagger UI disponible en `/docs` es la herramienta recomendada para manual testing. Permite probar todos los endpoints directamente desde el navegador con autenticación JWT, sin requerir configuración adicional. Swagger UI proporciona interfaz interactiva para enviar requests, ver responses, y explorar la API.

No se requieren colecciones de Postman o ejemplos de curl adicionales para MVP. Para testing desde terminal, se puede usar curl con ejemplos derivados de Swagger UI.

### Casos de Prueba de Ejemplo

#### Happy Path Examples

- POST /api/v1/documents con datos válidos → 201 Created
- GET /api/v1/documents/{id} → 200 OK
- POST /api/v1/auth/login con credenciales válidas → 200 OK con token

#### Edge Cases Examples

- POST /api/v1/documents con title vacío → 422 Unprocessable Entity
- GET /api/v1/documents/{id} con UUID inválido → 404 Not Found
- POST /api/v1/auth/login con password incorrecto → 401 Unauthorized

---

## 3. Logging

### Estrategia de Logging Estructurado

#### Enfoque MVP

Logging básico con structlog para JSON structured logging.

#### Campos de Log por Request

- timestamp
- level
- request_id
- user_id
- method
- path
- status_code
- latency_ms

#### Request ID

- Generado en middleware de FastAPI
- Propagado en headers de respuesta (X-Request-ID)
- Propagado a Celery workers via context para correlación de logs asíncronos

#### Correlación de Logs

Request ID permite correlacionar logs entre API síncrona y jobs asíncronos (Celery). No se requiere correlación con Redis o Qdrant en MVP.

#### Librería

structlog para JSON structured logging.

#### Niveles de Log

- INFO para requests exitosos
- ERROR para fallos
- DEBUG no habilitado en producción

#### Observabilidad Mínima

Alineado con technology-stack.md (observabilidad completa es post-MVP).

### Proceso de Debug de Errores

#### Proceso Básico de Debug

1. Buscar request ID en logs de API (structlog JSON logs)
2. Verificar health check endpoint (/api/v1/health) para estado de servicios
3. Revisar logs de Celery si el error es en job asíncrono (request ID propagado)
4. Revisar logs de PostgreSQL/Redis si es error de conexión

#### Logs a Revisar por Tipo de Error

- 400/422: Logs de API con request ID, validar input
- 404: Logs de API, verificar recurso existe en DB
- 500: Logs de API con stack_trace, revisar error en aplicación
- 503: Health check, revisar estado de servicios externos

#### Identificación de Performance

Revisar campo latency_ms en logs de API. Identificar requests >1s como lentos. Sin métricas detalladas en MVP, latencia en logs es la única fuente de datos de performance.

#### SLAs de Performance Esperados

Para MVP con carga baja (<10 req/s), los siguientes SLAs son objetivos de diseño:

- **GET /api/v1/documents/{id}**: p95 < 200ms, p99 < 500ms
- **GET /api/v1/documents** (listar con paginación): p95 < 300ms, p99 < 700ms
- **POST /api/v1/documents** (crear): p95 < 500ms, p99 < 1000ms
- **PUT /api/v1/documents/{id}** (actualizar): p95 < 500ms, p99 < 1000ms
- **POST /api/v1/auth/login**: p95 < 300ms, p99 < 600ms
- **GET /api/v1/health**: p95 < 100ms, p99 < 200ms

Estos SLAs se monitorean vía logs de latency_ms. Post-MVP se implementará métricas detalladas con Prometheus/Grafana.

---

## Referencias

- **[api-conventions.md](api-conventions.md)**: Convenciones de API
- **[api-endpoints-specification.md](api-endpoints-specification.md)**: Especificación de endpoints
- **[ADR-004](../decisiones/adr-004-ephemeral-jobs.md)**: Jobs efímeros y retry strategy
- **[technology-stack.md](technology-stack.md)**: Stack tecnológico y observabilidad
