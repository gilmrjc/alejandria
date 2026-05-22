---
id: TS-004
type: Technical Specification
related-features: [FEAT-009]
related-adrs: []
dependency: [FEAT-009, REQ-011]
related:
  - target: FEAT-009
    relationship_type: implements
    reason: Implementa la especificación técnica detallada del feature de dashboard general
  - target: REQ-011
    relationship_type: implements
    reason: Implementa los requisitos del dashboard general
---

# Especificación Técnica: Dashboard General

Especificación técnica detallada para el dashboard general de Alejandría.

---

## Índice

1. [Visión General](#1-visión-general)
2. [Resumen de Documentos](#2-resumen-de-documentos)
3. [Resumen de Gaps](#3-resumen-de-gaps)
4. [Resumen de Propuestas](#4-resumen-de-propuestas)
5. [Métricas de Progreso](#5-métricas-de-progreso)
6. [Navegación](#6-navegación)
7. [Requisitos No Funcionales](#7-requisitos-no-funcionales)

---

## 1. Visión General

**Propósito:**

Proporcionar punto de entrada claro para navegar el sistema y visibilidad del progreso general del proyecto.

**Contexto:**

Vista de alto nivel que unifica el estado del proyecto, mostrando documentos, gaps y métricas clave.

**Referencias:**

- [FEAT-009](../../producto/funcionalidades/dashboard-general.md): Dashboard General
- [REQ-011](../../producto/requisitos/.archived/requisitos-dashboard-general.md): Requisitos archivados

---

## 2. Resumen de Documentos

### Cálculo de Calificación Promedio

**Fórmula:**

```sql
SELECT AVG(rating) as avg_rating
FROM documents
WHERE project_id = :project_id
```

**Consideraciones:**

- Documentos sin rating (rating = NULL) se excluyen del promedio
- Redondeo a 1 decimal
- Caching del resultado (TTL: 5 minutos)

### Desglose de Documentos por Estado

**Estados:**

- `healthy`: rating >= 9
- `needs_improvement`: rating < 9
- `no_rating`: rating IS NULL

**Query:**

```sql
SELECT
  CASE
    WHEN rating >= 9 THEN 'healthy'
    WHEN rating < 9 THEN 'needs_improvement'
    ELSE 'no_rating'
  END as status,
  COUNT(*) as count
FROM documents
WHERE project_id = :project_id
GROUP BY status
```

### Desglose de Documentos por Tipo

**Tipos de documento:**

- ADR (Architecture Decision Record)
- PRD (Product Requirements Document)
- Feature
- Technical Spec
- Other

**Query:**

```sql
SELECT document_type, COUNT(*) as count
FROM documents
WHERE project_id = :project_id
GROUP BY document_type
ORDER BY count DESC
```

### Lista de Documentos Recientemente Actualizados

**Criterio:** Últimos 7 días

**Query:**

```sql
SELECT id, name, rating, updated_at
FROM documents
WHERE project_id = :project_id
  AND updated_at >= NOW() - INTERVAL '7 days'
ORDER BY updated_at DESC
LIMIT 10
```

**Display:**

- Nombre del documento
- Calificación actual
- Fecha de actualización
- Link al documento

---

## 3. Resumen de Gaps

### Conteo de Gaps por Prioridad

**Prioridades:**

- Alta
- Media
- Baja

**Query:**

```sql
SELECT priority, COUNT(*) as count
FROM gaps
WHERE project_id = :project_id
  AND status = 'pending'
GROUP BY priority
ORDER BY
  CASE priority
    WHEN 'alta' THEN 1
    WHEN 'media' THEN 2
    WHEN 'baja' THEN 3
  END
```

### Conteo de Gaps por Estado

**Estados:**

- `pending`: Detectado, esperando resolución
- `in_session`: En proceso de resolución
- `responded`: Respondido por usuario
- `rejected`: Rechazado por usuario

**Query:**

```sql
SELECT status, COUNT(*) as count
FROM gaps
WHERE project_id = :project_id
GROUP BY status
```

### Lista de Gaps de Alta Prioridad

**Criterio:** priority = 'alta' AND status = 'pending'

**Query:**

```sql
SELECT id, question, document_id, created_at
FROM gaps
WHERE project_id = :project_id
  AND priority = 'alta'
  AND status = 'pending'
ORDER BY created_at DESC
LIMIT 10
```

**Display:**

- Pregunta del gap
- Documento relacionado
- Fecha de detección
- Link al gap

### Tendencia de Gaps Resueltos en el Tiempo

**Granularidad:** Por día (últimos 30 días)

**Query:**

```sql
SELECT
  DATE(created_at) as date,
  COUNT(*) as resolved_count
FROM gaps
WHERE project_id = :project_id
  AND status = 'responded'
  AND created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date ASC
```

**Visualización:** Gráfico de línea mostrando tendencia

---

## 4. Resumen de Propuestas

### Conteo de Propuestas por Estado

**Estados:**

- `pending`: Generada, esperando aprobación
- `approved`: Aprobada por usuario
- `rejected`: Rechazada por usuario
- `applied`: Aplicada exitosamente
- `failed`: Falló la aplicación

**Query:**

```sql
SELECT status, COUNT(*) as count
FROM proposals
WHERE project_id = :project_id
GROUP BY status
```

### Lista de Propuestas Pendientes

**Criterio:** status = 'pending'

**Query:**

```sql
SELECT id, name, files_affected, created_at
FROM proposals
WHERE project_id = :project_id
  AND status = 'pending'
ORDER BY created_at DESC
LIMIT 10
```

**Display:**

- Nombre descriptivo
- Archivos afectados (count)
- Fecha de generación
- Link a la propuesta

### Tendencia de Propuestas Aplicadas en el Tiempo

**Granularidad:** Por día (últimos 30 días)

**Query:**

```sql
SELECT
  DATE(created_at) as date,
  COUNT(*) as applied_count
FROM proposals
WHERE project_id = :project_id
  AND status = 'applied'
  AND created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date ASC
```

**Visualización:** Gráfico de línea mostrando tendencia

---

## 5. Métricas de Progreso

### Definición de Métricas de Progreso

**Métricas principales:**

1. **Porcentaje de gaps resueltos:**
   - Fórmula: `(gaps_responded / total_gaps) * 100`
   - Objetivo: > 80%

2. **Porcentaje de documentos marcados como healthy:**
   - Fórmula: `(documents_healthy / total_documents) * 100`
   - Objetivo: > 70%

3. **Tiempo promedio de resolución de gaps:**
   - Fórmula: `AVG(resolved_at - created_at)` para gaps respondidos
   - Objetivo: < 48 horas

4. **Tasa de aceptación de propuestas:**
   - Fórmula: `(proposals_applied / total_proposals) * 100`
   - Objetivo: > 60%

### Porcentaje de Gaps Resueltos

**Query:**

```sql
SELECT
  (COUNT(CASE WHEN status = 'responded' THEN 1 END) * 100.0 / COUNT(*)) as percentage
FROM gaps
WHERE project_id = :project_id
```

**Display:** Gauge chart con porcentaje

### Porcentaje de Documentos Marcados como Healthy

**Query:**

```sql
SELECT
  (COUNT(CASE WHEN rating >= 9 THEN 1 END) * 100.0 / COUNT(*)) as percentage
FROM documents
WHERE project_id = :project_id
  AND rating IS NOT NULL
```

**Display:** Gauge chart con porcentaje

### Tiempo Promedio de Resolución de Gaps

**Query:**

```sql
SELECT
  AVG(EXTRACT(EPOCH FROM (resolved_at - created_at)) / 3600) as avg_hours
FROM gaps
WHERE project_id = :project_id
  AND status = 'responded'
  AND resolved_at IS NOT NULL
```

**Display:** Número en horas (ej: "24.5 horas")

---

## 6. Navegación

### Links a Secciones

**Secciones navegables:**

- Documentos (`/documents`)
- Preguntas (`/questions`)
- Gaps (`/gaps`)
- Propuestas (`/proposals`)
- Grafo (`/graph`)

**Implementación:**

- Botones prominentes en dashboard
- Iconos distintivos por sección
- Badges con conteos (ej: "Gaps (15)")

### Filtro por Módulo o Componente

**Selector de módulo:**

- Dropdown con lista de módulos del proyecto
- Opción "Todos los módulos" (default)
- Filtro aplica a todas las métricas del dashboard

**Query para módulos:**

```sql
SELECT DISTINCT module
FROM documents
WHERE project_id = :project_id
  AND module IS NOT NULL
ORDER BY module
```

### Filtro por Estado de Documento

**Estados filtrables:**

- Todos (default)
- Healthy
- Needs Improvement
- No Rating

**Implementación:**

- Tabs o toggle buttons
- Filtro aplica solo a sección de documentos

### Búsqueda Dentro del Dashboard

**Tipo de búsqueda:**

- Búsqueda global de documentos
- Búsqueda de gaps por pregunta
- Búsqueda de propuestas por nombre

**Implementación:**

- Search bar en header del dashboard
- Autocomplete para documentos
- Enter para ejecutar búsqueda

---

## 7. Requisitos No Funcionales

### Performance

**Tiempo máximo de carga del dashboard:**

- Métricas agregadas: 500ms
- Lista de documentos: 200ms
- Lista de gaps: 200ms
- Lista de propuestas: 200ms
- **Total:** < 1.5s

**Tiempo máximo de actualización de métricas:**

- Refresh manual: 1s
- Auto-refresh (cada 5 min): 1s

**Tiempo máximo de aplicación de filtros:**

- Filtro por módulo: 300ms
- Filtro por estado: 200ms
- Búsqueda: 500ms

### Usabilidad

**Claridad de presentación de métricas:**

- Uso de charts apropiados (gauge, line, bar)
- Labels claros y concisos
- Colores intuitivos (verde = bueno, rojo = malo)
- Tooltips con información adicional

**Facilidad de navegación a secciones:**

- Botones grandes y clickeables
- Iconos reconocibles
- Badges con conteos visibles
- Hover states claros

**Intuitividad de filtros:**

- Labels claros en dropdowns
- Opción de limpiar filtros
- Indicador visual de filtros activos
- Preservación de filtros en navegación

**Responsividad:**

- Mobile: Layout vertical, charts simplificados
- Tablet: Layout adaptativo, charts completos
- Desktop: Layout completo, todos los charts

### Actualización

**Frecuencia de actualización de métricas:**

- Auto-refresh: Cada 5 minutos
- Refresh manual: Botón de refresh
- Event-driven: Actualización inmediata cuando hay cambios

**Estrategia de actualización en tiempo real vs polling:**

- **MVP:** Polling cada 5 minutos
- **Futuro:** WebSockets para actualizaciones en tiempo real

**Notificaciones de cambios significativos:**

- Alerta cuando gaps de alta prioridad > 10
- Alerta cuando propuestas pendientes > 5
- Alerta cuando tiempo promedio de resolución > 72h

---

## Referencias

- [FEAT-009](../../producto/funcionalidades/dashboard-general.md): Dashboard General
- [REQ-011](../../producto/requisitos/.archived/requisitos-dashboard-general.md): Requisitos archivados

---

*Documento generado integrando requisitos técnicos archivados con especificación de feature actual.*
