---
id: EPC-006
type: Epic Implementation
related:
  - target: STR-003
    relationship_type: implements
    reason: Implementa la estrategia técnica de fase de aplicación
  - target: FEA-001
    relationship_type: implements
    reason: Implementa el feature de 5-phase workflow
  - target: TS-002
    relationship_type: implements
    reason: Implementa la especificación técnica de aplicación de cambios
  - target: T-027
    relationship_type: implements
    reason: Implementa la tarea de testing básico
---

## Epica 6: Implementación de Fase Aplicación

**Estado**: ⏳ PENDIENTE - Técnicas por definir

**Objetivo**: Implementar el sistema de aplicación automática con aprobación, diff viewer para revisión de cambios, versioning automático de documentos y rollback automático.

**Nota**: El workflow usa proceso asíncrono sin sesiones según decisión de diseño (ver 5-phase-workflow.md). Las propuestas se generan automáticamente cuando gaps son respondidos y verificados, y se aplican automáticamente tras aprobación. Este flujo se alinea con los skills actions-proposal-mcp (generación de propuestas) y document-editing-mcp (aplicación de propuestas).

---

## Referencias

- **[../../estrategia/estrategia/technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md)**: Roadmap técnico, Hito 6
- **[../arquitectura/technology-stack.md](../arquitectura/technology-stack.md)**: Stack tecnológico
- **[../arquitectura/mcp-server-specification.md](../arquitectura/mcp-server-specification.md)**: Especificación de MCP Server
- **[../arquitectura/job-implementation-guide.md](../arquitectura/job-implementation-guide.md)**: Guía de implementación de jobs

---

## Componentes

- Job asíncrono para generación de propuestas
- Job asíncrono para aplicación de propuestas
- Sistema de aprobación de propuestas
- Diff viewer para revisión de cambios antes de aplicar
- Versioning automático de documentos
- Rollback automático si se detectan errores

---

## Modelo de Datos de Propuestas

El modelo `Proposal` ya tiene implementadas las relaciones necesarias:

- **`ProposalDocument`** (M-N): Relaciona proposals con documentos que se van a mejorar
  - `proposal_id` → FK a `proposals`
  - `document_id` → FK a `documents`
  - Una propuesta puede afectar múltiples documentos

- **`ProposalGap`** (M-N): Relaciona proposals con gaps usados como inputs
  - `proposal_id` → FK a `proposals`
  - `gap_id` → FK a `gaps`
  - Una propuesta se genera a partir de múltiples gaps respondidos

**Nota**: Estas relaciones ya están implementadas en `shared/db/models.py`. El job `proposal_generation` debe crear las instancias de `ProposalDocument` y `ProposalGap` al generar una propuesta.

---

## Técnicas Individuales

### Estimación de Esfuerzo Total

**Estimación total**: ~28 horas

Desglose por tarea:

- T-054: Implementar Job proposal_generation - 8h
- T-055: Implementar Job proposal_application - 8h
- T-056: Implementar Sistema de aprobación de propuestas - 4h
- T-057: Implementar Diff viewer API - 4h
- T-058: Implementar Rollback automático - 4h

### T-054: Implementar Job proposal_generation

**Descripción**: Implementar job asíncrono (cron) para generar propuestas basadas en gaps respondidos. Este job se ejecuta cada 30 minutos y usa Qdrant para encontrar gaps respondidos semánticamente relacionados.

**Alineación con actions-proposal-mcp**: Este job implementa la lógica de generación de propuestas de actions-proposal-mcp, pero como job asíncrono en lugar de skill interactivo. Usa las mismas herramientas MCP (list_gaps, read_document, create_proposal) y Qdrant para búsqueda semántica.

**Criterios de Aceptación**:

- [ ] Job proposal_generation genera propuestas usando LLM con prompts similares a actions-proposal-mcp
- [ ] Generación detecta gaps respondidos en últimos 30 minutos (ejecución condicional)
- [ ] LLM usa `search_similar_documents` en Qdrant para encontrar gaps respondidos semánticamente relacionados
- [ ] Propuesta agrupa gaps relacionados en una sola propuesta de edición
- [ ] Propuesta incluye acciones para integrar respuestas al contenido principal
- [ ] Propuesta incluye mejoras de redacción y estilo
- [ ] Propuesta identifica documentos impactados indirectamente
- [ ] Job es idempotente usando celery_once
- [ ] Job maneja errores de LLM con retry strategy
- [ ] Job usa create_proposal para crear propuesta en base de datos

**Dependencias**: T-040 (Celery), T-044 (Agente LLM), T-048 (metadata), T-052 (vectorización)

**Estado**: PENDIENTE

---

### T-055: Implementar Job proposal_application

**Descripción**: Implementar job asíncrono para aplicar propuestas aprobadas. Este job se ejecuta cuando una propuesta es aprobada por el usuario.

**Alineación con document-editing-mcp**: Este job implementa la lógica de aplicación de propuestas de document-editing-mcp, pero como job asíncrono. Usa las mismas herramientas MCP (read_document, write_document, list_gaps).

**Criterios de Aceptación**:

- [ ] Job proposal_application aplica propuestas usando LLM con prompts similares a document-editing-mcp
- [ ] Aplicación integra respuestas de gaps al contenido principal
- [ ] Aplicación actualiza calificación del documento
- [ ] Aplicación mejora documentos relacionados según propuesta
- [ ] Job es idempotente usando celery_once
- [ ] Job maneja errores de LLM con retry strategy
- [ ] Job usa write_document para aplicar cambios con commit messages
- [ ] Job activa rollback automático si hay errores

**Dependencias**: T-040 (Celery), T-044 (Agente LLM), T-054 (proposal_generation), T-058 (rollback)

**Estado**: PENDIENTE

---

### T-056: Implementar Sistema de aprobación de propuestas

**Descripción**: Implementar sistema de aprobación de propuestas vía API endpoints.

**Alineación con actions-proposal-mcp**: actions-proposal-mcp crea propuestas pero no las aprueba. Este sistema implementa la aprobación humana vía API.

**Criterios de Aceptación**:

- [ ] PUT /api/v1/proposals/{id}/approve para aprobar propuesta
- [ ] PUT /api/v1/proposals/{id}/reject para rechazar propuesta
- [ ] Al aprobar, encola job proposal_application
- [ ] Al rechazar, actualiza estado de propuesta a rejected
- [ ] Schemas Pydantic para aprobación/rechazo
- [ ] Validación de que proposal esté en estado pending

**Dependencias**: T-054 (proposal_generation)

**Estado**: PENDIENTE

---

### T-057: Implementar Diff viewer API

**Descripción**: Implementar API endpoints para diff viewer que muestra cambios antes de aplicar.

**Alineación con document-editing-mcp**: document-editing-mcp aplica cambios. Este API permite revisar los cambios antes de la aplicación.

**Criterios de Aceptación**:

- [ ] GET /api/v1/proposals/{id}/diff con diff de cambios propuestos
- [ ] Diff muestra cambios línea por línea (antes/después)
- [ ] Diff incluye cambios en documentos relacionados
- [ ] Filtros por tipo de cambio (edición, creación, eliminación)
- [ ] Schemas Pydantic para respuestas de diff

**Dependencias**: T-054 (proposal_generation)

**Estado**: PENDIENTE

---

### T-058: Implementar Rollback automático

**Descripción**: Implementar sistema de rollback automático si se detectan errores durante la aplicación de propuestas.

**Alineación con document-editing-mcp**: document-editing-mcp lleva documentos a su forma final. Este sistema asegura reversibilidad si hay errores.

**Criterios de Aceptación**:

- [ ] Rollback automático se activa si job proposal_application falla
- [ ] Rollback usa versioning automático (ADR-006) para revertir a versión anterior
- [ ] Rollback restaura documento y documentos relacionados
- [ ] Rollback marca propuesta como failed
- [ ] Rollback registra error en metadata de propuesta
- [ ] Rollback es idempotente

**Dependencias**: T-055 (proposal_application), ADR-006 (versioning)

**Estado**: PENDIENTE

---

## Información Pendiente de Definir

Las siguientes secciones están marcadas como PENDIENTE y se definirán en fase de implementación:

- ~~Tareas técnicas individuales~~ ✅ DEFINIDO
