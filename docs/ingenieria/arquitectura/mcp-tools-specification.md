---
id: ARC-036
type: MCP Specification
rating: 9.0
rating-phase: document-editing
related:
  - target: ARC-030
    relationship_type: implements
    reason: Implementa la arquitectura definida en mcp-server-architecture.md
  - target: ADR-001
    relationship_type: implements
    reason: Implementa MCP como capa de abstracción para LLMs según ADR-001
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para persistencia de datos MCP
  - target: ARC-002
    relationship_type: references
    reason: Referencia el flujo end-to-end para definir tools de cada fase del pipeline
  - target: ARC-037
    relationship_type: references
    reason: Referencia la estrategia de consistencia y concurrencia
  - target: ARC-038
    relationship_type: references
    reason: Referencia la estrategia de performance y escalabilidad
  - target: ARC-039
    relationship_type: references
    reason: Referencia la estrategia de observabilidad y monitoreo
---

# MCP Tools Specification — Alejandria

Este documento define la especificación detallada de tools del MCP Server de Alejandria. Para la arquitectura general, ver [mcp-server-architecture.md](./mcp-server-architecture.md). Para deployment y testing, ver [mcp-deployment-testing.md](./mcp-deployment-testing.md).

Para detalles de consistencia y concurrencia, ver [mcp-server-data-consistency-concurrency.md](./mcp-server-data-consistency-concurrency.md). Para detalles de performance y escalabilidad, ver [mcp-server-performance-scalability.md](./mcp-server-performance-scalability.md). Para detalles de observabilidad y monitoreo, ver [mcp-server-observability-monitoring.md](./mcp-server-observability-monitoring.md).

---

## 1. Tools

Las tools MCP son funciones invocables por el LLM que ejecutan acciones específicas en el sistema Alejandria. Cada tool tiene un esquema de parámetros, un esquema de respuesta, y efectos secundarios documentados. Los agentes del pipeline usan estas tools para operar sobre documentos, gaps, proposals, questions y tags.

### Validación de Parámetros

**Tipos de datos y restricciones**: Se usa Pydantic para validación, alineado con schema de base de datos:

- `document_id`: UUID string validado
- `include_metadata`: boolean
- `limit`: integer con rango
- `status`: enum string (pending/responded/rejected/etc)
- `priority`: enum string (low/medium/high/critical)

Restricciones de longitud alineadas con schema PostgreSQL:

- `commit_message`: VARCHAR(255)
- `role_affected`: VARCHAR(100)
- `name` (tag): VARCHAR(100)
- `question`/`answer`/`context_missing`/`content`/`description`: TEXT (sin límite)

Pydantic valida automáticamente estos tipos y restricciones.

**Validación con FastMCP**: FastMCP maneja validación automáticamente con Pydantic. Cada tool se define con type hints en los parámetros. FastMCP genera automáticamente el JSON schema para el MCP client. No se requiere validación manual adicional. Los enums definidos en Pydantic (GapStatus, GapPriority, etc.) se validan automáticamente. FastMCP expone el schema automáticamente al cliente MCP.

### Versionamiento y Compatibility

Referencia: mcp-server-architecture.md (líneas 226-253). El MCP Server usa Semantic Versioning (SemVer) con formato MAJOR.MINOR.PATCH. Para backward compatibility: nunca eliminar parámetros requeridos, agregar parámetros opcionales con default values es seguro, cambios breaking requieren nueva tool con nombre diferente (ej: `read_document_v2`), mantener tools deprecadas por al menos una major version antes de eliminarlas.

### read_document

Esta tool permite recuperar el contenido completo de un documento del sistema, incluyendo metadatos opcionales. Es fundamental para que los agentes analicen documentos existentes antes de proponer modificaciones.

**Parámetros**:

```json
{
  "document_id": "uuid",
  "include_metadata": false
}
```

**Respuesta**:

```json
{
  "id": "uuid",
  "title": "Technical Brief",
  "content": "# Technical Brief\n\n...",
  "file_path": "/docs/technical-brief.md",
  "healthy": false,
  "created_at": "2026-05-22T12:00:00Z",
  "updated_at": "2026-05-22T12:00:00Z"
}
```

**Entidades Manipuladas**: Document (lectura)

**Uso**: El Agente 1 (detección de gaps) lee documentos para analizar su contenido e identificar información faltante. El Agente 4 (aplicación de cambios) lee documentos para aplicar modificaciones sugeridas tras verificación.

**Errores Específicos**: DocumentNotFoundError, PermissionDeniedError

---

### write_document

Esta tool permite actualizar el contenido de un documento existente. Es usada por el Agente 4 para aplicar cambios sugeridos tras verificación exitosa.

**Parámetros**:

```json
{
  "document_id": "uuid",
  "content": "# Technical Brief\n\n...",
  "commit_message": "Applied gap resolution changes"
}
```

**Respuesta**:

```json
{
  "id": "uuid",
  "title": "Technical Brief",
  "content": "# Technical Brief\n\n...",
  "file_path": "/docs/technical-brief.md",
  "healthy": true,
  "updated_at": "2026-05-22T12:00:00Z",
  "version": 2
}
```

**Entidades Manipuladas**: Document (actualización), DocumentSnapshot (creación automática según ADR-006)

**Uso**: El Agente 4 (aplicación de cambios) aplica modificaciones sugeridas al documento tras verificación exitosa.

**Errores Específicos**: DocumentNotFoundError, VersionConflictError, PermissionDeniedError

---

### list_gaps

Esta tool lista todos los gaps asociados a un documento, permitiendo filtrar por estado. Es usada por los agentes para obtener el estado actual de gaps pendientes.

**Parámetros**:

```json
{
  "document_id": "uuid",
  "status": "pending"
}
```

**Respuesta**:

```json
{
  "gaps": [
    {
      "id": "uuid",
      "question": "¿Por qué se eligió esta arquitectura?",
      "priority": "high",
      "status": "pending",
      "created_at": "2026-05-22T12:00:00Z"
    }
  ],
  "total": 5
}
```

**Entidades Manipuladas**: Gap (lectura)

**Uso**: El Agente 1 (detección) lista gaps para verificar completitud. El Agente 3 (resolución) lista gaps pendientes para priorizar respuestas.

---

### list_gaps_by_tag

Esta tool lista gaps asociados a un tag específico, permitiendo resolución eficiente por tema.

**Parámetros**:

```json
{
  "tag_id": "uuid",
  "status": "pending"
}
```

**Respuesta**:

```json
{
  "gaps": [
    {
      "id": "uuid",
      "question": "¿Por qué se eligió esta arquitectura?",
      "priority": "high",
      "status": "pending"
    }
  ],
  "total": 5
}
```

**Entidades Manipuladas**: Gap (lectura), Tag (lectura), GapTag (lectura)

**Uso**: El Agente 3 (resolución) lista gaps por tag para resolver temas específicos en sesiones enfocadas.

---

### create_gap

Esta tool crea un registro de gap detectado por el Agente 1 durante la fase de detección. El gap representa información faltante que impide comprensión completa del documento.

**Parámetros**:

```json
{
  "document_id": "uuid",
  "question": "¿Por qué se eligió esta arquitectura?",
  "context_missing": "No se justifica la elección de arquitectura de 5 fases",
  "priority": "high",
  "role_affected": "Senior Developer",
  "answer": "Según el ADR-002, la arquitectura de 5 fases fue elegida para..." 
}
```

**Respuesta**:

```json
{
  "id": "uuid",
  "document_id": "uuid",
  "question": "¿Por qué se eligió esta arquitectura?",
  "context_missing": "No se justifica la elección de arquitectura de 5 fases",
  "priority": "high",
  "role_affected": "Senior Developer",
  "answer": "Según el ADR-002...",
  "status": "pending",
  "created_at": "2026-05-22T12:00:00Z"
}
```

**Entidades Manipuladas**: Gap (creación)

**Uso**: El Agente 1 (detección) crea gaps cuando detecta información faltante en el documento. El campo `answer` es opcional y contiene una sugerencia de respuesta generada por el LLM usando contexto de documentos relacionados (vía `search_similar_documents`). El gap siempre se crea con `status=pending` independientemente de si hay sugerencia.

**Errores Específicos**: DocumentNotFoundError, ValidationError

---

### answer_gap

Esta tool registra una respuesta confirmada por el usuario para un gap específico. Cambia el estado a `responded`.

**Parámetros**:

```json
{
  "gap_slug": "gap-abc123",
  "answer": "ADR-002 justifica cada fase del pipeline..."
}
```

**Respuesta**:

```json
{
  "id": "uuid",
  "question": "¿Por qué se eligió esta arquitectura?",
  "answer": "ADR-002 justifica cada fase...",
  "status": "responded",
  "answered_at": "2026-05-22T14:00:00Z",
  "answered_by": null
}
```

**Side Effects**: Al responder via API REST (PUT /gaps/{id}), se encola `question_generation_task` para vectorizar la respuesta en Qdrant y hacerla disponible para búsqueda semántica y generación de propuestas.

**Entidades Manipuladas**: Gap (actualización: answer, status, answered_at, answered_by)

**Uso**: El usuario (via API REST o skill gap-resolution-mcp) confirma o modifica la sugerencia pre-llenada. El campo `answered_by` queda con el UUID del usuario autenticado cuando se usa la API REST.

**Errores Específicos**: GapNotFoundError, GapAlreadyAnsweredError

---

### create_tag

Esta tool crea un tag para clasificar gaps por tema. Los tags son reutilizables entre gaps de diferentes documentos.

**Parámetros**:

```json
{
  "name": "arquitectura"
}
```

**Respuesta**:

```json
{
  "id": "uuid",
  "name": "arquitectura",
  "created_at": "2026-05-22T12:00:00Z"
}
```

**Entidades Manipuladas**: Tag (creación)

**Uso**: El Agente 2 (agrupación) crea tags para agrupar gaps por temas afines.

---

### assign_tag_to_gap

Esta tool asigna un tag a un gap para clasificación múltiple.

**Parámetros**:

```json
{
  "gap_id": "uuid",
  "tag_id": "uuid"
}
```

**Respuesta**:

```json
{
  "gap_id": "uuid",
  "tag_id": "uuid",
  "assigned_at": "2026-05-22T12:00:00Z"
}
```

**Entidades Manipuladas**: GapTag (creación)

**Uso**: El Agente 2 (agrupación) asigna tags a gaps para facilitar resolución en bloques coherentes.

---

### list_proposals

Esta tool lista propuestas de cambios para un documento, permitiendo filtrar por estado.

**Parámetros**:

```json
{
  "document_id": "uuid",
  "status": "pending"
}
```

**Respuesta**:

```json
{
  "proposals": [
    {
      "id": "uuid",
      "description": "Agregar sección de justificación de arquitectura",
      "status": "pending",
      "created_at": "2026-05-22T12:00:00Z"
    }
  ],
  "total": 3
}
```

**Entidades Manipuladas**: Proposal (lectura)

**Uso**: El Agente 4 (aplicación) lista propuestas pendientes para aplicar cambios al documento.

---

### create_proposal

Esta tool crea una propuesta de cambio basada en respuestas verificadas. Es generada automáticamente tras verificación exitosa.

**Parámetros**:

```json
{
  "document_id": "uuid",
  "description": "Agregar sección de justificación de arquitectura",
  "context_entries": [
    {
      "type": "insert",
      "position": "after",
      "target": "## Arquitectura",
      "content": "### Justificación\n\nLa arquitectura de 5 fases se eligió porque..."
    }
  ]
}
```

**Respuesta**:

```json
{
  "id": "uuid",
  "document_id": "uuid",
  "description": "Agregar sección de justificación de arquitectura",
  "status": "pending",
  "created_at": "2026-05-22T12:00:00Z"
}
```

**Entidades Manipuladas**: Proposal (creación), ContextEntry (creación)

**Uso**: El Agente 1 (verificación) crea propuestas automáticamente cuando las respuestas a gaps son verificadas como completas.

---

### accept_proposal

Esta tool marca una propuesta como aceptada, habilitando su aplicación posterior.

**Parámetros**:

```json
{
  "proposal_id": "uuid"
}
```

**Respuesta**:

```json
{
  "id": "uuid",
  "status": "accepted",
  "accepted_at": "2026-05-22T14:00:00Z"
}
```

**Entidades Manipuladas**: Proposal (actualización)

**Uso**: El usuario acepta propuestas tras revisar los cambios sugeridos.

---

### apply_proposal

Esta tool aplica los cambios de una propuesta aceptada al documento.

**Parámetros**:

```json
{
  "proposal_id": "uuid"
}
```

**Respuesta**:

```json
{
  "id": "uuid",
  "status": "applied",
  "applied_at": "2026-05-22T14:00:00Z",
  "document_version": 3
}
```

**Entidades Manipuladas**: Proposal (actualización), Document (actualización), DocumentSnapshot (creación automática según ADR-006)

**Uso**: El Agente 4 (aplicación) aplica cambios al documento tras aceptación de propuesta.

---

### update_proposal_status

Esta tool actualiza el estado de una propuesta manualmente.

**Parámetros**:

```json
{
  "proposal_id": "uuid",
  "status": "rejected"
}
```

**Respuesta**:

```json
{
  "id": "uuid",
  "status": "rejected",
  "updated_at": "2026-05-22T14:00:00Z"
}
```

**Entidades Manipuladas**: Proposal (actualización)

**Uso**: El usuario puede rechazar o modificar el estado de propuestas manualmente.

---

### create_question

Esta tool crea una pregunta para la Sección de Preguntas, permitiendo reutilización de conocimiento acumulado.

**Parámetros**:

```json
{
  "question": "¿Cómo se maneja la concurrencia en documentos?",
  "answer": "Se usa pessimistic locking con SELECT FOR UPDATE...",
  "source_document_id": "uuid"
}
```

**Respuesta**:

```json
{
  "id": "uuid",
  "question": "¿Cómo se maneja la concurrencia en documentos?",
  "answer": "Se usa pessimistic locking con SELECT FOR UPDATE...",
  "source_document_id": "uuid",
  "created_at": "2026-05-22T12:00:00Z"
}
```

**Entidades Manipuladas**: Question (creación)

**Uso**: El Agente 3 (resolución) crea preguntas cuando las respuestas a gaps son valiosas para reutilización futura.

---

### list_questions

Esta tool lista preguntas disponibles, permitiendo filtrar por estado.

**Parámetros**:

```json
{
  "status": "pending"
}
```

**Respuesta**:

```json
{
  "questions": [
    {
      "id": "uuid",
      "question": "¿Cómo se maneja la concurrencia en documentos?",
      "answer": "Se usa pessimistic locking con SELECT FOR UPDATE...",
      "status": "pending"
    }
  ],
  "total": 10
}
```

**Entidades Manipuladas**: Question (lectura)

**Uso**: El usuario lista preguntas pendientes para priorizar respuestas.

---

### answer_question

Esta tool responde una pregunta pendiente.

**Parámetros**:

```json
{
  "question_id": "uuid",
  "answer": "Se usa pessimistic locking con SELECT FOR UPDATE..."
}
```

**Respuesta**:

```json
{
  "id": "uuid",
  "question": "¿Cómo se maneja la concurrencia en documentos?",
  "answer": "Se usa pessimistic locking con SELECT FOR UPDATE...",
  "status": "answered",
  "answered_at": "2026-05-22T14:00:00Z"
}
```

**Entidades Manipuladas**: Question (actualización)

**Uso**: El usuario responde preguntas pendientes para enriquecer la base de conocimiento.

---

### link_document_to_question

Esta tool vincula un documento a una pregunta, indicando que el documento contiene información relevante para responder la pregunta.

**Parámetros**:

```json
{
  "document_id": "uuid",
  "question_id": "uuid"
}
```

**Respuesta**:

```json
{
  "document_id": "uuid",
  "question_id": "uuid",
  "linked_at": "2026-05-22T12:00:00Z"
}
```

**Entidades Manipuladas**: DocumentQuestion (creación)

**Uso**: Los agentes vinculan documentos relevantes a preguntas para facilitar búsqueda de contexto.

---

### link_gap_to_question

Esta tool vincula un gap a una pregunta, indicando que la pregunta puede ayudar a resolver el gap.

**Parámetros**:

```json
{
  "gap_id": "uuid",
  "question_id": "uuid"
}
```

**Respuesta**:

```json
{
  "gap_id": "uuid",
  "question_id": "uuid",
  "linked_at": "2026-05-22T12:00:00Z"
}
```

**Entidades Manipuladas**: GapQuestion (creación)

**Uso**: Los agentes vinculan preguntas relevantes a gaps para facilitar resolución.

---

### search_similar_documents

Esta tool permite buscar documentos similares usando búsqueda semántica en Qdrant. Facilita la reutilización de conocimiento acumulado al encontrar documentos que tratan temas relacionados.

**Parámetros**:

```json
{
  "query": "arquitectura de 5 fases",
  "limit": 5
}
```

**Respuesta**:

```json
{
  "results": [
    {
      "document_id": "uuid",
      "title": "Technical Brief",
      "similarity": 0.95,
      "relevant_content": "El sistema opera en cinco fases..."
    }
  ]
}
```

**Entidades Manipuladas**: Document (búsqueda semántica vía Qdrant)

**Uso**: Todos los agentes del pipeline pueden buscar contexto acumulado de documentos similares para reutilizar respuestas previas, detectar patrones, y evitar duplicación de esfuerzo.

---

### get_gap_templates

Esta tool obtiene templates de gaps organizados por tipo de documento. Los templates aseguran consistencia en la detección de gaps y reducen el esfuerzo manual de definir preguntas estándar.

**Parámetros**:

```json
{
  "document_type": "architecture"
}
```

**Respuesta**:

```json
{
  "document_type": "architecture",
  "templates": [
    {
      "category": "arquitectura_y_diseño",
      "template": "¿Por qué se eligió {decision}?",
      "context_fields": ["alternativas_consideradas", "trade_offs"]
    }
  ]
}
```

**Entidades Manipuladas**: GapTemplate (lectura)

**Uso**: El Agente 1 (detección) usa estos templates para generar gaps consistentes basados en el tipo de documento, asegurando que se cubran las categorías relevantes (arquitectura, implementación técnica, dominio y terminología).

---

## Referencias

- **[mcp-server-architecture.md](./mcp-server-architecture.md)**: Arquitectura general del MCP Server
- **[mcp-deployment-testing.md](./mcp-deployment-testing.md)**: Deployment y testing del MCP Server
- **[ADR-001](../decisiones/adr-001-mcp-abstraction-layer.md)**: MCP como capa de abstracción
- **[database-schema-design.md](./database-schema-design.md)**: Schema de base de datos
