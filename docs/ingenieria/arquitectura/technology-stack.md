---
id: ARC-003
type: Architecture
rating: 9
rating-phase: document-editing
dependency: [STR-003]
related:
  - target: STR-002
    relationship_type: implements
    reason: Implementa la estrategia tecnológica con stack específico de tecnologías
  - target: STR-003
    relationship_type: implements
    reason: Implementa el roadmap técnico definiendo tecnologías por hito
  - target: STR-005
    relationship_type: implements
    reason: Implementa la estrategia de frontend definiendo stack de frontend
  - target: STR-006
    relationship_type: implements
    reason: Implementa la evaluación de LLM definiendo proveedores recomendados
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para definir tecnologías de persistencia
  - target: ARC-024
    relationship_type: implements
    reason: Implementa la configuración de producción post-MVP
---

# Technology Stack — Alejandria

Este documento define el stack tecnológico recomendado para el proyecto Alejandria y los principios técnicos que guían las decisiones arquitectónicas para la fase MVP Bootstrapped.

## Resumen Ejecutivo

El stack tecnológico de Alejandria se basa en Python (FastAPI, Celery, FastMCP) para aprovechar el ecosistema maduro de herramientas LLM/MCP, PostgreSQL para persistencia, Qdrant para búsqueda semántica, Redis como broker y cache, y React para el frontend. MCP (Model Context Protocol) se utiliza como capa de abstracción para comunicación con LLMs, permitiendo cambio de proveedores sin reescribir código.

---

## Stack Tecnológico Recomendado

Con la arquitectura definida en technology-strategy-core.md, esta sección presenta las tecnologías recomendadas para cada componente del sistema. Las elecciones de stack no son arbitrarias: cada tecnología se selecciona basándose en su ecosistema, madurez, y alineación con los principios técnicos del MVP.

### API Backend

#### Python (FastAPI)

- **Versión**: 0.135.0
- **Justificación**: Ver [ADR-002](../decisiones/adr-002-python-unified-stack.md) - Stack unificado en Python
- **Estado**: Decisión tomada - Python (FastAPI) por ecosistema LLM/MCP maduro

### Jobs y Orquestación

#### Python (Celery)

- **Versión**: 5.5.0
- **Decisión específica**: Celery seleccionado sobre RQ por features avanzadas de monitoreo, retry policies, y mejor ecosistema de herramientas (ver ADR-004)
- **Justificación**: Ver [ADR-002](../decisiones/adr-002-python-unified-stack.md) - Stack unificado en Python
- **Justificación jobs efímeros**: Ver [ADR-004](../decisiones/adr-004-ephemeral-jobs.md) - Jobs efímeros vs persistentes
- **Estado**: Decisión tomada - Python (Celery) por integración nativa con stack Python

### MCP Server

#### Python (FastMCP)

- **Versión**: 3.2.0
- **Justificación**: Ver [ADR-002](../decisiones/adr-002-python-unified-stack.md) - Stack unificado en Python
- **Justificación MCP**: Ver [ADR-001](../decisiones/adr-001-mcp-abstraction-layer.md) - MCP como capa de abstracción
- **Estado**: Decisión tomada - Python (FastMCP) por integración nativa con stack Python

### Base de Datos

#### PostgreSQL

- **Versión**: 18.3-bookworm
- **Justificación**: Elección por madurez y consistencia transaccional ACID. Versión sigue criterio "última versión estable menos un minor" para balancear estabilidad con acceso a features recientes. Imagen Debian elegida sobre Alpine para evitar problemas de compatibilidad (Alpine usa musl libc que puede causar incompatibilidades con ciertas dependencias Python, mientras que Debian usa glibc estándar).
- **Estado**: Decisión tomada - PostgreSQL por integridad de datos fuerte

#### Qdrant (Base de Datos Vectorial)

- **Versión**: v1.17.1
- **Justificación**: Para implementar valor de "Contexto Acumulativo" mediante búsqueda semántica. Versión sigue criterio "última versión estable menos un minor" para balancear estabilidad con acceso a features recientes.
- **Estado**: Decisión tomada - Qdrant por búsqueda semántica y despliegue local con Docker

#### Redis (Broker y Cache)

- **Versión**: 7.4.9-bookworm
- **Justificación**: Broker para Celery y caching del sistema. Versión sigue criterio "última versión estable menos un minor" para balancear estabilidad con acceso a features recientes. Imagen Debian elegida sobre Alpine para evitar problemas de compatibilidad (Alpine usa musl libc que puede causar incompatibilidades con ciertas dependencias Python, mientras que Debian usa glibc estándar).
- **Estado**: Decisión tomada - Redis por integración nativa con Celery

#### Migrations con Alembic

- **Versión**: 1.17.0
- **Estrategia**: Migrations backwards-compatible con downgrade scripts
- **Estado**: Decisión tomada - Alembic por integración nativa con stack Python

### Frontend

#### React (opción principal)

- **Versión**: PENDIENTE - Versión específica por definir en fase de implementación
- **Análisis de alternativas**: PENDIENTE - Análisis comparativo con Vue, Svelte, framework-less por definir en fase de implementación. Ver [frontend-strategy.md](../../estrategia/estrategia/frontend-strategy.md) para justificación estratégica de React como opción preliminar.
- **Estado**: Opción principal - React por ecosistema amplio y developer experience

##### Integración con Backend

La integración frontend-backend utiliza REST API como prioridad para operaciones CRUD estándar, con WebSockets limitado a edición de recursos en tiempo real (collaborative editing, real-time updates). FastAPI tiene soporte nativo para ambos protocolos. Este enfoque balancea simplicidad (REST) con funcionalidad específica (WebSockets para edición).

### LLM Providers

#### Qwen 3.5 (proveedor principal para MVP Bootstrapped)

- **Versión**: Qwen 3.5 (ejecutado vía Ollama)
- **Despliegue**: Ollama para desarrollo local
- **Justificación**: Sin costos de API durante desarrollo local, MCP permite cambio de provider fácilmente
- **Estado**: Decisión tomada - Qwen 3.5 en Ollama para MVP Bootstrapped

##### Criterios de Evaluación

Qwen 3.5 fue seleccionado basado en benchmarks y requisitos del proyecto. Los criterios de evaluación incluyen benchmarking formal con métricas específicas (SWE-bench 77.2% para Qwen 3.6 27B, MMLU ~85% para Qwen3 72B), performance local de 25-30 tokens/seg en Apple Silicon (más rápido que lectura humana), balance calidad-tamaño que lo hace ejecutable en hardware de desarrollo típico, licencia Apache 2.0 (true open source sin restricciones comerciales), soporte multilingüe de 29 idiomas nativos (ventaja para futura expansión), y context window de 262K (suficiente dado que archivos son <300 líneas y no se cargará mucho contexto). El contexto masivo de 10M tokens (Llama 4 Scout) no es prioridad para Alejandria, y MCP permite cambio de provider fácilmente si Qwen no funciona bien.

---

## Patrones Arquitectónicos

Esta sección define los patrones arquitectónicos que guían el diseño del sistema.

### Patrones de Diseño

Los patrones de diseño arquitectónico guían las decisiones fundamentales del sistema. Cada patrón seleccionado responde a un requisito específico del MVP Bootstrapped y se documenta en su respectivo ADR para mayor detalle.

- **Jobs efímeros**: Para escalabilidad horizontal y aislamiento de failures (ver ADR-004)
- **Versioning de documentos**: Para reversibilidad de cambios aplicados por agentes LLM (ver ADR-006)
- **Idempotencia de jobs**: Para prevenir duplicación de trabajo y asegurar consistencia (ver ADR-005)
- **MCP como capa de abstracción**: Para flexibilidad en cambio de proveedores LLM (ver ADR-001)

### Patrones de Integración

Los patrones de integración definen cómo interactúan los componentes del sistema. Estos patrones se definirán durante la fase de implementación basándose en los requisitos específicos de cada hito del roadmap.

- **Integración FastAPI con Celery**: Celery workers se ejecutan como procesos separados, Redis como broker para encolado de jobs, API REST encola jobs vía Celery Beat o programático
- **Integración FastMCP con FastAPI**: FastMCP y FastAPI se ejecutan como procesos separados pero no se comunican vía HTTP. Dado que MCP está dentro de la misma infraestructura y tiene acceso al mismo código, puede obtener información y realizar procesos de forma directa. El shared state se maneja vía PostgreSQL y Redis compartidos, permitiendo que FastMCP acceda directamente a datos y código sin overhead de comunicación HTTP (ver ADR-002)
- **Integración Redis como broker y cache**: Redis actúa como broker para Celery (colas de jobs) y como cache del sistema para almacenamiento temporal de datos frecuentes

### Estrategia de Observabilidad

Para MVP Bootstrapped, la estrategia de observabilidad se limita a logging básico sin metrics, tracing ni alerting. MVP Bootstrapped es desarrollo local donde observabilidad completa es overkill. Logging básico es suficiente para debuggear. Metrics, tracing y alerting son relevantes para producción post-MVP y pueden evolucionar a un stack completo cuando se requiera.

---

## Estructura de Proyecto

Esta sección define la estructura de directorios del proyecto y la organización del código base para MVP Bootstrapped.

### Monorepo

El proyecto utiliza un monorepo para MVP Bootstrapped con un desarrollador. Esto permite cambios atómicos entre backend y frontend y evita la coordinación entre múltiples repositorios.

### Estructura Híbrida Capas+Dominios

El código está organizado en capas (core, models, api, jobs, mcp) que separan responsabilidades, con dominios dentro de cada capa que organizan la lógica de negocio. La organización sigue el patrón dominio→capa, donde todo relacionado con un dominio está en un lugar, mejorando escalabilidad y navegación.

### Layout de Directorios

```text
alejandria/
├── backend/
│   ├── src/
│   │   ├── core/              # Capa: Configuración global
│   │   ├── models/            # Capa: Modelos de datos (GLOBAL)
│   │   ├── api/               # Capa: FastAPI endpoints
│   │   │   ├── documents/     # Dominio: documents
│   │   │   └── sessions/      # Dominio: sessions
│   │   ├── jobs/              # Capa: Celery tasks
│   │   │   ├── documents/     # Dominio: documents
│   │   │   └── sessions/      # Dominio: sessions
│   │   └── mcp/               # Capa: FastMCP server
│   │       ├── tools/         # Dominio: tools
│   │       │   ├── documents/
│   │       │   └── sessions/
│   │       └── server.py
│   ├── run.py                 # Script de inicio (api/worker/mcp)
│   └── Dockerfile
└── frontend/                  # React app
```

### Script de Inicio

Un script único `run.py` simplifica el deployment local y la integración con Docker Compose, permitiendo iniciar API, workers, o servidor MCP desde un punto de entrada unificado.

---

## Configuración de Desarrollo vs Producción

Esta sección define las diferencias de configuración entre entornos.

### Desarrollo (MVP Bootstrapped)

El entorno de desarrollo MVP Bootstrapped prioriza simplicidad operacional y control local. Docker Compose orquesta todos los servicios localmente, permitiendo desarrollo sin dependencias externas. Ollama ejecuta Qwen 3.5 localmente para evitar costos de API durante desarrollo. PostgreSQL, Qdrant y Redis se ejecutan en contenedores Docker con configuraciones optimizadas para desarrollo local.

- Docker Compose para orquestación local
- Ollama local para LLM provider (Qwen 3.5)
 PostgreSQL local con pg_dump para backups simples
- Qdrant local con Docker
- Redis local con Docker
- Testing con pytest y cobertura >90%

### Estrategia de Testing

La estrategia de testing utiliza un enfoque híbrido con capas autocontenidas. Cada capa tiene sus propios tests independientes, con mocks hacia otras capas que también están testeadas. Este enfoque permite testing rápido (unit) mientras valida integración real donde es crítico (integration), con E2E limitado a happy paths para evitar fragilidad.

- **Unit tests**: 70-80% de tests, rápidos (<1s cada uno). Prueban lógica de negocio, services, schemas sin dependencias externas.
- **Integration tests**: 15-20% de tests, con DB real (bases de datos separadas en docker-compose). Prueban integración por capa con mocks hacia otras capas.
- **E2E tests**: 5-10% de tests, flujos completos (crear documento → ejecutar job → verificar resultado). Solo happy paths para verificar integración final entre capas.
- **Mocks**: Requests HTTP entre capas, eventos de Redis, llamadas MCP.

### Monitoreo

El monitoreo para MVP Bootstrapped es mínimo sin alerting. Docker Compose logs (`docker-compose logs`) permiten ver el estado de servicios. Health checks básicos en Docker Compose verifican que servicios estén corriendo. No se recolectan métricas (Prometheus, Grafana) ni se configuran alertas para desarrollo local. MVP Bootstrapped es desarrollo local donde el desarrollador puede monitorear manualmente. Docker Compose logs son suficientes para debuggear y ver estado de servicios. Health checks básicos aseguran disponibilidad. Metrics y alerting son overkill para desarrollo local y se definirán post-MVP.

### Log Aggregation

El log aggregation para MVP Bootstrapped es mínimo sin centralización. No se usan herramientas como ELK o Loki. Docker Compose logs (`docker-compose logs`) permiten ver logs de todos los servicios. El logging estándar Python ya está definido previamente (JSON structured logging con request IDs). No hay retención específica; logs se manejan por defecto de Docker Compose. MVP Bootstrapped es desarrollo local donde el desarrollador puede ver logs directamente. Docker Compose logs centralizan logs de todos los servicios localmente. Logging estructurado con request IDs permite correlación manual. Estrategia completa de log aggregation se definirá post-MVP.

### Producción (Post-MVP)

- PENDIENTE - Configuración de producción por definir tras validación de problem-solution fit
- Consideraciones: Nomad/Kubernetes para orquestación, proveedores comerciales LLM, backups automatizados, monitoreo centralizado

---

## Requisitos de Recursos

Esta sección define los requisitos mínimos de recursos por componente para MVP Bootstrapped (desarrollo local).

### Especificación de Recursos

- **Ollama (Qwen 3.5 8B)**: 16GB RAM (CPU inference) o 8GB VRAM (GPU)
- **PostgreSQL**: 1GB RAM, 1 CPU, 10GB disco
- **Qdrant**: 1GB RAM, 1 CPU, 5GB disco (MMAP mode para desarrollo)
- **Redis**: 512MB RAM, 0.5 CPU, 1GB disco
- **FastAPI**: 512MB RAM, 1 CPU
- **Celery workers**: 512MB RAM, 1 CPU por worker (iniciar con 1 worker)

### Razonamiento

Qwen 3.5 8B fue seleccionado sobre 32B por accesibilidad de hardware (16GB vs 32GB requerido). Benchmarks muestran que Qwen 3.5 8B compite favorablemente con modelos mucho más grandes. PostgreSQL requiere 1GB RAM suficiente para desarrollo con configuración optimizada. Qdrant puede operar con límite de 1GB RAM usando MMAP según benchmarks oficiales. Redis requiere 512MB suficiente para broker/cache en desarrollo. FastAPI y Celery requieren 512MB por proceso razonable para API típica sin carga pesada. El total estimado es ~19-20GB RAM para desarrollo local completo.

---

## Principios Técnicos del MVP

Esta sección define los principios técnicos que guían las decisiones arquitectónicas y de stack para la fase MVP Bootstrapped.

### Non-negotiables para MVP

Estos principios son requisitos fundamentales que no pueden comprometerse en la fase MVP Bootstrapped. Cada non-negotiable responde a un riesgo crítico del sistema y se documenta en su respectivo ADR.

- **MCP como capa de abstracción**: Para flexibilidad futura en cambio de proveedores LLM (ver ADR-001)
- **Idempotencia de jobs**: Prevención de duplicación de trabajo y errores en procesamiento (ver ADR-005)
- **Versioning de documentos**: Reversibilidad de cambios aplicados por agentes LLM (ver ADR-006)

### Trade-offs Aceptables para MVP

Estos trade-offs representan decisiones conscientes donde sacrificamos un aspecto para ganar otro más crítico para la fase MVP Bootstrapped. Cada trade-off se justifica por el contexto de recursos limitados y validación inicial.

- **Complejidad arquitectónica por flexibilidad**: MCP desde el inicio añade complejidad pero evita costoso refactor futuro
- **Performance por simplicidad operacional**: Docker Compose y Ollama local priorizan simplicidad sobre performance óptima
- **Costo de desarrollo por calidad**: TDD con 90%+ cobertura requiere más tiempo inicial pero asegura confiabilidad

**Nota**: Estos principios aplican específicamente a la fase MVP Bootstrapped actual. Principios para fase post MVP se definirán tras validación de problem-solution fit.

---

## Modelo de Seguridad

Esta sección define el modelo de seguridad del stack para MVP Bootstrapped y la clasificación de medidas de seguridad entre MVP y post-MVP.

### Autenticación y Autorización

- **Autenticación**: JWT con OAuth2 para MVP Bootstrapped
  - Razonamiento: FastAPI tiene soporte nativo excelente, stateless se alinea con arquitectura de microservicios futura, estándar de industria
- **Autorización**: Sin modelo de roles - todo público en MVP Bootstrapped
  - Razonamiento: MVP Bootstrapped es fase de validación inicial, simplifica desarrollo, autorización puede implementarse post-MVP

### Encryption

- **TLS obligatorio**: HTTPS es non-negotiable para comunicación HTTP
- **Sin encryption at rest**: No se implementa encryption at rest para MVP Bootstrapped
  - Razonamiento: Añade complejidad sin beneficio inmediato para desarrollo local

### MCP/LLM Security

- **Sin API keys ni rate limiting**: Instancia local Ollama no requiere API keys
  - Razonamiento: Ollama local reduce riesgo de abuso externo, se implementará en fase posterior

### Clasificación MVP vs Post-MVP

Las medidas de seguridad se clasifican entre requisitos no negociables para MVP Bootstrapped y mejoras post-MVP. Esta clasificación refleja el trade-off entre seguridad mínima aceptable y complejidad operacional en fase de validación.

**Non-negotiable para MVP**:

- TLS/HTTPS para toda comunicación
- Validación de inputs (Pydantic)
- Sanitización de datos enviados a LLMs
- Environment variables para configuración sensible

**Post-MVP** (por definir tras validación de problem-solution fit):

- Encryption at rest
- Secrets manager (Vault, AWS Secrets Manager)
- Rate limiting
- MFA (Multi-Factor Authentication)
- RBAC granular (Role-Based Access Control)
- API keys externas para LLM providers
- Auditoría de seguridad

---

## Definiciones de Terminología Clave

**Qdrant**: Base de datos vectorial open-source especializada en búsqueda semántica. Almacena embeddings de texto y permite búsqueda por similitud semántica. Se usa en Alejandria para implementar el valor de "Contexto Acumulativo" mediante búsqueda y reutilización de respuestas previas.

**FastMCP**: Framework Python que simplifica la implementación de servidores MCP. Proporciona abstracciones de alto nivel para crear tools y resources MCP con menos código boilerplate que MCP estándar. Para detalles completos, ver [ADR-001](../decisiones/adr-001-mcp-abstraction-layer.md).

**Alembic**: Herramienta de migrations de base de datos para Python. Permite versionar cambios de schema de base de datos, aplicar upgrades y downgrades de forma controlada. Se usa con PostgreSQL para gestionar evolución del schema.

**Pydantic**: Biblioteca Python para validación de datos y type safety. Se integra con FastAPI para validación automática de requests y responses, asegurando que los datos cumplan con los esquemas definidos.

---

## Referencias a Documentos Relacionados

Este documento es parte de la estrategia tecnológica de Alejandria. Para una comprensión completa, consulte también:

- **[../../estrategia/estrategia/technology-strategy.md](../../estrategia/estrategia/technology-strategy.md)**: Estrategia tecnológica de alto nivel y arquitectura general
- **[architecture-overview.md](architecture-overview.md)**: Decisiones de diseño arquitectónico clave
- **[../decisiones/adr-001-mcp-abstraction-layer.md](../decisiones/adr-001-mcp-abstraction-layer.md)**: MCP como capa de abstracción
- **[../decisiones/adr-002-5-phase-architecture.md](../decisiones/adr-002-5-phase-architecture.md)**: Arquitectura de 5 fases
- **[../decisiones/adr-002-python-unified-stack.md](../decisiones/adr-002-python-unified-stack.md)**: Stack unificado en Python
- **[../decisiones/adr-004-ephemeral-jobs.md](../decisiones/adr-004-ephemeral-jobs.md)**: Jobs efímeros vs persistentes
- **[../decisiones/adr-006-document-versioning.md](../decisiones/adr-006-document-versioning.md)**: Versioning de documentos
- **[../decisiones/adr-005-job-idempotency.md](../decisiones/adr-005-job-idempotency.md)**: Idempotencia de jobs
- **[../../estrategia/estrategia/technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md)**: Roadmap técnico de implementación
- **[../../estrategia/estrategia/vision-mission.md](../../estrategia/estrategia/vision-mission.md)**: Vision and Mission Statement con propósito estratégico y valores organizacionales
- **[production-configuration.md](production-configuration.md)**: Configuración de producción post-MVP
