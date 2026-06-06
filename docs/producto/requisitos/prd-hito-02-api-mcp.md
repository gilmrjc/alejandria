---
id: PRD-002
type: PRD
rating: 9.2
rating-phase: document-editing
related:
  - target: STR-003
    relationship_type: implements
    reason: Implementa el roadmap técnico definiendo el Hito 2 de API REST y MCP Server
  - target: FSP-003
    relationship_type: implements
    reason: Implementa los casos de uso del Hito 2
  - target: FSP-004
    relationship_type: implements
    reason: Implementa las reglas de negocio del Hito 2
  - target: TRD-021
    relationship_type: implements
    reason: Implementa el TRD de Hito 2 con API REST
  - target: TRD-022
    relationship_type: implements
    reason: Implementa el TRD de Hito 2 con MCP Server
  - target: TRD-023
    relationship_type: implements
    reason: Implementa el TRD de Hito 2 con integraciones
  - target: ARC-005
    relationship_type: implements
    reason: Implementa la especificación de API REST
  - target: ARC-030
    relationship_type: implements
    reason: Implementa la especificación de MCP Server
  - target: ARC-033
    relationship_type: references
    reason: Referencia la implementación de búsqueda semántica para chunking y embeddings
---

# PRD: Hito 2 - API REST y MCP Server — Alejandria

Este documento define los requisitos del producto para el Hito 2: API REST y MCP Server del MVP Bootstrapped.

---

## Índice

1. [Visión General](#1-visión-general)
2. [Objetivo del Hito](#2-objetivo-del-hito)
3. [Componentes del Hito](#3-componentes-del-hito)
4. [Requisitos Funcionales](#4-requisitos-funcionales)
5. [Requisitos No Funcionales](#5-requisitos-no-funcionales)
6. [Criterios de Aceptación](#6-criterios-de-aceptación)
7. [Dependencias](#7-dependencias)

---

## 1. Visión General

**Propósito:**

Implementar la capa de aplicación que proporciona la interfaz programática (API REST) y la capa de abstracción para LLMs (MCP Server) necesarias para ejecutar el pipeline de 5 fases de Alejandria. Este hito transforma la infraestructura base configurada en el Hito 1 en una plataforma funcional capaz de procesar documentos, detectar gaps, facilitar sesiones de resolución y aplicar cambios sugeridos.

**Contexto:**

Este hito representa el corazón técnico de Alejandria, donde se implementan los componentes que orquestan el flujo de trabajo principal del sistema. La API REST sirve como interfaz para el frontend y clientes externos, mientras que el MCP Server proporciona la abstracción estandarizada que permite a los agentes LLM interactuar con el sistema sin dependencia de proveedores específicos. La combinación de estos componentes habilita la ejecución automatizada del pipeline de detección, agrupación, resolución, verificación y aplicación de cambios, que es el valor central de Alejandria.

---

## 2. Objetivo del Hito

**Objetivo Principal:**

Implementar API REST y MCP Server funcional que permita:

- Gestión de documentos (CRUD básico)
- Ejecución del pipeline de 5 fases
- Gestión de sesiones y gaps
- Integración con LLM (Ollama)
- Integración con búsqueda semántica (Qdrant)
- Autenticación JWT básica (sin refresh tokens ni RBAC detallado)

**Valor:**

Establecer la capa de aplicación que hace posible la ejecución del valor central de Alejandria: detección automática de gaps en documentación y facilitación de su resolución. Este hito transforma la infraestructura estática del Hito 1 en una plataforma dinámica capaz de procesar documentos, interactuar con LLMs y orquestar flujos de trabajo complejos. La implementación de MCP como capa de abstracción asegura flexibilidad futura para cambiar de proveedores LLM sin reescribir código, reduciendo vendor lock-in y permitiendo evolución tecnológica sin interrupciones.

---

## 3. Componentes del Hito

### 3.1 API REST

**Descripción:**

La API REST proporciona endpoints para gestión de documentos, sesiones, gaps, usuarios y organizaciones. La API sirve como interfaz principal para el frontend React y para integraciones externas. Para detalles técnicos de implementación, ver [ADR-002](../../ingenieria/decisiones/adr-002-python-unified-stack.md) y [ARC-005](../../ingenieria/arquitectura/api-specification.md).

**Requisitos:**

La API REST debe proporcionar endpoints completos para gestión de documentos (CRUD y snapshots), context entries para cambios sugeridos, y gestión básica de usuarios y organizaciones. La autenticación se implementa mediante JWT Bearer Token en su forma básica para MVP bootstrapped. Para detalles técnicos de implementación, ver documentos de arquitectura referenciados.

### 3.2 MCP Server

**Descripción:**

El MCP Server proporciona tools que los agentes LLM usan para interactuar con el sistema. MCP (Model Context Protocol) es un estándar abierto que permite cambio de proveedores LLM sin reescribir código, implementando directamente el principio estratégico de "complementar LLMs, no competir contra ellos". El MCP Server actúa como capa de abstracción entre los agentes y el sistema, proporcionando una interfaz unificada para operaciones como leer documentos, crear gaps, responder preguntas y aplicar cambios. Para detalles técnicos de implementación, ver [ADR-001](../../ingenieria/decisiones/adr-001-mcp-abstraction-layer.md) y [ARC-030](../../ingenieria/arquitectura/mcp-server-architecture.md).

**Requisitos:**

El MCP Server debe proporcionar tools principales para interactuar con entidades base: read_document, write_document, list_gaps, create_gap, answer_gap, create_proposal, apply_proposal, search_similar_documents, entre otros. Para MVP bootstrapped el transporte stdio es suficiente para desarrollo local. Para detalles de transporte HTTP y estrategia de integración, ver [ARC-030](../../ingenieria/arquitectura/mcp-server-architecture.md).

### 3.3 Integración con Ollama

**Descripción:**

La integración con Ollama permite ejecutar el modelo Qwen 3.5 localmente como proveedor LLM. Esta configuración proporciona privacidad, latencia baja y control sobre el modelo. Para detalles técnicos de implementación, ver [ADR-003](../../ingenieria/decisiones/adr-003-ollama-tailscale.md).

**Requisitos:**

- Cliente HTTP para comunicación con API de Ollama
- Modelo Qwen 3.5 configurado
- Función helper para enviar prompts y recibir respuestas
- Manejo de timeouts y errores de conexión
- Estrategia de fallback básica para MVP bootstrapped

### 3.5 Integración con Qdrant

**Descripción:**

La integración con Qdrant habilita búsqueda semántica y almacenamiento de embeddings. Esta capacidad es fundamental para funcionalidades como búsqueda inteligente de preguntas y agrupación de contenido similar. Para detalles técnicos de implementación, ver [ARC-033](../../ingenieria/arquitectura/semantic-search-implementation.md).

**Requisitos:**

- Cliente HTTP para comunicación con API de Qdrant
- Funciones para crear colecciones, insertar vectores, buscar por similitud
- Integración con modelo de embeddings BGE-M3
- Estrategia de chunking y actualización de vectores

### 3.6 Sistema de Usuarios y Organizaciones

**Descripción:**

El sistema de usuarios y organizaciones permite gestión de cuentas con estructura similar a GitHub (organizaciones personales y organizacionales). Este componente es crítico para multi-tenancy y aislamiento de datos. Para detalles técnicos de implementación, ver [database-schema-design.md](../../ingenieria/arquitectura/database-schema-design.md) y [FEAT-001](../../producto/funcionalidades/sistema-usuarios-organizaciones.md).

**Requisitos:**

- Registro de usuarios con email y contraseña
- Organización personal generada automáticamente al crear cuenta
- Organizaciones organizacionales opcionales
- Proyectos dentro de organizaciones
- Autenticación JWT básica para MVP bootstrapped (sin refresh tokens)
- Autorización básica para MVP bootstrapped (sin sistema RBAC detallado)

---

## 4. Requisitos Funcionales

### 4.1 Gestión de Documentos

La gestión de documentos es fundamental para el pipeline de Alejandria. Los documentos son la entidad principal sobre la cual opera el sistema de detección y resolución de gaps. La API REST debe proporcionar endpoints CRUD completos, mientras que el MCP Server debe proporcionar tools para que los agentes LLM puedan leer y escribir documentos. El versioning automático según ADR-006 asegura que todos los cambios sean reversibles.

**Requisitos:**

La API REST debe proporcionar endpoints completos para gestión de documentos: POST, GET, PUT, DELETE, además de endpoints para obtener snapshots y restaurar versiones anteriores. El MCP Server debe proporcionar tools read_document y write_document para que los agentes LLM puedan interactuar con documentos. Se debe implementar versioning automático antes de cada UPDATE según ADR-006. La capacidad de rollback debe permitir restaurar cualquier versión anterior de un documento mediante un endpoint específico, garantizando integridad de datos y reversibilidad de cambios.

### 4.2 Pipeline de 5 Fases

El pipeline de 5 fases es el flujo de trabajo central de Alejandria: detección → agrupación → resolución → verificación → aplicación. Para MVP bootstrapped, el pipeline se ejecuta vía MCP Server sin gestión de sesiones en la API REST. La implementación completa del pipeline con gestión de sesiones se realizará en hitos posteriores.

**Requisitos:**

- MCP Server: Ejecutar tools de detección, agrupación, resolución, verificación y aplicación
- Lógica de transición de estados: Para MVP bootstrapped, el pipeline se ejecuta vía MCP Server sin gestión de sesiones en la API REST. La implementación completa de lógica de transición de estados del pipeline se realizará en hitos posteriores cuando se implemente el sistema de gestión de sesiones.
- Encolado automático de jobs: Para MVP bootstrapped, no se implementa encolado automático de jobs al cambiar estados. Esta funcionalidad se implementará en el Hito 4 cuando se implemente el sistema de jobs (Celery).
- Agrupación de gaps por temas afines: Para MVP bootstrapped, no se implementa agrupación automática de gaps por temas afines (tags). Esta funcionalidad se implementará en hitos posteriores cuando se desarrolle la fase de agrupación del pipeline.

### 4.3 Autenticación y Autorización

La autenticación y autorización son críticas para seguridad y multi-tenancy. Para MVP bootstrapped, se implementa autenticación JWT básica sin refresh tokens ni sistema RBAC detallado. Todos los usuarios autenticados tienen los mismos permisos. El sistema de usuarios y organizaciones se implementa pero sin aislamiento de datos por organización en MVP.

**Requisitos:**

- API REST: Endpoint login para obtener tokens JWT
- API REST: Middleware de autenticación en endpoints protegidos
- Access tokens con expiración de 8 horas
- **NO APLICA**: Refresh tokens para renovación (post-MVP)
- **NO APLICA**: Sistema RBAC detallado con permisos granulares (post-MVP)
- **NO APLICA**: Aislamiento de datos por organización (post-MVP)

---

## 5. Requisitos No Funcionales

### 5.1 Performance

Los requisitos de performance para el Hito 2 se enfocan en funcionalidad básica sobre optimización prematura. Según ADR-002, el MVP Bootstrapped tiene carga esperada de <10 documentos/día, <10 req/s, lo cual está bien dentro de la capacidad de FastAPI (~15,000-20,000 req/s). Requisitos específicos de performance se definirán post-MVP.

**Requisitos:**

Para MVP bootstrapped, el enfoque es funcionalidad básica sobre optimización prematura según ADR-002. La carga esperada es <10 documentos/día y <10 req/s, lo cual está bien dentro de la capacidad de FastAPI (~15,000-20,000 req/s). Los requisitos específicos de performance como tiempo máximo de respuesta para API endpoints, tiempo máximo de ejecución por fase del pipeline, número máximo de documentos procesados concurrentemente, y número máximo de sesiones simultáneas no están especificados para MVP y se definirán post-MVP. La latencia debe ser aceptable para desarrollo local.

### 5.2 Seguridad

La seguridad es crítica para un sistema que gestiona documentación y permite ediciones automáticas. La validación de input, sanitización de datos y encriptación son fundamentales para prevenir vulnerabilidades. El sistema de autenticación y autorización debe ser robusto.

**Requisitos:**

La validación de input y sanitización para prevenir inyección SQL y XSS se implementará usando Pydantic 2.12.0 para validación automática de tipos y formatos en todos los endpoints, y SQLAlchemy ORM con parameterized queries previene inyección SQL automáticamente. La encriptación de datos en reposo y en tránsito, así como la política de retención de datos, se definirán post-MVP. Los passwords deben almacenarse como hash (no texto plano) y la autenticación se implementa mediante JWT Bearer Token.

### 5.3 Observabilidad

La observabilidad permite monitorear la salud del sistema y debuggear problemas. Según ADR-002, el MVP Bootstrapped tiene observabilidad mínima (logging estructurado JSON con request IDs, log aggregation vía Docker Compose logs, health checks básicos). Observabilidad completa (metrics, distributed tracing, alerting) es post-MVP.

**Requisitos:**

Para MVP bootstrapped, la observabilidad mínima incluye logging estructurado JSON con request IDs, log aggregation vía Docker Compose logs, y health checks básicos para verificar disponibilidad de servicios. Las métricas de API (latencia, throughput, error rate), monitoreo con Prometheus/Grafana, y distributed tracing se implementarán post-MVP cuando se valide el ajuste problema-solución.

### 5.4 Testing

El testing es crítico para asegurar calidad del código. Según ADR-002, el objetivo es >90% cobertura con pytest, con unit tests (70-80%), integration tests (15-20%) y E2E tests (5-10%). Testing de MCP servers y jobs asíncronos requiere estrategias específicas.

**Requisitos:**

- Cobertura objetivo: >90% con pytest
- Unit tests: lógica de negocio, services, schemas
- Integration tests: DB real (bases de datos separadas en docker-compose: POSTGRES_TEST_DB, REDIS_TEST_URL)
- E2E tests: flujos completos del pipeline
- Estrategia de testing específica para API, jobs asíncronos y MCP servers (ver TRD-021, TRD-022, TRD-023 para detalles técnicos de implementación)

### 5.5 Mantenibilidad

La mantenibilidad es crítica para reducir fricción en el trabajo y facilitar onboarding de nuevos miembros del equipo. La documentación clara, estructura de código organizada y convenciones consistentes son fundamentales.

**Requisitos:**

- Documentación de API automática (Swagger UI en `/docs`)
- Estructura de proyecto Python organizada (app/, models/, services/, api/)
- Convenciones de código consistentes
- README con instrucciones de setup y desarrollo

---

## 6. Criterios de Aceptación

Los criterios de aceptación definen las condiciones que deben cumplirse para considerar el Hito 2 como completado. Estos criterios se dividen en criterios de completitud del roadmap (funcionalidad técnica) y criterios adicionales (calidad y usabilidad).

**Criterios de Completitud (del roadmap):**

- [ ] API REST básica funcional (documents)
- [ ] MCP Server básico funcional con tools principales
- [ ] Integración con Ollama para LLM
- [ ] Integración con Qdrant para búsqueda semántica básica
- [ ] Autenticación JWT básica (access tokens, sin refresh tokens)

**Criterios Adicionales:**

Estos criterios complementan la funcionalidad técnica con aspectos de calidad y robustez. La documentación clara es fundamental para que desarrolladores puedan entender y extender el sistema. El testing básico asegura que el código funcione correctamente y reduce riesgo de regresiones. El manejo de errores robusto asegura que el sistema degrade gracefully cuando fallan componentes externos.

- [ ] Documentación de API disponible (Swagger UI)
- [ ] Testing básico implementado (unit tests con >70% cobertura)
- [ ] Manejo de errores robusto en integraciones externas
- [ ] Logging estructurado implementado
- [ ] Gaps identificados documentados para resolución posterior

---

## 7. Dependencias

Las dependencias del Hito 2 se dividen en externas (herramientas y servicios) e internas (otros hitos o componentes del proyecto). Este hito depende críticamente del Hito 1, que proporciona la infraestructura base necesaria.

**Dependencias Externas:**

- Python 3.11+
- uv para gestión de dependencias
- Infraestructura base (Hito 1): PostgreSQL, Redis, Qdrant, Ollama
- Docker Desktop para orquestación de servicios

**Dependencias Internas:**

- Hito 1: Infraestructura Base (dependencia crítica)
- database-schema.md: Schema de base de datos (rating: 9)
- ADR-001: MCP como capa de abstracción (rating: 9)
- ADR-002: Stack unificado en Python (rating: 9)
- ADR-004: Jobs efímeros (sin rating)
- ADR-005: Idempotencia de jobs (sin rating)
- ADR-006: Versioning de documentos (sin rating)
- mcp-server-architecture.md: Arquitectura de MCP Server (rating: 8)
- mcp-tools-specification.md: Tools de MCP (rating: 8)
- mcp-deployment-testing.md: Deployment y Testing de MCP (rating: 8)
- api-specification.md: Especificación de API REST (sin rating)

**Hitos Posteriores que Dependen de Este Hito:**

La API REST y MCP Server implementados en este hito son prerrequisitos para todos los hitos subsiguientes que implementan funcionalidades del sistema. Hito 3 (Frontend React) depende de la API REST para todas las operaciones. Hito 4 (Implementación de Fases Detección y Agrupación) depende del MCP Server y sistema de jobs (implementado en Hito 4) para ejecución del pipeline.

- Hito 3: Frontend React (depende de API REST)
- Hito 4: Implementación de Fases Detección y Agrupación (depende de MCP Server y Jobs)
- Todos los hitos subsiguientes dependen de esta capa de aplicación

---

## Referencias

- [STR-003](../../estrategia/estrategia/technical-roadmap.md): Technical Roadmap (Hito 2)
- [TRD-021](../../ingenieria/propuestas/trd-milestone-2-api-rest.md): TRD Hito 2 - API REST
- [TRD-022](../../ingenieria/propuestas/trd-milestone-2-mcp-server.md): TRD Hito 2 - MCP Server
- [TRD-023](../../ingenieria/propuestas/trd-milestone-2-integrations.md): TRD Hito 2 - Integraciones
- [ARC-005](../../ingenieria/arquitectura/api-specification.md): API Specification (sin rating)
- [ARC-030](../../ingenieria/arquitectura/mcp-server-architecture.md): MCP Server Architecture (rating: 8)
- [ARC-004](../../ingenieria/arquitectura/database-schema-design.md): Database Schema Design (rating: 9)
- [ENG-DEC-001](../../ingenieria/decisiones/adr-001-mcp-abstraction-layer.md): ADR-001 (rating: 9)
- [ENG-DEC-002](../../ingenieria/decisiones/adr-002-python-unified-stack.md): ADR-002 (rating: 9)
- [FEAT-001](../funcionalidades/sistema-usuarios-organizaciones.md): Sistema de Usuarios y Organizaciones (calificación: 3/10)
- [FEAT-007](../funcionalidades/busqueda-semantica.md): Búsqueda Semántica (calificación: 4/10)
