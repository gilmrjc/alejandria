---
id: ARC-021
type: Implementation Specification
rating: 9.5
rating-phase: document-editing
related:
  - target: ADR-006
    relationship_type: implements
    reason: Implementa la estrategia de versioning de documentos definida en ADR-006
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para implementación de snapshots
  - target: ARC-005
    relationship_type: references
    reason: "Referencia la especificación de API para endpoints de versioning (ver nota: ARC-005 es api-specification.md)"
  - target: ARC-019
    relationship_type: references
    reason: Referencia la estrategia de control de concurrencia para integración con SELECT FOR UPDATE
---

# Document Versioning Implementation — Alejandria

Este documento define la implementación específica del middleware de versioning automático de documentos según ADR-006.

## Índice

1. [Visión General](#1-visión-general)
2. [Arquitectura del Middleware](#2-arquitectura-del-middleware)
3. [Detección de Cambios](#3-detección-de-cambios)
4. [Creación de Snapshots](#4-creación-de-snapshots)
5. [Estrategia de Storage](#5-estrategia-de-storage)
6. [Implementación de Rollback](#6-implementación-de-rollback)
7. [Integración con Control de Concurrencia](#7-integración-con-control-de-concurrencia)
8. [Testing](#8-testing)

---

## 1. Visión General

### Propósito

Especificar la implementación del middleware que intercepta operaciones UPDATE en documentos y crea snapshots automáticos antes de cada modificación, permitiendo rollback a versiones anteriores.

### Referencia

Para la estrategia conceptual de versioning, ver [ADR-006: Versioning de Documentos](../decisiones/adr-006-document-versioning.md).

---

## 2. Arquitectura del Middleware

### Ubicación en el Stack

El middleware se implementa en la capa de aplicación (FastAPI) antes de que las operaciones lleguen a la base de datos.

### Componentes

El middleware se compone de cuatro componentes principales que trabajan en conjunto. El Interceptor de Operaciones detecta operaciones UPDATE en documentos, el Diff Engine compara el contenido anterior versus el nuevo, el Snapshot Manager crea snapshots cuando detecta cambios reales, y la Storage Strategy decide qué almacenar (full vs diff) según la configuración de retención.

### Implementación de Event Listeners

La captura del contenido anterior (`_old_content`) se implementa mediante SQLAlchemy event listeners. ADR-006 especifica el uso de `@event.listens_for(Document, 'before_update')` como mecanismo para capturar el estado del documento antes de que se ejecute la operación UPDATE. Este event listener permite acceder al contenido actual del documento antes de que sea modificado, lo cual es esencial para generar snapshots y detectar cambios.

### Justificación de Arquitectura

La implementación del versioning en código (middleware) en lugar de usar triggers de base de datos ofrece varias ventajas clave. Proporciona visibilidad al mantener la lógica de negocio visible en el código en lugar de oculta en triggers, permite mayor control sobre cuándo crear snapshots (por ejemplo, solo si el contenido realmente cambió), facilita el testing al ser más fácil de unit test que triggers, y ofrece flexibilidad para implementar lógica condicional compleja como la estrategia de storage basada en tiempo.

---

## 3. Detección de Cambios

### Algoritmo de Comparación

El middleware utiliza unified diff format estándar de Python (difflib.unified_diff) para snapshots tipo 'diff'. Este formato implementa el algoritmo de Myers y es ampliamente soportado, permite reconstrucción del contenido original, y se integra nativamente con el stack Python definido en ADR-002. Para snapshots de más de 30 días, se utiliza unified diff con contexto de líneas para optimizar storage. El diff incluye metadatos como líneas añadidas (+), líneas eliminadas (-), y contexto para reconstrucción, lo que permite aplicar el diff inverso durante rollback.

### Implementación de Hash para Detección de Cambios

Para detectar cambios de manera eficiente, el middleware calcula el hash del contenido usando MD5 vía `hashlib.md5(content.encode('utf-8')).hexdigest()`. MD5 es aproximadamente 3-4 veces más rápido que SHA-256 y la seguridad criptográfica no es requerida para este caso de uso de detección interna de cambios. La probabilidad de colisión es irrelevante en este contexto controlado. La implementación calcula el hash del contenido anterior y nuevo antes del UPDATE; si los hashes son iguales, no se crea snapshot, evitando así duplicados innecesarios.

### Ejemplo de Implementación de Unified Diff

El siguiente ejemplo muestra la implementación concreta de `difflib.unified_diff` para generar snapshots tipo 'diff':

```python
import difflib

def generate_unified_diff(old_content: str, new_content: str,
                          fromfile: str = "old", tofile: str = "new",
                          context_lines: int = 3) -> str:
    old_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        old_lines, new_lines,
        fromfile=fromfile, tofile=tofile,
        n=context_lines, lineterm='\n'
    )
    return ''.join(diff)
```

Los parámetros clave incluyen `n=3` para el contexto según ADR-006, `fromfile/tofile` para metadatos, `lineterm='\n'` para formato consistente, y `keepends=True` para preservar newlines para reconstrucción.

### Criterios para Crear Snapshot

El middleware solo crea snapshots cuando el contenido realmente ha cambiado, evitando así la creación de snapshots duplicados cuando no hay modificaciones. Para determinar si hubo un cambio, el sistema compara el hash del contenido anterior con el hash del nuevo contenido; si son iguales, no se crea ningún snapshot. Este enfoque optimiza el storage y asegura que cada snapshot represente una modificación real del documento.

---

## 4. Creación de Snapshots

### Proceso de Creación

El proceso de creación de snapshots sigue un flujo secuencial. Primero, el interceptor detecta una operación UPDATE en un documento. Luego, lee el contenido actual del documento y lo compara con el nuevo contenido proporcionado. Si se detecta un cambio real, crea un snapshot en la tabla `document_snapshots` con los campos document_id, old_content, new_content, diff_type, rating, y created_by. Este proceso se ejecuta dentro de la transacción de base de datos para asegurar consistencia.

### Tipos de Diff

- `full`: Snapshot completo del documento
- `diff`: Solo las diferencias (para optimización)

---

## 5. Estrategia de Storage

### Retención de Snapshots

- Últimos 30 días: snapshots completos
- Más de 30 días: snapshots comprimidos o eliminados
- Configurable según ADR-006

### Compresión

PostgreSQL TOAST comprime automáticamente TEXT fields con 80-90% de reducción en diffs. En PG14, LZ4 es 60-70% más rápido que PGLZ para compresión. La compresión es transparente y manejada completamente por PostgreSQL, por lo que no se requiere compresión manual a nivel de aplicación. Este mecanismo permite optimizar el storage sin añadir complejidad al código de aplicación.

---

## 6. Implementación de Rollback

### Proceso de Restauración

El proceso de restauración comienza cuando un usuario solicita rollback a un snapshot específico. El sistema lee el snapshot correspondiente de la tabla `document_snapshots`, restaura el contenido al documento, y crea un snapshot del estado actual antes de realizar la restauración para mantener un historial completo. Finalmente, actualiza los metadatos del documento (updated_by, updated_at) para registrar la operación de rollback.

### API Endpoints

- `POST /api/v1/documents/{id}/snapshots/{snapshot_id}/restore`

---

## 7. Integración con Control de Concurrencia

El middleware de versioning se integra con la estrategia de control de concurrencia definida en concurrency-control-strategy.md mediante el uso de SELECT FOR UPDATE. ADR-006 especifica que el middleware se ejecuta dentro de la transacción después de adquirir el lock con SELECT FOR UPDATE, manteniendo el lock durante toda la transacción (snapshot + UPDATE). Para operaciones de rollback, el orden de ejecución es: primero se adquiere el lock con SELECT FOR UPDATE, luego se valida la integridad del snapshot, y finalmente se actualiza el contenido. Este enfoque asegura que no haya condiciones de carrera durante la creación de snapshots o durante operaciones de rollback.

---

## 8. Testing

### Unit Tests

- Testing del interceptor de operaciones
- Testing del diff engine
- Testing del snapshot manager

### Integration Tests

- Testing de rollback end-to-end
- Testing de retención de snapshots
- Testing de compresión
