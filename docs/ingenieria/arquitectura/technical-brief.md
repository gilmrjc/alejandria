---
id: ARC-001
type: Architecture
rating: 9
rating-phase: document-critique
dependency: [ARC-003]
related:
  - target: STR-002
    relationship_type: implements
    reason: Implementa la estrategia tecnológica describiendo la arquitectura del sistema
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para definir persistencia de datos
  - target: ARC-007
    relationship_type: references
    reason: Referencia el job-implementation-guide para guía de implementación de jobs
---

# Alejandria — Knowledge Gap Pipeline

Sistema automatizado de análisis y enriquecimiento de documentación mediante agentes LLM. Detecta gaps de contexto en documentos, los resuelve mediante sesiones interactivas, y aplica los cambios de forma continua.

---

## Índice

1. [Visión general](#1-visión-general)
2. [Arquitectura](#2-arquitectura)
3. [Flujo completo end-to-end](end-to-end-flow.md)

---

## 1. Visión general

El sistema opera en cinco fases encadenadas:

| Fase         | Actor              | Descripción                                             |
|--------------|--------------------|---------------------------------------------------------|
| Detección    | Agente 1           | Lee un documento, genera preguntas (gaps) y sugerencias |
| Agrupación   | Agente 2           | Agrupa las preguntas por tema para sesiones coherentes  |
| Resolución   | Agente 3 + usuario | Sesión interactiva para responder las preguntas         |
| Verificación | Agente 1           | Evalúa si las respuestas revelan nuevos gaps (ciclo)    |
| Aplicación   | Agente 4           | Aplica sugerencias con el contexto enriquecido          |

Los agentes son **prompts accionados**: reciben contexto vía MCP, razonan, y persisten resultados vía MCP. La orquestación la maneja el API mediante estados y jobs.

---

## 2. Arquitectura

```text
┌─────────────────────────────────────────────────────────┐
│                        Frontend                         │
│         Dashboard / Sesión de respuestas / Docs         │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP
┌───────────────────────▼─────────────────────────────────┐
│                      API REST                           │
│         Entidades · Estados · Encolado de jobs          │
└──────┬────────────────┬────────────────┬────────────────┘
       │                │                │
┌──────▼──────┐  ┌──────▼──────┐   ┌─────▼──────┐
│  MCP Server │  │  Job Queue  │   │    Cron    │
│  (agentes)  │  │ (Celery) │   │  (health)  │
└─────────────┘  └─────────────┘   └────────────┘
```

**Stack recomendado:**

- API: Python (FastAPI)
- Jobs: Python (Celery)
- MCP Server: Python (FastMCP)
- Base de datos: PostgreSQL
- Frontend: React o cualquier SPA ligera

**Nota**: Para justificación detallada de las decisiones de stack, ver los Architecture Decision Records (ADRs):

- ADR-001: Uso de MCP como Capa de Abstracción para LLM
- ADR-002: Arquitectura de 5 Fases para Ciclo de Detección-Resolución
- ADR-002: Stack Unificado en Python (FastAPI + Celery + FastMCP)

**Especificaciones detalladas de componentes**:

- [API REST Specification](api-specification.md): Endpoints, request/response schemas, autenticación, rate limiting
- [MCP Server Specification](mcp-tools-specification.md): Tools, protocolo de comunicación con agentes
- [Job Implementation Guide](job-implementation-guide.md): Guía de implementación de jobs de Celery, chains, retry strategy

---

## 3. Flujo completo end-to-end

Para el flujo completo end-to-end, ver [end-to-end-flow.md](end-to-end-flow.md).

---

## Análisis de Document-Critique

### Estado del Análisis

- Análisis previo: NO
- Fecha del último análisis: 2026-05-26
- Versión anterior: N/A
- Gaps pendientes: 0
- Gaps respondidos: 0

### Clasificación del Documento

- Tipo: Documento de Arquitectura
- Rol Principal: Arquitecto
- Roles a Revisar: Arquitecto + Desarrollador
- Enfoque: Revisión de visión general del sistema y arquitectura de alto nivel
- Perspectiva: Senior + Junior
- Fecha de análisis: 2026-05-26
- Versión del análisis: 1

### Respuestas Encontradas en Referencias para Arquitecto

technology-stack.md:

- ¿Por qué Python unificado? Respuesta: Aprovechar ecosistema maduro de herramientas LLM/MCP
- ¿Por qué MCP como capa de abstracción? Respuesta: Permite cambio de proveedores LLM sin reescribir código
- Referencia: docs/ingenieria/arquitectura/technology-stack.md

### Respuestas Encontradas en Referencias para Desarrollador

technology-strategy.md:

- ¿Qué es MCP? Respuesta: Protocolo estándar para comunicación entre aplicaciones y modelos de lenguaje
- ¿Qué es FastMCP? Respuesta: Framework Python que simplifica implementación de servidores MCP
- Referencia: docs/estrategia/estrategia/technology-strategy.md

### Gaps Identificados

No se identificaron gaps críticos. El documento proporciona una visión clara y concisa del sistema y su arquitectura de alto nivel.

### Calificación del Documento: 9/10

**Desglose**:

- Completitud de Respuestas: 9/10 - El documento responde las preguntas clave sobre la arquitectura general del sistema
- Contexto Multi-Rol: 9/10 - Buen contexto para ambos roles. Senior tiene visión arquitectónica de componentes. Junior tiene descripción clara de las 5 fases y stack recomendado
- Calidad de Referencias: 9/10 - Referencias específicas a ADRs y documentos de especificación
- Estructura y Organización: 9/10 - Estructura clara con índice, visión general y arquitectura
- Consistencia: 9/10 - No se identificaron contradicciones

**Resumen**: El documento es excelente y conciso, proporcionando una visión clara del sistema y su arquitectura de alto nivel. Sirve como buen punto de entrada para entender el sistema antes de profundizar en documentos más específicos.
