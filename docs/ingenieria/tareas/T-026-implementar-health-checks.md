---
id: T-026
type: Task
rating: 9
rating-phase: document-editing
related:
  - target: EPC-002
    relationship_type: implements
    reason: Implementa la épica de API REST y MCP Server con health checks
  - target: T-017
    relationship_type: depends_on
    reason: Depende de los endpoints de documents en T-017 para health checks
---

# T-026: Implementar Health Checks

**Tipo**: Task
**Prioridad**: Media
**Estimación**: 2 horas
**Dependencias**: EPC-002, T-017

## Descripción

Implementar endpoint de health check para verificar estado de servicios. Ollama se ejecuta fuera de Docker (en el host o máquina remota) según ADR-003, conectado mediante Tailscale. Health check de Ollama verifica conectividad vía `/api/version` usando la URL de Tailscale configurada en OLLAMA_URL.

## Criterios de Aceptación

- [ ] GET /api/v1/health implementado
- [ ] Health check verifica PostgreSQL, Redis, Qdrant (Celery fuera de alcance para MVP)
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
