---
id: EPC-004
type: Epic Implementation
related:
  - target: STR-003
    relationship_type: implements
    reason: Implementa la estrategia técnica de detección y agrupación
  - target: FEA-001
    relationship_type: implements
    reason: Implementa el feature de 5-phase workflow
  - target: REQ-003
    relationship_type: implements
    reason: Implementa los requisitos de detección y agrupación
  - target: ARC-007
    relationship_type: references
    reason: Referencia el job-implementation-guide para implementación de jobs
  - target: ARC-013
    relationship_type: references
    reason: Referencia el llm-evals-guide para evals de LLM
---

## Epica 4: Implementación de Fases Detección y Agrupación

**Estado**: 🔄 EN PROGRESO - Implementación parcial completada

**Objetivo**: Implementar los agentes LLM para análisis de documentos, sistema de metadata de gaps, agrupación por tema, y dashboard de gaps detectados.

**Nota**: El workflow usa proceso asíncrono sin sesiones según decisión de diseño (ver 5-phase-workflow.md y PRD-002). La agrupación por similitud semántica se pospone a POST-MVP.

---

## Referencias

- **[../../estrategia/estrategia/technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md)**: Roadmap técnico, Hito 4
- **[../arquitectura/technology-stack.md](../arquitectura/technology-stack.md)**: Stack tecnológico
- **[../arquitectura/mcp-server-specification.md](../arquitectura/mcp-server-specification.md)**: Especificación de MCP Server
- **[../arquitectura/job-implementation-guide.md](../arquitectura/job-implementation-guide.md)**: Guía de implementación de jobs
- **[../arquitectura/llm-evals-guide.md](../arquitectura/llm-evals-guide.md)**: Guía de evals para LLM

---

## Componentes

- Sistema de jobs asíncronos con Celery
- Agentes LLM para análisis de documentos
- Sistema de metadata de gaps (tipo, severidad, rol afectado, contexto)
- Sistema de agrupación por tema (tags deterministas)
- Dashboard de gaps detectados con filtros

**Nota**: Agrupación por similitud semántica con Qdrant se pospone a POST-MVP.

---

## Técnicas Individuales

### Estimación de Esfuerzo Total

**Estimación total**: ~46 horas

Desglose por tarea:

- T-040: Configurar Celery para Jobs - 4h ✅ COMPLETADO
- T-041: Implementar Job gap_detection - 8h ✅ COMPLETADO
- T-042: Implementar Job vector_sync - 6h ✅ COMPLETADO
- T-043: Implementar Job question_generation - 6h ✅ COMPLETADO
- T-044: Implementar Agente LLM para análisis de documentos - 8h ✅ COMPLETADO
- T-045: Implementar Sistema de metadata de gaps - 4h ✅ COMPLETADO
- T-046: Implementar Sistema de agrupación por tema - 4h ✅ COMPLETADO (semántica POST-MVP)
- T-047: Implementar API Endpoints para Dashboard de Gaps - 6h ✅ COMPLETADO

Nota: Estimaciones detalladas están en tareas individuales.

### T-040: Configurar Celery para Jobs

**Descripción**: Configurar Celery con Redis como broker para sistema de jobs asíncronos según ADR-004.

**Criterios de Aceptación**:

- [x] Celery 5.5.0 configurado con Redis como broker
- [x] Workers de Celery configurados
- [x] Job types definidos: gap_detection, vector_sync, question_generation
- [x] Retry strategy implementada (backoff exponencial con jitter)
- [x] Máximo 5 reintentos por defecto
- [x] Timeout de 5 minutos para todos los jobs

**Retry Strategy**:

Backoff exponencial (1s, 2s, 4s, 8s, 16s con ±20% jitter), máximo 5 reintentos, timeout 5 minutos. Referencia: ADR-004 y ADR-005 para implementación detallada.

**Dependencias**: Hito 2 (API REST y MCP Server)

**Estado**: ✅ COMPLETADO

---

### T-041: Implementar Job gap_detection

**Descripción**: Implementar job para detección de gaps en documentos usando LLM.

**Criterios de Aceptación**:

- [x] Job gap_detection detecta gaps en documento usando LLM
- [ ] Gaps detectados tienen metadata completa (tipo, severidad, rol afectado, contexto) - PARCIAL (type/severity no almacenados)
- [x] Job es idempotente usando locks en base de datos
- [x] Job maneja errores de LLM con retry strategy

**Locks para Idempotencia**:

Implementación usando celery_once con Redis distributed locks. Referencia: ADR-005 para implementación completa.

**Dependencias**: T-040, T-044

**Estado**: ✅ COMPLETADO (con nota: type/severity pendientes en T-045)

---

### T-042: Implementar Job vector_sync

**Descripción**: Implementar job para sincronización de vectores con Qdrant.

**Criterios de Aceptación**:

- [x] Job vector_sync sincroniza embeddings con Qdrant
- [x] Estrategia de chunking implementada (512 tokens, 50 tokens overlap)
- [x] Metadata asociada a vectores para filtros
- [x] Job es idempotente usando locks en base de datos

**Estrategia de Chunking**:

- Tamaño máximo de chunk: 512 tokens
- Superposición entre chunks: 50 tokens (10%)
- Algoritmo: 1) Dividir texto en párrafos, 2) Agrupar párrafos hasta alcanzar ~512 tokens, 3) Mantener superposición de 50 tokens entre chunks adyacentes, 4) Preservar estructura de secciones en metadata

**Dependencias**: T-040

**Estado**: ✅ COMPLETADO

---

### T-043: Implementar Job question_generation

**Descripción**: Implementar job para generación de respuestas a preguntas usando LLM.

**Criterios de Aceptación**:

- [x] Job question_generation genera respuestas a preguntas
- [x] Respuestas se transforman en vectores para Qdrant
- [x] Job es idempotente usando locks en base de datos
- [x] Job maneja errores de LLM con retry strategy

**Dependencias**: T-040, T-042

**Estado**: ✅ COMPLETADO

---

### T-044: Implementar Agente LLM para análisis de documentos

**Descripción**: Implementar agente LLM para análisis de documentos y detección de gaps con generación de sugerencias de respuesta.

**Criterios de Aceptación**:

- [x] Agente LLM analiza documentos y detecta gaps
- [x] Prompt de gap_detection implementado según mcp-server-specification.md
- [x] LLM genera `answer` (sugerencia) para cada gap usando `search_similar_documents` para contexto relacionado
- [x] Integración con Ollama (Qwen 3.5) funcional
- [x] Manejo de timeouts y errores de conexión

**Dependencias**: Hito 2 (Integración con Ollama)

**Estado**: ✅ COMPLETADO

---

### T-045: Implementar Sistema de metadata de gaps

**Descripción**: Implementar sistema de metadata para gaps (rol afectado, contexto, answer pre-llenado).

**Nota**: Los campos type y severity que genera el LLM no se almacenan en el MVP para simplificar el modelo. Se posponen a POST-MVP. El campo `answer` se almacena como sugerencia pre-llenada por el LLM.

**Criterios de Aceptación**:

- [x] Metadata de gaps almacenada en base de datos
- [x] Campos: rol afectado, contexto, answer (sugerencia del LLM)
- [x] API endpoints para gestión de metadata
- [x] Filtros por rol
- [x] `GapService.create_gap()` persiste el campo `answer` del LLM

**Dependencias**: Hito 2 (API REST)

**Estado**: ✅ COMPLETADO

---

### T-046: Implementar Sistema de agrupación por tema

**Descripción**: Implementar sistema de agrupación de gaps por tema usando tags deterministas.

**Criterios de Aceptación**:

- [x] Gaps agrupados por tema usando tags
- [ ] Agrupación por similitud semántica usando Qdrant - POST-MVP
- [x] Dashboard de gaps con filtros por tema

**Dependencias**: T-042, T-045

**Estado**: ✅ COMPLETADO (agrupación semántica pospuesta a POST-MVP)

---

### T-047: Implementar API Endpoints para Dashboard de Gaps

**Descripción**: Implementar endpoints de API para datos del dashboard de gaps (backend-only).

**Criterios de Aceptación**:

- [x] GET /api/v1/gaps/dashboard con métricas agregadas
- [x] Filtros por tema, prioridad, estado, tipo
- [x] Agrupación por tema implementada
- [x] Metadata de tags incluida en respuestas
- [x] Paginación implementada

**Dependencias**: T-045, T-046

**Estado**: ✅ COMPLETADO

**Estimación**: 6h

**Nota**: Frontend del dashboard (visualización) se implementará en Épica 3-B (T-036)

---

## Información Pendiente de Definir

Las siguientes secciones están marcadas como PENDIENTE y se definirán en fase de implementación:

- ~~Tareas técnicas individuales para dashboard de gaps detectados con filtros~~ ✅ DEFINIDO (T-047 - backend)

## Tareas Pendientes para Completar Hito 4

**Estado**: ✅ Hito 4 COMPLETADO

Todas las tareas del Hito 4 están completadas según el diseño actual:

- ✅ Sistema de jobs asíncronos con Celery
- ✅ Agentes LLM para análisis de documentos
- ✅ Sistema de metadata de gaps (rol afectado, contexto)
- ✅ Sistema de agrupación por tema (tags deterministas)
- ✅ Dashboard de gaps detectados con filtros

**Notas de diseño**:
- El workflow usa proceso asíncrono sin sesiones (ver 5-phase-workflow.md)
- Los campos type y severity que genera el LLM no se almacenan en MVP para simplificar el modelo
- El campo `answer` se genera por el LLM durante la detección usando `search_similar_documents` para contexto relacionado
- La agrupación por similitud semántica se pospone a POST-MVP
