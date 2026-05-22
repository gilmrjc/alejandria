---
id: ARC-037
type: Architecture
rating: 9.0
rating-phase: document-editing
related:
  - target: ARC-030
    relationship_type: implements
    reason: Implementa la arquitectura definida en mcp-server-architecture.md
  - target: ARC-036
    relationship_type: extends
    reason: Extiende la especificación de tools con detalles de consistencia y concurrencia
  - target: ADR-006
    relationship_type: implements
    reason: Implementa el versioning de documentos con transacciones ACID
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para transacciones y locking
---

# MCP Server Data Consistency & Concurrency — Alejandria

Este documento define las estrategias de consistencia de datos y concurrencia del MCP Server de Alejandria. Para la especificación de tools, ver [mcp-tools-specification.md](./mcp-tools-specification.md). Para la arquitectura general, ver [mcp-server-architecture.md](./mcp-server-architecture.md).

---

## 1. Transacciones y Consistencia

### Transacciones Explícitas

Las tools MCP usan transacciones explícitas de base de datos mediante SQLAlchemy (`async with db.begin()`). Cada tool invocation está envuelta en una transacción que garantiza atomicidad.

**Propiedades ACID**:

- **Atomicidad**: Si cualquier operación dentro de la transacción falla (ej: snapshot creation), se hace rollback automático de todas las operaciones
- **Consistencia**: Las reglas de negocio y constraints de base de datos se respetan en todo momento
- **Isolation**: Las transacciones están aisladas de otras transacciones concurrentes
- **Durability**: Los cambios son permanentes una vez que la transacción es commited

**Implementación**:

```python
async with db.begin():
    # Operaciones que deben ser atómicas
    document = await db.get(Document, document_id)
    snapshot = create_snapshot(document)
    document.content = new_content
    await db.flush()
    # Si algo falla aquí, rollback automático
```

**Casos de uso críticos**:

- `write_document`: Crear snapshot + actualizar documento debe ser atómico
- `create_gap`: Validar documento + crear gap debe ser atómico
- `apply_proposal`: Validar propuesta + aplicar cambios + actualizar estado debe ser atómico

---

## 2. Concurrencia

### Pessimistic Locking

El sistema usa pessimistic locking mediante `SELECT FOR UPDATE` de PostgreSQL para evitar conflictos de escritura concurrentes.

**Implementación**:

```python
# Adquirir lock exclusivo en documento
document = await session.query(Document).filter_by(id=document_id).with_for_update().one()
# Lock se libera automáticamente al commit de la transacción
```

**Comportamiento**:

- Cuando una tool invoca `write_document`, se bloquea el row del documento exclusivamente durante la transacción
- Esto garantiza que solo un writer pueda modificar el documento a la vez
- El lock se libera automáticamente al commit de la transacción
- Si otro proceso intenta escribir el mismo documento concurrentemente, espera hasta que el lock se libera

**Ventajas**:

- Evita conflictos de escritura (write-write conflicts)
- Garantiza que los cambios se aplican en orden secuencial
- Previene condiciones de carrera en operaciones críticas

**Trade-offs**:

- Puede causar espera si múltiples procesos intentan escribir el mismo documento
- Requiere gestión adecuada de timeouts para evitar deadlocks

**Mitigación**:

- Timeout configurado para locks (ej: 30 segundos)
- Logging de locks que exceden timeout para identificar cuellos de botella
- Estrategia de retry con backoff exponencial para locks fallidos

---

## 3. Validación de Parámetros

### Tipos de Datos y Restricciones

Se usa Pydantic para validación, alineado con schema de base de datos:

**Tipos de datos**:

- `document_id`: UUID string validado
- `include_metadata`: boolean
- `limit`: integer con rango
- `status`: enum string (pending/responded/rejected/etc)
- `priority`: enum string (low/medium/high/critical)

**Restricciones de longitud** (alineadas con schema PostgreSQL):

- `commit_message`: VARCHAR(255)
- `role_affected`: VARCHAR(100)
- `name` (tag): VARCHAR(100)
- `question`/`answer`/`context_missing`/`content`/`description`: TEXT (sin límite)

Pydantic valida automáticamente estos tipos y restricciones.

### Validación con FastMCP

FastMCP maneja validación automáticamente con Pydantic:

- Cada tool se define con type hints en los parámetros
- FastMCP genera automáticamente el JSON schema para el MCP client
- No se requiere validación manual adicional
- Los enums definidos en Pydantic (GapStatus, GapPriority, etc.) se validan automáticamente
- FastMCP expone el schema automáticamente al cliente MCP

**Ejemplo**:

```python
@mcp.tool()
async def read_document(document_id: str, include_metadata: bool = False) -> dict:
    # FastMCP valida automáticamente que document_id sea UUID string
    # FastMCP valida automáticamente que include_metadata sea boolean
    pass
```

---

## 4. Versioning y Consistencia

### Versioning Automático

Según ADR-006, el MCP Server implementa versioning automático de documentos mediante snapshots.

**Integración con transacciones**:

- La creación de snapshot es parte de la transacción de `write_document`
- Si el snapshot falla, toda la transacción se hace rollback
- Esto garantiza que nunca se actualice un documento sin snapshot previo

**Flujo transaccional**:

1. Iniciar transacción
2. Adquirir lock en documento
3. Crear snapshot del contenido anterior
4. Actualizar contenido del documento
5. Incrementar versión del documento
6. Commit transacción
7. Liberar lock

**Rollback de snapshots**:

La función `rollback_document` también usa transacciones para garantizar consistencia:

1. Iniciar transacción
2. Adquirir lock en documento
3. Verificar integridad del snapshot
4. Actualizar contenido con snapshot
5. Crear nuevo snapshot del rollback
6. Commit transacción
7. Liberar lock

---

## 5. Manejo de Errores

### Errores de Consistencia

**DocumentNotFoundError**: Documento no existe en base de datos

**VersionConflictError**: Documento fue modificado por otro proceso después de leerse

**PermissionDeniedError**: Usuario no tiene permisos para operar sobre el documento

**SnapshotCorruptedError**: Snapshot está corrupto o incompleto

### Estrategia de Retry

Para errores de consistencia transitorios (ej: locks temporales), el cliente LLM debe implementar retry con backoff exponencial según ADR-005.

El MCP Server retorna códigos de error JSON-RPC apropiados para que el cliente decida si reintentar:

- `-32603` (Internal Error): Error inesperado, puede ser seguro reintentar
- `-32000` (Server Error): Error del servidor, puede ser seguro reintentar
- `-32001` (Request Failed): Error específico de la request, revisar antes de reintentar

---

## Referencias

- [mcp-server-architecture.md](./mcp-server-architecture.md): Arquitectura general del MCP Server
- [mcp-tools-specification.md](./mcp-tools-specification.md): Especificación de tools
- [ADR-006](../decisiones/adr-006-document-versioning.md): Versioning de documentos
- [database-schema-design.md](./database-schema-design.md): Schema de base de datos
