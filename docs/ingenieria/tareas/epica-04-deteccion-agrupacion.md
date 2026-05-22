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

**Estado**: ⏳ PENDIENTE - Técnicas por definir

**Objetivo**: Implementar los agentes LLM para análisis de documentos, sistema de metadata de gaps, agrupación por tema y similitud semántica, y dashboard de gaps detectados.

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
- Sistema de agrupación por tema y similitud semántica
- Metadata de sesiones (tema, subtema, prioridad)
- Dashboard de gaps detectados con filtros

---

## Técnicas Individuales

### Estimación de Esfuerzo Total

**Estimación total**: ~40 horas

Desglose por tarea:

- T-040: Configurar Celery para Jobs - 4h
- T-041: Implementar Job gap_detection - 8h
- T-042: Implementar Job vector_sync - 6h
- T-043: Implementar Job question_generation - 6h
- T-044: Implementar Agente LLM para análisis de documentos - 8h
- T-045: Implementar Sistema de metadata de gaps - 4h
- T-046: Implementar Sistema de agrupación por tema - 4h

Nota: Estimaciones detalladas están en tareas individuales.

### T-040: Configurar Celery para Jobs

**Descripción**: Configurar Celery con Redis como broker para sistema de jobs asíncronos según ADR-004.

**Criterios de Aceptación**:

- [ ] Celery 5.5.0 configurado con Redis como broker
- [ ] Workers de Celery configurados
- [ ] Job types definidos: gap_detection, vector_sync, question_generation
- [ ] Retry strategy implementada (backoff exponencial con jitter)
- [ ] Máximo 5 reintentos por defecto
- [ ] Timeout de 5 minutos para todos los jobs

**Retry Strategy**:

Backoff exponencial (1s, 2s, 4s, 8s, 16s con ±20% jitter), máximo 5 reintentos, timeout 5 minutos. Referencia: ADR-004 y ADR-005 para implementación detallada.

**Dependencias**: Hito 2 (API REST y MCP Server)

**Estado**: PENDIENTE

---

### T-041: Implementar Job gap_detection

**Descripción**: Implementar job para detección de gaps en documentos usando LLM.

**Criterios de Aceptación**:

- [ ] Job gap_detection detecta gaps en documento usando LLM
- [ ] Gaps detectados tienen metadata completa (tipo, severidad, rol afectado, contexto)
- [ ] Job es idempotente usando locks en base de datos
- [ ] Job maneja errores de LLM con retry strategy

**Locks para Idempotencia**:

Implementación usando celery_once con Redis distributed locks. Referencia: ADR-005 para implementación completa.

**Dependencias**: T-040, T-044

**Estado**: PENDIENTE

---

### T-042: Implementar Job vector_sync

**Descripción**: Implementar job para sincronización de vectores con Qdrant.

**Criterios de Aceptación**:

- [ ] Job vector_sync sincroniza embeddings con Qdrant
- [ ] Estrategia de chunking implementada (512 tokens, 50 tokens overlap)
- [ ] Metadata asociada a vectores para filtros
- [ ] Job es idempotente usando locks en base de datos

**Estrategia de Chunking**:

- Tamaño máximo de chunk: 512 tokens
- Superposición entre chunks: 50 tokens (10%)
- Algoritmo: 1) Dividir texto en párrafos, 2) Agrupar párrafos hasta alcanzar ~512 tokens, 3) Mantener superposición de 50 tokens entre chunks adyacentes, 4) Preservar estructura de secciones en metadata

**Dependencias**: T-040

**Estado**: PENDIENTE

---

### T-043: Implementar Job question_generation

**Descripción**: Implementar job para generación de respuestas a preguntas usando LLM.

**Criterios de Aceptación**:

- [ ] Job question_generation genera respuestas a preguntas
- [ ] Respuestas se transforman en vectores para Qdrant
- [ ] Job es idempotente usando locks en base de datos
- [ ] Job maneja errores de LLM con retry strategy

**Dependencias**: T-040, T-042

**Estado**: PENDIENTE

---

### T-044: Implementar Agente LLM para análisis de documentos

**Descripción**: Implementar agente LLM para análisis de documentos y detección de gaps.

**Criterios de Aceptación**:

- [ ] Agente LLM analiza documentos y detecta gaps
- [ ] Prompt de gap_detection implementado según mcp-server-specification.md
- [ ] Integración con Ollama (Qwen 3.5) funcional
- [ ] Manejo de timeouts y errores de conexión

**Dependencias**: Hito 2 (Integración con Ollama)

**Estado**: PENDIENTE

---

### T-045: Implementar Sistema de metadata de gaps

**Descripción**: Implementar sistema de metadata para gaps (tipo, severidad, rol afectado, contexto).

**Criterios de Aceptación**:

- [ ] Metadata de gaps almacenada en base de datos
- [ ] Campos: tipo, severidad, rol afectado, contexto
- [ ] API endpoints para gestión de metadata
- [ ] Filtros por tipo, severidad, rol

**Dependencias**: Hito 2 (API REST)

**Estado**: PENDIENTE

---

### T-046: Implementar Sistema de agrupación por tema

**Descripción**: Implementar sistema de agrupación de gaps por tema y similitud semántica.

**Criterios de Aceptación**:

- [ ] Gaps agrupados por tema usando tags
- [ ] Agrupación por similitud semántica usando Qdrant
- [ ] Dashboard de gaps con filtros por tema
- [ ] Metadata de sesiones (tema, subtema, prioridad)

**Dependencias**: T-042, T-045

**Estado**: PENDIENTE

---

## Información Pendiente de Definir

Las siguientes secciones están marcadas como PENDIENTE y se definirán en fase de implementación:

- Tareas técnicas individuales para metadata de sesiones
- Tareas técnicas individuales para dashboard de gaps detectados con filtros
