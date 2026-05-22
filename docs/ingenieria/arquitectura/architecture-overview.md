---
id: ARC-011
type: Architecture Overview
rating: 9
rating-phase: document-editing
related:
  - target: STR-002
    relationship_type: implements
    reason: Implementa la estrategia tecnológica con decisiones de diseño arquitectónico
  - target: ARC-003
    relationship_type: implements
    reason: Implementa el technology stack con decisiones específicas de arquitectura
  - target: ARC-025
    relationship_type: references
    reason: Referencia el mcp-server-implementation para implementación de MCP
  - target: ARC-015
    relationship_type: references
    reason: Referencia el qdrant para configuración de Qdrant
---

# Architecture Overview — Alejandria

Este documento documenta las decisiones de diseño arquitectónico clave del proyecto Alejandria. Cada decisión incluye justificación detallada, alineación con principios estratégicos y valores organizacionales, beneficios y trade-offs explícitos.

## Resumen Ejecutivo

Las decisiones de diseño de Alejandria se centran en: (1) Arquitectura de 5 fases secuenciales (Detección → Agrupación → Resolución → Verificación → Aplicación) para automatizar el ciclo de vida de la documentación, (2) Stack unificado en Python (FastAPI + Celery + FastMCP) para aprovechar el ecosistema maduro de herramientas LLM/MCP, (3) MCP como capa de abstracción para comunicación con LLMs, (4) Jobs efímeros para escalabilidad, (5) Versioning de documentos para reversibilidad, y (6) Idempotencia de jobs para consistencia. Estas decisiones implementan directamente los principios técnicos del MVP y los valores organizacionales establecidos en vision-mission.md.

---

## Stack Unificado en Python

**Decisión**: Usar un stack unificado en Python para todos los componentes backend:

1. **API Backend**: Python (FastAPI)
2. **Jobs y Orquestación**: Python (Celery)
3. **MCP Server**: Python (FastMCP)

**Implementación específica**:

- FastAPI para API REST con async nativo y type safety con Pydantic
- **Celery** para sistema de colas nativo de Python (decisión tomada: usar Celery desde el inicio)
- FastMCP para MCP Server con integración nativa con FastAPI
- PostgreSQL como base de datos con Alembic para migrations

**Decisión entre Celery y RQ**: Elegir Celery desde el inicio porque aunque es más complejo, el ecosistema es más maduro, tiene mejor documentación, y la curva de aprendizaje adicional vale la pena por la flexibilidad futura. RQ podría ser un cuello de botella si el sistema escala.

### Justificación

#### Ventajas del ecosistema Python para LLM/MCP

- La generación del servidor MCP está más desarrollada en Python
- Bibliotecas extensas para MCP y integraciones LLM
- Comunidades activas en LangChain, OpenAI, Anthropic, etc.
- Herramientas de orquestación y tool calling bien establecidas

#### Integración nativa y reducción de complejidad

- Usar un stack unificado en Python permite integración directa entre componentes
- Elimina la necesidad de bridges o APIs entre diferentes lenguajes
- Reduce complejidad operacional al tener un solo lenguaje de backend
- Facilita debugging y troubleshooting al tener consistencia tecnológica

#### Type safety y async nativo

- FastAPI proporciona type safety con Pydantic
- Async nativo para mejor performance en operaciones I/O intensivas
- Validación automática de requests y responses
- Documentación automática de API con OpenAPI/Swagger

### Alineación con principios estratégicos

- **Baja Fricción**: Stack unificado reduce fricción operacional, menor curva de aprendizaje al tener un solo lenguaje
- **Calidad Automática**: Pydantic proporciona validación automática de datos, type safety reduce bugs, ecosistema Python maduro con herramientas de testing robustas (pytest)

### Trade-offs

- **Performance vs Elixir/Phoenix**: Python puede ser más lento que Elixir para concurrencia masiva
- **Menor fault tolerance que Nomad**: Celery no tiene las capacidades de fault tolerance y auto-scaling de Nomad
- **Global Interpreter Lock (GIL)**: Python tiene limitaciones para true parallelism en CPU-bound tasks

### Mitigación

- Async nativo: FastAPI y Celery soportan async para mejor performance en I/O operations
- Jobs efímeros: Implementar jobs efímeros con locks en base de datos para idempotencia
- Escalabilidad horizontal: API stateless con load balancer para distribuir carga
- Optimización de queries: PostgreSQL con connection pooling y caching con Redis

### Alternativas consideradas y rechazadas

- **Rails 8 para API Backend**: Rechazada porque el ecosistema Python para LLM/MCP es más maduro
- **Elixir/Phoenix para API Backend**: Rechazada porque el ecosistema Python para LLM/MCP es más maduro y la diferencia en performance no es crítica para fase bootstrapped
- **Nomad para Jobs y Orquestación**: Rechazada para fase bootstrapped porque Celery/RQ proporciona integración nativa con stack Python y menor complejidad operacional
- **Stack Híbrido (Python + Otro Lenguaje)**: Rechazada porque un stack unificado reduce complejidad operacional

---

## MCP como Capa de Abstracción

**Decisión**: Usar MCP (Model Context Protocol) como capa de abstracción para comunicación con LLMs

### Justificación de MCP como Capa de Abstracción

MCP permite estandarizar la comunicación con LLMs, facilita el cambio de proveedores y habilita tool calling estructurado. Es la forma más simple de interactuar con agentes tanto interactiva como automáticamente, aprovechando que es un estándar que expone el sistema de manera consistente. Además, MCP permite usar agentes externos además de los internos, por lo que esta capa puede utilizarse para ambos usos (agentes internos del sistema y agentes externos de terceros).

**Concepto fundamental**: MCP es un protocolo estandarizado que define cómo las aplicaciones pueden pedirle cosas a los LLMs de manera consistente (como HTTP para la web), y es una capa que separa la lógica de negocio de Alejandria de los detalles específicos de cómo hablar con cada LLM. Sin MCP, el código de Alejandria estaría lleno de llamadas específicas a OpenAI, Anthropic, etc. Con MCP, Alejandria solo sabe "ejecutar herramienta X" y MCP se encarga de traducir eso al formato específico de cada proveedor.

### Alineación con principios estratégicos de MCP

Esta decisión implementa directamente el principio de "complementar LLMs, no competir contra ellos" establecido en vision-mission.md:

- **Cambio de proveedores sin reescribir código**: MCP permite cambiar entre Anthropic, OpenAI u otros proveedores sin modificar la arquitectura. Alejandria no depende de un solo LLM.
- **Enfoque en valor de dominio**: MCP estandariza tool calling, permitiendo que Alejandria se enfoque en orquestación y detección de gaps (su valor de dominio) en lugar de construir capacidades LLM propias.
- **Flexibilidad futura**: MCP habilita adoptar nuevos modelos a medida que surjan, reforzando que Alejandria complementa la evolución de LLM.
- **Interacción simple y estandarizada**: MCP es la forma más simple de interactuar con agentes tanto interactiva como automáticamente, aprovechando que es un estándar.
- **Apalancamiento de tecnología existente**: MCP es la capa técnica que implementa la decisión estratégica de apalancar tecnología base existente en lugar de desarrollar capacidades desde cero.

### Alineación con valores organizacionales de MCP

MCP como capa de abstracción implementa el valor de "Integración Continua" al permitir integración con múltiples herramientas y proveedores sin cambios drásticos en arquitectura.

### Beneficios

- Componibilidad y testabilidad: Cada componente puede probarse independientemente
- Cambio de proveedores sin rewrite: Reducción de vendor lock-in
- Ecosistema de herramientas estándar: Acceso a herramientas preexistentes
- Interacción simple y estandarizada con agentes: Menor complejidad en integración

### Trade-offs de MCP

- Capa adicional de complejidad: Añade una capa más a la arquitectura
- Learning curve para equipo: El equipo necesita aprender MCP

### MCP en Fase MVP Bootstrapped

#### Trade-off Específico para Fase Inicial

En fase MVP Bootstrapped, existe un trade-off entre simplicidad inicial (integración directa con un solo proveedor LLM) y flexibilidad futura (MCP como capa de abstracción).

#### Alternativa Considerada: Integración Directa

- **Ventaja inicial**: Menor complejidad arquitectónica, setup más simple, menor learning curve
- **Desventaja a largo plazo**: Vendor lock-in, dificultad para cambiar de proveedor, arquitectura menos flexible

#### Decisión: MCP desde el Inicio

- **Justificación para MVP Bootstrapped**: Aunque añade complejidad inicial, MCP se justifica desde el inicio porque:
  1. **Costo de cambio futuro**: Refactorizar de integración directa a MCP después sería más costoso que implementar MCP desde el inicio
  2. **Flexibilidad para dogfooding**: MCP permite probar diferentes modelos LLM durante fase de desarrollo sin reescribir código
  3. **Agentes externos**: MCP habilita el uso de agentes externos además de los internos, lo que puede ser valioso durante fase de experimentación
  4. **Ecosistema Python**: Con FastMCP, la implementación en Python es relativamente sencilla y el ecosistema proporciona soporte robusto

#### Mitigación de Complejidad en Fase MVP Bootstrapped

- Usar FastMCP (framework Python simplificado) para reducir complejidad de implementación
- Comenzar con un solo proveedor LLM (Qwen 3.5 en Ollama) para simplificar configuración inicial
- Documentar claramente el patrón MCP para facilitar onboarding del equipo

---

## Jobs Efímeros vs Persistentes

**Decisión**: Usar jobs efímeros con Celery/RQ para mejor utilización de recursos y fault tolerance

### Justificación de Jobs Efímeros

- **Escalabilidad horizontal**: Los jobs efímeros pueden distribuirse across múltiples workers según demanda
- **Aislamiento de failures**: Si un job falla, no afecta otros jobs ni el sistema principal
- **Mejor resource utilization**: Los recursos se asignan solo cuando se necesitan, no se mantienen workers idle
- **Integración nativa con stack Python**: Celery está mejor acoplado con el stack de Python y ofrece mayor control durante la programación

**Concepto fundamental**: Jobs efímeros son procesos que se inician para ejecutar una tarea específica y terminan cuando la tarea completa. Jobs persistentes son procesos que quedan corriendo continuamente, esperando tareas en una cola. La diferencia es el ciclo de vida: efímeros = ciclo corto, persistentes = ciclo largo. Son mejores para Alejandria porque permiten escalar horizontalmente (agregar más workers cuando hay mucho trabajo) y mejor aislamiento de failures (si un job falla, no afecta a otros workers). Nota: se refiere a trabajos que se ejecutan conforme se encolan, no a workers on demand.

### Alineación con valores organizacionales de Jobs Efímeros

Jobs efímeros implementan el valor de "Baja Fricción" al permitir escalabilidad horizontal sin configuración manual compleja. El sistema escala automáticamente según demanda, reduciendo la fricción operacional.

---

## Versioning de Documentos

**Decisión**: Crear snapshot automático antes de cada UPDATE en `documents.content`

### Justificación de Versioning de Documentos

- **Reversibilidad de cambios de agentes LLM**: Si un agente hace un cambio incorrecto, podemos revertir
- **Audit trail completo**: Tenemos historial completo de todos los cambios
- **Protección contra malas sugerencias**: Los cambios se pueden revisar antes de aceptarlos definitivamente

**Concepto fundamental**: El sistema usa documentación que se guarda en base de datos y es accesible via API. No hay forma de usar Git porque la documentación no es local, es en la nube, principalmente por esa razón no se consideró Git. Por lo tanto, el versioning a nivel de aplicación es necesario porque Git no es viable para documentación almacenada en base de datos/cloud.

### Alineación con valores organizacionales de Versioning

Versioning de documentos implementa el valor de "Verificación Iterativa" al permitir revertir cambios si se detectan errores. Esto asegura que la documentación mejore iterativamente sin riesgo de degradación.

---

## Idempotencia de Jobs

**Decisión**: Implementar Redis distributed locks con celery_once

### Justificación de Idempotencia de Jobs

- **Prevenir duplicación de trabajo**: Un job no se ejecuta dos veces para la misma tarea
- **Consistencia en estados**: El estado del sistema permanece consistente incluso con reintentos
- **Manejo de reintentos**: Si un job falla y se reintentra, no causa efectos secundarios duplicados

### Alineación con valores organizacionales de Idempotencia

Idempotencia de jobs implementa el valor de "Calidad Automática" al prevenir duplicación de trabajo y asegurar consistencia. Esto mantiene la calidad sin supervisión manual.

---

## Definiciones de Terminología Clave

**MCP (Model Context Protocol)**: Protocolo estándar para comunicación entre aplicaciones y modelos de lenguaje (LLMs). Permite cambio de proveedores LLM sin reescribir código, proporcionando una capa de abstracción con componentes de client, server, tools y resources. Para detalles técnicos completos, ver [adr-001-mcp-abstraction-layer.md](adr-001-mcp-abstraction-layer.md).

**FastMCP**: Framework Python que simplifica la implementación de servidores MCP. Proporciona abstracciones de alto nivel para crear tools y resources MCP con menos código boilerplate que MCP estándar. Se usa en Alejandria para reducir la complejidad de implementación de MCP en fase MVP Bootstrapped.

**Celery**: Sistema de colas de tareas para Python. Celery es robusto con features avanzadas y permite ejecución asíncrona de jobs con Redis como broker. La decisión de usar Celery se tomó según ADR-004.

---

## Referencias a Documentos Relacionados

Este documento es parte de la estrategia tecnológica de Alejandria. Para una comprensión completa, consulte también:

- **[../../estrategia/estrategia/technology-strategy.md](../../estrategia/estrategia/technology-strategy.md)**: Estrategia tecnológica de alto nivel y arquitectura general
- **[../arquitectura/technology-stack.md](../arquitectura/technology-stack.md)**: Stack tecnológico recomendado y principios técnicos del MVP
- **[../../estrategia/estrategia/technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md)**: Roadmap técnico de implementación
- **[../../estrategia/politicas/operational-strategies.md](../../estrategia/politicas/operational-strategies.md)**: Estrategias operacionales (escalabilidad, seguridad, monitoreo, deployment, testing)
- **[../../estrategia/estrategia/vision-mission.md](../../estrategia/estrategia/vision-mission.md)**: Vision and Mission Statement con propósito estratégico y valores organizacionales
- **[adr-001-mcp-abstraction-layer.md](adr-001-mcp-abstraction-layer.md)**: Architecture Decision Record detallado sobre MCP como capa de abstracción
- **[../../producto/5-phase-workflow.md](../../producto/5-phase-workflow.md)**: Definición de producto sobre arquitectura de 5 fases
- **[adr-002-python-unified-stack.md](adr-002-python-unified-stack.md)**: Architecture Decision Record detallado sobre stack unificado en Python
- **[adr-003-local-infrastructure-docker-compose.md](adr-003-local-infrastructure-docker-compose.md)**: Architecture Decision Record detallado sobre infraestructura local con Docker Compose
- **[adr-004-ephemeral-jobs.md](adr-004-ephemeral-jobs.md)**: Architecture Decision Record detallado sobre jobs efímeros vs persistentes
- **[adr-005-job-idempotency.md](adr-005-job-idempotency.md)**: Architecture Decision Record detallado sobre idempotencia de jobs
- **[adr-006-document-versioning.md](adr-006-document-versioning.md)**: Architecture Decision Record detallado sobre versioning de documentos
