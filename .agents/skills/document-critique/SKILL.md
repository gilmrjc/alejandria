---
name: document-critique
description: Document Critique - Genera preguntas críticas sobre cualquier tipo de documento identificando gaps en contexto, enfocándose en preguntas "cómo" y "por qué" con gestión idempotente de análisis previos. Adaptable a documentos estratégicos, de producto, técnicos, manuales de usuario, procesos, y cualquier otro tipo de documentación.
---

# Document Critique

## Objetivos y Principios

**Propósito fundamental**: Generar preguntas críticas sobre cualquier tipo de documento identificando gaps en contexto, asegurando que las preguntas fundamentales (cómo, por qué, qué, cuándo, quién, dónde) estén adecuadamente formuladas para los roles funcionales relevantes según el tipo de documento, aplicando una perspectiva dual por nivel de experiencia (senior y junior) con gestión idempotente para evitar generación infinita de preguntas.

**Principios de validación**:
- **Idempotencia**: El proceso es idempotente - ejecuciones múltiples no generan preguntas duplicadas
- **Gestión de estado**: Cada gap tiene un estado explícito ([PENDIENTE], [RESPONDIDO], [NO APLICA], [OBSOLETO])
- **Detección de análisis previo**: Detecta si existe un análisis previo y valida su vigencia
- **Deduplicación**: Compara nuevos gaps con existentes para evitar duplicados
- **Contexto de gaps previos**: Utiliza gaps respondidos y marcados como [NO APLICA] como contexto para evaluaciones posteriores
- **Enfoque multi-rol**: Atender las necesidades de diferentes roles funcionales según el tipo de documento (estratégico, producto, técnico, operaciones, usuario, etc.)
- **Perspectiva dual por nivel**: Aplicar simultáneamente la perspectiva senior (decisiones, contexto estratégico, impacto negocio/largo plazo) y junior (pros y contras fundamentales, conceptos de dominio, terminología, paso a paso)
- **Priorizar documentación fuente**: La documentación es la fuente de razones y decisiones (el código implementa pero no explica el por qué; para documentos no técnicos, las fuentes relevantes varían según el tipo de documento)
- **Identificar gaps estratégicamente**: Enfocarse en preguntas "cómo" y "por qué" más que en detalles de implementación granulares
- **Detectar información fuera de scope**: Identificar cuando el documento contiene información que no corresponde a su tipo y propósito (ej. detalles de implementación en un PRD, decisiones de negocio en un documento de arquitectura técnica, etc.)
- **Referencias fuente específicas**: Proporcionar URLs de GitHub, commits para cada pieza de información agregada
- **Mantener estructura original**: Preservar estructura y formato de la documentación original al agregar contexto
- **Documentar en el mismo archivo**: Las sugerencias, gaps identificados y referencias deben documentarse dentro del mismo archivo analizado
- **Documentar contradicciones**: Identificar y documentar contradicciones entre fuentes cuando se identifiquen

**Cuando la información no esté disponible**: Si el código existe pero no hay documentación que explique el por qué, marca explícitamente este gap. El objetivo es identificar información faltante, no inventar respuestas.

## Estructura del Skill

Este skill utiliza una estructura modular para facilitar el mantenimiento y la navegación. Los componentes detallados se encuentran en:

### Archivos Principales

- **`SKILL.md`**: Este archivo - Objetivos, principios y resumen del proceso
- **`references/classification.md`**: Tipos de documentos, roles funcionales y perspectivas de nivel de experiencia
- **`references/workflows.md`**: Índice de los pasos del proceso con enlaces a archivos detallados

### Scripts de Apoyo

- **`scripts/detect_relations.py`**: Script para detectar y validar relaciones entre documentos (campo `related` del frontmatter). Útil en el Paso 4 de investigación para:
  - Identificar automáticamente archivos relacionados del documento
  - Validar que los targets de las relaciones existan en el repositorio
  - Obtener información estructurada de relaciones para facilitar la investigación

**Uso del script**:
```bash
python .agents/skills/document-critique/scripts/detect_relations.py <ruta-del-archivo>
```

Ejemplo:
```bash
python .agents/skills/document-critique/scripts/detect_relations.py docs/ingenieria/arquitectura/database-schema-design.md
```

### Archivos de Proceso (workflows/)

- **`workflows/00-detection.md`**: Detección de análisis previo
- **`workflows/01-classification.md`**: Preparación y clasificación del documento
- **`workflows/02-gaps-validation.md`**: Evaluación de gaps previos
- **`workflows/03-validation.md`**: Validación de respuestas y consistencia por rol
- **`workflows/04-investigation.md`**: Investigación de referencias por rol
- **`workflows/05-identification.md`**: Identificación de contexto faltante por rol
- **`workflows/06-quality-evaluation.md`**: Evaluación de calidad y decisión de adición de gaps
- **`workflows/07-final-review.md`**: Revisión integrativa final

### Archivos de Referencia

- **`references/priorities.md`**: Niveles de prioridad, categorías temáticas y criterios de consolidación
- **`references/guardrails.md`**: Errores comunes, manejo de contradicciones y mejores prácticas
- **`references/templates.md`**: Plantillas de formato para documentación de hallazgos con estados de gaps
- **`references/quality-criteria.md`**: Criterios detallados de calificación por nivel (1-10)
- **`references/state-transitions.md`**: Diagrama de transiciones de estados de gaps
- **`references/flowchart.md`**: Diagrama de flujo visual del proceso completo
- **`references/troubleshooting.md`**: Guía de troubleshooting para casos borde
- **`references/idempotency.md`**: Gestión de idempotencia y detección de análisis previo
- **`references/io-expectations.md`**: Expectativas de entrada y salida del skill

## Proceso

El proceso sigue un enfoque sistemático que incluye: (1) detección de análisis previo, (2) preparación y clasificación del documento, (3) evaluación de gaps previos si aplica, (4) validación de respuestas y consistencia por rol, (5) investigación de referencias por rol, (6) identificación de contexto faltante por rol, (7) evaluación de calidad y decisión de adición de gaps, y (8) revisión final integradora.

Para instrucciones detalladas paso a paso, consulta **`references/workflows.md`**.

### Criterios de Terminación

El proceso termina cuando:
- Se ha detectado y validado el análisis previo (si existe)
- Se ha clasificado el documento y determinado roles funcionales y perspectivas
- Se han evaluado todos los gaps previos actualizando sus estados según corresponda
- Se han validado respuestas y consistencia cruzada para cada rol funcional (mínimo 2-3 roles)
- Se han investigado archivos de referencia para cada rol funcional
- Se han identificado nuevos gaps con deduplicación contra existentes aplicando preguntas clave
- Se ha calificado el documento (1-10) con desglose por criterios
- Se ha decidido si los gaps se agregan al archivo original (calificación < 9) o solo se documentan en el análisis (calificación ≥ 9)
- Se ha verificado cobertura multi-rol, consistencia de perspectiva dual, y ausencia de contradicciones

### Resumen de Pasos

1. **Detección de Análisis Previo**: Determinar si existe un análisis previo en el documento y validar su vigencia
2. **Preparación y Clasificación**: Determinar tipo de documento, rol funcional principal, y perspectivas a aplicar (ver `references/classification.md`)
3. **Evaluación de Gaps Previos**: Si existen gaps previos, validar su estado, buscar respuestas, y actualizar según corresponda
4. **Validación de Respuestas y Consistencia**: Para cada rol funcional (mínimo 2-3), validar respuestas existentes y consistencia cruzada entre fuentes
5. **Investigación de Referencias**: Para cada rol funcional, revisar archivos de referencia y documentar hallazgos. **Nota importante**: Si un gap se resuelve mediante el uso de un archivo relacionado, este archivo debe anotarse en el frontmatter en el campo "related" para documentar también la forma en que se relacionan los archivos. Cuando un archivo contiene este campo, debe usarse como referencia de investigación para no repetir o duplicar gaps resueltos previamente gracias a estas relaciones.
6. **Identificación de Contexto Faltante**: Para cada rol funcional, identificar contexto faltante aplicando preguntas clave (cómo/por qué/qué/cuándo/quién/dónde)
7. **Evaluación de Calidad y Decisión de Adición de Gaps**: Calificar el documento (1-10) y decidir si los gaps deben agregarse al archivo original (calificación < 9) o solo documentarse en el análisis (calificación ≥ 9)
8. **Revisión Final**: Verificar cobertura multi-rol, consistencia de perspectiva dual, contradicciones, y criterios de terminación

## Gestión de Idempotencia

Para detalles sobre gestión de idempotencia, consultar `references/idempotency.md`.

## Expectativas de Entrada/Salida

Para detalles sobre expectativas de entrada y salida, consultar `references/io-expectations.md`.

## Uso

Invoca este skill al revisar archivos de documentación para generar preguntas críticas de forma idempotente. El skill ayudará a mantener la calidad de documentación asegurando que todas las preguntas "cómo" y "por qué" sean abordadas con referencias apropiadas, evitando generación infinita de preguntas mediante gestión de estado y deduplicación.

## Instrucción de Lista de Tareas

**ANTES DE COMENZAR**: Debes crear una lista de tareas utilizando la herramienta `todo_list` con cada paso a ejecutar y su descripción. Esta lista debe incluir:

- **Todos los pasos del proceso** (pasos 1-8) con descripciones claras
- **Estado inicial**: Marcar el primer paso como "in_progress" y los demás como "pending"
- **Prioridades**: Asignar prioridad "high" a pasos críticos, "medium" a pasos importantes
- **Actualización continua**: Marcar cada tarea como "completed" inmediatamente después de terminarla
- **Visibilidad**: Esto permite tener claro qué se debe hacer antes de empezar y seguimiento del progreso

**Ejemplo de estructura de tareas**:
1. Detección de Análisis Previo - Determinar si existe un análisis previo y validar su vigencia
2. Preparación y Clasificación - Determinar tipo de documento, roles funcionales y perspectivas
3. Evaluación de Gaps Previos - Validar estado de gaps existentes y actualizar según corresponda
4. Validación de Respuestas y Consistencia - Para cada rol funcional, validar respuestas y consistencia cruzada
5. Investigación de Referencias - Para cada rol funcional, revisar archivos de referencia
6. Identificación de Contexto Faltante - Para cada rol funcional, identificar contexto faltante con preguntas clave
7. Evaluación de Calidad y Decisión - Calificar documento y decidir adición de gaps
8. Revisión Final - Verificar cobertura multi-rol, consistencia y criterios de terminación

## Referencias Adicionales

Para detalles específicos sobre:

- **Priorización y categorización de gaps**: Consulta `references/priorities.md`
- **Errores comunes y mejores prácticas**: Consulta `references/guardrails.md`
- **Manejo de contradicciones**: Consulta `references/guardrails.md`
- **Plantillas de formato con estados**: Consulta `references/templates.md`
- **Gestión de idempotencia**: Consulta `references/idempotency.md`
- **Expectativas de entrada/salida**: Consulta `references/io-expectations.md`
