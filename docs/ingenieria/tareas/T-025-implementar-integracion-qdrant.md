---
id: T-025
type: Task
rating: 9
rating-phase: document-editing
related:
  - target: EPC-002
    relationship_type: implements
    reason: Implementa la épica de API REST y MCP Server con integración Qdrant
  - target: T-014
    relationship_type: depends_on
    reason: Depende de la estructura Python configurada en T-014 para integración Qdrant
---

# T-025: Implementar Integración con Qdrant

**Tipo**: Task
**Prioridad**: Alta
**Estimación**: 5 horas
**Dependencias**: EPC-002, T-014

## Descripción

Implementar cliente HTTP para comunicación con Qdrant y operaciones vectoriales. BGE-M3 se ejecuta vía Ollama para MVP bootstrapped (API externa para producción). Incluye estrategia de re-indexación incremental cuando documentos cambian.

## Criterios de Aceptación

- [ ] Cliente HTTP para API de Qdrant
- [ ] Funciones para crear colecciones, insertar vectores, buscar por similitud
- [ ] Estrategia de chunking para texto largo (máximo 256 tokens, superposición de 25 tokens, preserva estructura de secciones)
- [ ] Metadata asociada a vectores para filtros (obligatoria: document_id, question_id, author, created_at, updated_at, document_type, module; opcional: tags, priority, language)
- [ ] BGE-M3 configurado vía Ollama (API: `curl http://localhost:11434/api/embeddings -d '{"model": "bge-m3", "prompt": "texto"}'`)
- [ ] Estrategia de actualización de vectores implementada (trigger: evento de actualización de documento; re-indexación incremental: eliminar vectores existentes, aplicar chunking al contenido actualizado, generar embeddings, insertar vectores con metadata, actualizar vector_sync_log)

## Archivos a Crear

```
app/services/
  └── qdrant_service.py
```

## Referencias

- [TRD - Hito 2](../propuestas/trd-milestone-2-api-mcp.md): RF-010: Integration with Qdrant
- [Semantic Search](../../producto/funcionalidades/busqueda-semantica.md): Búsqueda Semántica

