# Objetivos y Principios

## Propósito Fundamental

Generar planes de trabajo basados en gaps resueltos ([RESUELTO]) para integrar respuestas al contenido principal, proponiendo mejoras estructurales y de redacción, e identificando archivos impactados indirectamente. El skill SÍ escribe el plan de trabajo en el archivo analizado y actualiza el estado de gaps de [RESUELTO] a [PLANEADO], pero NO realiza otras ediciones como integrar respuestas al contenido principal, actualizar la calificación final del documento, o actualizar otros estados de gaps.

## Principios de Generación

- **Idempotencia**: El proceso es idempotente - ejecuciones múltiples no generan planes duplicados
- **Validación de plan vigente**: Detecta si existe un plan de trabajo y valida su vigencia antes de proponer nuevas acciones
- **Escritura del plan**: El skill SÍ escribe el plan de trabajo en el archivo analizado (Paso 5)
- **Sin otras ediciones**: El skill NO realiza otras ediciones en el archivo (no integra respuestas al contenido principal, no actualiza la calificación final del documento, no actualiza otros estados de gaps excepto [RESUELTO] → [PLANEADO])
- **Priorización por impacto en calificación**: Organiza acciones basándose en su impacto en la calificación del documento, no solo en la prioridad del gap
- **Asignación de responsables**: Sugiere roles funcionales responsables para cada acción
- **Referencias específicas**: Cada acción incluye referencias a fuentes necesarias para su ejecución
- **Priorización de tipo de acción**: Aplica un orden jerárquico estricto: (1) ediciones del archivo analizado, (2) ediciones a archivos existentes, (3) creación de nuevos archivos como último recurso
- **Consolidación temática**: Sugiere organización de hallazgos en documentos estructurados apropiados solo cuando las ediciones no son suficientes
- **División atómica**: Propone división de documentos densos o grandes en archivos atómicos cuando el documento excede los límites de tamaño recomendados para su tipo
- **Documentos siguientes**: Identifica y propone documentos lógicos como siguientes pasos para extender la documentación del sistema solo cuando no caben en la estructura existente
- **Validación de autonomía**: Cada archivo atómico propuesto debe ser autónomo con contenido sustantivo propio
- **Evitar archivos tipo índice**: No proponer división que resulte en archivos que solo sirven como índices o resúmenes
- **Trazabilidad**: Mantener trazabilidad clara entre gaps resueltos y acciones de integración propuestas

## Cuándo Usar Este Skill

- Cuando el documento tiene gaps con estado `[RESUELTO]` (gaps que ya tienen respuestas documentadas)
- Cuando existe un plan de trabajo previo que necesita validación de vigencia
- Cuando se requiere proponer mejoras estructurales (división atómica, consolidación, documentos siguientes)
- Cuando se necesita mantener un plan de trabajo vigente y actualizado
- Para evitar generación infinita de planes mediante gestión de estado y validación de vigencia

## Responsabilidades del Skill

- Generar planes de trabajo basados en gaps resueltos ([RESUELTO])
- Proponer cómo integrar las respuestas de gaps al contenido principal de la documentación
- Proponer mejoras de redacción y estilo (evitar colecciones de bullet points, promover documentos narrativos, identificar texto out of scope)
- Identificar archivos impactados indirectamente por las respuestas de gaps y proponer actualizaciones correspondientes
- Evaluar calidad, densidad temática y tamaño del documento para informar propuestas estructurales
- Escribir el plan de trabajo en el archivo analizado
- Proponer mejoras estructurales (división atómica, consolidación, documentos siguientes) cuando sea necesario
- Validar y actualizar planes de trabajo existentes
- Priorizar acciones de edición del archivo analizado sobre propuestas de nuevos archivos
- Sugerir ediciones a archivos existentes antes de proponer nuevos documentos
- Sugerir consolidación de hallazgos en documentos estructurados solo cuando las ediciones no son suficientes
- Proponer división atómica de documentos densos o grandes
- Identificar y proponer documentos lógicos como siguientes pasos solo cuando no caben en la estructura existente
- Mantener trazabilidad entre gaps resueltos y acciones de integración
- Actualizar estados de gaps de [RESUELTO] a [PLANEADO] para gaps con acciones propuestas
- **NO realizar otras ediciones** en el archivo (no integrar respuestas al contenido principal, no actualizar la calificación final del documento, no actualizar otros estados de gaps excepto [RESUELTO] → [PLANEADO])

## Responsabilidades que NO son de Este Skill

- **NO clasificar el documento**: Eso es responsabilidad del proceso de identificación de gaps y preguntas críticas
- **NO calificar el documento inicial**: Eso es responsabilidad del proceso de identificación de gaps y preguntas críticas
- **NO integrar respuestas al contenido principal**: Eso es responsabilidad del proceso de aplicación de planes de trabajo
- **NO actualizar estados de gaps a [IMPLEMENTADO]**: Eso es responsabilidad del proceso de aplicación de planes de trabajo
- **NO aplicar el plan de trabajo**: Eso es responsabilidad del proceso de aplicación de planes de trabajo
- **NO actualizar la calificación final del documento**: Eso es responsabilidad del proceso de aplicación de planes de trabajo (después de aplicar los cambios)
- **NO generar gaps o preguntas críticas**: Eso es responsabilidad del proceso de identificación de gaps y preguntas críticas
- **NO resolver gaps**: Eso es responsabilidad del proceso de resolución de gaps

## Distinción Clave con Otros Procesos

### vs Proceso de Identificación de Gaps y Preguntas Críticas

- **Proceso de identificación de gaps**: Genera preguntas críticas (gaps) y identifica contexto faltante
- **actions-proposal**: Genera planes de trabajo para integrar respuestas de gaps ya resueltos

### vs Proceso de Resolución de Gaps

- **Proceso de resolución de gaps**: Resuelve gaps respondiendo las preguntas críticas
- **actions-proposal**: Genera planes de trabajo para integrar esas respuestas al contenido principal

### vs Proceso de Aplicación de Planes de Trabajo

- **Proceso de aplicación de planes**: Aplica el plan de trabajo generado por actions-proposal, integra respuestas al contenido principal, actualiza estados de gaps de [PLANEADO] a [IMPLEMENTADO], actualiza la calificación final del documento para reflejar el estado real después de los cambios, y mejora la calidad completa de la documentación implementando cambios en documentos relacionados del plan (sin agregar información no existente ni inventar razonamientos)
- **actions-proposal**: Genera el plan de trabajo basado en gaps resueltos, proponiendo mejoras estructurales y de redacción, pero NO aplica los cambios ni actualiza la calificación final

## Flujo de Ejecución del Sistema

```text
identificación de gaps (genera gaps)
  → resolución de gaps (resuelve gaps)
  → actions proposal (propone plan para usar respuestas)
  → aplicación de planes (aplica el plan)
```

Este skill es el único que propone acciones de integración. El proceso de aplicación de planes debe aplicar los cambios según el plan, sin añadir ni modificar el plan.

## Transición de Estados de Gaps

Los gaps pasan por los siguientes estados a lo largo del flujo del sistema:

### Estados de Gaps

- **`[PENDIENTE]`**: Gap identificado por el proceso de identificación de gaps, aún sin respuesta
- **`[RESPONDIDO]`**: Gap con respuesta proporcionada por el proceso de resolución de gaps
- **`[RESUELTO]`**: Gap cuya respuesta ha sido validada como adecuada por el proceso de resolución de gaps
- **`[PLANEADO]`**: Gap con acción de integración propuesta por actions-proposal
- **`[IMPLEMENTADO]`**: Gap cuya acción de integración ha sido ejecutada por el proceso de aplicación de planes

### Transiciones

1. **`[PENDIENTE]` → `[RESPONDIDO]`**: El proceso de resolución de gaps proporciona una respuesta al gap
2. **`[RESPONDIDO]` → `[RESUELTO]`**: El proceso de resolución de gaps valida que la respuesta es adecuada y completa
3. **`[RESUELTO]` → `[PLANEADO]`**: actions-proposal genera una acción de integración para el gap y actualiza el estado
4. **`[PLANEADO]` → `[IMPLEMENTADO]`**: El proceso de aplicación de planes ejecuta la acción de integración y actualiza el estado

### Responsabilidades por Estado

- **Proceso de identificación de gaps**: Crea gaps en estado `[PENDIENTE]`
- **Proceso de resolución de gaps**: Transiciona gaps de `[PENDIENTE]` a `[RESPONDIDO]` y luego a `[RESUELTO]`
- **actions-proposal**: Transiciona gaps de `[RESUELTO]` a `[PLANEADO]` al generar acciones de integración
- **Proceso de aplicación de planes**: Transiciona gaps de `[PLANEADO]` a `[IMPLEMENTADO]` al ejecutar las acciones
