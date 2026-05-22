---
name: actions-proposal
description: Actions Proposal - Genera planes de trabajo basados en gaps resueltos para integrar respuestas al contenido principal, con gestión idempotente de planes existentes, sin realizar otras ediciones en el archivo
---

# Actions Proposal

## Objetivos y Principios

**Propósito fundamental**: Generar planes de trabajo basados en gaps resueltos ([RESUELTO]) para integrar respuestas al contenido principal, proponiendo mejoras estructurales y de redacción, e identificando archivos impactados indirectamente. El skill SÍ escribe el plan de trabajo en el archivo y actualiza el estado de gaps de [RESUELTO] a [PLANEADO], pero NO realiza otras ediciones como integrar respuestas al contenido principal, actualizar la calificación final del documento, o actualizar otros estados de gaps.

**Principios de generación**:
- **Idempotencia**: El proceso es idempotente - ejecuciones múltiples no generan planes duplicados
- **Validación de plan vigente**: Detecta si existe un plan de trabajo y valida su vigencia antes de proponer nuevas acciones
- **Escritura del plan**: El skill SÍ escribe el plan de trabajo en el archivo analizado
- **Sin otras ediciones**: El skill NO realiza otras ediciones en el archivo (no integra respuestas al contenido principal, no actualiza la calificación final del documento, no actualiza otros estados de gaps excepto [RESUELTO] → [PLANEADO])
- **Priorización por impacto en calificación**: Organiza acciones basándose en su impacto en la calificación del documento, no solo en la prioridad del gap
- **Asignación de responsables**: Sugiere roles funcionales responsables para cada acción
- **Referencias específicas**: Cada acción incluye referencias a fuentes necesarias para su ejecución
- **Priorización de tipo de acción**: Aplica un orden jerárquico estricto: (1) ediciones del archivo analizado, (2) ediciones a archivos existentes, (3) creación de nuevos archivos como último recurso
- **Consolidación temática**: Sugiere organización de hallazgos en documentos estructurados apropiados solo cuando las ediciones no son suficientes
- **División atómica**: Propone división de documentos densos o grandes en archivos atómicos cuando el documento excede los límites de tamaño recomendados para su tipo
- **Documentos siguientes**: Identifica y propone documentos lógicos como siguientes pasos para extender la documentación del sistema solo cuando no caben en la estructura existente
- **Mejoras de redacción**: Propone mejoras de estilo narrativo, evitando colecciones excesivas de bullet points y promoviendo documentos narrativos
- **Impacto indirecto**: Identifica archivos impactados indirectamente por las respuestas de gaps y propone actualizaciones correspondientes

**Responsabilidades**:
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

## Estructura del Skill

Este skill utiliza una estructura modular para facilitar el mantenimiento y la navegación. Los componentes detallados se encuentran en:

### Archivos Principales

- **`SKILL.md`**: Este archivo - Objetivos, principios y resumen del proceso
- **`reference/workflows.md`**: Índice de los pasos del proceso con enlaces a archivos detallados

### Archivos de Proceso (workflows/)

- **`workflows/00-detection.md`**: Detección de plan de trabajo existente
- **`workflows/01-validation.md`**: Validación de vigencia del plan
- **`workflows/02-proposal.md`**: Propuesta de nuevas acciones
- **`workflows/03-update.md`**: Actualización del plan de trabajo
- **`workflows/04-atomic-division.md`**: Propuesta de división atómica
- **`workflows/05-consolidation.md`**: Sugerencia de consolidación
- **`workflows/06-next-documents.md`**: Propuesta de documentos siguientes

### Archivos de Referencia

- **`reference/objectives-principles.md`**: Propósito fundamental, principios de generación y distinción con otros skills
- **`reference/guardrails.md`**: Errores comunes y mejores prácticas específicas de actions-proposal
- **`reference/templates.md`**: Plantillas de formato para planes de trabajo y validación de planes vigentes
- **`reference/idempotency.md`**: Gestión de idempotencia y detección de plan existente
- **`reference/io-expectations.md`**: Expectativas de entrada y salida del skill
- **`reference/priorities.md`**: Niveles de prioridad de acciones y criterios de ordenamiento
- **`reference/action-types.md`**: Tipos de acciones (edición archivo actual, edición archivos existentes, creación nuevos archivos)
- **`reference/flowchart.md`**: Diagrama de flujo visual del proceso completo
- **`reference/troubleshooting.md`**: Guía de troubleshooting para casos borde

## Proceso

El proceso sigue un enfoque sistemático organizado en 5 fases:

**Fase 1: Evaluación de Calidad** (Paso 8)
- Evaluación de calidad del documento
- Evaluación de densidad temática
- Evaluación de tamaño del documento
- Análisis de impacto en calificación (Paso 8b)

**Fase 2: Gestión de Plan Existente** (Pasos 0-1)
- Detección de plan de trabajo existente
- Validación de vigencia del plan

**Fase 3: Propuesta de Acciones** (Paso 2)
- Propuesta de acciones para integrar respuestas de gaps resueltos al contenido principal (incluyendo ediciones del archivo actual, ediciones a archivos existentes, y creación de nuevos archivos como último recurso)
- Propuesta de mejoras de redacción y estilo (evitar colecciones de bullet points, promover documentos narrativos, identificar texto out of scope)
- Identificación de archivos impactados indirectamente por las respuestas de gaps y propuesta de actualizaciones correspondientes
- Priorización basada en impacto en calificación del documento

**Fase 4: Actualización del Plan** (Paso 3)
- Actualización del plan de trabajo con calificación esperada

**Fase 5: Propuestas Estructurales** (Pasos 4-7)
- Propuesta de división atómica
- Sugerencia de consolidación
- Propuesta de documentos siguientes
- Validación cruzada de propuestas

Para instrucciones detalladas paso a paso, consulta **`reference/workflows.md`**.

### Criterios de Terminación

El proceso termina cuando:
- Se ha evaluado la calidad, densidad y tamaño del documento
- Se ha analizado el impacto en calificación de cada gap resuelto
- Se ha validado la vigencia del plan existente (si aplica)
- Se han propuesto acciones para integrar todos los gaps resueltos ([RESUELTO]) al contenido principal, priorizando por impacto en calificación
- Se han propuesto mejoras de redacción y estilo cuando sea necesario
- Se han identificado archivos impactados indirectamente por las respuestas de gaps y se han propuesto actualizaciones correspondientes
- Se ha actualizado el plan de trabajo con versión incrementada y calificación esperada
- Se ha propuesto división atómica si el documento excede los límites de tamaño recomendados para su tipo
- Se ha sugerido consolidación si aplica
- Se han identificado documentos siguientes lógicos cuando no caben en la estructura existente

### Resumen de Pasos

**Fase 1: Evaluación de Calidad**
0. **Evaluación de Calidad**: Evaluar calidad, densidad y tamaño del documento
1. **Análisis de Impacto en Calificación**: Analizar cómo cada gap resuelto mejorará la calificación del documento

**Fase 2: Gestión de Plan Existente**
2. **Detección de Plan Existente**: Determinar si existe un plan de trabajo previo en el documento
3. **Validación de Vigencia**: Validar si el plan existente sigue siendo vigente dado el estado actual de gaps

**Fase 3: Propuesta de Acciones**
4. **Propuesta de Acciones**: Generar acciones para integrar gaps resueltos ([RESUELTO]) al contenido principal, priorizando por impacto en calificación. Incluye propuestas de mejoras de redacción y estilo, e identificación de archivos impactados indirectamente

**Fase 4: Actualización del Plan**
5. **Actualización del Plan**: Actualizar el plan de trabajo existente o crear uno nuevo con versionamiento y calificación esperada

**Fase 5: Propuestas Estructurales**
6. **Propuesta de División Atómica**: Proponer división de documentos densos o grandes en archivos atómicos si el documento excede los límites de tamaño recomendados
7. **Sugerencia de Consolidación**: Proponer organización de hallazgos en documentos estructurados si aplica
8. **Propuesta de Documentos Siguientes**: Identificar y proponer documentos lógicos como siguientes pasos cuando no caben en la estructura existente
9. **Validación Cruzada de Propuestas**: Validar consistencia entre tipos de propuestas estructurales y acciones propuestas

## Gestión de Idempotencia

Para detalles sobre gestión de idempotencia, consultar `reference/idempotency.md`.

## Expectativas de Entrada/Salida

Para detalles sobre expectativas de entrada y salida, consultar `reference/io-expectations.md`.

## Uso

Invoca este skill cuando el documento tiene gaps con estado `[RESUELTO]` (gaps que ya tienen respuestas documentadas) para generar planes de trabajo de forma idempotente. El skill ayudará a mantener un plan de trabajo vigente y actualizado, evitando generación infinita de planes mediante gestión de estado y validación de vigencia. El skill SÍ escribe el plan de trabajo en el archivo y actualiza estados de [RESUELTO] a [PLANEADO], pero NO realiza otras ediciones (no integra respuestas al contenido principal, no actualiza otros estados de gaps).

## Instrucción de Lista de Tareas

**ANTES DE COMENZAR**: Debes crear una lista de tareas utilizando la herramienta `todo_list` con cada paso a ejecutar y su descripción. Esta lista debe incluir:

- **Todos los pasos del proceso** (Fase 1-4, pasos 0-6) con descripciones claras
- **Estado inicial**: Marcar el primer paso como "in_progress" y los demás como "pending"
- **Prioridades**: Asignar prioridad "high" a pasos críticos, "medium" a pasos importantes
- **Actualización continua**: Marcar cada tarea como "completed" inmediatamente después de terminarla
- **Visibilidad**: Esto permite tener claro qué se debe hacer antes de empezar y seguimiento del progreso

**Ejemplo de estructura de tareas**:
0. Detección de Plan Existente - Determinar si existe un plan de trabajo previo
1. Validación de Vigencia - Validar si el plan existente sigue siendo vigente
2. Propuesta de Acciones - Generar acciones para integrar gaps resueltos al contenido principal
3. Actualización del Plan - Actualizar o crear plan de trabajo con versionamiento
4. Propuesta de División Atómica - Proponer división si aplica
5. Sugerencia de Consolidación - Proponer organización si aplica
6. Propuesta de Documentos Siguientes - Identificar documentos lógicos siguientes

## Referencias Adicionales

Para detalles específicos sobre:

- **Objetivos y principios**: Consulta `reference/objectives-principles.md`
- **Proceso de propuesta**: Consulta `reference/workflows.md`
- **Errores comunes y mejores prácticas**: Consulta `reference/guardrails.md`
- **Plantillas de formato**: Consulta `reference/templates.md`
- **Gestión de idempotencia**: Consulta `reference/idempotency.md`
- **Expectativas de entrada/salida**: Consulta `reference/io-expectations.md`
