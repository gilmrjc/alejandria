---
id: TRD-022
type: Technical Requirements Document
rating: 9.5
rating-phase: document-editing
related:
  - target: FSP-003
    relationship_type: implements
    reason: Implementa los casos de uso del Hito 2 con requisitos técnicos de MCP Server
  - target: FSP-004
    relationship_type: implements
    reason: Implementa las reglas de negocio del Hito 2 con requisitos técnicos de MCP Server
  - target: ADR-001
    relationship_type: depends_on
    reason: Depende de ADR-001 para implementación de MCP Server
  - target: ADR-002
    relationship_type: depends_on
    reason: Depende de ADR-002 para stack unificado Python (FastMCP)
  - target: ADR-006
    relationship_type: depends_on
    reason: Depende de ADR-006 para versioning de documentos
  - target: ARC-030
    relationship_type: implements
    reason: Implementa la especificación de MCP Server en requisitos funcionales
  - target: ARC-036
    relationship_type: references
    reason: Referencia la especificación de tools de MCP
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

# TRD - Hito 2: MCP Server

## Visión General

### Objetivo del Hito

Implementar el MCP Server básico que permita orquestar el pipeline de 5 fases, gestionar documentos, sesiones, gaps y configuración del sistema. Este hito establece la capa de abstracción para LLMs sobre la infraestructura base configurada en el Hito 1.

### Propósito

Proporcionar la capa de abstracción para LLMs (MCP Server) que será utilizada por los agentes del sistema. Este hito habilita la ejecución del pipeline de detección, agrupación, resolución, verificación y aplicación de cambios en documentos mediante tools estandarizadas.

### Referencias

Este hito se fundamenta en varios documentos de arquitectura y decisiones técnicas:

**Roadmap y Estrategia:**
- [technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md): Hito 2 - API REST y MCP Server

**Decisiones Arquitectónicas (ADR):**
- [ADR-001](../decisiones/adr-001-mcp-abstraction-layer.md): Uso de MCP como Capa de Abstracción para LLM
- [ADR-002](../decisiones/adr-002-python-unified-stack.md): Stack Unificado en Python (FastAPI + FastMCP)
- [ADR-006](../decisiones/adr-006-document-versioning.md): Versioning de Documentos

**Arquitectura MCP (ARC):**
- [mcp-server-architecture.md](../arquitectura/mcp-server-architecture.md): Arquitectura de MCP Server (ARC-030)
- [mcp-tools-specification.md](../arquitectura/mcp-tools-specification.md): Tools de MCP (ARC-036)
- [mcp-server-data-consistency-concurrency.md](../arquitectura/mcp-server-data-consistency-concurrency.md): Consistencia y Concurrency (ARC-037)
- [mcp-server-performance-scalability.md](../arquitectura/mcp-server-performance-scalability.md): Performance y Escalabilidad (ARC-038)
- [mcp-server-observability-monitoring.md](../arquitectura/mcp-server-observability-monitoring.md): Observabilidad y Monitoreo (ARC-039)
- [mcp-deployment-testing.md](../arquitectura/mcp-deployment-testing.md): Deployment y Testing de MCP (ARC-032)

**Arquitectura General:**
- [end-to-end-pipeline.md](../arquitectura/end-to-end-pipeline.md): Flujo end-to-end del pipeline (ARC-002)

**Documentos Relacionados:**
- [trd-milestone-1-infrastructure.md](./trd-milestone-1-infrastructure.md): TRD Hito 1 (rating: 9)
- [trd-milestone-2-api-rest.md](./trd-milestone-2-api-rest.md): TRD Hito 2 - API REST (TRD-021)
- [trd-milestone-2-integrations.md](./trd-milestone-2-integrations.md): TRD Hito 2 - Integraciones (TRD-023)

---

## Requisitos Funcionales

### RF-007: MCP Server Implementation

#### Descripción - RF-007

Implementar el MCP Server usando FastMCP con las tools definidas en mcp-tools-specification.md.

#### Criterios de Aceptación - RF-007

- [ ] MCP Server implementado con FastMCP 3.2.0
- [ ] Tools MCP implementadas (read_document, write_document, list_gaps, create_gap, answer_gap, etc.)
- [ ] Transporte stdio para desarrollo local
- [ ] Transporte HTTP para producción
- [ ] Integración con PostgreSQL, Qdrant y Redis
- [ ] Testing de MCP server con FastMCP Client

#### Prioridad - RF-007: Alta

### RF-009: Integration with Ollama

#### Descripción - RF-009

Implementar integración con Ollama para ejecución de LLM Qwen 3.5.

#### Criterios de Aceptación - RF-009

- [ ] Cliente HTTP para comunicarse con API de Ollama
- [ ] Modelo Qwen 3.5 configurado como proveedor LLM
- [ ] Función helper para enviar prompts y recibir respuestas
- [ ] Manejo de timeouts y errores de conexión
- [ ] **Fallback**: Manejo básico de errores sin retry automático, cliente LLM responsable de reintentar tools cuando fallan, SIN fallback a proveedor alternativo (OpenAI/Anthropic) para MVP
- [ ] **Nota**: Parámetros del modelo configurados en Ollama (Hito 1), Hito 2 solo implementa cliente HTTP, valores por defecto de Ollama, solo configurar `OLLAMA_URL`

#### Prioridad - RF-009: Alta

---

## Requisitos No Funcionales

### RNF-001: Performance

#### Criterios - RNF-001

- [ ] Tiempo máximo de respuesta para MCP tools (SLAs p95/p99 para tools principales, monitoreo vía latency_ms en logs)
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
- [ ] Métricas de MCP tools (latencia, throughput, error rate) - monitoreo de latencia vía logs, sin metrics detalladas para MVP (post-MVP)
- [ ] Monitoreo de métricas con Prometheus/Grafana (post-MVP según ADR-002)
- [ ] Distributed tracing (post-MVP según ADR-002)

### RNF-004: Testing

#### Criterios - RNF-004

- [ ] Cobertura objetivo: >90% con pytest (según ADR-002)
- [ ] Unit tests (70-80%): lógica de negocio, services, schemas
- [ ] Integration tests (15-20%): DB real (bases de datos separadas en docker-compose: POSTGRES_TEST_DB, REDIS_TEST_URL)
- [ ] E2E tests (5-10%): flujos completos del pipeline
- [ ] Estrategia de testing de API específica (pytest, bases de datos separadas en docker-compose, FastMCP Client)
- [ ] Testing de MCP servers con FastMCP Client (pytest-asyncio)

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

- ADR-001: MCP como capa de abstracción
- ADR-002: Stack unificado en Python
- ADR-006: Versioning de documentos
- mcp-server-specification.md: Especificación de MCP Server
- mcp-tools-specification.md: Especificación de tools MCP

### Dependencias de Otros Hitos

- Hito 1: Infraestructura Base (dependencia crítica)

---

## Criterios de Completitud del Hito

Basado en technical-roadmap.md, el Hito 2 se considera completo cuando:

- [ ] MCP Server básico funcional con tools principales
- [ ] Integración con Ollama para LLM

### Criterios Adicionales de este TRD

- [ ] Todos los requisitos funcionales (RF-007, RF-009) están cumplidos
- [ ] Testing básico implementado (unit tests)
- [ ] Documentación de MCP tools disponible

---

## Criterio de Éxito

**Objetivo cualitativo**: El MCP Server es funcional para ejecutar el pipeline básico de detección y resolución de gaps.

Justificación: Para el MVP Bootstrapped, el criterio de éxito es funcionalidad básica sobre optimización de performance. Los gaps identificados en requisitos no funcionales (performance, observabilidad avanzada) se resolverán en fases post-MVP según ADR-002.

---

## Riesgos y Mitigación

### Riesgo 1: Complejidad de implementación de MCP Server

**Mitigación**: Usar FastMCP (framework simplificado) según ADR-001. Comenzar con subset de tools críticas (read_document, write_document, create_gap, answer_gap) y expandir posteriormente.

### Riesgo 4: Integración con Ollama tiene latencia alta

**Mitigación**: Ollama ejecuta fuera de Docker (en host o máquina remota) según ADR-003. Usar Tailscale para conexión de baja latencia. Implementar timeouts apropiados y manejo de errores.
