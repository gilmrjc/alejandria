---
id: ARC-023
type: Implementation Specification
rating: 10
rating-phase: document-editing
related:
  - target: ARC-005
    relationship_type: implements
    reason: Implementa la validación de input definida en la especificación de API
  - target: TRD-021
    relationship_type: references
    reason: Referencia el TRD de Hito 2 para requisitos de seguridad de API
  - target: EPC-002
    relationship_type: implements
    reason: Implementa la validación de input para la épica de API y MCP
---

# API Input Validation Strategy — Alejandria

Este documento define la estrategia de validación de input y sanitización para prevenir vulnerabilidades de seguridad.

## Índice

1. [Visión General](#1-visión-general)
2. [Framework de Validación](#2-framework-de-validación)
3. [Validación por Endpoint](#3-validación-por-endpoint)
4. [Sanitización de Input](#4-sanitización-de-input)
5. [Rate Limiting por Endpoint](#5-rate-limiting-por-endpoint)
6. [Error Handling de Validación](#6-error-handling-de-validación)
7. [Testing de Validación](#7-testing-de-validación)

---

## 1. Visión General

### Propósito

Definir la estrategia de validación de input y sanitización para prevenir inyección SQL, XSS, y otras vulnerabilidades de seguridad en la API REST.

### Referencia

Para la especificación de API REST, ver [api-specification.md](api-specification.md).

---

## 2. Framework de Validación

### Pydantic Schemas

Pydantic se usa para validación de request/response:

```python
from pydantic import BaseModel, EmailStr, Field, validator

class DocumentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    file_path: str = Field(..., regex=r"^/docs/.*\.md$")
    
    @validator('title')
    def title_must_not_contain_html(cls, v):
        if '<' in v or '>' in v:
            raise ValueError('Title must not contain HTML')
        return v
```

### Configuración Global

```python
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 3. Validación por Endpoint

### POST /api/v1/documents

**Validaciones**:

- title: 1-200 caracteres, sin HTML
- content: mínimo 1 carácter, sanitizado contra XSS
- file_path: debe comenzar con `/docs/` y terminar en `.md`

### PUT /api/v1/documents/{id}

**Validaciones**:

- title: 1-200 caracteres, sin HTML
- content: mínimo 1 carácter, sanitizado contra XSS
- file_path: debe comenzar con `/docs/` y terminar en `.md`
- expected_version: entero positivo (para concurrencia)

### POST /api/v1/auth/login

**Validaciones**:

- email: formato válido de email
- password: mínimo 8 caracteres, al menos 1 mayúscula, 1 minúscula, 1 número

### Validaciones por Entidad

Las validaciones específicas para cada entidad están definidas en api-specification.md:

- **Documents**: title (1-500), slug (3-100, URL-safe), content (TEXT), filename (1-255), rating (0-10)
- **Folders**: name (1-200), slug (3-100, URL-safe)
- **Projects**: name (1-200), slug (3-100, URL-safe), description (TEXT)
- **Tags**: name (1-100), slug (3-50, URL-safe)
- **Organizations**: name (1-200), slug (3-50, URL-safe)
- **Users**: email (3-255, formato email), username (3-30, alphanumeric + underscores), password (8-128)
- **Gaps**: question (1-2000), answer (0-10000, markdown)
- **Questions**: question (1-2000), answer (0-10000, markdown)
- **Proposals**: name (1-200), description (0-5000, markdown)
- **Query parameters**: page (≥1), per_page (1-100, max: 100), healthy (boolean), updated_after (ISO 8601), status/priority (enums), sort_by (campos permitidos), order (asc/desc)

---

## 4. Sanitización de Input

### SQL Injection Prevention

**Estrategia**: Usar SQLAlchemy ORM con parameterized queries

```python
# CORRECTO (parameterized query)
document = db.query(Document).filter(Document.id == document_id).first()

# INCORRECTO (vulnerable a SQL injection)
document = db.query(Document).filter(f"id = {document_id}").first()
```

### XSS Prevention

**Estrategia**: Sanitizar input de usuario antes de almacenar

```python
from bleach import clean

def sanitize_html(content: str) -> str:
    # Remover tags HTML peligrosos
    return clean(content, tags=[], strip=True)
```

### Estrategia Completa de Sanitización

La estrategia completa de sanitización está definida en api-specification.md:

- **Framework**: Pydantic 2.12.0 para validación automática, SQLAlchemy ORM con parámetros parametrizados para SQL injection prevention
- **Sanitización de Markdown**: Bleach con bleach-allowlist
- **Whitelist conservativa para MVP**:
  - Tags permitidos: p, br, strong, em, u, code, pre, blockquote, ul, ol, li, h1-h6, a
  - Atributos permitidos: a: href con http/https, title; code: class para syntax highlighting
  - Protocolos permitidos: http, https

---

## 5. Rate Limiting por Endpoint

### Límites por Rol

| Rol | Requests por minuto |
|-----|---------------------|
| admin | 1000 |
| user | 100 |
| readonly | 50 |

### Implementación con SlowAPI

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/documents")
@limiter.limit("100/minute")
async def create_document(request: Request, document: DocumentCreate):
    pass
```

### Límites Específicos por Endpoint

Los límites específicos de rate limiting están definidos en api-specification.md:

- **Rate limiting específico por endpoint**: Post-MVP (no implementado en MVP según api-specification.md línea 1162)
- **Headers de rate limit**: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
- **Response al exceder**: 429 Too Many Requests con retry_after
- **Para fase post-MVP**: Considerar límites diferentes por operación (GET vs POST) y endpoint específicos según ARC-006 (mcp-server-specification.md) que marca rate limiting como NO APLICA para MVP local con stdio

---

## 6. Error Handling de Validación

### Formato de Errores

```json
{
  "error": "validation_error",
  "message": "Validation failed",
  "details": {
    "title": "Title must not contain HTML",
    "content": "Content is required",
    "email": "Invalid email format"
  }
}
```

### Implementación

```python
from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "validation_error",
            "message": "Validation failed",
            "details": exc.errors()
        }
    )
```

---

## 7. Testing de Validación

### Unit Tests

- Testing de Pydantic schemas
- Testing de validadores custom
- Testing de sanitización

### Integration Tests

- Testing de validación por endpoint
- Testing de rate limiting
- Testing de error handling

### Escenarios de Test

1. Input inválido → 422 Unprocessable Entity
2. Input con HTML → sanitizado o rechazado
3. Rate limit excedido → 429 Too Many Requests
4. SQL injection attempt → bloqueado por ORM
