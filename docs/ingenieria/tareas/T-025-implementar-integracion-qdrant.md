---
id: T-025
type: Task
rating:
rating-phase:
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
- [ ] **GAP**: Estrategia de chunking para texto largo
- [ ] **GAP**: Metadata asociada a vectores para filtros
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

---

## Análisis de Documento

**ESTADO DEL ANÁLISIS**

- Análisis previo: NO
- Fecha del análisis: 2026-05-27
- Versión del análisis: 1
- Gaps pendientes: 5
- Gaps respondidos: 0
- Gaps NO APLICA: 0

**CLASIFICACIÓN DEL DOCUMENTO**

- Tipo: Documento de Proyecto (Task)
- Rol Principal: Desarrollador/Ingeniero
- Roles a Revisar: Desarrollador + Arquitecto + Gerente de Proyecto
- Enfoque: Implementación de integración con Qdrant y operaciones vectoriales
- Perspectiva: Senior + Junior
- Fecha de análisis: 2026-05-27
- Versión del análisis: 1

### Gaps Identificados

**IMPLEMENTACIÓN TÉCNICA**

**GAP: Configuración de modelo de embeddings (BGE-M3)** [PRIORIDAD: Alto] [ESTADO: PENDIENTE]

- **Pregunta**: La tarea menciona "Configuración de modelo de embeddings (BGE-M3)" como GAP. ¿BGE-M3 se ejecuta vía Ollama o API externa? ¿Cómo se configura? ¿Cuál es el endpoint o configuración específica?
- **Contexto faltante**: Detalles de configuración del modelo de embeddings BGE-M3, incluyendo si se ejecuta vía Ollama o API externa, y configuración específica.
- **Rol afectado**: Desarrollador Senior
- **Referencia**: Línea 30 del documento actual
- **Fecha de identificación**: 2026-05-27

**GAP: Estrategia de chunking para texto largo** [PRIORIDAD: Alto] [ESTADO: PENDIENTE]

- **Pregunta**: La tarea menciona "Estrategia de chunking para texto largo" como GAP. ¿Qué algoritmo de chunking se usa? ¿Tamaño máximo de chunk? ¿Superposición entre chunks? ¿Cómo se preserva estructura de secciones?
- **Contexto faltante**: Detalles de la estrategia de chunking, incluyendo algoritmo, tamaño de chunk, superposición, y preservación de estructura según especificación de búsqueda semántica.
- **Rol afectado**: Desarrollador Senior
- **Referencia**: Línea 31 del documento actual, busqueda-semantica.md
- **Fecha de identificación**: 2026-05-27

**GAP: Metadata asociada a vectores para filtros** [PRIORIDAD: Medio] [ESTADO: PENDIENTE]

- **Pregunta**: La tarea menciona "Metadata asociada a vectores para filtros" como GAP. ¿Qué metadata se almacena con cada vector? ¿Cómo se estructura? ¿Qué filtros se soportan?
- **Contexto faltante**: Detalles de la metadata asociada a vectores, incluyendo estructura, tipos de datos, y filtros soportados.
- **Rol afectado**: Desarrollador Senior
- **Referencia**: Línea 32 del documento actual
- **Fecha de identificación**: 2026-05-27

**GAP: Estrategia de actualización de vectores cuando documentos cambian** [PRIORIDAD: Alto] [ESTADO: PENDIENTE]

- **Pregunta**: La tarea menciona "Estrategia de actualización de vectores cuando documentos cambian" como GAP. ¿Se regeneran todos los embeddings del documento? ¿Solo cambios incrementales? ¿Cuándo se dispara? ¿Cómo se manejan documentos borrados?
- **Contexto faltante**: Detalles de la estrategia de actualización de vectores, incluyendo regeneración vs incremental, trigger de actualización, y manejo de documentos borrados.
- **Rol afectado**: Desarrollador Senior
- **Referencia**: Línea 33 del documento actual
- **Fecha de identificación**: 2026-05-27

**GESTIÓN DE PROYECTO**

**GAP: Criterios para estimación de esfuerzo** [PRIORIDAD: Bajo] [ESTADO: PENDIENTE]

- **Pregunta**: La tarea tiene una estimación de 5 horas. ¿Qué criterios se usaron para esta estimación? ¿Es basada en experiencia previa? ¿Referencias externas?
- **Contexto faltante**: Justificación de la estimación de esfuerzo para esta tarea específica.
- **Rol afectado**: Gerente de Proyecto
- **Referencia**: Línea 19 del documento actual
- **Fecha de identificación**: 2026-05-27
