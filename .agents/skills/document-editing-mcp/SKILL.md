---
name: document-editing-mcp
description: Document Editing MCP - Aplica propuestas para integrar respuestas al contenido principal, realizar ediciones según la propuesta, actualizar la calificación del documento y mejorar documentación relacionada orgánicamente. Usa las herramientas MCP de Alejandria para operar sobre documentos almacenados en la base de datos.
---

# Document Editing MCP

## Objetivos y Principios

**Propósito fundamental**: Aplicar propuestas generadas para mejorar documentos almacenados en Alejandria llevándolos a su forma final. Este skill NO propone mejoras estructurales o de contenido - esa responsabilidad corresponde a actions-proposal-mcp. document-editing-mcp ejecuta las acciones propuestas en la propuesta, actualiza la calificación del documento para reflejar su estado real después de los cambios, y mejora la calidad completa de la documentación mediante implementación de cambios en documentos relacionados según la propuesta.

**Diferencia con document-editing**: Este skill usa las herramientas MCP de Alejandria (`read_document`, `write_document`, `list_gaps`) para operar sobre documentos almacenados en la base de datos de Alejandria, en lugar de operar directamente sobre archivos del sistema de archivos.

**Principios de edición**:
- **Ejecución de la propuesta**: Seguir fielmente la propuesta proporcionada
- **Edición precisa**: Implementar exactamente las acciones propuestas, sin añadir ni quitar
- **Integración de respuestas**: Integrar las respuestas de gaps al contenido principal según la propuesta
- **Actualización de estados**: Actualizar los estados de gaps de `responded` a reflejar que fueron aplicados
- **Actualización de calificación**: Recalcular y actualizar la calificación del documento para reflejar su estado real después de los cambios
- **Mejora orgánica de documentación**: Implementar cambios en documentos relacionados según la propuesta, mejorando la calidad completa de la documentación de forma orgánica y ordenada
- **Sin invención**: NO agregar información no existente ni inventar razonamientos. Solo implementar información existente en las respuestas de gaps
- **Documentación de cambios**: Registrar todos los cambios realizados usando `write_document` con commit messages
- **No propuesta**: NO proponer mejoras adicionales, NO evaluar calidad más allá de la actualización de calificación, NO sugerir cambios estructurales
- **Uso de herramientas MCP**: Todas las operaciones se realizan mediante herramientas MCP de Alejandria

**Responsabilidades**:
- Leer y entender la propuesta proporcionada usando `read_document` y `list_gaps`
- Aplicar las acciones propuestas en la propuesta
- Realizar ediciones del documento actual según la propuesta usando `write_document`
- Realizar ediciones a documentos existentes según la propuesta (incluyendo documentos relacionados) usando `write_document`
- Crear nuevos documentos según la propuesta (como último recurso) usando `create_document` y `write_document`
- Integrar respuestas de gaps al contenido principal según la propuesta
- Actualizar la calificación del documento para reflejar su estado real después de los cambios
- Implementar cambios en documentos relacionados según la propuesta para mejorar la calidad completa de la documentación
- Documentar cambios realizados usando `write_document` con commit messages apropiados
- Llevar el documento a su forma final
- NO proponer mejoras estructurales (división, consolidación, documentos siguientes)
- NO proponer mejoras de contenido o redacción
- NO evaluar calidad del documento más allá de la actualización de calificación
- NO clasificar o calificar el documento de forma independiente
- NO agregar información no existente ni inventar razonamientos

## Estructura del Skill

Este skill utiliza una estructura modular para facilitar el mantenimiento y la navegación.

### Archivos Principales

- **`SKILL.md`**: Este archivo - Objetivos, principios y resumen del proceso
- **`reference/workflows.md`**: Índice de los pasos del proceso con enlaces a archivos detallados

### Archivos de Proceso (workflows/)

- **`workflows/00-proposal-reading.md`**: Lectura y validación de la propuesta usando `read_document` y `list_gaps`
- **`workflows/01-execution.md`**: Ejecución de acciones propuestas
- **`workflows/02-integration.md`**: Integración de respuestas al contenido principal usando `write_document`
- **`workflows/03-related-docs.md`**: Implementación de cambios en documentos relacionados usando `write_document`
- **`workflows/04-rating-update.md`**: Actualización de calificación del documento
- **`workflows/05-final-validation.md`**: Validación final y verificación de forma final

### Archivos de Referencia

- **`reference/objectives-principles.md`**: Propósito fundamental, principios de edición y distinción con otros skills
- **`reference/guardrails.md`**: Errores comunes y mejores prácticas específicas de document-editing-mcp
- **`reference/templates.md`**: Plantillas de formato para actualización de calificación y estados
- **`reference/io-expectations.md`**: Expectativas de entrada y salida del skill
- **`reference/flowchart.md`**: Diagrama de flujo visual del proceso completo
- **`reference/troubleshooting.md`**: Guía de troubleshooting para casos borde
- **`reference/mcp-tools.md`**: Referencia de herramientas MCP disponibles

## Herramientas MCP Utilizadas

Este skill utiliza las siguientes herramientas MCP de Alejandria:

- **`read_document`**: Leer el contenido del documento desde la base de datos (usa document_slug)
- **`write_document`**: Actualizar el contenido del documento con cambios (usa document_slug)
- **`create_document`**: Crear nuevos documentos si la propuesta lo requiere
- **`list_gaps`**: Obtener gaps para verificar estado y contexto (usa document_slug)
- **`search_similar_documents`**: Buscar documentos relacionados para impacto indirecto

## Proceso

El proceso sigue un enfoque sistemático organizado en 6 pasos: (1) lectura y validación de la propuesta usando `read_document` y `list_gaps`, (2) ejecución de acciones propuestas, (3) integración de respuestas al contenido principal usando `write_document`, (4) implementación de cambios en documentos relacionados usando `write_document`, (5) actualización de calificación del documento, y (6) validación final.

Para instrucciones detalladas paso a paso, consulta **`reference/workflows.md`**.

### Criterios de Terminación

El proceso termina cuando:
- Se ha leído y validado la propuesta usando `read_document` y `list_gaps`
- Se han ejecutado todas las acciones propuestas en el orden establecido
- Se han integrado todas las respuestas de gaps al contenido principal usando `write_document`
- Se han implementado cambios en documentos relacionados según la propuesta usando `write_document`
- Se ha actualizado la calificación del documento para reflejar su estado real después de los cambios
- Se ha verificado que el documento está en su forma final
- Se ha confirmado que la documentación relacionada se mejoró orgánicamente

### Resumen de Pasos

1. **Lectura y Validación de la Propuesta**: Usar `read_document` y `list_gaps` para leer y entender la propuesta proporcionada
2. **Ejecución de Acciones**: Aplicar las acciones propuestas en el orden establecido (prioridad y tipo)
3. **Integración de Respuestas**: Usar `write_document` para integrar respuestas de gaps al contenido principal según la propuesta
4. **Implementación en Documentos Relacionados**: Usar `write_document` para aplicar cambios a documentos relacionados según la propuesta para mejorar la calidad completa de la documentación
5. **Actualización de Calificación**: Recalcular y actualizar la calificación del documento para reflejar su estado real después de los cambios
6. **Validación Final**: Validar que el documento está en su forma final y que la documentación relacionada se mejoró orgánicamente

## Expectativas de Entrada/Salida

Para detalles sobre expectativas de entrada y salida, consultar `reference/io-expectations.md`.

## Uso

Invoca este skill después de que se haya generado una propuesta usando actions-proposal-mcp. Este skill ejecuta las acciones propuestas en la propuesta, actualiza la calificación del documento para reflejar su estado real, y mejora la documentación relacionada de forma orgánica usando las herramientas MCP de Alejandria, llevando el documento a su forma final.

**Entrada esperada**:
- `document_slug`: Slug del documento en Alejandria
- `proposal_id`: UUID de la propuesta a ejecutar (opcional, si se proporciona)

**Salida esperada**:
- Documento actualizado usando `write_document`
- Calificación del documento actualizada
- Documentos relacionados actualizados si aplica

## Instrucción de Lista de Tareas

**ANTES DE COMENZAR**: Debes crear una lista de tareas utilizando la herramienta `todo_list` con cada paso a ejecutar y su descripción. Esta lista debe incluir:

- **Todos los pasos del proceso** (pasos 1-6) con descripciones claras
- **Estado inicial**: Marcar el primer paso como "in_progress" y los demás como "pending"
- **Prioridades**: Asignar prioridad "high" a pasos críticos, "medium" a pasos importantes
- **Actualización continua**: Marcar cada tarea como "completed" inmediatamente después de terminarla
- **Visibilidad**: Esto permite tener claro qué se debe hacer y seguimiento del progreso

**Ejemplo de estructura de tareas**:
1. Lectura y Validación de la Propuesta - Usar read_document y list_gaps para leer y entender la propuesta proporcionada
2. Ejecución de Acciones - Aplicar las acciones propuestas en el orden establecido
3. Integración de Respuestas - Usar write_document para integrar respuestas de gaps al contenido principal según la propuesta
4. Implementación en Documentos Relacionados - Usar write_document para aplicar cambios a documentos relacionados según la propuesta
5. Actualización de Calificación - Recalcular y actualizar la calificación del documento
6. Validación Final - Validar que el documento está en su forma final y que la documentación relacionada se mejoró orgánicamente

## Referencias Adicionales

Para detalles específicos sobre:

- **Objetivos y principios**: Consulta `reference/objectives-principles.md`
- **Proceso de edición**: Consulta `reference/workflows.md`
- **Errores comunes y mejores prácticas**: Consulta `reference/guardrails.md`
- **Plantillas de formato**: Consulta `reference/templates.md`
- **Expectativas de entrada/salida**: Consulta `reference/io-expectations.md`
- **Herramientas MCP disponibles**: Consulta `reference/mcp-tools.md`
