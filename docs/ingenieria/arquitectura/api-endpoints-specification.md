---
id: ARC-035
type: API Specification
rating: 9
rating-phase: document-editing
related:
  - target: ARC-005
    relationship_type: extends
    reason: Separa la especificación de endpoints de las convenciones para mejor organización
  - target: ARC-034
    relationship_type: references
    reason: Referencia las convenciones de API (autenticación, validación, paginación)
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para definir endpoints y modelos de datos
  - target: ADR-006
    relationship_type: implements
    reason: Implementa el versioning de documentos con snapshots en endpoints de documentos
---

# API Endpoints Specification — Alejandria

Este documento define la especificación de endpoints de la API REST de Alejandria. Para las convenciones generales (autenticación, validación, paginación), ver [api-conventions.md](api-conventions.md).

---

## Índice

1. [Documents](#1-documents)
2. [Jobs](#2-jobs)
3. [Users](#3-users)
4. [Health](#4-health)

---

## 1. Documents

### Crear Documento

```http
POST /api/v1/documents
```

Request:

```json
{
  "title": "Technical Brief",
  "content": "# Technical Brief\n\n...",
  "file_path": "/docs/technical-brief.md"
}
```

Response (201):

```json
{
  "id": "uuid",
  "title": "Technical Brief",
  "content": "# Technical Brief\n\n...",
  "file_path": "/docs/technical-brief.md",
  "healthy": false,
  "created_at": "2026-05-22T12:00:00Z",
  "updated_at": "2026-05-22T12:00:00Z",
  "created_by": "user_uuid",
  "updated_by": null
}
```

**Side Effects**: Encola job `gap_detection` automáticamente.

### Leer Documento

```http
GET /api/v1/documents/{id}
```

Response (200):

```json
{
  "id": "uuid",
  "title": "Technical Brief",
  "content": "# Technical Brief\n\n...",
  "file_path": "/docs/technical-brief.md",
  "healthy": false,
  "created_at": "2026-05-22T12:00:00Z",
  "updated_at": "2026-05-22T12:00:00Z",
  "created_by": "user_uuid",
  "updated_by": "job_uuid"
}
```

### Listar Documentos

```http
GET /api/v1/documents
```

Query Parameters:

- `page`: Número de página (default: 1)
- `per_page`: Items por página (default: 25, max: 100)
- `healthy`: Filtrar por estado healthy (true/false)
- `updated_after`: Filtrar por fecha de actualización (ISO 8601)
- `sort_by`: Campo para ordenar (default: updated_at)
- `order`: Dirección de orden (asc/desc, default: desc)

Response (200):

```json
{
  "items": [
    {
      "id": "uuid",
      "title": "Technical Brief",
      "file_path": "/docs/technical-brief.md",
      "healthy": false,
      "created_at": "2026-05-22T12:00:00Z",
      "updated_at": "2026-05-22T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total": 100,
    "total_pages": 4
  }
}
```

### Actualizar Documento

```http
PUT /api/v1/documents/{id}
```

Request:

```json
{
  "title": "Technical Brief (Updated)",
  "content": "# Technical Brief\n\nUpdated content...",
  "file_path": "/docs/technical-brief.md"
}
```

Response (200):

```json
{
  "id": "uuid",
  "title": "Technical Brief (Updated)",
  "content": "# Technical Brief\n\nUpdated content...",
  "file_path": "/docs/technical-brief.md",
  "healthy": false,
  "created_at": "2026-05-22T12:00:00Z",
  "updated_at": "2026-05-22T14:00:00Z",
  "created_by": "user_uuid",
  "updated_by": "user_uuid"
}
```

**Side Effects**:

- Crea snapshot automático en `document_snapshots`
- Reencola job `gap_detection` si el documento fue editado manualmente

**Control de Concurrencia**:

- Pessimistic locking usando SELECT FOR UPDATE antes de editar
- Adquisición de lock al inicio de la transacción, liberación automática al commit
- Re-intento con backoff exponencial si el lock falla
- Esta estrategia evita conflictos completamente al bloquear el documento durante la edición

### Eliminar Documento

```http
DELETE /api/v1/documents/{id}
```

Response (204)

**Side Effects**:

- CASCADE DELETE de gaps, document_snapshots
- Cancela jobs activos relacionados

### Obtener Snapshots de Documento

```http
GET /api/v1/documents/{id}/snapshots
```

Response (200):

```json
{
  "items": [
    {
      "id": "uuid",
      "document_id": "document_uuid",
      "content": "# Old content...",
      "created_at": "2026-05-22T12:00:00Z",
      "created_by": "job_uuid"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total": 10,
    "total_pages": 1
  }
}
```

### Restaurar Snapshot

```http
POST /api/v1/documents/{id}/snapshots/{snapshot_id}/restore
```

Response (200):

```json
{
  "id": "uuid",
  "title": "Technical Brief",
  "content": "# Old content...",
  "file_path": "/docs/technical-brief.md",
  "healthy": false,
  "created_at": "2026-05-22T12:00:00Z",
  "updated_at": "2026-05-22T15:00:00Z",
  "created_by": "user_uuid",
  "updated_by": "user_uuid"
}
```

**Side Effects**: Crea snapshot del estado actual antes de restaurar.

---

## 2. Jobs

**Nota**: Endpoints de jobs son para administración y debugging, no para usuarios finales del MVP.

### Listar Jobs

```http
GET /api/v1/jobs
```

Query Parameters:

- `entity_type`: Filtrar por tipo de entidad (document, question)
- `entity_id`: Filtrar por ID de entidad
- `status`: Filtrar por estado (completed/failed)
- `job_type`: Filtrar por tipo (gap_detection, suggestion_application, vector_sync, question_generation)

Response (200):

```json
{
  "items": [
    {
      "id": "uuid",
      "job_type": "gap_detection",
      "entity_type": "document",
      "entity_id": "uuid",
      "status": "completed",
      "completed_at": "2026-05-22T12:05:00Z",
      "error_message": null,
      "created_at": "2026-05-22T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total": 100,
    "total_pages": 4
  }
}
```

### Reintentar Job Fallido

```http
POST /api/v1/jobs/{id}/retry
```

Response (200):

```json
{
  "id": "uuid",
  "job_type": "gap_detection",
  "entity_type": "document",
  "entity_id": "uuid",
  "status": "pending",
  "completed_at": null,
  "error_message": null,
  "created_at": "2026-05-22T12:00:00Z"
}
```

**Side Effects**: Reencola el job en Celery.

---

## 3. Users

**Nota**: Para MVP bootstrapped, solo se implementa login. Gestión de usuarios (crear, listar) se hace via scripts de inicialización o directamente en DB.

### Login

El endpoint de login se define en [api-conventions.md](api-conventions.md). Ver sección [Autenticación y Autorización](#3-autenticación-y-autorización) para detalles del endpoint POST /api/v1/auth/login.

---

## 4. Health

### Health Check

```http
GET /api/v1/health
```

Response (200):

```json
{
  "status": "healthy",
  "timestamp": "2026-05-22T16:00:00Z",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "qdrant": "healthy",
    "celery": "healthy"
  }
}
```

---

## Referencias

- **[api-conventions.md](api-conventions.md)**: Convenciones de API (autenticación, validación, paginación)
- **[api-testing-logging.md](api-testing-logging.md)**: Estrategias de testing y logging
- **[database-schema-design.md](database-schema-design.md)**: Diseño conceptual de esquema de base de datos
- **[ADR-006](../decisiones/adr-006-document-versioning.md)**: Versioning de documentos
