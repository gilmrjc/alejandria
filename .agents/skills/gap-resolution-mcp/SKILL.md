---
name: gap-resolution-mcp
description: Gap Resolution MCP - Sesiones colaborativas para resolver gaps identificados en documentos de Alejandria mediante preguntas, lluvia de ideas y validación conjunta. NO identifica gaps nuevos, solo resuelve gaps ya identificados con estado pending. Usa las herramientas MCP de Alejandria para operar sobre gaps almacenados en la base de datos.
---

# Gap Resolution MCP

## Objetivos y Principios

**Propósito fundamental**: Facilitar sesiones interactivas donde el usuario y el AI colaboran para resolver gaps identificados en documentos almacenados en Alejandria, mediante rondas de preguntas estructuradas, lluvia de ideas, creación de definiciones y establecimiento de razonamientos que deben ser validados por el usuario.

**Diferencia con gap-resolution**: Este skill usa las herramientas MCP de Alejandria (`list_gaps`, `answer_gap`, `read_document`) para operar sobre gaps almacenados en la base de datos de Alejandria, en lugar de operar directamente sobre archivos del sistema de archivos.

**Límite de responsabilidad**: Este skill NO identifica gaps nuevos. Solo trabaja con gaps ya identificados con estado `pending`. La identificación de gaps es responsabilidad de un proceso previo de análisis de documentación (document-critique-mcp) que genera preguntas críticas sobre el documento.

**Principios de interacción**:
- **Enfoque colaborativo**: La sesión es un diálogo bidireccional donde el AI propone y el usuario valida
- **Rondas estructuradas**: Las preguntas se organizan en rondas temáticas con apoyo y sugerencias específicas
- **Validación continua**: Cada propuesta, definición o razonamiento requiere confirmación explícita del usuario
- **Brainstorming guiado**: Proveer sugerencias y alternativas para estimular el pensamiento creativo del usuario
- **Construcción progresiva**: Avanzar desde conceptos fundamentales hacia detalles más específicos
- **Documentación en tiempo real**: Capturar decisiones, definiciones y razonamientos a medida que se validan
- **Respeto a prioridades**: Seguir las prioridades asignadas en el proceso de identificación de gaps (critical > high > medium > low)
- **No re-identificación**: No crear nuevos gaps, solo resolver los existentes
- **Uso de herramientas MCP**: Todas las operaciones se realizan mediante herramientas MCP de Alejandria

**Responsabilidades**:
- Preparar la sesión usando `list_gaps` para revisar gaps identificados en el documento
- Establecer orden de trabajo basado en prioridades asignadas a los gaps
- Realizar rondas de preguntas estructuradas con contexto y sugerencias
- Facilitar brainstorming guiado para estimular el pensamiento del usuario
- Validar cada propuesta, definición o razonamiento con el usuario
- Documentar decisiones, definiciones y razonamientos en tiempo real
- Usar `answer_gap` para incorporar respuestas validadas en la base de datos
- Documentar gaps persistentes con planes de acción
- Actualizar estados de gaps de `pending` a `responded` usando `answer_gap`

**Lo que NO hace este skill**:
- NO identifica gaps nuevos (responsabilidad de document-critique-mcp)
- NO califica documentos (responsabilidad de document-critique-mcp)
- NO modifica prioridades asignadas en el proceso de identificación
- NO trabaja con gaps en estado `rejected`
- NO edita el contenido principal del documento (solo responde gaps usando `answer_gap`)

**Investigación de fuentes**: gap-resolution-mcp SÍ puede investigar fuentes externas durante las rondas de preguntas porque la documentación pudo mejorar entre el proceso de identificación de gaps y este paso. Esta investigación se realiza usando `search_similar_documents` para:
- Encontrar respuestas en documentos actualizados
- Validar si gaps ya fueron resueltos en otras fuentes
- Proveer contexto adicional para las sugerencias
- Documentar referencias que respalden las propuestas

## Estructura del Skill

Este skill utiliza una estructura modular para facilitar el mantenimiento y la navegación.

### Archivos Principales

- **`SKILL.md`**: Este archivo - Objetivos, principios, límites de responsabilidad y resumen del proceso
- **`reference/workflows.md`**: Índice de los pasos del proceso con enlaces a archivos detallados

### Archivos de Proceso (workflows/)

- **`workflows/00-preparation.md`**: Preparación de la sesión usando `list_gaps`
- **`workflows/01-question-rounds.md`**: Rondas de preguntas estructuradas
- **`workflows/02-response-handling.md`**: Manejo de respuestas del usuario
- **`workflows/03-documentation.md`**: Documentación de resultados usando `answer_gap`

### Archivos de Referencia

- **`reference/guardrails.md`**: Errores comunes, manejo de situaciones especiales y mejores prácticas (incluye objetivos y principios)
- **`reference/templates.md`**: Plantillas de formato para sesión, rondas de preguntas, respuestas y resultados
- **`reference/idempotency.md`**: Gestión de idempotencia y detección de sesión previa
- **`reference/state-transitions.md`**: Diagrama de transiciones de estados de gaps
- **`reference/input-output.md`**: Expectativas de entrada y salida del skill
- **`reference/flowchart.md`**: Diagrama de flujo visual del proceso completo
- **`reference/troubleshooting.md`**: Guía de troubleshooting para casos borde
- **`reference/gap-classification.md`**: Tipos de gaps, roles involucrados y enfoques por tipo
- **`reference/mcp-tools.md`**: Referencia de herramientas MCP disponibles

## Herramientas MCP Utilizadas

Este skill utiliza las siguientes herramientas MCP de Alejandria:

- **`read_document`**: Leer el contenido del documento desde la base de datos para contexto (usa document_slug)
- **`list_gaps`**: Obtener gaps existentes para un documento (usa document_slug, filtrar por status=pending)
- **`answer_gap`**: Responder gaps con respuestas validadas por el usuario (usa gap_slug)
- **`search_similar_documents`**: Buscar documentos similares para investigación de referencias

## Resumen del Proceso

El proceso sigue 4 pasos sistemáticos:

1. **Preparación de la sesión**: Usar `list_gaps` para revisar gaps identificados, establecer orden de trabajo y documentar estado inicial
2. **Rondas de preguntas estructuradas**: Para cada gap, realizar rondas con contexto, preguntas, sugerencias y validación
3. **Manejo de respuestas**: Documentar validaciones, modificaciones o rechazos según el feedback del usuario
4. **Documentación de resultados**: Usar `answer_gap` para incorporar respuestas validadas en la base de datos y documentar gaps persistentes

Para instrucciones detalladas paso a paso, consulta **`reference/workflows.md`**.

## Gestión de Idempotencia

Para detalles sobre gestión de idempotencia, consultar `reference/idempotency.md`.

## Expectativas de Entrada/Salida

Para detalles sobre expectativas de entrada y salida, consultar `reference/input-output.md`.

## Uso

Invoca este skill cuando:
- Un documento en Alejandria tiene gaps identificados con estado `pending`
- Necesitas resolver gaps colaborativamente con el usuario
- Necesitas hacer lluvia de ideas para definir conceptos o estrategias
- Quieres establecer razonamientos y justificaciones con validación del usuario
- El documento tiene secciones que requieren desarrollo conjunto

**Entrada esperada**:
- `document_slug`: Slug del documento en Alejandria

**Salida esperada**:
- Gaps respondidos usando `answer_gap` (estado cambia a `responded`)
- Respuestas documentadas en la base de datos

**Prerrequisito**: El documento debe haber sido analizado previamente por document-critique-mcp para identificar gaps y tener gaps con estado `pending`. Los gaps deben tener prioridades asignadas (critical/high/medium/low) y categorías temáticas definidas.

## Instrucción de Lista de Tareas

**ANTES DE COMENZAR**: Debes crear una lista de tareas utilizando la herramienta `todo_list` con cada paso a ejecutar y su descripción. Esta lista debe incluir:

- **Todos los pasos del proceso** (pasos 1-4) con descripciones claras
- **Estado inicial**: Marcar el primer paso como "in_progress" y los demás como "pending"
- **Prioridades**: Asignar prioridad "high" a pasos críticos, "medium" a pasos importantes
- **Actualización continua**: Marcar cada tarea como "completed" inmediatamente después de terminarla
- **Visibilidad**: Esto permite tener claro qué se debe hacer antes de empezar y seguimiento del progreso

**Ejemplo de estructura de tareas**:
1. Preparación de la Sesión - Usar list_gaps para revisar gaps identificados, establecer orden de trabajo y documentar estado inicial
2. Rondas de Preguntas Estructuradas - Para cada gap, realizar rondas con contexto, preguntas, sugerencias y validación
3. Manejo de Respuestas - Documentar validaciones, modificaciones o rechazos según feedback del usuario
4. Documentación de Resultados - Usar answer_gap para incorporar respuestas validadas y documentar gaps persistentes

## Referencias Adicionales

Para detalles específicos sobre:

- **Errores comunes y mejores prácticas**: Consulta `reference/guardrails.md`
- **Plantillas de formato**: Consulta `reference/templates.md`
- **Gestión de idempotencia**: Consulta `reference/idempotency.md`
- **Transiciones de estado**: Consulta `reference/state-transitions.md`
- **Expectativas de entrada/salida**: Consulta `reference/input-output.md`
- **Diagrama de flujo visual**: Consulta `reference/flowchart.md`
- **Guía de troubleshooting**: Consulta `reference/troubleshooting.md`
- **Clasificación de gaps**: Consulta `reference/gap-classification.md`
- **Herramientas MCP disponibles**: Consulta `reference/mcp-tools.md`
