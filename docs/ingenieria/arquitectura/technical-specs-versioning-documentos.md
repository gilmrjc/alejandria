---
id: TS-002
type: Technical Specification
dependency: [FEAT-006, FEAT-008, REQ-009]
related:
  - target: ARC-004
    relationship_type: implements
    reason: Implementa el schema de base de datos con especificación de versioning
---

# Especificación Técnica: Versioning de Documentos

Especificación técnica detallada para el sistema de versioning de documentos de Alejandría.

---

## Índice

1. [Visión General](#1-visión-general)
2. [Sistema de Snapshots](#2-sistema-de-snapshots)
3. [Comparación de Versiones](#3-comparación-de-versiones)
4. [Rollback](#4-rollback)
5. [Trazabilidad](#5-trazabilidad)
6. [Requisitos No Funcionales](#6-requisitos-no-funcionales)

---

## 1. Visión General

**Propósito:**

Mantener trazabilidad de cambios, permitir comparación entre versiones y facilitar reversión si es necesario.

**Contexto:**

Sistema de control de versiones para documentos con historial completo, comparación y rollback.

**Referencias:**

- [FEAT-006](../../producto/funcionalidades/versioning-documentos.md): Versioning de Documentos
- [FEAT-008](../../producto/funcionalidades/diff-viewer.md): Diff Viewer
- [REQ-009](../../producto/requisitos/.archived/requisitos-versioning-documentos.md): Requisitos archivados

---

## 2. Sistema de Snapshots

### Creación de Snapshots

**Trigger de creación:**

- Antes de cada UPDATE de documento
- Antes de cada DELETE de documento
- Manualmente (snapshot explícito solicitado por usuario)

**Estructura de snapshot:**

```yaml
snapshot_id: UUID
document_id: UUID
version_number: Integer
content: String (completo)
author: User ID
created_at: Timestamp
motivo: String (opcional)
metadata: Object
```

**Almacenamiento:**

- Tabla: `document_snapshots`
- Índices: document_id, created_at, version_number
- Compresión: GZIP para contenido > 10KB

### Compresión de Snapshots

**Estrategia:**

- Documentos < 1KB: Sin compresión
- Documentos 1KB - 10KB: Compresión GZIP (nivel 6)
- Documentos > 10KB: Compresión GZIP (nivel 9)

**Ratio de compresión esperado:** 70-80% para Markdown técnico

**Trade-off:** Compresión nivel 9 es más lenta pero ahorra más espacio

### Límite de Versiones

**Política de retención:**

- Últimas 50 versiones: Retención completa
- Versiones 51-100: Retención diaria (1 por día)
- Versiones > 100: Retención semanal (1 por semana)
- Máximo total: 200 versiones por documento

**Estrategia de purga:**

- Job nocturno que elimina versiones fuera de política
- Notificación al usuario antes de eliminar versiones antiguas
- Opción de marcar versiones como "permanent" (nunca se eliminan)

### Metadata de Snapshots

**Campos obligatorios:**

- `author`: ID de usuario que realizó el cambio
- `created_at`: Timestamp de creación
- `version_number`: Número secuencial de versión
- `motivo`: Motivo del cambio (manual o automático)

**Campos opcionales:**

- `related_gap_id`: ID del gap que motivó el cambio
- `related_proposal_id`: ID de la propuesta que generó el cambio
- `change_type`: Tipo de cambio (manual, auto_apply, rollback)
- `reviewer_id`: ID de usuario que aprobó el cambio (si aplica)

---

## 3. Comparación de Versiones

### Motor de Comparación

**Algoritmo:** Myers diff algorithm (implementación estándar en Git)

**Granularidad:**

- Línea por línea (default)
- Palabra por palabra (opcional para secciones cortas)
- Carácter por carácter (opcional para debugging)

**Resaltado de cambios:**

- Adiciones: Verde (+)
- Eliminaciones: Rojo (-)
- Modificaciones: Amarillo (~)
- Sin cambios: Sin resaltado

### Sincronización de Scroll

**Implementación:**

- Paneles lado a lado (left: versión anterior, right: versión nueva)
- Scroll sincronizado: scrolling en un panel afecta al otro
- Líneas correspondientes alineadas visualmente
- Highlight de línea activa en ambos paneles

**UX:**

- Botón de toggle para scroll sincronizado
- Scroll independiente disponible para comparación detallada
- Zoom同步 para documentos largos

### Navegación por Secciones

**Características:**

- Navegación por bloques de cambios (saltar al siguiente/anterior cambio)
- Contador de cambios totales (ej: "15 cambios encontrados")
- Resumen estadístico:
  - Líneas agregadas: X
  - Líneas eliminadas: Y
  - Líneas modificadas: Z

**Implementación:**

- Índice de cambios pre-calculado
- Atajos de teclado (Ctrl+G para siguiente, Ctrl+Shift+G para anterior)
- Panel lateral con lista de cambios clickeables

### Comparación Entre Cualquier Par de Versiones

**Interfaz:**

- Dropdowns para seleccionar versión A y versión B
- Visualización temporal (timeline) para selección visual
- Comparación no secuencial (ej: v5 vs v10, saltando v6-v9)

**Validación:**

- No permitir comparar versión consigo misma
- Orden cronológico: versión A debe ser anterior a versión B
- Warning si hay más de 50 versiones de diferencia

---

## 4. Rollback

### Sistema de Rollback

**Proceso de rollback:**

1. Usuario selecciona versión objetivo en historial
2. Sistema muestra diff entre versión actual y versión objetivo
3. Usuario confirma rollback
4. Sistema crea snapshot de versión actual (backup)
5. Sistema restaura contenido de versión objetivo
6. Sistema crea nuevo snapshot post-rollback
7. Sistema actualiza version_number del documento

**Validación antes de rollback:**

- Confirmación explícita del usuario (modal con diff)
- Verificación de que versión objetivo existe
- Verificación de que usuario tiene permisos de rollback
- Warning si hay cambios no guardados en documento actual

### Confirmación de Rollback

**Modal de confirmación:**

- Diff visual entre versión actual y versión objetivo
- Resumen de cambios que se revertirán
- Campo obligatorio: "Motivo del rollback"
- Opción: "Crear snapshot de versión actual antes de rollback" (default: true)

### Creación de Snapshot Post-Rollback

**Estructura especial:**

```yaml
snapshot_id: UUID
document_id: UUID
version_number: N+1
content: [versión restaurada]
author: User ID
created_at: Timestamp
motivo: "Rollback to version M"
rollback_from_version: M
metadata:
  change_type: "rollback"
  previous_snapshot_id: [snapshot de versión actual]
```

### Trazabilidad de Operaciones de Rollback

**Registro en tabla `rollback_operations`:**

```yaml
operation_id: UUID
document_id: UUID
from_version: Integer
to_version: Integer
author: User ID
created_at: Timestamp
motivo: String
pre_rollback_snapshot_id: UUID
post_rollback_snapshot_id: UUID
```

**Auditoría:**

- Todos los rollbacks son auditables
- Reporte de rollbacks por documento
- Reporte de rollbacks por usuario
- Alerta si hay más de 3 rollbacks en el mismo documento en 24h

---

## 5. Trazabilidad

### Registro de Autor de Cada Cambio

**Campo obligatorio en snapshot:**

- `author`: ID de usuario que realizó el cambio
- Para cambios automáticos: `system` como autor
- Para cambios por propuesta: ID de usuario que aprobó la propuesta

### Registro de Timestamp de Cada Cambio

**Precisión:** Milisegundos

**Zona horaria:** UTC (almacenamiento), local (display)

**Índice:** created_at para queries temporales eficientes

### Registro de Motivo de Cada Cambio

**Tipos de motivos:**

- Manual: "Edición manual por usuario"
- Auto_apply: "Aplicación automática de propuesta [proposal_id]"
- Rollback: "Rollback a versión [version_number]"
- Regeneration: "Regeneración de respuesta [question_id]"

**Campo obligatorio:** motivo no puede ser null

### Historial de Cambios por Documento

**Query:**

```sql
SELECT * FROM document_snapshots
WHERE document_id = :document_id
ORDER BY created_at DESC
LIMIT 50
```

**Display:**

- Timeline visual de cambios
- Filtros por tipo de cambio
- Filtros por autor
- Filtros por rango de fechas

### Historial de Cambios por Usuario

**Query:**

```sql
SELECT * FROM document_snapshots
WHERE author = :user_id
ORDER BY created_at DESC
LIMIT 100
```

**Display:**

- Lista de cambios realizados por usuario
- Agregación por documento
- Métricas: número de cambios por día/semana/mes

---

## 6. Requisitos No Funcionales

### Performance

**Creación de snapshot:**

- Tiempo máximo: 100ms para documentos < 10KB
- Tiempo máximo: 500ms para documentos 10KB - 100KB
- Tiempo máximo: 2s para documentos > 100KB

**Comparación de versiones:**

- Tiempo máximo para generar diff: 200ms para documentos < 10KB
- Tiempo máximo para generar diff: 1s para documentos 10KB - 100KB
- Tiempo máximo para renderizar diff visual: 300ms

**Rollback:**

- Tiempo máximo para realizar rollback: 500ms
- Tiempo máximo para crear snapshot post-rollback: 200ms

**Recuperación de historial:**

- Tiempo máximo para recuperar últimas 50 versiones: 100ms
- Tiempo máximo para recuperar historial completo: 500ms

### Escalabilidad

**Capacidad máxima de snapshots por documento:**

- Límite duro: 200 versiones por documento
- Límite blando: 50 versiones antes de aplicar retención diaria

**Estrategia de almacenamiento:**

- Compresión GZIP para reducir espacio
- Deduplicación de snapshots idénticos (si aplica)
- Particionamiento por document_id para queries eficientes

**Estimación de almacenamiento:**

- Promedio por snapshot: 5KB (comprimido)
- 200 snapshots por documento: 1MB
- 10,000 documentos: 10GB total

### Seguridad

**Control de acceso para operaciones de rollback:**

- Permisos requeridos: `document:rollback`
- Roles con permiso: Owner, Admin, Editor
- Audit log de todos los rollbacks

**Auditoría de cambios sensibles:**

- Rollbacks siempre auditados
- Cambios por propuestas siempre auditados
- Cambios masivos (múltiples documentos) siempre auditados

**Protección contra eliminación de snapshots:**

- Snapshots marcados como "permanent" no se eliminan automáticamente
- Eliminación manual requiere permiso `document:delete_snapshot`
- Confirmación requerida para eliminación manual

---

## Referencias

- [FEAT-006](../../producto/funcionalidades/versioning-documentos.md): Versioning de Documentos
- [FEAT-008](../../producto/funcionalidades/diff-viewer.md): Diff Viewer
- [REQ-009](../../producto/requisitos/.archived/requisitos-versioning-documentos.md): Requisitos archivados

---

*Documento generado integrando requisitos técnicos archivados con especificación de feature actual.*
