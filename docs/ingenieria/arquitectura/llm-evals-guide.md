---
id: ARC-013
type: Technical Guide
rating:
rating-phase:
dependency: [ESTR-STR-002, ARC-004, ARC-007]
related:
  - target: STR-002
    relationship_type: implements
    reason: Implementa la estrategia tecnológica con guía de evals de LLM
  - target: ARC-007
    relationship_type: references
    reason: Referencia el job-implementation-guide para evals de jobs
---

## Guía de Evals para LLM — Alejandria

Este documento define el framework de evaluación sistemática para calidad de respuestas de LLM en las fases de detección, resolución y aplicación del sistema Alejandria.

---

## Estado del Documento

**PENDIENTE**: Este documento es un placeholder. El análisis de riesgos en el technical-roadmap identifica problemas de uso de LLM como riesgo principal para Hitos 4, 5 y 6, con mitigación de implementar evals sistemáticos. Se requiere especificación técnica de cómo implementar evals sistemáticos.

---

## Contexto del Riesgo

Según el análisis de riesgos en [technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md):

**Riesgo identificado**: Problemas de uso de LLM para los pasos en Hitos 4, 5 y 6.

**Mitigación propuesta**: Implementar evals (investigar en web) para tener una base de calidad persistente.

**Hitos afectados**:

- Hito 4 (Detección y Agrupación): Agentes LLM para análisis de documentos
- Hito 5 (Resolución y Verificación): Verificación automática de consistencia
- Hito 6 (Aplicación): Aplicación automática de cambios

---

## Referencias

- **[../../estrategia/estrategia/technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md)**: Análisis de riesgos por hito
- **[../arquitectura/mcp-server-specification.md](../arquitectura/mcp-server-specification.md)**: Especificación de MCP Server y prompts de agentes
- **[../arquitectura/job-implementation-guide.md](../arquitectura/job-implementation-guide.md)**: Guía de implementación de jobs

---

## Información Pendiente de Definir

Las siguientes secciones están marcadas como PENDIENTE y se definirán tras investigación de evals:

- Framework de evaluación a implementar (ej. RAGAS, Promptfoo, custom evals)
- Métricas de calidad a evaluar (precisión, recall, relevancia, consistencia)
- Conjunto de datos de prueba para evals
- Estrategia de evaluación continua vs puntual
- Umbrales de aceptación para métricas de calidad
- Proceso de integración de evals en pipeline de CI/CD
- Estrategia de manejo de evals fallidos
- Reporting y visualización de resultados de evals
