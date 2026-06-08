---
id: ARC-016
type: API Specification
rating: 9.0
rating-phase: document-editing
related:
  - target: EPC-004
    relationship_type: implements
    reason: Implementa la especificación de API para metadata de gaps en Épica 4
  - target: ARC-005
    relationship_type: extends
    reason: Extiende api-specification con endpoints específicos de gaps
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para definir modelos de datos
---

# API Specification - Gaps Metadata

Este documento define la especificación de API endpoints para gestión de metadata de gaps y dashboard de gaps. Para la especificación general de API, ver [api-specification.md](./api-specification.md). Para convenciones de API, ver [api-conventions.md](./api-conventions.md).

---

## 1. Schema de Base de Datos

### 1.1 Tabla: gaps

```sql
CREATE TABLE gaps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    context_missing TEXT NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('implementation', 'clarification', 'consistency', 'prerequisite')),
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    role_affected VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'responded', 'rejected')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_gaps_document_id ON gaps(document_id);
CREATE INDEX idx_gaps_status ON gaps(status);
CREATE INDEX idx_gaps_severity ON gaps(severity);
CREATE INDEX idx_gaps_type ON gaps(type);
```

### 1.2 Tabla: gap_tags

```sql
CREATE TABLE gap_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gap_id UUID NOT NULL REFERENCES gaps(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    value VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_gap_tags_gap_id ON gap_tags(gap_id);
CREATE INDEX idx_gap_tags_name ON gap_tags(name);
```

---

## 2. Endpoints de Metadata de Gaps

### 2.1 GET /api/v1/gaps

Lista todos los gaps con filtros opcionales.

**Query Parameters:**
- `document_id` (UUID, optional): Filtrar por documento
- `status` (string, optional): Filtrar por estado (pending, responded, rejected)
- `severity` (string, optional): Filtrar por severidad (low, medium, high, critical)
- `type` (string, optional): Filtrar por tipo (implementation, clarification, consistency, prerequisite)
- `role_affected` (string, optional): Filtrar por rol afectado
- `page` (integer, optional): Número de página (default: 1)
- `limit` (integer, optional): Items por página (default: 50, max: 100)

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": "uuid",
      "document_id": "uuid",
      "question": "How are JWT tokens generated?",
      "context_missing": "Missing information about token generation algorithm",
      "type": "implementation",
      "severity": "high",
      "role_affected": "developer",
      "status": "pending",
      "created_at": "2026-06-07T12:00:00Z",
      "updated_at": "2026-06-07T12:00:00Z",
      "tags": [
        {
          "id": "uuid",
          "name": "theme",
          "value": "authentication"
        }
      ]
    }
  ],
  "total": 100,
  "page": 1,
  "limit": 50,
  "pages": 2
}
```

### 2.2 GET /api/v1/gaps/{gap_id}

Obtiene detalles de un gap específico.

**Response (200 OK):**
```json
{
  "id": "uuid",
  "document_id": "uuid",
  "question": "How are JWT tokens generated?",
  "context_missing": "Missing information about token generation algorithm",
  "type": "implementation",
  "severity": "high",
  "role_affected": "developer",
  "status": "pending",
  "created_at": "2026-06-07T12:00:00Z",
  "updated_at": "2026-06-07T12:00:00Z",
  "tags": [
    {
      "id": "uuid",
      "name": "theme",
      "value": "authentication"
    },
    {
      "id": "uuid",
      "name": "subtheme",
      "value": "token-generation"
    }
  ]
}
```

### 2.3 POST /api/v1/gaps

Crea un nuevo gap.

**Request Body:**
```json
{
  "document_id": "uuid",
  "question": "How are JWT tokens generated?",
  "context_missing": "Missing information about token generation algorithm",
  "type": "implementation",
  "severity": "high",
  "role_affected": "developer",
  "tags": [
    {
      "name": "theme",
      "value": "authentication"
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "document_id": "uuid",
  "question": "How are JWT tokens generated?",
  "context_missing": "Missing information about token generation algorithm",
  "type": "implementation",
  "severity": "high",
  "role_affected": "developer",
  "status": "pending",
  "created_at": "2026-06-07T12:00:00Z",
  "updated_at": "2026-06-07T12:00:00Z",
  "tags": [
    {
      "id": "uuid",
      "name": "theme",
      "value": "authentication"
    }
  ]
}
```

### 2.4 PATCH /api/v1/gaps/{gap_id}

Actualiza metadata de un gap.

**Request Body:**
```json
{
  "severity": "critical",
  "status": "responded",
  "tags": [
    {
      "name": "theme",
      "value": "authentication"
    },
    {
      "name": "priority",
      "value": "high"
    }
  ]
}
```

**Response (200 OK):**
```json
{
  "id": "uuid",
  "document_id": "uuid",
  "question": "How are JWT tokens generated?",
  "context_missing": "Missing information about token generation algorithm",
  "type": "implementation",
  "severity": "critical",
  "role_affected": "developer",
  "status": "responded",
  "created_at": "2026-06-07T12:00:00Z",
  "updated_at": "2026-06-07T13:00:00Z",
  "tags": [
    {
      "id": "uuid",
      "name": "theme",
      "value": "authentication"
    },
    {
      "id": "uuid",
      "name": "priority",
      "value": "high"
    }
  ]
}
```

### 2.5 DELETE /api/v1/gaps/{gap_id}

Elimina un gap.

**Response (204 No Content):**

---

## 3. Endpoints de Dashboard de Gaps

### 3.1 GET /api/v1/gaps/dashboard

Obtiene métricas agregadas del dashboard de gaps.

**Query Parameters:**
- `theme` (string, optional): Filtrar por tema
- `priority` (string, optional): Filtrar por prioridad
- `status` (string, optional): Filtrar por estado
- `type` (string, optional): Filtrar por tipo

**Response (200 OK):**
```json
{
  "total_gaps": 150,
  "by_status": {
    "pending": 80,
    "responded": 60,
    "rejected": 10
  },
  "by_severity": {
    "low": 30,
    "medium": 50,
    "high": 50,
    "critical": 20
  },
  "by_type": {
    "implementation": 60,
    "clarification": 40,
    "consistency": 30,
    "prerequisite": 20
  },
  "by_theme": [
    {
      "theme": "authentication",
      "count": 25,
      "by_severity": {
        "low": 5,
        "medium": 10,
        "high": 8,
        "critical": 2
      }
    },
    {
      "theme": "database",
      "count": 30,
      "by_severity": {
        "low": 8,
        "medium": 12,
        "high": 7,
        "critical": 3
      }
    }
  ],
  "by_role_affected": {
    "developer": 80,
    "architect": 40,
    "product": 20,
    "stakeholder": 10
  },
  "resolution_rate": 0.53,
  "avg_resolution_time_hours": 24.5
}
```

### 3.2 GET /api/v1/gaps/grouped

Obtiene gaps agrupados por tema con filtros.

**Query Parameters:**
- `group_by` (string, required): Campo de agrupación (theme, type, severity, role_affected)
- `status` (string, optional): Filtrar por estado
- `limit` (integer, optional): Límite de grupos (default: 20)

**Response (200 OK):**
```json
{
  "group_by": "theme",
  "groups": [
    {
      "key": "authentication",
      "count": 25,
      "gaps": [
        {
          "id": "uuid",
          "question": "How are JWT tokens generated?",
          "severity": "high",
          "status": "pending"
        }
      ]
    },
    {
      "key": "database",
      "count": 30,
      "gaps": [
        {
          "id": "uuid",
          "question": "What is the consistency strategy?",
          "severity": "critical",
          "status": "pending"
        }
      ]
    }
  ]
}
```

---

## 4. Schema Pydantic

### 4.1 GapCreate

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class GapType(str, Enum):
    IMPLEMENTATION = "implementation"
    CLARIFICATION = "clarification"
    CONSISTENCY = "consistency"
    PREREQUISITE = "prerequisite"

class GapSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class GapStatus(str, Enum):
    PENDING = "pending"
    RESPONDED = "responded"
    REJECTED = "rejected"

class GapRole(str, Enum):
    DEVELOPER = "developer"
    ARCHITECT = "architect"
    PRODUCT = "product"
    STAKEHOLDER = "stakeholder"
    OTHER = "other"

class TagCreate(BaseModel):
    name: str = Field(..., max_length=100)
    value: Optional[str] = Field(None, max_length=255)

class GapCreate(BaseModel):
    document_id: str
    question: str
    context_missing: str
    type: GapType
    severity: GapSeverity
    role_affected: GapRole
    tags: Optional[List[TagCreate]] = []
```

### 5.2 GapResponse

```python
class TagResponse(BaseModel):
    id: str
    name: str
    value: Optional[str]

class GapResponse(BaseModel):
    id: str
    document_id: str
    question: str
    context_missing: str
    type: GapType
    severity: GapSeverity
    role_affected: GapRole
    status: GapStatus
    created_at: str
    updated_at: str
    tags: List[TagResponse] = []
```

### 5.3 DashboardMetrics

```python
class DashboardMetrics(BaseModel):
    total_gaps: int
    by_status: Dict[str, int]
    by_severity: Dict[str, int]
    by_type: Dict[str, int]
    by_theme: List[Dict[str, Any]]
    by_role_affected: Dict[str, int]
    resolution_rate: float
    avg_resolution_time_hours: Optional[float]
```

---

## 6. Estrategia de Versioning

Según [api-conventions.md](./api-conventions.md), la API usa versioning en la URL. Para cambios breaking en endpoints de gaps:

- Cambiar nombre de endpoint: `GET /api/v1/gaps` → `GET /api/v2/gaps`
- Mantener endpoint v1 por al menos una major version
- Documentar cambios en changelog

---

## 6. Referencias

- [api-specification.md](./api-specification.md): Especificación general de API
- [api-conventions.md](./api-conventions.md): Convenciones de API
- [database-schema-design.md](./database-schema-design.md): Schema de base de datos
- [epica-04-deteccion-agrupacion.md](../tareas/epica-04-deteccion-agrupacion.md): Épica 4 - T-045, T-047

---

*Fin del documento de especificación de API para metadata de gaps.*
