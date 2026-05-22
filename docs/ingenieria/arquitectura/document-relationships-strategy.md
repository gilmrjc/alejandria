---
id: ARC-009
type: Implementation Strategy
related:
  - target: ARC-004
    relationship_type: implements
    reason: Implementa el schema de base de datos con estrategia de relaciones
  - target: FEA-001
    relationship_type: implements
    reason: Implementa el workflow de 5 fases con estrategia de relaciones
  - target: FEA-005
    relationship_type: references
    reason: Referencia el 5-phase-workflow para detalles del workflow
---

# Document Relationships Strategy

## Contexto

La tabla `document_relationships` captura conexiones semánticas entre documentos para visualización de grafos, análisis de impacto y trazabilidad de dependencias. Este documento define la estrategia de implementación para generación, validación y uso de relaciones.

## Clasificación de Relaciones por Dirección

### Inflow vs Outflow

Las relaciones entre documentos se clasifican en dos categorías según la dirección del flujo de información:

**Outflow (A → B)**: Cambios en B afectan a A. El documento A depende o se ve impactado por B.

- `depends_on`: A depende de B (ej: ADR depende de technical-brief)
- `references`: A cita B sin dependencia fuerte (ej: "ver también")
- `implements`: A concreta B (ej: código implementa diseño)
- `supersedes`: A reemplaza B (ej: ADR v2 reemplaza ADR v1)
- `reinforces`: A refuerza B (ej: ejemplo valida principio)
- `contradicts`: A contradice B (ej: diseño vs implementación divergente)

**Inflow (A ← B)**: A aporta contexto a B. El documento A proporciona información adicional o contexto a B.

- `explains`: A explica conceptos de B (ej: tutorial explica ADR)
- `extends`: A deriva/extiende B (ej: deep dive de concepto general)

**Implicaciones para queries**:

- Para análisis de impacto, buscar outflow desde un documento (qué documentos se verían afectados si este cambia)
- Para contexto adicional, buscar inflow hacia un documento (qué documentos proporcionan contexto a este)
- La dirección se almacena explícitamente en el campo `direction` de la tabla `document_relationships` para facilitar queries eficientes

## Estrategia de Generación

### Fase MVP (Manual)

**Enfoque**: Creación manual de relaciones por usuarios con rol de Arquitecto Senior/CTO.

**Workflow**:

1. Usuario selecciona dos documentos en UI
2. Usuario selecciona tipo de relación del catálogo
3. Usuario escribe `reason` explicando la relación
4. Sistema valida que no exista duplicado (mismo source, target, type)
5. Sistema crea relación con `created_by` = usuario

**Justificación**: En MVP, la calidad de las relaciones es más importante que la cantidad. Creación manual asegura que las relaciones sean significativas y bien documentadas.

### Fase Post-MVP (LLM + Manual)

**Enfoque**: Detección automática por LLM con validación humana.

**Workflow**:

1. Durante Fase 1 (Detección), LLM analiza pares de documentos
2. LLM propone relaciones con `relationship_type` y `reason`
3. Propuestas se muestran en UI para aprobación/rechazo
4. Usuario puede modificar `reason` antes de aprobar
5. Relaciones aprobadas se crean con `created_by` = NULL (automático)

**Tipos de relaciones que LLM puede detectar**:

- `depends_on`: Analiza referencias, imports, dependencias técnicas
- `implements`: Compara diseño vs implementación
- `contradicts`: Detecta inconsistencias semánticas
- `supersedes`: Identifica versiones sucesivas

**Tipos que requieren intervención manual**:

- `explains`: Requiere juicio humano sobre qué es "explicación"
- `extends`: Requiere juicio sobre profundidad de extensión
- `reinforces`: Requiere juicio sobre validez de refuerzo
- `references`: LLM puede detectar, pero usuario debe validar relevancia

## Validación de Ciclos

### Tipos de Relación con Validación de Ciclos

| Tipo de Relación | ¿Prevenir ciclos? | Método de Validación              |
|------------------|-------------------|-----------------------------------|
| `depends_on`     | **SÍ**            | Query recursiva antes de INSERT   |
| `implements`     | **SÍ**            | Query recursiva antes de INSERT   |
| `references`     | NO                | Permitir ciclos                   |
| `explains`       | NO                | Permitir ciclos                   |
| `extends`        | NO                | Permitir ciclos                   |
| `supersedes`     | NO                | Imposible por definición temporal |
| `reinforces`     | NO                | Permitir ciclos                   |
| `contradicts`    | NO                | Permitir ciclos                   |

### Implementación de Validación

**Query recursiva para detectar ciclos en `depends_on` e `implements`:**

```sql
WITH RECURSIVE path AS (
  SELECT target_document_id, 1 as depth
  FROM document_relationships
  WHERE source_document_id = :new_source
  AND relationship_type IN ('depends_on', 'implements')
  
  UNION ALL
  
  SELECT dr.target_document_id, p.depth + 1
  FROM document_relationships dr
  JOIN path p ON dr.source_document_id = p.target_document_id
  WHERE dr.relationship_type IN ('depends_on', 'implements')
  AND p.depth < 100 -- previene loops infinitos
)
SELECT EXISTS(SELECT 1 FROM path WHERE target_document_id = :new_target)
```

**Validación en código (Python):**

```python
def create_relationship(source_id, target_id, rel_type, reason, created_by=None):
    # Validar ciclos solo para depends_on e implements
    if rel_type in ['depends_on', 'implements']:
        if has_cycle(source_id, target_id, rel_type):
            raise ValidationError(
                f"Ciclo detectado: {source_id} -> {target_id} ({rel_type}). "
                "Esto rompe análisis de impacto y debe resolverse manualmente."
            )
    
    # Validar auto-relación (excepto para reinforces/contradicts)
    if source_id == target_id and rel_type not in ['reinforces', 'contradicts']:
        raise ValidationError(
            f"Auto-relación no permitida para tipo {rel_type}"
        )
    
    # Validar duplicado
    if relationship_exists(source_id, target_id, rel_type):
        raise ValidationError(
            f"Relación ya existe: {source_id} -> {target_id} ({rel_type})"
        )
    
    # Insertar relación
    # ...
```

### Job Periódico de Detección

**Propósito**: Detectar ciclos que puedan haberse creado por bugs o migraciones.

**Frecuencia**: Diaria

**Query**:

```sql
-- Detecta todos los ciclos en depends_on e implements
WITH RECURSIVE cycles AS (
  -- query recursiva para detectar ciclos
)
SELECT * FROM cycles;
```

**Acción**: Alertar a administradores si se detectan ciclos.

## Propagación de Cambios

### Análisis de Impacto

**Cuando se modifica un documento B, identificar documentos afectados:**

```sql
-- Outflow: Documentos que dependen de B
SELECT dr.source_document_id, dr.relationship_type, dr.reason
FROM document_relationships dr
WHERE dr.target_document_id = :document_id
AND dr.relationship_type IN ('depends_on', 'implements', 'supersedes');

-- Inflow: Documentos que proporcionan contexto a B
SELECT dr.source_document_id, dr.relationship_type, dr.reason
FROM document_relationships dr
WHERE dr.target_document_id = :document_id
AND dr.relationship_type IN ('explains', 'extends');

-- Contradicciones: Documentos que contradicen B
SELECT dr.source_document_id, dr.reason
FROM document_relationships dr
WHERE dr.target_document_id = :document_id
AND dr.relationship_type = 'contradicts';
```

### Integración con Fase 5 (Aplicación)

**Workflow**:

1. Antes de aplicar cambios a documento B
2. Ejecutar análisis de impacto usando queries arriba
3. Mostrar al usuario lista de documentos afectados
4. Usuario puede aprobar cambios o cancelar
5. Si se aprueba, marcar documentos afectados para re-procesamiento en siguiente ciclo

### Priorización de Re-procesamiento

**Reglas**:

- Documentos con `depends_on` al documento modificado: Alta prioridad
- Documentos con `implements` al documento modificado: Alta prioridad
- Documentos con `contradicts` al documento modificado: Crítica (requiere intervención)
- Documentos con `explains` o `extends`: Baja prioridad

## Queries de Grafo para UI

### Grafo de Impacto (Outflow)

```sql
-- Subgrafo de dependencias desde documento raíz
WITH RECURSIVE impact_graph AS (
  SELECT source_document_id, target_document_id, relationship_type, reason, 0 as depth
  FROM document_relationships
  WHERE source_document_id = :root_document_id
  AND relationship_type IN ('depends_on', 'implements')
  
  UNION ALL
  
  SELECT dr.source_document_id, dr.target_document_id, dr.relationship_type, dr.reason, ig.depth + 1
  FROM document_relationships dr
  JOIN impact_graph ig ON dr.source_document_id = ig.target_document_id
  WHERE dr.relationship_type IN ('depends_on', 'implements')
  AND ig.depth < 5 -- límite de profundidad
)
SELECT * FROM impact_graph;
```

### Grafo Temporal (Supersedes)

```sql
-- Cadena de versiones
WITH RECURSIVE version_chain AS (
  SELECT source_document_id, target_document_id, reason, 0 as depth
  FROM document_relationships
  WHERE target_document_id = :current_document_id
  AND relationship_type = 'supersedes'
  
  UNION ALL
  
  SELECT dr.source_document_id, dr.target_document_id, dr.reason, vc.depth + 1
  FROM document_relationships dr
  JOIN version_chain vc ON dr.target_document_id = vc.source_document_id
  WHERE dr.relationship_type = 'supersedes'
  AND vc.depth < 10
)
SELECT * FROM version_chain ORDER BY depth;
```

### Grafo de Contradicciones

```sql
-- Componentes conectados por contradicciones
SELECT dr1.source_document_id as doc_a, 
       dr1.target_document_id as doc_b,
       dr1.reason as reason_a_to_b,
       dr2.reason as reason_b_to_a
FROM document_relationships dr1
JOIN document_relationships dr2 
  ON dr1.source_document_id = dr2.target_document_id 
  AND dr1.target_document_id = dr2.source_document_id
WHERE dr1.relationship_type = 'contradicts'
  AND dr2.relationship_type = 'contradicts';
```

### Filtrado por Tipo

```sql
-- Relaciones de un tipo específico
SELECT source_document_id, target_document_id, reason
FROM document_relationships
WHERE relationship_type = :relationship_type
AND (source_document_id = :doc_id OR target_document_id = :doc_id);
```

## Integración con las 5 Fases del Pipeline

### Fase 1: Detección

**Impacto de relaciones**:

- Priorizar detección en documentos con muchas dependencias (`depends_on`)
- Usar `contradicts` para detectar inconsistencias automáticamente
- Detectar automáticamente `supersedes` comparando versiones de documentos

**Query de priorización**:

```sql
-- Documentos con más dependencias (outflow)
SELECT d.id, d.title, COUNT(dr.id) as dependency_count
FROM documents d
LEFT JOIN document_relationships dr ON d.id = dr.source_document_id
  AND dr.relationship_type = 'depends_on'
WHERE d.project_id = :project_id
GROUP BY d.id, d.title
ORDER BY dependency_count DESC;
```

### Fase 2: Agrupación

**Impacto de relaciones**:

- Agrupar gaps de documentos relacionados por `depends_on`
- Usar `explains` para proporcionar contexto adicional al usuario

**Query de agrupación**:

```sql
-- Gaps en documentos que dependen de un documento específico
SELECT g.id, g.question, g.priority, d.title as document_title
FROM gaps g
JOIN documents d ON g.document_id = d.id
JOIN document_relationships dr ON d.id = dr.source_document_id
WHERE dr.target_document_id = :related_document_id
AND dr.relationship_type = 'depends_on'
ORDER BY g.priority DESC;
```

### Fase 3: Resolución

**Impacto de relaciones**:

- Mostrar documentos relacionados como contexto al resolver gaps
- Usar `reason` de relaciones para explicar por qué el contexto es relevante

**Query de contexto**:

```sql
-- Documentos relacionados al documento del gap
SELECT d.id, d.title, dr.relationship_type, dr.reason
FROM document_relationships dr
JOIN documents d ON 
  (dr.source_document_id = :gap_document_id AND d.id = dr.target_document_id)
  OR (dr.target_document_id = :gap_document_id AND d.id = dr.source_document_id)
ORDER BY 
  CASE dr.relationship_type
    WHEN 'depends_on' THEN 1
    WHEN 'implements' THEN 2
    WHEN 'explains' THEN 3
    ELSE 4
  END;
```

### Fase 4: Verificación

**Impacto de relaciones**:

- Verificar que `supersedes` no tiene contradicciones con versiones viejas
- Detectar nuevas contradicciones entre documentos relacionados
- Validar consistencia de `depends_on` después de cambios

**Query de verificación**:

```sql
-- Contradicciones entre documentos relacionados por depends_on
SELECT dr1.source_document_id as doc_a,
       dr2.target_document_id as doc_b,
       dr1.reason as depends_reason,
       c.reason as contradicts_reason
FROM document_relationships dr1
JOIN document_relationships dr2 ON dr1.target_document_id = dr2.source_document_id
JOIN document_relationships c ON dr1.source_document_id = c.source_document_id
  AND dr2.target_document_id = c.target_document_id
WHERE dr1.relationship_type = 'depends_on'
  AND dr2.relationship_type = 'depends_on'
  AND c.relationship_type = 'contradicts';
```

### Fase 5: Aplicación

**Impacto de relaciones**:

- Análisis de impacto antes de aplicar cambios
- Marcar documentos afectados para re-procesamiento
- Validar que cambios no rompen `depends_on` o `implements`

**Query de impacto**:

```sql
-- Documentos afectados por cambio en documento B
SELECT d.id, d.title, dr.relationship_type, dr.reason
FROM document_relationships dr
JOIN documents d ON dr.source_document_id = d.id
WHERE dr.target_document_id = :modified_document_id
AND dr.relationship_type IN ('depends_on', 'implements')
ORDER BY 
  CASE dr.relationship_type
    WHEN 'depends_on' THEN 1
    WHEN 'implements' THEN 2
  END;
```

## Monitoreo y Métricas

### Métricas Clave

- **Densidad de relaciones**: Número de relaciones / número de documentos
- **Tipos de relaciones más comunes**: Distribución por `relationship_type`
- **Documentos con más dependencias**: Top 10 por outflow
- **Documentos más influyentes**: Top 10 por inflow
- **Ciclos detectados**: Número de ciclos en `depends_on`/`implements` (debe ser 0)

### Query de Métricas

```sql
-- Densidad de relaciones por proyecto
SELECT 
  p.id as project_id,
  p.name as project_name,
  COUNT(d.id) as document_count,
  COUNT(dr.id) as relationship_count,
  ROUND(COUNT(dr.id)::numeric / NULLIF(COUNT(d.id), 0), 2) as density
FROM projects p
LEFT JOIN documents d ON p.id = d.project_id
LEFT JOIN document_relationships dr ON d.id = dr.source_document_id
GROUP BY p.id, p.name
ORDER BY density DESC;
```

## Referencias

- **[database-schema-design.md](database-schema-design.md)**: Definición de tabla `document_relationships`
- **[5-phase-workflow.md](../producto/5-phase-workflow.md)**: Pipeline de 5 fases
- **[ui-sections-specification.md](../producto/funcionalidades/ui-sections-specification.md)**: Sección de Grafo
