---
name: gap-resolution
description: Gap Resolution - Sesiones colaborativas para resolver gaps identificados en documentación mediante preguntas, lluvia de ideas y validación conjunta. NO identifica gaps nuevos, solo resuelve gaps ya identificados con estado [PENDIENTE].
---

# Gap Resolution

## Objetivos y Principios

**Propósito fundamental**: Facilitar sesiones interactivas donde el usuario y el AI colaboran para resolver gaps identificados en documentación, mediante rondas de preguntas estructuradas, lluvia de ideas, creación de definiciones y establecimiento de razonamientos que deben ser validados por el usuario.

**Límite de responsabilidad**: Este skill NO identifica gaps nuevos. Solo trabaja con gaps ya identificados con estado `[PENDIENTE]`. La identificación de gaps es responsabilidad de un proceso previo de análisis de documentación que genera preguntas críticas sobre el documento.

**Principios de interacción**:
- **Enfoque colaborativo**: La sesión es un diálogo bidireccional donde el AI propone y el usuario valida
- **Rondas estructuradas**: Las preguntas se organizan en rondas temáticas con apoyo y sugerencias específicas
- **Validación continua**: Cada propuesta, definición o razonamiento requiere confirmación explícita del usuario
- **Brainstorming guiado**: Proveer sugerencias y alternativas para estimular el pensamiento creativo del usuario
- **Construcción progresiva**: Avanzar desde conceptos fundamentales hacia detalles más específicos
- **Documentación en tiempo real**: Capturar decisiones, definiciones y razonamientos a medida que se validan
- **Respeto a prioridades**: Seguir las prioridades asignadas en el proceso de identificación de gaps (Crítico > Alto > Medio > Bajo)
- **No re-identificación**: No crear nuevos gaps, solo resolver los existentes

**Responsabilidades**:
- Preparar la sesión revisando gaps identificados en el documento
- Establecer orden de trabajo basado en prioridades asignadas a los gaps
- Realizar rondas de preguntas estructuradas con contexto y sugerencias
- Facilitar brainstorming guiado para estimular el pensamiento del usuario
- Validar cada propuesta, definición o razonamiento con el usuario
- Documentar decisiones, definiciones y razonamientos en tiempo real
- Incorporar respuestas validadas en la sección de gaps del documento (NO en el contenido principal)
- Documentar gaps persistentes con planes de acción
- Actualizar estados de gaps de `[PENDIENTE]` a `[RESUELTO]`

**Lo que NO hace este skill**:
- NO identifica gaps nuevos (responsabilidad del proceso de análisis de documentación)
- NO califica documentos (responsabilidad del proceso de análisis de documentación)
- NO modifica prioridades asignadas en el proceso de identificación
- NO trabaja con gaps en estado `[NO APLICA]` u `[OBSOLETO]`
- NO edita el contenido principal del documento (solo agrega respuestas en la sección de gaps)

**Investigación de fuentes**: gap-resolution SÍ puede investigar fuentes externas durante las rondas de preguntas porque la documentación pudo mejorar entre el proceso de identificación de gaps y este paso. Esta investigación se realiza para:
- Encontrar respuestas en documentos actualizados
- Validar si gaps ya fueron resueltos en otras fuentes
- Proveer contexto adicional para las sugerencias
- Documentar referencias que respalden las propuestas

Este skill facilita sesiones interactivas donde el usuario y el AI colaboran para resolver gaps identificados en documentación. Para detalles completos sobre objetivos, principios y proceso, consulta los archivos de referencia en el directorio `reference/`.

## Estructura del Skill

Este skill utiliza una estructura modular para facilitar el mantenimiento y la navegación. Los componentes detallados se encuentran en:

### Archivos Principales

- **`SKILL.md`**: Este archivo - Objetivos, principios, límites de responsabilidad y resumen del proceso
- **`reference/workflows.md`**: Índice de los pasos del proceso con enlaces a archivos detallados

### Archivos de Proceso (workflows/)

- **`workflows/00-preparation.md`**: Preparación de la sesión
- **`workflows/01-question-rounds.md`**: Rondas de preguntas estructuradas
- **`workflows/02-response-handling.md`**: Manejo de respuestas del usuario
- **`workflows/03-documentation.md`**: Documentación de resultados

### Archivos de Referencia

- **`reference/guardrails.md`**: Errores comunes, manejo de situaciones especiales y mejores prácticas (incluye objetivos y principios)
- **`reference/templates.md`**: Plantillas de formato para sesión, rondas de preguntas, respuestas y resultados
- **`reference/idempotency.md`**: Gestión de idempotencia y detección de sesión previa
- **`reference/state-transitions.md`**: Diagrama de transiciones de estados de gaps
- **`reference/input-output.md`**: Expectativas de entrada y salida del skill
- **`reference/flowchart.md`**: Diagrama de flujo visual del proceso completo
- **`reference/troubleshooting.md`**: Guía de troubleshooting para casos borde
- **`reference/gap-classification.md`**: Tipos de gaps, roles involucrados y enfoques por tipo

## Resumen del Proceso

El proceso sigue 4 pasos sistemáticos:

1. **Preparación de la sesión**: Revisar gaps identificados, establecer orden de trabajo y documentar estado inicial
2. **Rondas de preguntas estructuradas**: Para cada gap, realizar rondas con contexto, preguntas, sugerencias y validación
3. **Manejo de respuestas**: Documentar validaciones, modificaciones o rechazos según el feedback del usuario
4. **Documentación de resultados**: Incorporar respuestas validadas al documento y documentar gaps persistentes

Para instrucciones detalladas paso a paso, consulta **`reference/workflows.md`**.

## Gestión de Idempotencia

Para detalles sobre gestión de idempotencia, consultar `reference/idempotency.md`.

## Expectativas de Entrada/Salida

Para detalles sobre expectativas de entrada y salida, consultar `reference/input-output.md`.

## Uso

Invoca este skill cuando:
- Un documento tiene gaps identificados con estado `[PENDIENTE]`
- Necesitas resolver gaps colaborativamente con el usuario
- Necesitas hacer lluvia de ideas para definir conceptos o estrategias
- Quieres establecer razonamientos y justificaciones con validación del usuario
- El documento tiene secciones que requieren desarrollo conjunto

**Prerrequisito**: El documento debe haber sido analizado previamente para identificar gaps y tener gaps con estado `[PENDIENTE]`. Los gaps deben tener prioridades asignadas (Crítico/Alto/Medio/Bajo) y categorías temáticas definidas.

## Instrucción de Lista de Tareas

**ANTES DE COMENZAR**: Debes crear una lista de tareas utilizando la herramienta `todo_list` con cada paso a ejecutar y su descripción. Esta lista debe incluir:

- **Todos los pasos del proceso** (pasos 1-4) con descripciones claras
- **Estado inicial**: Marcar el primer paso como "in_progress" y los demás como "pending"
- **Prioridades**: Asignar prioridad "high" a pasos críticos, "medium" a pasos importantes
- **Actualización continua**: Marcar cada tarea como "completed" inmediatamente después de terminarla
- **Visibilidad**: Esto permite tener claro qué se debe hacer antes de empezar y seguimiento del progreso

**Ejemplo de estructura de tareas**:
1. Preparación de la Sesión - Revisar gaps identificados, establecer orden de trabajo y documentar estado inicial
2. Rondas de Preguntas Estructuradas - Para cada gap, realizar rondas con contexto, preguntas, sugerencias y validación
3. Manejo de Respuestas - Documentar validaciones, modificaciones o rechazos según feedback del usuario
4. Documentación de Resultados - Incorporar respuestas validadas al documento y documentar gaps persistentes

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
