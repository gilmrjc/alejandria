---
id: STR-003
type: Strategy
rating: 9
rating-phase: document-critique
related:
  - target: STR-002
    relationship_type: implements
    reason: Implementa la estrategia tecnológica definiendo el roadmap de hitos secuenciales
  - target: STR-005
    relationship_type: references
    reason: Referencia la estrategia de frontend para Hito 3
  - target: STR-004
    relationship_type: references
    reason: Referencia la evaluación de LLM para decisiones de proveedores
  - target: POL-001
    relationship_type: references
    reason: Referencia la política de dogfooding para estrategia de validación
  - target: ARC-011
    relationship_type: references
    reason: Referencia el architecture overview para decisiones de diseño arquitectónico
  - target: EPC-001
    relationship_type: implements
    reason: Implementa la épica de infraestructura base para Hito 1
  - target: EPC-002
    relationship_type: implements
    reason: Implementa la épica de API REST y MCP Server para Hito 2
  - target: EPC-003
    relationship_type: implements
    reason: Implementa la épica de frontend React para Hito 3
  - target: EPC-004
    relationship_type: implements
    reason: Implementa la épica de detección y agrupación para Hito 4
  - target: EPC-005
    relationship_type: implements
    reason: Implementa la épica de resolución y verificación para Hito 5
  - target: EPC-006
    relationship_type: implements
    reason: Implementa la épica de aplicación para Hito 6
  - target: EPC-007
    relationship_type: implements
    reason: Implementa la épica de integraciones para Hito 7
    reason: Referencia el architecture overview para decisiones de diseño arquitectónico
  - target: ARC-001
    relationship_type: references
    reason: Referencia el technical brief para descripción de arquitectura del sistema
  - target: ARC-012
    relationship_type: references
    reason: Referencia el api-architecture para arquitectura de API
  - target: ARC-016
    relationship_type: references
    reason: Referencia el database para configuración de base de datos
  - target: ARC-017
    relationship_type: references
    reason: Referencia el debugging para procedimientos de debugging
---

# Technical Roadmap — Alejandria

Este documento define el roadmap técnico para implementar el ciclo de 5 fases del sistema Alejandria. A diferencia de roadmaps tradicionales basados en fechas, este roadmap se basa en funcionalidades priorizadas según necesidad.

## Resumen Ejecutivo

El roadmap técnico define 7 hitos secuenciales para implementar el ciclo de 5 fases en la Fase MVP Bootstrapped. Cada hito tiene criterios de completitud y dependencias con hitos anteriores. Funcionalidades post MVP se definirán tras validación de problem-solution fit.

---

## Contexto del Roadmap

Con la arquitectura y decisiones de diseño establecidas en technology-strategy.md y [../../ingenieria/decisiones/design-decisions.md](../../ingenieria/decisiones/design-decisions.md), este roadmap define las funcionalidades requeridas para implementar el ciclo de 5 fases. Las funcionalidades se implementan según necesidad y prioridad, con revisión obligatoria a 12 meses según vision-mission.md. Este enfoque es apropiado para una fase MVP Bootstrapped donde los recursos son limitados y la validación de problem-solution fit es prioritaria.

## Estructura del Roadmap por Fase de Desarrollo

Este roadmap se enfoca exclusivamente en la **Fase MVP Bootstrapped (Actual)**: funcionalidades esenciales que se implementarán con recursos disponibles (fundador unipersonal, sin inversión externa). Funcionalidades post MVP (integraciones enterprise, búsqueda semántica avanzada, multi-tenant, compliance SOC2/HIPAA) se definirán tras validación de problem-solution fit.

**Principio**: Este roadmap es una guía de alto nivel que muestra hitos, capacidades agregadas y dependencias. Detalles técnicos (implementación específica, estrategia de testing, análisis de riesgos, tiempos estimados, procesos de transición) pertenecen a documentos específicos (PRDs, arquitectura, especificaciones técnicas).

---

## Hitos de Implementación - MVP Bootstrapped

Estos hitos secuenciales implementan el ciclo de 5 fases con recursos MVP Bootstrapped. Cada hito depende de la completitud del hito anterior. La progresión sigue una lógica de capas: infraestructura base (Hito 1) → comunicación con LLMs (Hito 2) → interfaz de usuario (Hito 3) → implementación del workflow central (Hitos 4-6) → integraciones externas (Hito 7). Este orden permite validación temprana de UX mientras se construye el core del sistema, asegura que cada fase del workflow tenga su infraestructura lista antes de implementarse, y mantiene dependencias lógicas donde componentes posteriores dependen de anteriores.

### Hito 1: Infraestructura Base

**Objetivo**: Configurar infraestructura base para desarrollo local

**Componentes**:

- Docker Compose para orquestación local
- PostgreSQL local con schema inicial
- Redis local para broker y cache
- Qdrant local para búsqueda semántica
- Ollama local con Qwen 3.5

**Nota**: Qdrant se configura en Hito 1 como infraestructura base porque se necesita en Hito 2 para la Sección de Preguntas (transformación de respuestas a vectores) y en Hito 4 para búsqueda semántica. Configurarlo desde el inicio asegura que la infraestructura de base de datos vectorial esté lista cuando se necesite en cualquier fase del workflow.

**Features Asociados**:

- [FEAT-007: Búsqueda Semántica](../../producto/funcionalidades/busqueda-semantica.md) - Base de datos vectorial Qdrant

**Criterios de Completitud**:

- Docker Compose levanta todos los servicios sin errores
- PostgreSQL acepta conexiones y tiene schema versionado
- Redis acepta conexiones como broker
- Qdrant acepta conexiones y permite crear colecciones
- Ollama responde a prompts con Qwen 3.5

**Dependencias**: Ninguna (hito inicial)

---

### Hito 2: API REST y MCP Server Básico

**Objetivo**: Implementar API REST y MCP Server para comunicación con LLMs

**Componentes**:

- FastAPI con endpoints básicos
- MCP Server implementado con FastMCP (sincrónico para MVP bootstrapped)
- Integración con Ollama (Qwen 3.5)

**Nota**: MCP (Model Context Protocol) Server es una capa de abstracción que estandariza la comunicación entre aplicaciones y modelos de lenguaje. Permite cambiar de proveedor de LLM sin modificar el código, habilita agentes externos, y aunque añade complejidad inicial, el costo de cambio futuro sería más costoso si se integrara directamente con un solo proveedor.

**Nota**: Para MVP bootstrapped, el MCP Server se implementa de forma sincrónica. El sistema de jobs asíncronos (Celery) se implementará en Hito 4 cuando se requiera ejecución de tareas pesadas de LLM (gap_detection, verification, application).

**Features Asociados**:

- [FEAT-001: Sistema de Usuarios y Organizaciones](../../producto/funcionalidades/sistema-usuarios-organizaciones.md) - Autenticación y gestión de usuarios/organizaciones
- [FEAT-007: Búsqueda Semántica](../../producto/funcionalidades/busqueda-semantica.md) - Motor de búsqueda semántica

**Criterios de Completitud**:

- API REST responde a requests de health check
- MCP Server expone tools básicas para comunicación con LLM
- Integración con Ollama funciona correctamente

**Dependencias**: Hito 1 (Infraestructura Base)

---

### Hito 3: Frontend React

**Objetivo**: Implementar frontend React para interfaz de usuario

**Componentes**:

- SPA React con componentes principales
- Dashboard de documentos y gaps
- Interfaz de sesión interactiva
- Diff viewer integrado

**Features Asociados**:

- [FEAT-009: Dashboard General](../../producto/funcionalidades/dashboard-general.md) - Vista de alto nivel y navegación
- [FEAT-008: Diff Viewer](../../producto/funcionalidades/diff-viewer.md) - Comparación visual de cambios
- [Sección de Documentos](../../producto/funcionalidades/seccion-documentos.md) - Vista de documentos
- [Sección de Preguntas](../../producto/funcionalidades/seccion-preguntas.md) - Vista de preguntas
- [Sección de Gaps](../../producto/funcionalidades/seccion-gaps.md) - Vista de gaps
- [Sección de Propuestas](../../producto/funcionalidades/seccion-propuestas.md) - Vista de propuestas
- [FEAT-004: Sección de Grafo](../../producto/funcionalidades/seccion-grafo.md) - Visualización de relaciones

**Criterios de Completitud**:

- Frontend se conecta a API REST correctamente
- Dashboard muestra documentos y gaps
- Sesiones interactivas funcionan en frontend
- Diff viewer muestra cambios correctamente

**Dependencias**: Hito 2 (API REST y MCP Server)

**Nota**: Este hito se movió desde la posición original del Hito 6 para facilitar dogfooting y validación temprana de UX desde el inicio del ciclo.

---

### Hito 4: Implementación de Fases Detección y Agrupación

**Objetivo**: Implementar detección de gaps y agrupación por tema

**Componentes**:

- Sistema de jobs asíncronos con Celery
- Agentes LLM para análisis de documentos
- Sistema de metadata de gaps (tipo, severidad, rol afectado, contexto)
- Sistema de agrupación por tema y similitud semántica
- Metadata de sesiones (tema, subtema, prioridad)
- Dashboard de gaps detectados con filtros

**Nota**: El sistema de jobs asíncronos (Celery) se implementa en este hito porque las fases de detección y agrupación requieren ejecución de tareas pesadas de LLM (gap_detection, vector_sync) que no pueden bloquear el servidor principal. Según ADR-004, se usa Celery con Redis como broker para jobs efímeros con retry strategy y backoff exponencial.

**Features Asociados**:

- [Sección de Preguntas](../../producto/funcionalidades/seccion-preguntas.md) - Captura de conocimiento inicial
- [Sección de Gaps](../../producto/funcionalidades/seccion-gaps.md) - Detección y agrupación de gaps
- [FEAT-007: Búsqueda Semántica](../../producto/funcionalidades/busqueda-semantica.md) - Transformación a vectores

**Criterios de Completitud**:

- Sistema de jobs asíncronos configurado y funcional
- Jobs pueden encolarse y ejecutarse
- Agentes LLM detectan gaps en documentos de prueba
- Gaps detectados tienen metadata completa
- Sistema agrupa gaps por tema correctamente
- Dashboard muestra gaps y sesiones pendientes

**Dependencias**: Hito 2 (API REST y MCP Server)

**Nota**: Este hito se movió desde la posición original del Hito 3.

---

### Hito 5: Implementación de Fases Resolución y Verificación

**Objetivo**: Implementar resolución interactiva y verificación automática

**Componentes**:

- Interfaz de sesión interactiva con agentes LLM
- Metadata de respuestas (quién, cuándo, calidad, fuentes)
- Sistema de verificación automática de consistencia
- Metadata de verificación (confianza, gaps nuevos, contradicciones)
- Detección de contradicciones entre respuestas

**Features Asociados**:

- [Sección de Gaps](../../producto/funcionalidades/seccion-gaps.md) - Resolución de gaps
- [FEAT-004: Sección de Grafo](../../producto/funcionalidades/seccion-grafo.md) - Visualización de impacto

**Criterios de Completitud**:

- Sesiones interactivas permiten responder gaps
- Respuestas tienen metadata completa
- Sistema verifica consistencia de respuestas
- Contradicciones se detectan correctamente

**Dependencias**: Hito 4 (Detección y Agrupación)

**Nota**: Este hito se movió desde la posición original del Hito 4.

---

### Hito 6: Implementación de Fase Aplicación

**Objetivo**: Implementar aplicación automática de cambios

**Componentes**:

- Sistema de aplicación automática con aprobación
- Diff viewer para revisar cambios antes de aplicar
- Versioning automático de documentos
- Rollback automático si se detectan errores

**Features Asociados**:

- [Sección de Propuestas](../../producto/funcionalidades/seccion-propuestas.md) - Generación y aplicación de propuestas
- [FEAT-006: Versioning de Documentos](../../producto/funcionalidades/versioning-documentos.md) - Versioning automático y rollback
- [FEAT-008: Diff Viewer](../../producto/funcionalidades/diff-viewer.md) - Revisión de cambios

**Criterios de Completitud**:

- Sistema genera diff de cambios correctamente
- Diff viewer permite revisar cambios antes de aplicar
- Versioning crea snapshots antes de cada UPDATE
- Rollback restaura snapshots correctamente

**Dependencias**: Hito 5 (Resolución y Verificación)

**Nota**: Este hito se movió desde la posición original del Hito 5.

---

### Hito 7: Integraciones Básicas

**Objetivo**: Implementar integraciones básicas para dogfooding

**Componentes**:

- Integración con Git (lectura/escritura de archivos)
- PENDIENTE - Otras integraciones por definir según necesidades de dogfooding

**Features Asociados**:

- [FEAT-005: Integración con Git](../../producto/funcionalidades/integracion-git.md) - Conexión con repositorios y arqueología de código
- [FEAT-002: Onboarding de Proyecto Nuevo](../../producto/funcionalidades/onboarding-proyecto-nuevo.md) - Conexión de repositorio
- [FEAT-003: Onboarding de Proyecto Legacy](../../producto/funcionalidades/onboarding-proyecto-legacy.md) - Análisis de salud y arqueología

**Criterios de Completitud**:

- Sistema lee y escribe archivos en repositorio Git
- Integración funciona con repositorios de prueba

**Dependencias**: Hito 6 (Aplicación)

**Nota**: Este hito se movió desde la posición original del Hito 6.

---

## Mapeo Features - Hitos

Esta sección mapea los 13 features del MVP Bootstrapped a los hitos del roadmap, proporcionando visibilidad explícita del desarrollo. El mapeo agrupa features según dependencias técnicas y la fase del workflow de 5 fases que implementan. Algunos features como Búsqueda Semántica (FEAT-007) aparecen en múltiples hitos porque su implementación es progresiva: configuración de infraestructura en hitos tempranos y funcionalidad completa en hitos posteriores. Esta agrupación permite un desarrollo incremental donde cada hito agrega capacidades específicas sin bloquear el progreso de otros componentes.

Hito 1: Infraestructura Base

- **FEAT-007: Búsqueda Semántica** - Configuración de Qdrant (base de datos vectorial)

Hito 2: API REST y MCP Server Básico

- **FEAT-001: Sistema de Usuarios y Organizaciones** - Autenticación y gestión de usuarios/organizaciones
- **FEAT-007: Búsqueda Semántica** - Motor de búsqueda semántica

Hito 3: Frontend React

- **FEAT-009: Dashboard General** - Vista de alto nivel y navegación
- **FEAT-008: Diff Viewer** - Comparación visual de cambios
- **Sección de Documentos** - Vista de documentos
- **Sección de Preguntas** - Vista de preguntas
- **Sección de Gaps** - Vista de gaps
- **Sección de Propuestas** - Vista de propuestas
- **FEAT-004: Sección de Grafo** - Visualización de relaciones

Hito 4: Implementación de Fases Detección y Agrupación

- **Sección de Preguntas** - Captura de conocimiento inicial
- **Sección de Gaps** - Detección y agrupación de gaps
- **FEAT-007: Búsqueda Semántica** - Transformación a vectores

Hito 5: Implementación de Fases Resolución y Verificación

- **Sección de Gaps** - Resolución de gaps
- **FEAT-004: Sección de Grafo** - Visualización de impacto

Hito 6: Implementación de Fase Aplicación

- **Sección de Propuestas** - Generación y aplicación de propuestas
- **FEAT-006: Versioning de Documentos** - Versioning automático y rollback
- **FEAT-008: Diff Viewer** - Revisión de cambios

Hito 7: Integraciones Básicas

- **FEAT-005: Integración con Git** - Conexión con repositorios y arqueología de código
- **FEAT-002: Onboarding de Proyecto Nuevo** - Conexión de repositorio
- **FEAT-003: Onboarding de Proyecto Legacy** - Análisis de salud y arqueología

---

## Nota sobre Funcionalidades Post MVP

Integraciones enterprise (Confluence, Notion, Jira), búsqueda semántica avanzada con Qdrant, analytics organizacionales, multi-tenant, compliance SOC2/HIPAA, y enterprise features (SSO, RBAC avanzado) se definirán tras validación de problem-solution fit y obtención de inversión externa. Estas funcionalidades están fuera del alcance del MVP bootstrapped actual.

**Referencia**: La priorización de estas funcionalidades se definirá en [feature-prioritization-policy.md](../politicas/feature-prioritization-policy.md) (por crear).

---

## Referencias a Documentos Relacionados

Este documento es parte de la estrategia tecnológica de Alejandria. Para una comprensión completa, consulte también:

- **[technology-strategy.md](technology-strategy.md)**: Estrategia tecnológica de alto nivel y arquitectura general
- **[frontend-strategy.md](frontend-strategy.md)**: Estrategia de frontend
- **[llm-evaluation.md](llm-evaluation.md)**: Evaluación de modelos LLM
- **[../politicas/dogfooding-validation-policy.md](../politicas/dogfooding-validation-policy.md)**: Política de dogfooding y validación
- **[../../ingenieria/arquitectura/technology-stack.md](../../ingenieria/arquitectura/technology-stack.md)**: Stack tecnológico recomendado y principios técnicos del MVP
- **[../../ingenieria/arquitectura/architecture-overview.md](../../ingenieria/arquitectura/architecture-overview.md)**: Decisiones de diseño arquitectónico clave
- **[../../ingenieria/arquitectura/technical-brief.md](../../ingenieria/arquitectura/technical-brief.md)**: Descripción de arquitectura del sistema
- **[../../ingenieria/arquitectura/end-to-end-flow.md](../../ingenieria/arquitectura/end-to-end-flow.md)**: Flujo completo end-to-end del sistema
- **[../../ingenieria/tareas/hito-implementation-specification.md](../../ingenieria/tareas/hito-implementation-specification.md)**: Índice de épicas de implementación por hito
- **[../../producto/5-phase-workflow.md](../../producto/5-phase-workflow.md)**: Arquitectura de 5 fases (definición de producto)
- **[vision-mission.md](vision-mission.md)**: Vision and Mission Statement con propósito estratégico y valores organizacionales

### Referencias a Documentación Externa

Para detalles técnicos específicos de las tecnologías utilizadas en este roadmap:

- **FastAPI**: <https://fastapi.tiangolo.com/> - Framework web moderno y rápido para Python
- **Celery**: <https://docs.celeryq.dev/> - Sistema de colas distribuido para procesamiento asíncrono
- **RQ**: <https://python-rq.org/> - Biblioteca de colas simple para Python
- **FastMCP**: <https://github.com/jlowin/fastmcp> - Implementación de Model Context Protocol
- **Qdrant**: <https://qdrant.tech/documentation/> - Motor de búsqueda semántica y base de datos vectorial
- **Ollama**: <https://ollama.com/> - Plataforma para ejecutar modelos de lenguaje localmente
- **React**: <https://react.dev/> - Biblioteca JavaScript para construir interfaces de usuario
- **Docker Compose**: <https://docs.docker.com/compose/> - Herramienta para orquestar contenedores Docker
