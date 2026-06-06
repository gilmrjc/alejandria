---
name: document-critique-mcp
description: Document Critique MCP - Genera preguntas críticas sobre documentos en Alejandria identificando gaps en contexto, enfocándose en preguntas "cómo" y "por qué" con gestión idempotente de análisis previos. Usa las herramientas MCP de Alejandria para operar sobre documentos almacenados en la base de datos.
---

# Document Critique MCP

## Objetivos y Principios

**Propósito fundamental**: Generar preguntas críticas sobre documentos almacenados en Alejandria identificando gaps en contexto, asegurando que las preguntas fundamentales (cómo, por qué, qué, cuándo, quién, dónde) estén adecuadamente formuladas para los roles funcionales relevantes según el tipo de documento, aplicando una perspectiva dual por nivel de experiencia (senior y junior) con gestión idempotente para evitar generación infinita de preguntas.

**Diferencia con document-critique**: Este skill usa las herramientas MCP de Alejandria (`read_document`, `create_gap`, `list_gaps`, `create_tag`, `assign_tag_to_gap`) para operar sobre documentos almacenados en la base de datos de Alejandria, en lugar de operar directamente sobre archivos del sistema de archivos.

**Principios de validación**:
- **Idempotencia**: El proceso es idempotente - ejecuciones múltiples no generan preguntas duplicadas
- **Gestión de estado**: Cada gap tiene un estado explícito (pending, responded, rejected)
- **Detección de análisis previo**: Detecta si existe un análisis previo usando `list_gaps` para obtener gaps existentes
- **Deduplicación**: Compara nuevos gaps con existentes para evitar duplicados
- **Contexto de gaps previos**: Utiliza gaps respondidos y rechazados como contexto para evaluaciones posteriores
- **Enfoque multi-rol**: Atender las necesidades de diferentes roles funcionales según el tipo de documento (estratégico, producto, técnico, operaciones, usuario, etc.)
- **Perspectiva dual por nivel**: Aplicar simultáneamente la perspectiva senior (decisiones, contexto estratégico, impacto negocio/largo plazo) y junior (pros y contras fundamentales, conceptos de dominio, terminología, paso a paso)
- **Identificar gaps estratégicamente**: Enfocarse en preguntas "cómo" y "por qué" más que en detalles de implementación granulares
- **Detectar información fuera de scope**: Identificar cuando el documento contiene información que no corresponde a su tipo y propósito
- **Uso de herramientas MCP**: Todas las operaciones se realizan mediante herramientas MCP de Alejandria

**Cuando la información no esté disponible**: Si el código existe pero no hay documentación que explique el por qué, marca explícitamente este gap creando un gap con `create_gap`. El objetivo es identificar información faltante, no inventar respuestas.

## Estructura del Skill

Este skill utiliza una estructura modular para facilitar el mantenimiento y la navegación.

### Archivos Principales

- **`SKILL.md`**: Este archivo - Objetivos, principios y resumen del proceso
- **`reference/workflows.md`**: Índice de los pasos del proceso con enlaces a archivos detallados

### Archivos de Proceso (workflows/)

- **`workflows/00-detection.md`**: Detección de análisis previo usando `list_gaps`
- **`workflows/01-classification.md`**: Preparación y clasificación del documento
- **`workflows/02-gaps-validation.md`**: Evaluación de gaps previos
- **`workflows/03-validation.md`**: Validación de respuestas y consistencia por rol
- **`workflows/04-investigation.md`**: Investigación de referencias usando `search_similar_documents`
- **`workflows/05-identification.md`**: Identificación de contexto faltante por rol usando `create_gap`
- **`workflows/06-tagging.md`**: Agrupación de gaps usando `create_tag` y `assign_tag_to_gap`
- **`workflows/07-quality-evaluation.md`**: Evaluación de calidad y decisión de adición de gaps
- **`workflows/08-final-review.md`**: Revisión integrativa final

### Archivos de Referencia

- **`reference/classification.md`**: Tipos de documentos, roles funcionales y perspectivas de nivel de experiencia
- **`reference/priorities.md`**: Niveles de prioridad, categorías temáticas y criterios de consolidación
- **`reference/guardrails.md`**: Errores comunes, manejo de contradicciones y mejores prácticas
- **`reference/templates.md`**: Plantillas de formato para documentación de hallazgos
- **`reference/quality-criteria.md`**: Criterios detallados de calificación por nivel (1-10)
- **`reference/state-transitions.md`**: Diagrama de transiciones de estados de gaps
- **`reference/flowchart.md`**: Diagrama de flujo visual del proceso completo
- **`reference/troubleshooting.md`**: Guía de troubleshooting para casos borde
- **`reference/idempotency.md`**: Gestión de idempotencia y detección de análisis previo
- **`reference/io-expectations.md`**: Expectativas de entrada y salida del skill
- **`reference/mcp-tools.md`**: Referencia de herramientas MCP disponibles

## Herramientas MCP Utilizadas

Este skill utiliza las siguientes herramientas MCP de Alejandria:

- **`read_document`**: Leer el contenido del documento desde la base de datos (usa document_slug)
- **`list_gaps`**: Obtener gaps existentes para un documento (usa document_slug)
- **`create_gap`**: Crear nuevos gaps identificados (usa document_slug, genera gap_slug automáticamente)
- **`create_tag`**: Crear tags para agrupación temática (genera tag_slug automáticamente)
- **`assign_tag_to_gap`**: Asignar tags a gaps para agrupación (usa gap_slug y tag_slug)
- **`list_gaps_by_tag`**: Listar gaps por tag para verificación (usa tag_slug)
- **`search_similar_documents`**: Buscar documentos similares para investigación de referencias

## Proceso

El proceso sigue un enfoque sistemático que incluye: (1) detección de análisis previo usando `list_gaps`, (2) preparación y clasificación del documento usando `read_document`, (3) evaluación de gaps previos si aplica, (4) validación de respuestas y consistencia por rol, (5) investigación de referencias usando `search_similar_documents`, (6) identificación de contexto faltante por rol usando `create_gap`, (7) agrupación de gaps usando `create_tag` y `assign_tag_to_gap`, (8) evaluación de calidad y decisión de adición de gaps, y (9) revisión final integradora.

Para instrucciones detalladas paso a paso, consulta **`reference/workflows.md`**.

### Criterios de Terminación

El proceso termina cuando:
- Se ha detectado y validado el análisis previo (si existe) usando `list_gaps`
- Se ha clasificado el documento y determinado roles funcionales y perspectivas
- Se han evaluado todos los gaps previos actualizando sus estados según corresponda
- Se han validado respuestas y consistencia cruzada para cada rol funcional (mínimo 2-3 roles)
- Se han investigado documentos similares usando `search_similar_documents` para cada rol funcional
- Se han identificado nuevos gaps con deduplicación contra existentes aplicando preguntas clave usando `create_gap`
- Se han agrupado gaps temáticamente usando `create_tag` y `assign_tag_to_gap`
- Se ha calificado el documento (1-10) con desglose por criterios
- Se ha decidido si los gaps se agregan (calificación < 9) o solo se documentan en el análisis (calificación ≥ 9)
- Se ha verificado cobertura multi-rol, consistencia de perspectiva dual, y ausencia de contradicciones

### Resumen de Pasos

1. **Detección de Análisis Previo**: Usar `list_gaps` para determinar si existen gaps previos y validar su vigencia
2. **Preparación y Clasificación**: Usar `read_document` para leer el documento, determinar tipo, rol funcional principal, y perspectivas (ver `reference/classification.md`)
3. **Evaluación de Gaps Previos**: Si existen gaps previos, validar su estado, buscar respuestas, y actualizar según corresponda
4. **Validación de Respuestas y Consistencia**: Para cada rol funcional (mínimo 2-3), validar respuestas existentes y consistencia cruzada entre fuentes
5. **Investigación de Referencias**: Para cada rol funcional, usar `search_similar_documents` para revisar documentos similares y documentar hallazgos
6. **Identificación de Contexto Faltante**: Para cada rol funcional, identificar contexto faltante aplicando preguntas clave (cómo/por qué/qué/cuándo/quién/dónde) y crear gaps usando `create_gap`
7. **Agrupación de Gaps**: Crear tags usando `create_tag` y asignarlos a gaps usando `assign_tag_to_gap` para agrupación temática
8. **Evaluación de Calidad y Decisión de Adición de Gaps**: Calificar el documento (1-10) y decidir si los gaps deben agregarse
9. **Revisión Final**: Verificar cobertura multi-rol, consistencia de perspectiva dual, contradicciones, y criterios de terminación

## Gestión de Idempotencia

Para detalles sobre gestión de idempotencia, consultar `reference/idempotency.md`.

## Expectativas de Entrada/Salida

Para detalles sobre expectativas de entrada y salida, consultar `reference/io-expectations.md`.

## Uso

Invoca este skill al revisar documentos almacenados en Alejandria para generar preguntas críticas de forma idempotente. El skill ayudará a mantener la calidad de documentación asegurando que todas las preguntas "cómo" y "por qué" sean abordadas, evitando generación infinita de preguntas mediante gestión de estado y deduplicación usando las herramientas MCP de Alejandria.

**Entrada esperada**:
- `document_slug`: Slug del documento en Alejandria

**Salida esperada**:
- Gaps creados en la base de datos usando `create_gap`
- Tags creados y asignados usando `create_tag` y `assign_tag_to_gap`
- Calificación del documento evaluada

## Instrucción de Lista de Tareas

**ANTES DE COMENZAR**: Debes crear una lista de tareas utilizando la herramienta `todo_list` con cada paso a ejecutar y su descripción. Esta lista debe incluir:

- **Todos los pasos del proceso** (pasos 1-9) con descripciones claras
- **Estado inicial**: Marcar el primer paso como "in_progress" y los demás como "pending"
- **Prioridades**: Asignar prioridad "high" a pasos críticos, "medium" a pasos importantes
- **Actualización continua**: Marcar cada tarea como "completed" inmediatamente después de terminarla
- **Visibilidad**: Esto permite tener claro qué se debe hacer antes de empezar y seguimiento del progreso

**Ejemplo de estructura de tareas**:
1. Detección de Análisis Previo - Usar list_gaps para determinar si existe un análisis previo y validar su vigencia
2. Preparación y Clasificación - Usar read_document para leer el documento, determinar tipo, roles funcionales y perspectivas
3. Evaluación de Gaps Previos - Validar estado de gaps existentes y actualizar según corresponda
4. Validación de Respuestas y Consistencia - Para cada rol funcional, validar respuestas y consistencia cruzada
5. Investigación de Referencias - Para cada rol funcional, usar search_similar_documents para revisar documentos similares
6. Identificación de Contexto Faltante - Para cada rol funcional, identificar contexto faltante con preguntas clave y crear gaps usando create_gap
7. Agrupación de Gaps - Crear tags y asignarlos a gaps para agrupación temática
8. Evaluación de Calidad y Decisión - Calificar documento y decidir adición de gaps
9. Revisión Final - Verificar cobertura multi-rol, consistencia y criterios de terminación

## Referencias Adicionales

Para detalles específicos sobre:

- **Clasificación de documentos y roles**: Consulta `reference/classification.md`
- **Priorización y categorización de gaps**: Consulta `reference/priorities.md`
- **Errores comunes y mejores prácticas**: Consulta `reference/guardrails.md`
- **Manejo de contradicciones**: Consulta `reference/guardrails.md`
- **Plantillas de formato**: Consulta `reference/templates.md`
- **Gestión de idempotencia**: Consulta `reference/idempotency.md`
- **Expectativas de entrada/salida**: Consulta `reference/io-expectations.md`
- **Herramientas MCP disponibles**: Consulta `reference/mcp-tools.md`
