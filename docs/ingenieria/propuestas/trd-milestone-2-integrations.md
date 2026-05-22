---
id: TRD-023
type: Technical Requirements Document
rating: 9.5
rating-phase: document-editing
related:
  - target: FSP-003
    relationship_type: implements
    reason: Implementa los casos de uso del Hito 2 con requisitos técnicos de integraciones
  - target: FSP-004
    relationship_type: implements
    reason: Implementa las reglas de negocio del Hito 2 con requisitos técnicos de integraciones
  - target: ADR-002
    relationship_type: depends_on
    reason: Depende de ADR-002 para stack unificado Python
  - target: ADR-004
    relationship_type: depends_on
    reason: Depende de ADR-004 para estrategia de ephemeral jobs
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para implementación de integraciones
  - target: ARC-033
    relationship_type: references
    reason: Referencia la implementación de búsqueda semántica
  - target: ARC-037
    relationship_type: references
    reason: Referencia la estrategia de consistencia y concurrencia
  - target: ARC-038
    relationship_type: references
    reason: Referencia la estrategia de performance y escalabilidad
  - target: ARC-039
    relationship_type: references
    reason: Referencia la estrategia de observabilidad y monitoreo
  - target: ARC-002
    relationship_type: references
    reason: Referencia el flujo end-to-end para casos de uso del pipeline
---

# TRD - Hito 2: Integraciones

## Visión General

### Objetivo del Hito

Implementar las integraciones con servicios externos (Qdrant, Redis) que permitan orquestar el pipeline de 5 fases, gestionar documentos, sesiones, gaps y configuración del sistema. Este hito establece las conexiones con servicios de almacenamiento vectorial y caché sobre la infraestructura base configurada en el Hito 1.

### Propósito

Proporcionar las integraciones con servicios externos que serán utilizados por la API REST y el MCP Server. Este hito habilita la ejecución del pipeline de detección, agrupación, resolución, verificación y aplicación de cambios en documentos mediante búsqueda semántica y caché de sesiones.

### Referencias

Este hito se fundamenta en varios documentos de arquitectura y decisiones técnicas:

**Roadmap y Estrategia:**
- [technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md): Hito 2 - API REST y MCP Server

**Decisiones Arquitectónicas (ADR):**
- [ADR-002](../decisiones/adr-002-python-unified-stack.md): Stack Unificado en Python (FastAPI + FastMCP)
- [ADR-004](../decisiones/adr-004-ephemeral-jobs.md): Estrategia de Ephemeral Jobs

**Arquitectura General:**
- [semantic-search-implementation.md](../arquitectura/semantic-search-implementation.md): Implementación de Búsqueda Semántica (ARC-033)
- [database-schema-design.md](../arquitectura/database-schema-design.md): Diseño conceptual de schema de PostgreSQL (ARC-004)
- [mcp-server-data-consistency-concurrency.md](../arquitectura/mcp-server-data-consistency-concurrency.md): Consistencia y Concurrency (ARC-037)
- [mcp-server-performance-scalability.md](../arquitectura/mcp-server-performance-scalability.md): Performance y Escalabilidad (ARC-038)
- [mcp-server-observability-monitoring.md](../arquitectura/mcp-server-observability-monitoring.md): Observabilidad y Monitoreo (ARC-039)
- [end-to-end-pipeline.md](../arquitectura/end-to-end-pipeline.md): Flujo end-to-end del pipeline (ARC-002)

**Documentos Relacionados:**
- [trd-milestone-1-infrastructure.md](./trd-milestone-1-infrastructure.md): TRD Hito 1 (rating: 9)
- [trd-milestone-2-api-rest.md](./trd-milestone-2-api-rest.md): TRD Hito 2 - API REST (TRD-021)
- [trd-milestone-2-mcp-server.md](./trd-milestone-2-mcp-server.md): TRD Hito 2 - MCP Server (TRD-022)

---

## Requisitos Funcionales

**Nota sobre webhooks**: Para MVP Bootstrapped, NO implementar webhooks. Post-MVP: Implementar webhooks cuando se requiera integración con sistemas externos. Retry strategy: Usar ADR-004 (backoff exponencial con jitter ±20%) cuando se implemente.

### RF-008: Integration with Qdrant

#### Descripción - RF-008

Implementar integración con Qdrant para búsqueda semántica y almacenamiento de embeddings.

#### Criterios de Aceptación - RF-008

- [ ] Cliente HTTP para comunicarse con API de Qdrant
- [ ] Funciones para crear colecciones, insertar vectores, buscar por similitud
- [ ] **Modelo de embeddings**: BGE-M3 configurado como modelo de embeddings
- [ ] **Estrategia de chunking**: Tamaño máximo 256 tokens, superposición 25 tokens (10%), algoritmo de división por párrafos con agrupación inteligente
- [ ] **Metadata asociada a vectores**: document_id, section_title, chunk_index, created_at
- [ ] **Actualización de vectores**: Para documentos actualizados, eliminar vectores existentes, chunking nuevo, generar embeddings, insertar dentro de transacción en Python para atomicidad

#### Prioridad - RF-008: Media

### RF-010: Integration with Redis

#### Descripción - RF-010

Implementar integración con Redis para caché de sesiones y gestión de estado.

#### Criterios de Aceptación - RF-010

- [ ] Cliente Redis para caché de sesiones
- [ ] Funciones para almacenar y recuperar estado de sesiones
- [ ] TTL configurado para entradas de caché
- [ ] Manejo de errores de conexión a Redis
- [ ] **Estrategia de fallback**: Si Redis no está disponible, continuar con operación sin caché (degradación graceful)

#### Prioridad - RF-010: Media

---

## Requisitos No Funcionales

### RNF-001: Performance

#### Criterios - RNF-001

- [ ] Tiempo máximo de respuesta para operaciones de integración (SLAs p95/p99 para operaciones principales, monitoreo vía latency_ms en logs)
- [ ] Tiempo máximo de ejecución por fase del pipeline
- [ ] Número máximo de documentos procesados concurrentemente
- [ ] Número máximo de sesiones simultáneas

### RNF-002: Seguridad

#### Criterios - RNF-002

- [ ] Validación de input y sanitización para prevenir inyección SQL, XSS (Pydantic 2.12.0 + Bleach con bleach-allowlist para sanitización de markdown, validaciones específicas por entidad)
- [ ] Encriptación de datos en reposo y en tránsito (HTTPS obligatorio en producción TLS 1.3, HTTP solo en localhost para desarrollo, NO SSL en PostgreSQL para MVP, passwords con bcrypt cost factor 12, datos en reposo con disk encryption)
- [ ] Política de retención de datos (SIN política de retención explícita para MVP, datos retenidos indefinidamente sin cleanup automático, post-MVP implementar política cuando se requiera compliance)
- [ ] Passwords almacenados como hash (no texto plano)

### RNF-003: Observabilidad

#### Criterios - RNF-003

- [ ] Logging estructurado JSON con request IDs (según ADR-002)
- [ ] Métricas de integraciones (latencia, throughput, error rate) - monitoreo de latencia vía logs, sin metrics detalladas para MVP (post-MVP)
- [ ] Monitoreo de métricas con Prometheus/Grafana (post-MVP según ADR-002)
- [ ] Distributed tracing (post-MVP según ADR-002)

### RNF-004: Testing

#### Criterios - RNF-004

- [ ] Cobertura objetivo: >90% con pytest (según ADR-002)
- [ ] Unit tests (70-80%): lógica de negocio, services, schemas
- [ ] Integration tests (15-20%): DB real (testcontainers PostgreSQL, Redis)
- [ ] E2E tests (5-10%): flujos completos del pipeline
- [ ] Estrategia de testing de integraciones específica (pytest, testcontainers)
- [ ] Testing de integraciones con servicios externos (Qdrant, Redis)

---

## Casos de Uso

### UC-001: Crear Documento y Detectar Gaps

#### Actor - UC-001: Usuario

#### Precondiciones - UC-001

- Infraestructura base operativa (Hito 1)
- Usuario autenticado

#### Flujo Principal - UC-001

1. Usuario crea documento vía API REST
2. API crea registro en tabla `documents`
3. API invoca MCP Server con LLM (Ollama) de forma sincrónica
4. MCP Server usa tool `read_document` para leer contenido
5. MCP Server usa tool `create_gap` para crear gaps detectados
6. Gaps se almacenan en tabla `gaps`
7. Usuario puede ver gaps vía MCP tools

#### Postcondiciones - UC-001

- Documento creado en base de datos
- Gaps detectados y almacenados

---

## Dependencias

### Dependencias Externas

- Python 3.11+
- uv para gestión de dependencias
- Infraestructura base (Hito 1): PostgreSQL, Redis, Qdrant, Ollama

### Dependencias Internas

- database-schema.md: Schema de base de datos
- ADR-002: Stack unificado en Python
- ADR-004: Estrategia de ephemeral jobs
- semantic-search-implementation.md: Implementación de búsqueda semántica

### Dependencias de Otros Hitos

- Hito 1: Infraestructura Base (dependencia crítica)

---

## Criterios de Completitud del Hito

Basado en technical-roadmap.md, el Hito 2 se considera completo cuando:

- [ ] Integración con Qdrant para búsqueda semántica básica
- [ ] Integración con Redis para caché de sesiones

### Criterios Adicionales de este TRD

- [ ] Todos los requisitos funcionales (RF-008, RF-010) están cumplidos
- [ ] Testing básico implementado (unit tests)
- [ ] Documentación de integraciones disponible

---

## Criterio de Éxito

**Objetivo cualitativo**: Las integraciones con Qdrant y Redis son funcionales para ejecutar el pipeline básico de detección y resolución de gaps.

Justificación: Para el MVP Bootstrapped, el criterio de éxito es funcionalidad básica sobre optimización de performance. Los gaps identificados en requisitos no funcionales (performance, observabilidad avanzada) se resolverán en fases post-MVP según ADR-002.

---

## Riesgos y Mitigación

### Riesgo 2: Integración con Qdrant tiene latencia alta

**Mitigación**: Qdrant ejecuta en Docker según configuración de Hito 1. Usar conexión local para baja latencia. Implementar timeouts apropiados y manejo de errores. Considerar caché de resultados de búsqueda semántica para queries frecuentes.

### Riesgo 3: Redis como single point of failure

**Mitigación**: Para MVP, Redis como single instance es aceptable. Implementar degradación graceful cuando Redis no está disponible (continuar sin caché). Post-MVP considerar Redis Cluster o Redis Sentinel para alta disponibilidad.
