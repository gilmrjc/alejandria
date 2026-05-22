# Guía de Troubleshooting

## Casos Borde Comunes

### Caso 1: Plan de Trabajo Corrupto

**Síntoma**: El plan de trabajo existe pero tiene formato inválido o incompleto.

**Solución**:

1. Detectar el formato corrupto en el Paso 0
2. Marcar el plan como inválido en la validación
3. Crear un nuevo plan en el Paso 3
4. Documentar la razón de recreación en el historial de cambios

### Caso 2: Gaps sin Acción de Integración

**Síntoma**: Un gap tiene estado `[RESUELTO]` pero no tiene acción de integración asociada en el plan de trabajo.

**Solución**:

1. En el Paso 2, identificar gaps `[RESUELTO]` sin acción de integración
2. Generar acción de integración para el gap según la respuesta proporcionada
3. Asignar prioridad según la prioridad del gap
4. En el Paso 3, marcar el gap como `[PLANEADO]` al escribir el plan

### Caso 3: Contradicción entre Respuestas

**Síntoma**: Dos gaps tienen respuestas contradictorias.

**Solución**:

1. En el Paso 2, detectar contradicciones entre respuestas
2. Proponer acción: "Resolver contradicción mediante sesión colaborativa"
3. Asignar prioridad alta (contradicciones bloquean ejecución)
4. Documentar los gaps contradictorios en la acción

### Caso 4: Archivo Referenciado No Existe

**Síntoma**: Una acción propone editar un archivo que no existe.

**Solución**:

1. En el Paso 2, validar que los archivos existan antes de proponer edición
2. Si el archivo no existe, cambiar tipo de acción a "Creación de nuevo archivo"
3. Documentar la razón del cambio de tipo
4. Justificar por qué se necesita el nuevo archivo

### Caso 5: Plan Demasiado Grande

**Síntoma**: El plan de trabajo tiene más de 50 acciones.

**Solución**:

1. En el Paso 2, agrupar acciones relacionadas
2. Proponer consolidación de acciones en acciones compuestas
3. Priorizar acciones críticas sobre acciones de menor prioridad
4. Considerar dividir el plan en fases si aplica

### Caso 6: División Atómica vs Consolidación Conflicto

**Síntoma**: El documento cumple criterios para división atómica y consolidación simultáneamente.

**Solución**:

1. En el Paso 7 (validación cruzada), detectar el conflicto
2. Evaluar cuál propuesta resuelve mejor el problema de calidad
3. Priorizar la propuesta más específica y enfocada
4. Documentar la contradicción y la decisión tomada

### Caso 7: Documento Siguiente Ya Existe

**Síntoma**: Se propone un documento siguiente que ya existe en el proyecto.

**Solución**:

1. En el Paso 6, validar duplicados sistemáticamente
2. Si existe documento similar con alto solapamiento: sugerir edición al existente
3. Si no existe duplicado o solapamiento es bajo: proceder con propuesta
4. Documentar la validación realizada

### Caso 8: Gaps Obsoletos en Plan

**Síntoma**: El plan de trabajo incluye acciones para gaps que ya no existen o están `[OBSOLETO]`.

**Solución**:

1. En el Paso 1 (validación), identificar gaps obsoletos
2. Marcar estas acciones para remoción en el Paso 3
3. Documentar las acciones removidas en el historial de cambios
4. Actualizar el conteo de gaps a resolver

### Caso 9: Cambio de Prioridad de Gaps

**Síntoma**: La prioridad de un gap cambió desde la última generación del plan.

**Solución**:

1. En el Paso 1 (validación), detectar cambios de prioridad
2. Reordenar acciones según las nuevas prioridades
3. Documentar los cambios de prioridad en el historial
4. Incrementar la versión del plan

### Caso 10: Sin Gaps Pendientes

**Síntoma**: El documento no tiene gaps con estado `[RESUELTO]` (todos están `[PLANEADO]` u otros estados).

**Solución**:

1. En el Paso 0, detectar ausencia de gaps `[RESUELTO]`
2. Si existen gaps `[PLANEADO]`: validar que el plan existente sigue siendo vigente
3. Si no existe plan: no generar nuevo plan (no es necesario)
4. Documentar que no se requiere plan de trabajo nuevo

## Errores Comunes y Cómo Evitarlos

### Error: Proponer Acciones Duplicadas

**Causa**: No verificar si ya existe una acción similar para el mismo gap.
**Prevención**: En el Paso 2, siempre verificar deduplicación antes de crear nuevas acciones.

### Error: No Priorizar Ediciones del Archivo Actual

**Causa**: Ir directamente a proponer nuevos archivos sin evaluar ediciones del archivo actual.
**Prevención**: Aplicar estrictamente el orden jerárquico: archivo actual > archivos existentes > nuevos archivos.

### Error: Ignorar Referencias en Acciones

**Causa**: Proponer acciones sin identificar las fuentes necesarias para ejecutarlas.
**Prevención**: Cada acción debe incluir referencias específicas a fuentes necesarias.

### Error: Proponer División sin Validar Autonomía

**Causa**: Proponer división atómica sin verificar que los archivos resultantes sean autónomos.
**Prevención**: En el Paso 4, siempre validar los 5 criterios de autonomía antes de proponer división.

### Error: No Validar Duplicados en Documentos Siguientes

**Causa**: Proponer documentos siguientes sin verificar si ya existen documentos similares.
**Prevención**: En el Paso 6, siempre realizar validación de duplicados sistemática.

## Validaciones de Sanidad

Antes de finalizar el proceso, verificar:

1. **Cada gap [RESUELTO] tiene acción de integración asignada** (si aplica)
2. **Gaps con acciones propuestas están marcados como [PLANEADO]**
3. **Cada acción tiene tipo, responsable y referencias**
4. **No hay acciones duplicadas**
5. **Las acciones están ordenadas por prioridad correcta**
6. **Las propuestas estructurales no tienen contradicciones**
7. **El plan tiene versión incrementada**
8. **El historial de cambios está documentado**

Si alguna validación falla, corregir antes de finalizar.
