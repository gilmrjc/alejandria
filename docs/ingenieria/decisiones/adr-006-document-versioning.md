---
id: ADR-006
type: Architecture Decision Record
rating: 9.5
rating-phase: document-editing
related:
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para tabla document_snapshots
  - target: ADR-002
    relationship_type: implements
    reason: Implementa el stack unificado Python con middleware de versioning
  - target: ADR-005
    relationship_type: extends
    reason: Extiende las decisiones de arquitectura con estrategia de versioning específica
---

# ADR-006: Versioning de Documentos

## Contexto y Problema

Alejandria aplica cambios automáticos a la documentación mediante agentes LLM. Sin un sistema de versioning, el sistema tendría:

- **Irreversibilidad de cambios**: Si un agente hace un cambio incorrecto, no hay forma de revertir
- **Pérdida de historial**: No se puede rastrear qué cambios se hicieron ni cuándo
- **Falta de audit trail**: Imposible determinar quién o qué causó un cambio específico
- **Riesgo de degradación**: Cambios incorrectos pueden degradar la calidad de la documentación sin posibilidad de recuperación

El problema es crítico porque los agentes LLM pueden cometer errores (alucinaciones, malinterpretación de contexto) y los usuarios necesitan confianza en que pueden revertir cambios si algo sale mal.

## Decisiones

**Decisión**: Crear snapshot automático antes de cada UPDATE en `documents.content`.

**Implementación específica**:

- Middleware en código (Python/SQLAlchemy) que captura el estado actual antes de cada UPDATE
  - Implementación usando SQLAlchemy event listeners: `@event.listens_for(Document, 'before_update')`
  - Verificación de cambio de contenido antes de crear snapshot (evita snapshots duplicados)
  - Garantiza transacción atómica entre snapshot y UPDATE
- Almacenamiento de snapshots en tabla `document_snapshots` con:
  - `id`: Primary key
  - `document_id`: Foreign key a documents (CASCADE DELETE)
  - `old_content`: Contenido anterior (TEXT, NULL para primera versión)
  - `new_content`: Contenido nuevo (TEXT, diff o snapshot completo)
  - `diff_type`: Tipo de snapshot ('full' o 'diff')
    - Formato de diff: Unified diff format con contexto de 3 líneas usando Myers algorithm (Python difflib.unified_diff)
    - El diff incluye metadatos: líneas añadidas (+), líneas eliminadas (-), y contexto para reconstrucción
    - Para rollback: aplicar el diff inverso al contenido actual para reconstruir el estado original
  - `rating`: Rating del documento en este snapshot
  - `created_at`: Timestamp del snapshot
  - `created_by`: Foreign key a users (SET NULL)
  - Índices en document_id y created_at para optimizar queries de rollback y cleanup
- Estrategia de retención: Configurable via `system_settings.retention_days` (default: 5 años según database-schema-design.md)
- Capacidad de rollback: Función para restaurar un snapshot específico
  - Firma: `rollback_document(document_id: int, snapshot_id: int) -> bool`
  - Flujo transaccional:
    1. Iniciar transacción con BEGIN
    2. Adquirir lock pessimistic en documento: `session.query(Document).filter_by(id=document_id).with_for_update().one()`
    3. Verificar integridad del snapshot (validar que old_content no es NULL)
    4. Actualizar documents.content con el contenido del snapshot
    5. Crear nuevo snapshot del rollback (old_content = contenido actual, new_content = contenido restaurado)
    6. Commit transacción
  - Manejo de errores:
    - Si snapshot está corrupto: rollback transacción, loggear error, retornar False
    - Si documento fue modificado después del snapshot: validar versión, si mismatch retornar False
    - Logging: registrar todas las operaciones de rollback con timestamp y usuario
  - Consideraciones de concurrencia:
    - Lock adquirido durante toda la operación de rollback
    - Validación de que no hay cambios pendientes antes de proceder
- Función helper para actualizar `updated_at` automáticamente en cada UPDATE

## Análisis de Performance

**Impacto esperado en latencia de cada UPDATE**:

- Overhead estimado: SQLAlchemy before_update (<1ms) + PostgreSQL INSERT con TOAST (5-15ms para 50KB) = 6-16ms total
- Mitigación: solo snapshot si contenido cambió, TOAST compresión automática (LZ4 60-70% más rápido en PG14), estrategia híbrida (30 días full, >30 días diff)
- Criterios de aceptación: <20ms por UPDATE, <5% tiempo total

**Referencias**: pganalyze.com (TOAST performance), hakibenita.com (medium text performance), SQLAlchemy docs (event listeners)

## Análisis de Storage

**Estimación cuantitativa del overhead de storage**:

- Basado en benchmarks de TOAST (PGLZ ratio 2.23, LZ4 ratio 2.07)
- Documento promedio 50KB, 10 cambios/día:
  - Últimos 30 días (full): 15MB/documento
  - >30 días (diff comprimido 52%): 43.68MB/documento para 5 años
- Total: ~58.68MB/documento con 5 años de retención
- Escala lineal con número de documentos y frecuencia de cambios

**Referencias**: PostgreSQL Fastware (LZ4 vs PGLZ benchmarks), Microsoft Learn (SharePoint versioning storage)

## Justificación

### Beneficios del Versioning Automático

**Reversibilidad de cambios de agentes LLM**:

- Si un agente hace un cambio incorrecto, podemos revertir al snapshot anterior
- Permite experimentación con cambios sin riesgo permanente
- Los usuarios pueden revisar cambios antes de aceptarlos definitivamente

**Audit trail completo**:

- Tenemos historial completo de todos los cambios
- Podemos rastrear qué job o usuario causó cada cambio
- Facilita debugging de problemas en detección/aplicación de cambios

**Protección contra malas sugerencias**:

- Los cambios se pueden revisar antes de aceptarlos definitivamente
- Permite identificar patrones de errores en agentes LLM
- Proporciona datos para mejorar calidad de detección y aplicación

### Alineación con Valores Organizacionales

Versioning de documentos implementa el valor de "Verificación Iterativa" al permitir revertir cambios si se detectan errores. Esto asegura que la documentación mejore iterativamente sin riesgo de degradación.

También implementa "Calidad Automática" al proporcionar un mecanismo de seguridad que mantiene la calidad sin supervisión manual constante.

## Trade-offs

### Desventajas

- **Storage adicional**: Snapshots duplican contenido de documentos, aumentando storage
- **Complejidad de implementación**: Requiere middleware en código y tabla adicional
- **Performance overhead**: Capturar snapshot antes de cada UPDATE añade latencia
- **Costo de mantenimiento**: Estrategia de retención y cleanup requiere gestión

### Mitigación

- **Compresión de snapshots**: PostgreSQL TOAST comprime automáticamente TEXT fields (80-90% reducción en diffs)
- **Estrategia de storage híbrida**: Últimos 30 días snapshots completos ('full'), >30 días diffs comprimidos ('diff')
- **Retención configurable**: Mantener snapshots por 5 años por defecto (configurable via system_settings.retention_days)
- **Cleanup automático**: Job periódico para eliminar snapshots antiguos según retención configurada
- **Optimización de middleware**: Usar SQLAlchemy event listeners eficientes para minimizar overhead

## Alternativas Consideradas

### Sin Versioning (Updates Directos)

**Ventaja**: Menor complejidad, menor storage, menor overhead

**Desventaja**: Irreversibilidad de cambios, falta de audit trail, riesgo de degradación permanente

**Decisión**: Rechazada porque el riesgo de cambios incorrectos por agentes LLM es inaceptable sin mecanismo de reversión.

### Versioning Manual (Git-style)

**Ventaja**: Control manual de cuándo crear versiones, menor storage

**Desventaja**: Requiere intervención manual, no es automático, propenso a errores humanos

**Decisión**: Rechazada porque el objetivo es automatización completa; versioning manual contradice el principio de "Calidad Automática".

### Versioning con Herramientas Externas (Git Integration)

**Ventaja**: Aprovecha herramientas maduras como Git, audit trail robusto

**Desventaja**: Complejidad de integración, requiere repositorio Git externo, overhead de sincronización

**Decisión**: Rechazada para fase bootstrapped porque versioning en base de datos es más simple y proporciona suficiente funcionalidad. Git integration puede considerarse en fase post-MVP para integración con workflows existentes.

## Consecuencias

### Impacto Positivo

- **Seguridad**: Capacidad de revertir cambios incorrectos
- **Transparencia**: Audit trail completo de todos los cambios
- **Confianza**: Los usuarios pueden confiar en que los cambios son reversibles
- **Debugging**: Facilita identificación de problemas en agentes LLM

### Impacto Negativo

- **Storage**: Snapshots duplican contenido, aumentando storage
- **Complejidad**: Requiere tabla adicional y middleware en código
- **Performance**: Overhead en cada UPDATE de documento
- **Mantenimiento**: Estrategia de retención y cleanup requiere gestión

### Requerimientos de Implementación

- Tabla `document_snapshots` con campos: id, document_id, old_content, new_content, diff_type, rating, created_at, created_by
- Middleware SQLAlchemy event listener para capturar snapshot antes de cada UPDATE en `documents.content`
- Función helper para actualizar `updated_at` automáticamente en cada UPDATE
- Función de rollback para restaurar snapshot específico
- Job periódico para cleanup de snapshots antiguos según retención configurada
- Estrategia de storage híbrida: últimos 30 días snapshots completos ('full'), >30 días diffs comprimidos ('diff')
- Monitoreo de storage de snapshots
- Estrategia de manejo de concurrencia: Pessimistic locking usando SQLAlchemy `with_for_update()`
  - Implementación: `session.query(Document).filter_by(id=document_id).with_for_update().one()`
  - Configuración de timeout: 5 segundos para adquisición de lock
  - Estrategia de re-intento con backoff exponencial:
    - 3 reintentos máximos
    - Delays: 100ms, 500ms, 1000ms
    - Si falla después de 3 reintentos, retornar error de concurrencia
  - Manejo de deadlock detection:
    - PostgreSQL detecta deadlocks automáticamente y retorna error
    - En caso de deadlock, rollback transacción y reintentar con backoff
  - Consideraciones para alta concurrencia:
    - El lock se mantiene durante toda la transacción (snapshot + UPDATE)
    - Minimizar tiempo de lock: validar cambios antes de adquirir lock
    - Monitorear frecuencia de deadlocks para ajustar timeout si necesario

## Referencias

- architecture-overview.md: Sección "Versioning de Documentos"
- technology-strategy.md: Sección "Componentes Principales" (Base de datos)
- database-schema-design.md: Sección "document_snapshots" (schema detallado, estrategia de storage híbrida)
- T-006: Implementar middleware de versioning en código
