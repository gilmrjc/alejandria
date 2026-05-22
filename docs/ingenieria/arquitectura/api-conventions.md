---
id: ARC-034
type: API Specification
rating: 9
rating-phase: document-editing
related:
  - target: ARC-005
    relationship_type: splits
    reason: Separa las convenciones de la especificación de endpoints para mejor organización
  - target: ADR-002
    relationship_type: implements
    reason: Implementa el stack unificado Python usando FastAPI para la API REST
  - target: ARC-022
    relationship_type: references
    reason: Referencia la implementación de JWT para autenticación
---

# API Conventions — Alejandria

Este documento define las convenciones generales de la API REST de Alejandria, incluyendo autenticación, validación, paginación y manejo de errores. Para la especificación de endpoints específicos, ver [api-endpoints-specification.md](api-endpoints-specification.md).

---

## Índice

1. [Visión General](#1-visión-general)
2. [Convenciones HTTP](#2-convenciones-http)
3. [Autenticación y Autorización](#3-autenticación-y-autorización)
4. [Validación y Sanitización](#4-validación-y-sanitización)

---

## 1. Visión General

### Base URL

```text
Desarrollo: http://localhost:8000/api/v1
Producción: https://api.alejandria.com/api/v1
```

### Versioning de API

La API usa versioning en la URL. La versión actual es `v1`.

#### Estrategia para MVP

Para MVP bootstrapped, solo se mantiene versión v1. No se requieren cambios breaking en MVP.

#### Estrategia para Fases Posteriores

Estrategia de deprecar versiones y mantener múltiples versiones simultáneamente se definirá en fases posteriores cuando se introduzcan cambios breaking.

### Formato de Datos

- **Request/Response**: JSON
- **Encoding**: UTF-8
- **Date Format**: ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)

### Clientes Soportados

- MCP Server (como fallback)
- Jobs Celery
- Scripts de administración
- **Nota**: Frontend React se implementará en Hito 3

### Justificación de Arquitectura REST

REST + FastAPI fue elegido por ventajas técnicas específicas sobre GraphQL:

#### Generación Automática de OpenAPI

FastAPI genera automáticamente la especificación OpenAPI (Swagger) de la API sin configuración adicional. La especificación está disponible en:

- **Interactivo**: `/docs` (Swagger UI)
- **JSON**: `/openapi.json`
- **YAML**: `/openapi.yaml` (si se configura)

Esta especificación se puede usar para generar clientes SDK automáticamente en múltiples lenguajes.

#### Ventajas de REST con FastAPI

- Documentación automática con OpenAPI/Swagger (disponible en /docs) sin configuración adicional
- Caching HTTP nativo (ETag, Cache-Control) con proxies y CDNs estándar
- Mejor integración con herramientas estándar (Postman, curl, HTTP clients)
- Type safety con Pydantic para validación automática de requests/responses
- Simplicidad de debugging (requests HTTP estándar, fácil de tracear)

#### Trade-offs Evaluados

- GraphQL: Flexible, evita over-fetching/under-fetching, pero requiere implementación custom de caching, documentación, y herramientas de monitoreo. Añade complejidad con schema, resolvers, y N+1 query problem.
- REST: Over-fetching potencial, pero para MVP con carga baja (<10 req/s) y endpoints optimizados para retornar solo datos necesarios, no es un problema significativo.

#### Consideraciones de Over-fetching/Under-fetching

- Para MVP bootstrapped con CRUD simple y carga baja, over-fetching no es un problema crítico
- Los endpoints de la API están diseñados para retornar solo datos necesarios (ej: listas sin contenido completo de documentos)
- Si el frontend requiere data fetching complejo post-MVP, se puede evaluar GraphQL o GraphQL Federation

#### Decisión Alineada con MVP

Prioridad es simplicidad operacional y madurez del ecosistema sobre flexibilidad extrema. FastAPI + REST proporciona todo lo necesario para MVP sin overhead adicional.

### Principios REST

#### Principios REST Seguidos

- Client-server separation: Cliente y servidor son independientes
- Stateless: No session state en API
- Cacheable: HTTP caching (ETag, Cache-Control)
- Uniform interface: Recursos con URIs, métodos HTTP estándar, códigos de status HTTP
- Layered system: API puede tener proxies, gateways

#### Métodos HTTP Específicos

- GET para leer (idempotente, cacheable)
- POST para crear (no idempotente)
- PUT para reemplazar completo (idempotente)
- DELETE para eliminar (idempotente)

Estos métodos siguen la semántica estándar de HTTP para interoperabilidad.

#### Recursos como URIs

Cada entidad (documents, jobs) es un recurso con URI única (/api/v1/documents/{id}).

---

## 2. Convenciones HTTP

### HTTP Methods

| Method | Uso                           | Idempotente |
|--------|-------------------------------|-------------|
| GET    | Leer recursos                 | Sí          |
| POST   | Crear recursos                | No          |
| PUT    | Reemplazar recursos completos | Sí          |
| PATCH  | Actualización parcial         | No          |
| DELETE | Eliminar recursos             | Sí          |

### Status Codes

| Code | Significado           | Uso                                        |
|------|-----------------------|--------------------------------------------|
| 200  | OK                    | Request exitoso                            |
| 201  | Created               | Recurso creado exitosamente                |
| 204  | No Content            | Request exitoso sin contenido de respuesta |
| 400  | Bad Request           | Request inválido                           |
| 401  | Unauthorized          | Autenticación requerida o fallida          |
| 403  | Forbidden             | Usuario no tiene permisos                  |
| 404  | Not Found             | Recurso no encontrado                      |
| 409  | Conflict              | Conflicto (ej. duplicado)                  |
| 422  | Unprocessable Entity  | Validación falló                           |
| 429  | Too Many Requests     | Rate limit excedido (post-MVP)             |
| 500  | Internal Server Error | Error del servidor                         |
| 503  | Service Unavailable   | Servicio temporalmente no disponible       |

#### Guía de Elección de Códigos de Status

- **400 Bad Request**: Sintaxis de request inválida (ej: JSON malformado, parámetro faltante obligatorio)
- **422 Unprocessable Entity**: Sintaxis válida pero semántica inválida (ej: email con formato inválido, violación de constraint de negocio). Pydantic validation errors retornan 422
- **409 Conflict**: Conflicto con estado actual del recurso (ej: duplicado, versión obsoleta). Usar cuando el request es válido pero no puede ejecutarse por conflicto

Seguir RFC 7231 para códigos de status HTTP.

### Paginación

Para endpoints que retornan listas, usar paginación:

```http
GET /api/v1/documents?page=1&per_page=25
```

Response:

```json
{
  "items": [...],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total": 100,
    "total_pages": 4
  }
}
```

#### Algoritmo de Paginación

Para MVP con carga baja (<10 req/s), se usa paginación offset/limit con OFFSET/LIMIT de PostgreSQL.

Algoritmo: `SELECT * FROM table ORDER BY updated_at DESC LIMIT per_page OFFSET (page-1)*per_page`

#### Limitaciones

Offset/limit es ineficiente para datasets grandes (offset alto requiere scan de muchas filas), pero para MVP con datasets pequeños es aceptable.

#### Cursor-based Pagination

No se requiere en MVP. Límite máximo de 100 items por página para evitar performance issues.

### Filtering

Filtros vía query parameters:

```http
GET /api/v1/documents?healthy=true&updated_after=2026-05-01
```

### Sorting

Ordenamiento vía query parameters:

```http
GET /api/v1/documents?sort_by=updated_at&order=desc
```

---

## 3. Autenticación y Autorización

### Autenticación

#### JWT Bearer Token

```http
Authorization: Bearer <token>
```

#### Obtención de Token

```http
POST /api/v1/auth/login
```

Request:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### Implementación JWT para MVP

- Autenticación JWT básica sin refresh tokens
- Los tokens tienen expiración de 1 hora (3600 segundos)
- Cuando un token expira, el usuario debe volver a autenticarse
- El sistema de roles (RBAC) no se implementará en MVP

Para detalles de implementación técnica, ver [jwt-authentication-implementation.md](jwt-authentication-implementation.md).

#### Consideraciones de Seguridad Hardening

**HTTPS Obligatorio**:

- Todos los endpoints de autenticación y datos sensibles requieren HTTPS en producción
- HTTP solo permitido en desarrollo (localhost)
- Redirección automática de HTTP a HTTPS en producción

**Storage Seguro de Tokens**:

- **Recomendado**: httpOnly cookies con flag Secure y SameSite=Strict
- **Alternativa aceptable para MVP**: localStorage con validación XSS
- **NO usar**: sessionStorage (se pierde al cerrar navegador)
- Tokens nunca deben exponerse en URLs o logs

**Best Practices de JWT**:

- Usar algoritmos fuertes (HS256 con secretos ≥256 bits o RS256 con claves RSA)
- Validar expiración (exp claim) en cada request
- Validar issuer (iss) y audience (aud) si se configuran
- Rotar secretos regularmente (cada 90 días recomendado)
- No incluir información sensible en el payload del token
- Implementar revocación de tokens si se requiere (post-MVP con blacklist en Redis)

### Autorización

#### Roles

- `admin`: Acceso completo a todos los endpoints
- `user`: Acceso a endpoints de lectura y escritura de documentos propios
- `readonly`: Solo acceso a endpoints de lectura

#### Verificación de Permisos

La API verifica permisos en cada request basándose en el rol del usuario y el recurso solicitado.

---

## 4. Validación y Sanitización

### Framework de Validación

- Pydantic 2.12.0 para validación automática de requests/responses con FastAPI
- SQLAlchemy ORM con parámetros parametrizados para prevención de SQL injection
- Bleach con bleach-allowlist para sanitización de markdown

### Sanitización de Markdown

Whitelist conservativa para MVP:

- Tags permitidos: p, br, strong, em, u, code, pre, blockquote, ul, ol, li, h1-h6, a
- Atributos permitidos: a: href con http/https, title; code: class para syntax highlighting
- Protocolos permitidos: http, https

### Validaciones por Entidad

- Documents: title (1-500), slug (3-100, URL-safe), content (TEXT), filename (1-255), rating (0-10)
- Users: email (3-255, formato email), username (3-30, alphanumeric + underscores), password (8-128)

### Validaciones de Query Parameters

- Paginación: page (≥1, default: 1), per_page (1-100, default: 25, max: 100)
- Filtering: healthy (boolean), updated_after (ISO 8601), status/priority (enums)
- Sorting: sort_by (campos permitidos), order (asc/desc, default: desc)
- Cada parámetro máximo una vez (repetido → 400), parámetro inesperado → 400, formato inválido → 422

### Validación de UUIDs

Validar formato UUID en campos *_id usando Pydantic (UUID type). Idealmente se usan slugs para referencias en la API.

### Cambios Requeridos al Schema

Agregar campo `slug` único a documents (generado desde title en formato URL-safe). Users no requiere slug (username ya es único).

### Formato y Generación de Slug

**Formato URL-safe**:

- Solo caracteres alfanuméricos (a-z, 0-9) y guiones (-)
- Sin espacios, caracteres especiales, o acentos
- Longitud: 3-100 caracteres
- Todo en minúsculas
- Sin guiones consecutivos (--) ni al inicio/fin

**Algoritmo de generación desde title**:

1. Convertir a minúsculas
2. Reemplazar espacios y caracteres no alfanuméricos con guiones
3. Eliminar acentos y caracteres especiales (normalización Unicode NFKD)
4. Remover guiones consecutivos
5. Truncar a máximo 100 caracteres si es necesario
6. Asegurar que no comienza/termina con guión

**Ejemplo**:

- Title: "Technical Brief 2026" → slug: "technical-brief-2026"
- Title: "¿Por qué usar REST?" → slug: "por-que-usar-rest"
- Title: "API Documentation (v1)" → slug: "api-documentation-v1"

---

## Referencias

- **[api-endpoints-specification.md](api-endpoints-specification.md)**: Especificación de endpoints
- **[api-testing-logging.md](api-testing-logging.md)**: Estrategias de testing y logging
- **[jwt-authentication-implementation.md](jwt-authentication-implementation.md)**: Implementación de JWT
- **[ADR-002](../decisiones/adr-002-python-unified-stack.md)**: Stack unificado Python
