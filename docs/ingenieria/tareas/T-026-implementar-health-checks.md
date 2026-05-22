---
id: T-026
type: Task
rating:
rating-phase:
related:
  - target: EPC-002
    relationship_type: implements
    reason: Implementa la épica de API REST y MCP Server con health checks
  - target: T-017
    relationship_type: depends_on
    reason: Depende de los endpoints de documents en T-017 para health checks
  - target: T-021
    relationship_type: depends_on
    reason: Depende de la configuración de Celery en T-040 para health checks
---

# T-026: Implementar Health Checks

**Tipo**: Task
**Prioridad**: Media
**Estimación**: 2 horas
**Dependencias**: EPC-002, T-017, T-021

## Descripción

Implementar endpoint de health check para verificar estado de servicios. Ollama se ejecuta fuera de Docker (en el host o máquina remota) según ADR-003, conectado mediante Tailscale. Health check de Ollama verifica conectividad vía `/api/version` usando la URL de Tailscale configurada en OLLAMA_URL.

## Criterios de Aceptación

- [ ] GET /api/v1/health implementado
- [ ] Health check verifica PostgreSQL, Redis, Qdrant, Celery
- [ ] Health check verifica Ollama vía Tailscale (endpoint `/api/version`)
- [ ] Health check retorna JSON con estado de cada servicio

## Archivos a Crear

```
app/api/
  └── health.py
app/services/
  └── health_service.py
```

## Referencias

- [TRD - Hito 2](../propuestas/trd-milestone-2-api-mcp.md): RF-013: Health Checks

---

## Análisis de Documento

**ESTADO DEL ANÁLISIS**

- Análisis previo: NO
- Fecha del análisis: 2026-05-27
- Versión del análisis: 1
- Gaps pendientes: 2
- Gaps respondidos: 0
- Gaps NO APLICA: 0

**CLASIFICACIÓN DEL DOCUMENTO**

- Tipo: Documento de Proyecto (Task)
- Rol Principal: Desarrollador/Ingeniero
- Roles a Revisar: Desarrollador + Arquitecto + Gerente de Proyecto
- Enfoque: Implementación de endpoint de health check para servicios
- Perspectiva: Senior + Junior
- Fecha de análisis: 2026-05-27
- Versión del análisis: 1

### Gaps Identificados

**IMPLEMENTACIÓN TÉCNICA**

**GAP: Health check de Ollama (vía Tailscale)** [PRIORIDAD: Medio] [ESTADO: PENDIENTE]

- **Pregunta**: La tarea menciona "Health check de Ollama (vía Tailscale)" como GAP. ¿Por qué Tailscale? ¿Ollama no está en el mismo Docker Compose? ¿Cómo se verifica conectividad vía Tailscale? ¿Qué endpoint se usa?
- **Contexto faltante**: Detalles del health check de Ollama vía Tailscale, incluyendo por qué se usa Tailscale, mecanismo de verificación de conectividad, y endpoint específico.
- **Rol afectado**: Desarrollador Senior
- **Referencia**: Línea 34 del documento actual
- **Fecha de identificación**: 2026-05-27

**GESTIÓN DE PROYECTO**

**GAP: Criterios para estimación de esfuerzo** [PRIORIDAD: Bajo] [ESTADO: PENDIENTE]

- **Pregunta**: La tarea tiene una estimación de 2 horas. ¿Qué criterios se usaron para esta estimación? ¿Es basada en experiencia previa? ¿Referencias externas?
- **Contexto faltante**: Justificación de la estimación de esfuerzo para esta tarea específica.
- **Rol afectado**: Gerente de Proyecto
- **Referencia**: Línea 22 del documento actual
- **Fecha de identificación**: 2026-05-27
