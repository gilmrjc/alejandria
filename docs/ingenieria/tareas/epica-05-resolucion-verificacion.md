---
id: EPC-005
type: Epic Implementation
related:
  - target: STR-003
    relationship_type: implements
    reason: Implementa la estrategia técnica de resolución y verificación
  - target: FEA-001
    relationship_type: implements
    reason: Implementa el feature de 5-phase workflow
  - target: ARC-007
    relationship_type: references
    reason: Referencia el job-implementation-guide para implementación de jobs
  - target: ARC-013
    relationship_type: references
    reason: Referencia el llm-evals-guide para evals de LLM
---

## Epica 5: Implementación de Fases Resolución y Verificación

**Estado**: 🟡 PARCIALMENTE COMPLETADO - T-048, T-049, T-052 completados. T-050, T-051, T-053 OUT OF SCOPE (movidas a Fase 4 Propuestas).

**Objetivo**: Implementar resolución asíncrona de gaps con sugerencias pre-llenadas por LLM, metadata de respuestas (`answered_by` FK UUID), y vectorización automática de respuestas para generación de propuestas.

**Nota**: El workflow usa proceso asíncrono sin sesiones según decisión de diseño (ver 5-phase-workflow.md). Los usuarios responden gaps individualmente vía API con sugerencias pre-llenadas por el LLM. Las respuestas se vectorizan automáticamente en Qdrant para ser usadas por el cron de Propuestas (Fase 4). La verificación de consistencia y detección de contradicciones se realiza en el contexto de generación de propuestas, no como jobs separados.

---

## Referencias

- **[../../estrategia/estrategia/technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md)**: Roadmap técnico, Hito 5
- **[../arquitectura/technology-stack.md](../arquitectura/technology-stack.md)**: Stack tecnológico
- **[../arquitectura/mcp-server-specification.md](../arquitectura/mcp-server-specification.md)**: Especificación de MCP Server
- **[../arquitectura/job-implementation-guide.md](../arquitectura/job-implementation-guide.md)**: Guía de implementación de jobs
- **[../arquitectura/llm-evals-guide.md](../arquitectura/llm-evals-guide.md)**: Guía de evals para LLM

---

## Componentes

- ✅ Metadata de respuestas (`answered_by` FK UUID, `answer` pre-llenado por LLM)
- ✅ Vectorización automática de respuestas en Qdrant (`question_generation_task`)
- ✅ API endpoints para responder gaps individualmente con auto-encolado de vectorización
- ~~Job asíncrono para verificación de respuestas~~ OUT OF SCOPE (parte de Fase 4 Propuestas)
- ~~Sistema de verificación automática de consistencia~~ OUT OF SCOPE (parte de Fase 4 Propuestas)
- ~~Detección de contradicciones entre respuestas~~ OUT OF SCOPE (parte de Fase 4 Propuestas)

---

## Técnicas Individuales

### Estimación de Esfuerzo Total

**Estimación original**: ~30 horas
**Esfuerzo real implementado**: ~10 horas (T-048 + T-049 + T-052)

Desglose por tarea:

- ✅ T-048: Implementar Sistema de metadata de respuestas - 4h (COMPLETADO)
- ✅ T-049: Vectorización de respuestas - 3h (COMPLETADO)
- ❌ T-050: Implementar Servicio de verificación LLM - 6h (OUT OF SCOPE - Fase 4 Propuestas)
- ❌ T-051: Implementar Detección de contradicciones - 6h (OUT OF SCOPE - Fase 4 Propuestas)
- ✅ T-052: Auto-encolado de vectorización al responder gaps - 3h (COMPLETADO)
- ❌ T-053: Implementar API Endpoints para verificación - 3h (OUT OF SCOPE - Fase 4 Propuestas)

### T-048: Implementar Sistema de metadata de respuestas

**Descripción**: Agregar `answered_by` (FK UUID a `users`) al modelo Gap y generar sugerencias de respuesta (`answer` pre-llenado) durante la detección de gaps.

**Alineación con gap-resolution-mcp**: El skill gap-resolution-mcp usa `answer_gap` para responder gaps. Esta tarea implementa la metadata de qué usuario confirmó la respuesta y provee sugerencias pre-llenadas para facilitar la resolución.

**Criterios de Aceptación**:

- [x] Campo `answered_by` (FK UUID a `users`, SET NULL on delete) agregado al modelo Gap
- [x] Migración Alembic `add_gap_answered_by` aplicada
- [x] Schemas Pydantic actualizados (`GapResponse` incluye `answered_by: UUID | None`)
- [x] LLM genera `answer` (sugerencia) para cada gap durante `gap_detection` usando `search_similar_documents`
- [x] `GapService.create_gap()` persiste el campo `answer` del LLM
- [x] MCP `create_gap` acepta parámetro `answer` opcional
- [x] MCP `answer_gap` retorna `answered_by` en la respuesta
- [x] API endpoints `PUT /gaps/{id}` setean `answered_by = current_user.id` al responder

**Semántica del campo `answer`**:
- `status=pending` + `answer!=null`: sugerencia del LLM pre-llenada
- `status=responded` + `answered_by=UUID`: usuario confirmó/modificó la respuesta

**Dependencias**: Hito 2 (API REST)

**Estado**: COMPLETADO

---

### T-049: Vectorización de respuestas (`question_generation_task`)

**Descripción**: El job `question_generation_task` (ya existente) vectoriza las respuestas confirmadas de gaps en Qdrant para hacer disponible la búsqueda semántica y la generación de propuestas. No es un job de verificación LLM independiente.

**Nota de diseño**: La verificación de respuestas forma parte del flujo de Propuestas (Fase 4), donde el LLM agrupa gaps respondidos semánticamente para generar propuestas de edición.

**Criterios de Aceptación**:

- [x] `question_generation_task` vectoriza la respuesta del gap en colección `gap_answers` de Qdrant
- [x] API endpoints `PUT /gaps/{id}` encolan `question_generation_task` al pasar a `status=responded`
- [x] Encolado falla silenciosamente (try/except + log) sin romper el request

**Dependencias**: T-040 (Celery), T-048 (metadata)

**Estado**: COMPLETADO

---

### T-050: Implementar Servicio de verificación LLM

**Estado**: ❌ OUT OF SCOPE

**Razón**: La verificación de respuestas se implementará en el contexto del cron de Propuestas (Fase 4), donde el LLM agrupa gaps respondidos semánticamente y genera propuestas de edición. No se requiere un servicio de verificación separado.

---

### T-051: Implementar Detección de contradicciones

**Estado**: ❌ OUT OF SCOPE

**Razón**: La detección de contradicciones se implementará en el contexto del cron de Propuestas (Fase 4), donde el LLM puede usar `search_similar_documents` en Qdrant para encontrar respuestas semánticamente relacionadas y detectar inconsistencias. No se requiere un sistema separado.

---

### T-052: Auto-encolado de vectorización al responder gaps

**Descripción**: Al responder un gap via API REST, encolar `question_generation_task` para vectorizar la respuesta en Qdrant. Esto garantiza que las respuestas confirmadas por el usuario sean indexadas y disponibles para búsqueda semántica y el cron de Propuestas.

**Criterios de Aceptación**:

- [x] `PUT /api/v1/gaps/{id}` encola `question_generation_task` al pasar a `status=responded`
- [x] `PUT /api/v1/gaps/slug/{slug}` encola `question_generation_task` al pasar a `status=responded`
- [x] Status de gap se actualiza a `responded` inmediatamente (no espera el job)
- [x] `answered_by` se setea con `current_user.id`
- [x] Encolado falla silenciosamente (try/except + warning log)

**Dependencias**: T-048 (metadata)

**Estado**: COMPLETADO

---

### T-053: Implementar API Endpoints para verificación

**Estado**: ❌ OUT OF SCOPE

**Razón**: Como no hay job de verificación separado ni sistema de contradicciones independiente, no se requieren endpoints específicos para consultar metadata de verificación. La información relevante se expondrá a través de los endpoints de Propuestas (Fase 4).

---

## Información Pendiente de Definir

Las siguientes secciones están marcadas como PENDIENTE y se definirán en fase de implementación:

- ~~Tareas técnicas individuales~~ ✅ DEFINIDO
- ~~Servicio de verificación LLM~~ ❌ OUT OF SCOPE (Fase 4 Propuestas)
- ~~Detección de contradicciones~~ ❌ OUT OF SCOPE (Fase 4 Propuestas)
