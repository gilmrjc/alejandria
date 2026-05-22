# Índice de Workflows

## Resumen

El proceso sigue un enfoque sistemático organizado en 6 pasos: (1) lectura y validación del plan de trabajo, (2) ejecución de acciones propuestas, (3) integración de respuestas al contenido principal, (4) implementación de cambios en documentos relacionados, (5) actualización de calificación del documento, y (6) actualización de estados de gaps y validación final.

## Workflows Detallados

Para instrucciones detalladas paso a paso, consulta los siguientes archivos:

### Paso 0: Lectura y Validación del Plan de Trabajo

**Archivo**: `workflows/00-plan-reading.md`

- Localizar el plan de trabajo en el documento
- Leer el encabezado del plan (versión, fecha, calificación esperada)
- Revisar acciones propuestas organizadas por prioridad
- Identificar tipos de acciones (edición archivo actual, edición archivos existentes, creación nuevos archivos)
- Identificar documentos relacionados
- Verificar referencias y responsables
- Validar que el plan está completo y vigente

### Paso 1: Ejecución de Acciones Propuestas

**Archivo**: `workflows/01-execution.md`

- Ejecutar acciones en orden de prioridad (Crítica > Alta > Media)
- Dentro de cada prioridad, ejecutar en orden de tipo (archivo actual > archivos existentes > nuevos archivos)
- Aplicar ediciones del archivo actual
- Aplicar ediciones a archivos existentes
- Crear nuevos archivos (último recurso)
- Verificar cada cambio antes de continuar
- Documentar cada acción ejecutada

### Paso 2: Integración de Respuestas al Contenido Principal

**Archivo**: `workflows/02-integration.md`

- Identificar gaps con respuestas en estado `[PLANEADO]`
- Leer las respuestas proporcionadas
- Determinar el punto de integración en el documento
- Aplicar la integración manteniendo contexto y flujo natural
- Verificar que no hay duplicación de información
- Eliminar la sección de respuesta original
- Validar coherencia del documento después de la integración

### Paso 3: Implementación en Documentos Relacionados

**Archivo**: `workflows/03-related-docs.md`

- Identificar documentos relacionados según el plan de trabajo
- Leer acciones para documentos relacionados
- Validar existencia de documentos relacionados
- Aplicar cambios a documentos relacionados
- Verificar impacto en calidad de cada documento
- Validar consistencia entre documento principal y relacionados
- Mejorar la calidad completa de la documentación de forma orgánica

### Paso 4: Actualización de Calificación del Documento

**Archivo**: `workflows/04-rating-update.md`

- Leer la calificación original del documento
- Leer la calificación esperada del plan de trabajo
- Evaluar el estado actual del documento después de los cambios
- Calcular la nueva calificación basada en criterios (completitud, claridad, consistencia, estructura, referencias)
- Comparar con calificación esperada
- Actualizar la calificación en el frontmatter del documento
- Documentar la calificación anterior y la nueva

### Paso 5: Actualización de Estados de Gaps y Limpieza

**Archivo**: `workflows/05-state-update.md`

- Actualizar estados de gaps de `[PLANEADO]` a `[IMPLEMENTADO]`
- Documentar fecha de implementación y acción ejecutada para cada gap
- Verificar completitud de actualizaciones
- Eliminar el plan de trabajo del documento
- Eliminar secciones temporales (registro de cambios)
- Eliminar la sección de gaps implementados (gaps ya resueltos no permanecen en documento final)
- Verificar que el documento está en su forma final

### Paso 6: Validación Final

**Archivo**: `workflows/06-final-validation.md`

- Verificar completitud de acciones ejecutadas
- Validar integración de respuestas
- Validar actualización de estados de gaps
- Validar calificación actualizada
- Validar documentos relacionados actualizados
- Validar forma final del documento (sin secciones temporales)
- Validar calidad general de la documentación
- Confirmar que el documento está listo para producción

## Criterios de Terminación

El proceso termina cuando:

- Se ha leído y validado el plan de trabajo
- Se han ejecutado todas las acciones propuestas en el orden establecido
- Se han integrado todas las respuestas de gaps al contenido principal
- Se han implementado cambios en documentos relacionados según el plan
- Se ha actualizado la calificación del documento para reflejar su estado real después de los cambios
- Se han actualizado los estados de gaps de `[PLANEADO]` a `[IMPLEMENTADO]`
- Se ha verificado que el documento está en su forma final (sin reportes adicionales)
- Se ha confirmado que la documentación relacionada se mejoró orgánicamente
