# Paso 4: Actualización de Calificación del Documento

## Objetivo

Recalcular y actualizar la calificación del documento para reflejar su estado real después de los cambios implementados.

## Propósito

La calificación del documento debe reflejar su estado actual después de implementar el plan de trabajo. Esto permite mantener un registro preciso de la calidad de la documentación y verificar que las mejoras propuestas tuvieron el impacto esperado.

## Proceso

### 1. Leer la Calificación Original

Identificar la calificación actual del documento antes de los cambios. Esta calificación debe estar documentada en el frontmatter o en una sección de análisis previo.

### 2. Leer la Calificación Esperada

Revisar la calificación esperada que se definió en el plan de trabajo proporcionado. Esta calificación representa el objetivo de calidad después de implementar el plan.

### 3. Evaluar el Estado Actual del Documento

Analizar el documento después de los cambios para determinar su estado real:

- **Completitud**: ¿Se han integrado todas las respuestas de gaps?
- **Claridad**: ¿El contenido es claro y fácil de entender?
- **Consistencia**: ¿No hay contradicciones en el documento?
- **Estructura**: ¿La estructura del documento es lógica y organizada?
- **Referencias**: ¿Las referencias están completas y son apropiadas?
- **Documentos relacionados**: ¿Se han actualizado los documentos relacionados?

### 4. Calcular la Nueva Calificación

Basado en la evaluación del estado actual, calcular la nueva calificación del documento (escala 1-10). Considerar:

- Gaps que se resolvieron con la implementación
- Mejoras en claridad y consistencia
- Actualizaciones en documentos relacionados
- Cualquier problema residual que persista

### 5. Comparar con Calificación Esperada

Comparar la calificación calculada con la calificación esperada del plan de trabajo:

- Si son iguales o mayores: La implementación fue exitosa
- Si es menor: Documentar la discrepancia y las razones

### 6. Actualizar la Calificación en el Documento

Actualizar la calificación en el frontmatter del documento:

```yaml
---
rating: [nueva calificación]
rating-phase: [fase de calificación]
---
```

Si el documento no tiene frontmatter, agregarlo con la calificación.

## Criterios de Calificación

Evaluar el documento según los siguientes criterios:

- **Completitud (1-10)**: ¿Qué tan completo está el documento?
- **Claridad (1-10)**: ¿Qué tan claro es el contenido?
- **Consistencia (1-10)**: ¿Qué tan consistente es el documento?
- **Estructura (1-10)**: ¿Qué tan bien estructurado está el documento?
- **Referencias (1-10)**: ¿Qué tan completas son las referencias?

La calificación final es el promedio de estos criterios.

## Principios de Actualización

- **Evaluación objetiva**: Calificar basado en el estado real del documento
- **Comparación con esperado**: Verificar que se alcanzó el objetivo
- **Documentación de cambios**: Registrar la calificación anterior y la nueva
- **Justificación**: Documentar las razones de la calificación si es necesario

## Criterios de Terminación

Este paso termina cuando:

- Se ha leído la calificación original
- Se ha leído la calificación esperada
- Se ha evaluado el estado actual del documento
- Se ha calculado la nueva calificación
- Se ha comparado con la calificación esperada
- Se ha actualizado la calificación en el documento

## Salida

- Calificación actualizada en el documento
- Comparación entre calificación esperada y alcanzada
- Justificación de la calificación si es necesario
