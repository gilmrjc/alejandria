---
name: document-editing
description: Document Editing - Aplica planes de trabajo para integrar respuestas al contenido principal, realizar ediciones según el plan, actualizar la calificación del documento y mejorar documentación relacionada orgánicamente
---

# Document Editing

## Objetivos y Principios

**Propósito fundamental**: Aplicar planes de trabajo generados para mejorar documentos llevándolos a su forma final. Este skill NO propone mejoras estructurales o de contenido - esa responsabilidad corresponde a otros procesos del sistema. document-editing ejecuta las acciones propuestas en el plan de trabajo, actualiza la calificación del documento para reflejar su estado real después de los cambios, y mejora la calidad completa de la documentación mediante implementación de cambios en documentos relacionados según el plan.

**Principios de edición**:
- **Ejecución del plan**: Seguir fielmente el plan de trabajo proporcionado
- **Edición precisa**: Implementar exactamente las acciones propuestas, sin añadir ni quitar
- **Integración de respuestas**: Integrar las respuestas de gaps al contenido principal según el plan
- **Actualización de estados**: Actualizar los estados de gaps de `[PLANEADO]` a `[IMPLEMENTADO]` según el plan
- **Actualización de calificación**: Recalcular y actualizar la calificación del documento para reflejar su estado real después de los cambios
- **Mejora orgánica de documentación**: Implementar cambios en documentos relacionados según el plan, mejorando la calidad completa de la documentación de forma orgánica y ordenada
- **Limpieza completa**: Eliminar todas las secciones temporales incluyendo plan de trabajo, registro de cambios, y sección de gaps implementados
- **Sin invención**: NO agregar información no existente ni inventar razonamientos. Solo implementar información existente en las respuestas de gaps
- **Documentación de cambios**: Registrar todos los cambios realizados
- **No propuesta**: NO proponer mejoras adicionales, NO evaluar calidad más allá de la actualización de calificación, NO sugerir cambios estructurales

**Responsabilidades**:
- Leer y entender el plan de trabajo proporcionado
- Aplicar las acciones propuestas en el plan de trabajo
- Realizar ediciones del archivo actual según el plan
- Realizar ediciones a archivos existentes según el plan (incluyendo documentos relacionados)
- Crear nuevos archivos según el plan (como último recurso)
- Integrar respuestas de gaps al contenido principal según el plan
- Actualizar estados de gaps de `[PLANEADO]` a `[IMPLEMENTADO]` según el plan
- Actualizar la calificación del documento para reflejar su estado real después de los cambios
- Implementar cambios en documentos relacionados según el plan para mejorar la calidad completa de la documentación
- Documentar cambios realizados
- Llevar el documento a su forma final (sin reportes adicionales de plan de trabajo)
- NO proponer mejoras estructurales (división, consolidación, documentos siguientes)
- NO proponer mejoras de contenido o redacción
- NO evaluar calidad del documento más allá de la actualización de calificación
- NO clasificar o calificar el documento de forma independiente
- NO agregar información no existente ni inventar razonamientos

## Estructura del Skill

Este skill utiliza una estructura modular para facilitar el mantenimiento y la navegación. Los componentes detallados se encuentran en:

### Archivos Principales

- **`SKILL.md`**: Este archivo - Objetivos, principios y resumen del proceso
- **`reference/workflows.md`**: Índice de los pasos del proceso con enlaces a archivos detallados

### Archivos de Proceso (workflows/)

- **`workflows/00-plan-reading.md`**: Lectura y validación del plan de trabajo
- **`workflows/01-execution.md`**: Ejecución de acciones propuestas
- **`workflows/02-integration.md`**: Integración de respuestas al contenido principal
- **`workflows/03-related-docs.md`**: Implementación de cambios en documentos relacionados
- **`workflows/04-rating-update.md`**: Actualización de calificación del documento
- **`workflows/05-state-update.md`**: Actualización de estados de gaps y limpieza
- **`workflows/06-final-validation.md`**: Validación final y verificación de forma final

### Archivos de Referencia

- **`reference/objectives-principles.md`**: Propósito fundamental, principios de edición y distinción con otros skills
- **`reference/guardrails.md`**: Errores comunes y mejores prácticas específicas de document-editing
- **`reference/templates.md`**: Plantillas de formato para actualización de calificación y estados
- **`reference/io-expectations.md`**: Expectativas de entrada y salida del skill
- **`reference/flowchart.md`**: Diagrama de flujo visual del proceso completo
- **`reference/troubleshooting.md`**: Guía de troubleshooting para casos borde

## Proceso

El proceso sigue un enfoque sistemático organizado en 6 pasos: (1) lectura y validación del plan de trabajo, (2) ejecución de acciones propuestas, (3) integración de respuestas al contenido principal, (4) implementación de cambios en documentos relacionados, (5) actualización de calificación del documento, y (6) actualización de estados de gaps y validación final.

Para instrucciones detalladas paso a paso, consulta **`reference/workflows.md`**.

### Criterios de Terminación

El proceso termina cuando:
- Se ha leído y validado el plan de trabajo
- Se han ejecutado todas las acciones propuestas en el orden establecido
- Se han integrado todas las respuestas de gaps al contenido principal
- Se han implementado cambios en documentos relacionados según el plan
- Se ha actualizado la calificación del documento para reflejar su estado real después de los cambios
- Se han actualizado los estados de gaps de `[PLANEADO]` a `[IMPLEMENTADO]`
- Se ha verificado que el documento está en su forma final (sin reportes adicionales)
- Se ha confirmado que la documentación relacionada se mejoró orgánicamente

### Resumen de Pasos

1. **Lectura y Validación del Plan**: Leer y entender el plan de trabajo proporcionado
2. **Ejecución de Acciones**: Aplicar las acciones propuestas en el orden establecido (prioridad y tipo)
3. **Integración de Respuestas**: Integrar respuestas de gaps al contenido principal según el plan
4. **Implementación en Documentos Relacionados**: Aplicar cambios a documentos relacionados según el plan para mejorar la calidad completa de la documentación
5. **Actualización de Calificación**: Recalcular y actualizar la calificación del documento para reflejar su estado real después de los cambios
6. **Actualización de Estados y Validación Final**: Actualizar estados de gaps, limpiar el plan de trabajo y validar que el documento está en su forma final

## Expectativas de Entrada/Salida

Para detalles sobre expectativas de entrada y salida, consultar `reference/io-expectations.md`.

## Uso

Invoca este skill después de que se haya generado un plan de trabajo. Este skill ejecuta las acciones propuestas en el plan, actualiza la calificación del documento para reflejar su estado real, y mejora la documentación relacionada de forma orgánica, llevando el documento a su forma final sin reportes adicionales.

## Instrucción de Lista de Tareas

**ANTES DE COMENZAR**: Debes crear una lista de tareas utilizando la herramienta `todo_list` con cada paso a ejecutar y su descripción. Esta lista debe incluir:

- **Todos los pasos del proceso** (pasos 1-6) con descripciones claras
- **Estado inicial**: Marcar el primer paso como "in_progress" y los demás como "pending"
- **Prioridades**: Asignar prioridad "high" a pasos críticos, "medium" a pasos importantes
- **Actualización continua**: Marcar cada tarea como "completed" inmediatamente después de terminarla
- **Visibilidad**: Esto permite tener claro qué se debe hacer y seguimiento del progreso

**Ejemplo de estructura de tareas**:
1. Lectura y Validación del Plan - Leer y entender el plan de trabajo proporcionado
2. Ejecución de Acciones - Aplicar las acciones propuestas en el orden establecido
3. Integración de Respuestas - Integrar respuestas de gaps al contenido principal según el plan
4. Implementación en Documentos Relacionados - Aplicar cambios a documentos relacionados según el plan
5. Actualización de Calificación - Recalcular y actualizar la calificación del documento
6. Actualización de Estados y Validación Final - Actualizar estados de gaps, limpiar el plan y validar forma final
