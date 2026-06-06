---
id: ARC-025
type: Architecture
rating:
rating-phase:
dependency: [ADR-001, ARC-003]
related:
  - target: ADR-001
    relationship_type: implements
    reason: Implementa la decisión de MCP con guía de implementación
  - target: ARC-003
    relationship_type: implements
    reason: Implementa el technology stack con guía de implementación de MCP
---

# MCP Server Implementation — Alejandria

Este documento define la implementación del servidor MCP (Model Context Protocol) para Alejandria.

## Transporte HTTP

El servidor MCP utiliza exclusivamente transporte HTTP para todos los entornos (desarrollo y producción).

**Razones del cambio de stdio a HTTP**:

1. **Compatibilidad FastMCP-SQLAlchemy**: El transporte stdio tenía problemas fundamentales con los tipos `Session` de SQLAlchemy en pydantic-core, causando errores de schema generation que impedían el funcionamiento del servidor MCP
2. **Autenticación API KEY nativa**: HTTP permite autenticación vía headers de forma estándar, ya implementada en el código para transporte HTTP
3. **Mejor integración con IDEs**: Los IDEs modernos (Devin IDE, Windsurf, Claude Code) tienen mejor soporte para servidores MCP HTTP
4. **Arquitectura más apropiada para producción**: HTTP es el estándar para servidores MCP en entornos de producción

## Configuración del Servidor HTTP

El servidor MCP se configura con FastMCP usando transporte HTTP:

```python
from fastmcp import FastMCP
import asyncio

# Crear servidor MCP
mcp = FastMCP("Alejandria MCP Server")

# Ejecutar servidor HTTP
asyncio.run(mcp.run_http_async(host="0.0.0.0", port=8000))
```

**Parámetros de configuración**:

- `host="0.0.0.0"`: Escucha en todas las interfaces de red
- `port=8000`: Puerto donde se expone el servidor MCP

## Autenticación HTTP

El servidor implementa autenticación mediante API Keys para transporte HTTP:

- Validación de API key en cada request HTTP
- La API key se envía en el header `Authorization: Bearer <api_key>`
- Configuración mediante variable de entorno `MCP_API_KEY_REQUIRED`

## Estado de Implementación

✅ **Completado**: Migración a transporte HTTP exitosa
- Servidor MCP funcionando en `http://localhost:8000/mcp`
- Todas las herramientas MCP disponibles y funcionando
- Configuración actualizada en Devin IDE (Windsurf)
- Documentación actualizada

## Información Pendiente de Definir

Las siguientes secciones están marcadas como PENDIENTE y se definirán en fase de implementación:

- Cómo maneja la capa de abstracción MCP las características específicas de proveedores que pueden no estar estandarizadas entre diferentes proveedores LLM
- Patrones de integración FastMCP con FastAPI
- MCP tool unit testing patterns
- MCP tool testing coverage para edge cases

## Referencias

- [ADR-001: MCP como capa de abstracción](../decisiones/adr-001-mcp-abstraction-layer.md)
- [technology-stack.md](technology-stack.md): Stack tecnológico recomendado
