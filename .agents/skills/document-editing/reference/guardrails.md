# Guardrails y Mejores Prácticas

## Errores Comunes

### 1. Proponer Mejoras Adicionales

**Error**: Agregar mejoras estructurales o de contenido que no están en el plan de trabajo.

**Por qué es un error**: La responsabilidad de proponer mejoras corresponde a otros procesos del sistema. document-editing solo debe ejecutar las acciones propuestas.

**Cómo evitarlo**: Seguir fielmente el plan de trabajo. Si se identifica una mejora necesaria, documentarla pero no implementarla. La mejora debe ser propuesta por el proceso correspondiente en el siguiente ciclo.

### 2. Inventar Información

**Error**: Agregar información que no existe en las respuestas de gaps o derivar información a partir de inferencias o supuestos.

**Por qué es un error**: El objetivo es implementar información existente, no inventar respuestas. Esto puede introducir información incorrecta o inconsistente.

**Cómo evitarlo**: Solo implementar información que exista explícitamente en las respuestas de gaps. Si falta información, marcar esa sección como pendiente.

### 3. No Actualizar la Calificación

**Error**: Olvidar actualizar la calificación del documento después de implementar los cambios.

**Por qué es un error**: La calificación debe reflejar el estado real del documento después de los cambios. Sin esta actualización, no hay registro del impacto de las mejoras.

**Cómo evitarlo**: Incluir siempre el paso de actualización de calificación después de implementar los cambios.

### 4. Ignorar Documentos Relacionados

**Error**: No implementar cambios en documentos relacionados según el plan de trabajo.

**Por qué es un error**: Los documentos relacionados son parte de la mejora orgánica de la documentación. Ignorarlos deja la documentación incompleta o inconsistente.

**Cómo evitarlo**: Revisar cuidadosamente el plan de trabajo para identificar acciones que afectan documentos relacionados y ejecutarlas.

### 5. Dejar Secciones Temporales

**Error**: No eliminar el plan de trabajo o secciones temporales después de la implementación.

**Por qué es un error**: El documento debe quedar en su forma final sin reportes adicionales. Las secciones temporales son para seguimiento interno durante la ejecución.

**Cómo evitarlo**: Siempre limpiar el documento eliminando el plan de trabajo y secciones temporales después de completar la implementación.

### 6. No Validar Consistencia

**Error**: No validar la consistencia entre el documento principal y los documentos relacionados.

**Por qué es un error**: La inconsistencia entre documentos puede causar confusión y errores en el futuro.

**Cómo evitarlo**: Siempre validar que los cambios en documentos relacionados mantienen consistencia con el documento principal.

## Mejores Prácticas

### 1. Ejecución Fiel al Plan

- Implementar exactamente las acciones propuestas sin añadir ni quitar
- Seguir el orden de prioridad y tipo de acción establecido
- Verificar cada cambio antes de continuar con el siguiente

### 2. Integración Natural

- Integrar respuestas en secciones lógicas del documento
- Asegurar que el contenido fluya naturalmente con el texto existente
- Evitar duplicación de información
- Mantener el contexto de la respuesta

### 3. Actualización Completa de Estados

- Actualizar todos los gaps de `[PLANEADO]` a `[IMPLEMENTADO]`
- Documentar fecha de implementación y acción ejecutada
- Mantener gaps implementados como registro histórico

### 4. Calificación Precisa

- Evaluar el estado real del documento después de los cambios
- Calcular la nueva calificación basada en criterios objetivos
- Comparar con la calificación esperada del plan
- Documentar discrepancias si las hay

### 5. Mejora Orgánica

- Implementar cambios en documentos relacionados según el plan
- Validar consistencia entre documentos
- Mejorar la calidad completa de la documentación de forma ordenada
- No agregar información no existente

### 6. Forma Final

- Eliminar todas las secciones temporales
- Verificar que el documento fluye lógicamente
- Confirmar que no hay duplicación de información
- Validar que el documento está listo para producción

## Casos Borde

### Plan de Trabajo Incompleto

Si el plan de trabajo está incompleto o tiene acciones mal definidas:

1. Documentar el problema
2. Ejecutar las acciones que están claramente definidas
3. Solicitar aclaración para las acciones ambiguas
4. No inventar acciones o interpretaciones

### Documento Relacionado No Existe

Si un documento relacionado especificado en el plan no existe:

1. Documentar el problema
2. Continuar con otras acciones
3. Notificar la situación en la validación final
4. No crear el documento automáticamente (esto es responsabilidad del proceso de generación de planes)

### Calificación No Alcanzada

Si la calificación alcanzada es menor que la esperada:

1. Documentar la discrepancia
2. Analizar las razones de la diferencia
3. Registrar las razones en el documento
4. Considerar si se necesita un nuevo ciclo de mejora

### Respuesta No Se Puede Integrar

Si una respuesta no se puede integrar de forma natural:

1. Revisar el punto de integración propuesto
2. Considerar una sección alternativa
3. Si no es posible integrar, documentar el problema
4. No forzar una integración que rompa el flujo del documento
