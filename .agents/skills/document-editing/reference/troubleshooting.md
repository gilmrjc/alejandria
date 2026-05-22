# Guía de Troubleshooting

## Casos Borde Comunes

### Plan de Trabajo No Encontrado

**Síntoma**: No se encuentra la sección "PLAN DE TRABAJO" en el documento.

**Causas posibles**:

- El plan no fue generado
- El plan fue eliminado manualmente
- El plan está en una ubicación diferente

**Solución**:

1. Verificar que el proceso de generación de planes se ejecutó correctamente
2. Buscar secciones similares con diferente nombre
3. Si no existe plan, documentar el problema y solicitar que se ejecute el proceso de generación de planes primero

### Plan de Trabajo Incompleto

**Síntoma**: El plan de trabajo falta información crítica (versión, fecha, acciones).

**Causas posibles**:

- El proceso de generación de planes no completó la generación del plan
- El plan fue truncado durante la edición

**Solución**:

1. Documentar la información faltante
2. Ejecutar las acciones que están claramente definidas
3. Solicitar regeneración del plan para la información faltante

### Acción No Se Puede Ejecutar

**Síntoma**: Una acción del plan no se puede ejecutar según lo especificado.

**Causas posibles**:

- Referencias faltantes o incorrectas
- Archivo objetivo no existe
- Descripción de acción ambigua

**Solución**:

1. Documentar el problema específico
2. Intentar interpretar la intención de la acción
3. Si no es posible ejecutar, saltar la acción y documentar
4. Continuar con otras acciones del plan

### Respuesta No Se Puede Integrar

**Síntoma**: Una respuesta de gap no se puede integrar de forma natural en el documento.

**Causas posibles**:

- Punto de integración incorrecto
- Respuesta demasiado larga o compleja
- Estructura del documento no adecuada

**Solución**:

1. Revisar el punto de integración propuesto
2. Considerar una sección alternativa
3. Dividir la respuesta en partes más pequeñas
4. Si no es posible integrar, documentar el problema y mantener la respuesta en la sección de gaps

### Documento Relacionado No Existe

**Síntoma**: Un documento relacionado especificado en el plan no existe.

**Causas posibles**:

- El proceso de generación de planes propuso un documento que no se creó
- Ruta del documento incorrecta
- Documento fue movido o eliminado

**Solución**:

1. Verificar la ruta del documento
2. Buscar el documento en ubicaciones alternativas
3. Documentar el problema
4. No crear el documento automáticamente (esto es responsabilidad del proceso de generación de planes)

### Calificación No Alcanzada

**Síntoma**: La calificación alcanzada es menor que la calificación esperada del plan.

**Causas posibles**:

- Algunas acciones no se ejecutaron correctamente
- Problemas de calidad persisten
- Evaluación de calificación demasiado estricta

**Solución**:

1. Documentar la discrepancia
2. Analizar las razones de la diferencia
3. Verificar si todas las acciones se ejecutaron
4. Registrar las razones en el documento
5. Considerar si se necesita un nuevo ciclo de mejora

### Documento No Queda en Forma Final

**Síntoma**: Después de la limpieza, el documento todavía tiene secciones temporales o problemas de flujo.

**Causas posibles**:

- Secciones temporales no identificadas
- Problemas de integración no resueltos
- Duplicación de información

**Solución**:

1. Revisar el documento completo buscando secciones temporales
2. Verificar el flujo del documento
3. Eliminar cualquier duplicación
4. Si no es posible resolver, documentar los problemas

## Errores de Ejecución

### Error de Lectura de Archivo

**Síntoma**: No se puede leer un archivo especificado en el plan.

**Solución**:

1. Verificar que el archivo existe
2. Verificar permisos de lectura
3. Documentar el error
4. Continuar con otras acciones

### Error de Escritura de Archivo

**Síntoma**: No se puede escribir en un archivo.

**Solución**:

1. Verificar permisos de escritura
2. Verificar que el archivo no está bloqueado
3. Documentar el error
4. Continuar con otras acciones

### Error de Sintaxis en Markdown

**Síntoma**: El archivo tiene errores de sintaxis después de la edición.

**Solución**:

1. Revertir el cambio si es posible
2. Corregir la sintaxis
3. Verificar que el cambio no rompe el formato
4. Documentar el error

## Validaciones Fallidas

### Validación de Plan Falla

**Síntoma**: El plan de trabajo no pasa las validaciones iniciales.

**Solución**:

1. Documentar las validaciones que fallan
2. Solicitar corrección del plan
3. No ejecutar el plan si tiene errores críticos

### Validación Final Falla

**Síntoma**: El documento no pasa la validación final.

**Solución**:

1. Identificar qué validaciones fallan
2. Intentar corregir los problemas
3. Documentar los problemas que no se pueden corregir
4. Marcar el documento como "REQUIERE ATENCIÓN"

## Recuperación de Errores

### Recuperación Parcial

Si algunas acciones fallan pero otras tienen éxito:

1. Documentar todas las acciones ejecutadas exitosamente
2. Documentar todas las acciones que fallaron
3. Actualizar estados de gaps para acciones exitosas
4. Mantener gaps para acciones fallidas en estado `[PLANEADO]`
5. Solicitar corrección del plan para acciones fallidas

### Recuperación Completa

Si el proceso falla completamente:

1. Documentar el error general
2. No hacer cambios al documento
3. Mantener el plan de trabajo
4. Solicitar revisión del plan y del proceso

## Prevención de Errores

### Mejores Prácticas

- Validar el plan de trabajo antes de ejecutar
- Verificar existencia de archivos antes de editar
- Hacer copias de seguridad si es posible
- Documentar todos los errores y problemas
- No forzar acciones que no se pueden ejecutar
- Mantener trazabilidad de todas las acciones

### Monitoreo

- Verificar cada cambio antes de continuar
- Validar el estado del documento después de cada paso
- Revisar logs de errores si están disponibles
- Solicitar confirmación para acciones críticas
