---
id: TRD-021
type: Technical Requirements Document
rating: 9.5
rating-phase: document-editing
related:
  - target: FSP-003
    relationship_type: implements
    reason: Implementa los casos de uso del Hito 2 con requisitos técnicos de API REST
  - target: FSP-004
    relationship_type: implements
    reason: Implementa las reglas de negocio del Hito 2 con requisitos técnicos de API REST
  - target: ADR-002
    relationship_type: depends_on
    reason: Depende de ADR-002 para stack unificado Python (FastAPI)
  - target: ADR-006
    relationship_type: depends_on
    reason: Depende de ADR-006 para versioning de documentos
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para implementación de API
  - target: ARC-005
    relationship_type: implements
    reason: Implementa la especificación de API REST en requisitos funcionales
  - target: ARC-034
    relationship_type: references
    reason: Referencia las convenciones de API
  - target: ARC-035
    relationship_type: references
    reason: Referencia la especificación de endpoints de API
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

# TRD - Hito 2: API REST

## Visión General

### Objetivo del Hito

Implementar la API REST que permita orquestar el pipeline de 5 fases, gestionar documentos, sesiones, gaps y configuración del sistema. Este hito establece la capa de aplicación sobre la infraestructura base configurada en el Hito 1.

### Propósito

Proporcionar la interfaz programática (API REST) que será utilizada por el frontend del sistema. Este hito habilita la ejecución del pipeline de detección, agrupación, resolución, verificación y aplicación de cambios en documentos.

### Justificación de REST vs GraphQL

Se seleccionó REST sobre GraphQL por varias razones técnicas clave. FastAPI genera documentación Swagger/ReDoc automáticamente mediante OpenAPI, lo que facilita la integración y el descubrimiento de la API. Además, REST aprovecha el caching HTTP nativo (ETag, Cache-Control) para mejorar el rendimiento, mientras que Pydantic proporciona validación de tipos robusta en request/response. Finalmente, la simplicidad de debugging con herramientas estándar HTTP (curl, Postman) evita el overhead adicional que introduce GraphQL.

### Referencias

Este hito se fundamenta en varios documentos de arquitectura y decisiones técnicas:

**Roadmap y Estrategia:**
- [technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md): Hito 2 - API REST y MCP Server

**Decisiones Arquitectónicas (ADR):**
- [ADR-002](../decisiones/adr-002-python-unified-stack.md): Stack Unificado en Python (FastAPI + FastMCP)
- [ADR-006](../decisiones/adr-006-document-versioning.md): Versioning de Documentos

**Arquitectura API:**
- [api-specification.md](../arquitectura/api-specification.md): Especificación de la API REST (ARC-005)
- [api-conventions.md](../arquitectura/api-conventions.md): Convenciones de API (ARC-034)
- [api-endpoints-specification.md](../arquitectura/api-endpoints-specification.md): Especificación de Endpoints (ARC-035)

**Arquitectura General:**
- [database-schema-design.md](../arquitectura/database-schema-design.md): Diseño conceptual de schema de PostgreSQL (ARC-004)
- [mcp-server-data-consistency-concurrency.md](../arquitectura/mcp-server-data-consistency-concurrency.md): Consistencia y Concurrency (ARC-037)
- [mcp-server-performance-scalability.md](../arquitectura/mcp-server-performance-scalability.md): Performance y Escalabilidad (ARC-038)
- [mcp-server-observability-monitoring.md](../arquitectura/mcp-server-observability-monitoring.md): Observabilidad y Monitoreo (ARC-039)
- [end-to-end-pipeline.md](../arquitectura/end-to-end-pipeline.md): Flujo end-to-end del pipeline (ARC-002)

**Documentos Relacionados:**
- [trd-milestone-1-infrastructure.md](./trd-milestone-1-infrastructure.md): TRD Hito 1 (rating: 9)
- [trd-milestone-2-mcp-server.md](./trd-milestone-2-mcp-server.md): TRD Hito 2 - MCP Server (TRD-022)
- [trd-milestone-2-integrations.md](./trd-milestone-2-integrations.md): TRD Hito 2 - Integraciones (TRD-023)

---

## Requisitos Funcionales

### RF-001: FastAPI Application Setup

#### Descripción - RF-001

Configurar la aplicación FastAPI con la estructura base, dependencias y configuración para servir la API REST.

#### Criterios de Aceptación - RF-001

- [ ] Aplicación FastAPI configurada con Pydantic 2.12.0 para validación
- [ ] Estructura de proyecto Python organizada (app/, models/, services/, api/)
- [ ] Dependencias instaladas via uv (FastAPI 0.135.0, SQLAlchemy, Alembic, etc.)
- [ ] Configuración de variables de entorno centralizada
- [ ] Comando `uvicorn app.main:app --reload` inicia el servidor de desarrollo
- [ ] Documentación automática de API disponible en `/docs` (Swagger UI)
- [ ] Documentación automática de API disponible en `/redoc` (ReDoc)

#### Prioridad - RF-001: Alta

### RF-002: API REST Endpoints - Documents

#### Descripción - RF-002

Implementar endpoints de la API REST para gestión de documentos (CRUD básico).

#### Criterios de Aceptación - RF-002

- [ ] `POST /api/v1/documents` - Crear documento
- [ ] `GET /api/v1/documents/{id}` - Leer documento
- [ ] `GET /api/v1/documents` - Listar documentos con paginación
- [ ] `PUT /api/v1/documents/{id}` - Actualizar documento
- [ ] `DELETE /api/v1/documents/{id}` - Eliminar documento
- [ ] `GET /api/v1/documents/{id}/snapshots` - Obtener snapshots de documento
- [ ] `POST /api/v1/documents/{id}/snapshots/{snapshot_id}/restore` - Restaurar snapshot
- [ ] Todos los endpoints retornan códigos de status HTTP apropiados
- [ ] Validación de request con Pydantic schemas
- [ ] **Versioning de API**: URLs incluyen versión (v1), estrategia MVP sin cambios breaking, estrategia post-MVP pendiente
- [ ] **Concurrencia**: Pessimistic locking con SELECT FOR UPDATE, backoff exponencial si lock falla

#### Prioridad - RF-002: Alta

### RF-005: API REST Endpoints - Context Entries

#### Descripción - RF-005

Implementar endpoints de la API REST para gestión de context entries (cambios sugeridos).

#### Criterios de Aceptación - RF-005

- [ ] `GET /api/v1/sessions/{id}/context-entries` - Obtener cambios sugeridos
- [ ] `POST /api/v1/context-entries/{id}/approve` - Aprobar cambio
- [ ] **Nota**: Context-entries se aprueban y aplican vía MCP tools, detalles pendientes de implementación en Hito 4

#### Prioridad - RF-005: Media

### RF-006: API REST Endpoints - Users y Organizations

#### Descripción - RF-006

Implementar endpoints de la API REST para gestión de usuarios y organizaciones (básico para Hito 2).

#### Criterios de Aceptación - RF-006

- [ ] `POST /api/v1/users` - Crear usuario
- [ ] `GET /api/v1/users` - Listar usuarios (solo admin)
- [ ] **Gestión de organizaciones**: Tabla `organizations` con campo `is_personal` (TRUE=espacio personal único por usuario, FALSE=organización empresarial), FK a `users` via `created_by`
- [ ] **Gestión de proyectos**: Tabla `projects` con `organization_id` FK, proyectos como contenedores de documentos y configuración (name, slug, description, created_by)

#### Prioridad - RF-006: Media

### RF-011: Database Migrations

#### Descripción - RF-011

Implementar migrations de Alembic para el schema de base de datos definido en database-schema-design.md.

#### Criterios de Aceptación - RF-011

- [ ] Alembic 1.17.0 configurado
- [ ] Migration inicial (001_initial_schema) crea todas las tablas del schema
- [ ] Índices creados según especificación
- [ ] Migrations backwards-compatible con downgrade scripts
- [ ] **Middleware de versioning**: SQLAlchemy event listeners (@event.listens_for), verificación de cambio de contenido, snapshot automático
- [ ] **Nota**: Función helper en código para actualizar updated_at, no triggers de base de datos

#### Prioridad - RF-011: Alta

### RF-012: Authentication and Authorization

#### Descripción - RF-012

Implementar sistema de autenticación y autorización para la API REST.

#### Criterios de Aceptación - RF-012

- [ ] Autenticación JWT Bearer Token implementada (JWT básico sin refresh tokens para MVP, re-autenticación requerida cuando expira, expiración de 1 hora, Bearer token en Authorization header)
- [ ] Endpoint `POST /api/v1/auth/login` para obtener tokens
- [ ] Roles implementados: admin, user, readonly (verificación de permisos por request, sin RBAC granular para MVP)
- [ ] Middleware de autenticación en endpoints protegidos

#### Prioridad - RF-012: Alta

---

## Requisitos No Funcionales

### RNF-001: Performance

#### Criterios - RNF-001

- [ ] Tiempo máximo de respuesta para API endpoints (SLAs p95/p99 para endpoints principales, monitoreo vía latency_ms en logs)
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
- [ ] Métricas de API (latencia, throughput, error rate) - monitoreo de latencia vía logs, sin metrics detalladas para MVP (post-MVP)
- [ ] Monitoreo de métricas con Prometheus/Grafana (post-MVP según ADR-002)
- [ ] Distributed tracing (post-MVP según ADR-002)

### RNF-004: Testing

#### Criterios - RNF-004

- [ ] Cobertura objetivo: >90% con pytest (según ADR-002)
- [ ] Unit tests (70-80%): lógica de negocio, services, schemas
- [ ] Integration tests (15-20%): DB real (testcontainers PostgreSQL, Redis)
- [ ] E2E tests (5-10%): flujos completos del pipeline
- [ ] Estrategia de testing de API específica (pytest, testcontainers, FastMCP Client)
- [ ] Testing de MCP servers con FastMCP Client (pytest-asyncio)

---

## Casos de Uso

### UC-001: Crear Documento y Detectar Gaps

#### Actor - UC-001: Usuario

#### Precondiciones - UC-001

- Infraestructura base operativa (Hito 1)
- Usuario autenticado

#### Flujo Principal - UC-001

1. Usuario crea documento vía `POST /api/v1/documents`
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
- ADR-006: Versioning de documentos
- api-specification.md: Especificación de API REST
- api-conventions.md: Convenciones de API
- api-endpoints-specification.md: Especificación de endpoints

### Dependencias de Otros Hitos

- Hito 1: Infraestructura Base (dependencia crítica)

---

## Criterios de Completitud del Hito

Basado en technical-roadmap.md, el Hito 2 se considera completo cuando:

- [ ] API REST básica funcional (documents)
- [ ] Autenticación básica JWT

### Criterios Adicionales de este TRD

- [ ] Todos los requisitos funcionales (RF-001, RF-002, RF-005, RF-006, RF-011, RF-012) están cumplidos
- [ ] Testing básico implementado (unit tests)
- [ ] Documentación de API disponible (Swagger UI)

---

## Criterio de Éxito

**Objetivo cualitativo**: La API REST es funcional para ejecutar el pipeline básico de detección y resolución de gaps.

Justificación: Para el MVP Bootstrapped, el criterio de éxito es funcionalidad básica sobre optimización de performance. Los gaps identificados en requisitos no funcionales (performance, observabilidad avanzada) se resolverán en fases post-MVP según ADR-002.

---

## Riesgos y Mitigación

### Riesgo 2: Versioning de documentos causa overhead de performance

**Mitigación**: Seguir especificación de ADR-006 con snapshots automáticos. Considerar compresión y retención limitada (90 días) para controlar storage.
