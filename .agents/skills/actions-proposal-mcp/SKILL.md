---
name: actions-proposal-mcp
description: Actions Proposal MCP - Genera propuestas de mejora basadas en gaps resueltos para integrar respuestas al contenido principal, con gestión idempotente de propuestas existentes. Usa las herramientas MCP de Alejandria para operar sobre gaps y documentos almacenados en la base de datos.
---

# Actions Proposal MCP

## Objetivos y Principios

**Propósito fundamental**: Generar propuestas de mejora basadas en gaps resueltos (responded) para integrar respuestas al contenido principal, proponiendo mejoras estructurales y de redacción, e identificando documentos impactados indirectamente. Este skill usa las herramientas MCP de Alejandria (`create_proposal`, `list_gaps`, `read_document`, `write_document`) para operar sobre la base de datos.

**Diferencia con actions-proposal**: Este skill usa las herramientas MCP de Alejandria para crear propuestas en la base de datos en lugar de escribir planes de trabajo directamente en archivos. Las propuestas se almacenan como entidades `Proposal` en la base de datos y se pueden ejecutar posteriormente.

**Principios de generación**:
- **Idempotencia**: El proceso es idempotente - ejecuciones múltiples no generan propuestas duplicadas
- **Validación de propuesta vigente**: Detecta si existe una propuesta para los gaps y valida su vigencia antes de proponer nuevas acciones
- **Creación de propuestas**: El skill crea propuestas usando `create_proposal` en la base de datos
- **Sin edición directa**: El skill NO edita directamente el documento usando `write_document` - solo crea propuestas
- **Priorización por impacto en calificación**: Organiza acciones basándose en su impacto en la calificación del documento, no solo en la prioridad del gap
- **Asignación de responsables**: Sugiere roles funcionales responsables para cada acción
- **Referencias específicas**: Cada acción incluye referencias a fuentes necesarias para su ejecución
- **Priorización de tipo de acción**: Aplica un orden jerárquico estricto: (1) ediciones del documento analizado, (2) ediciones a documentos existentes, (3) creación de nuevos documentos como último recurso
- **Consolidación temática**: Sugiere organización de hallazgos en documentos estructurados apropiados solo cuando las ediciones no son suficientes
- **División atómica**: Propone división de documentos densos o grandes en documentos atómicos cuando el documento excede los límites de tamaño recomendados para su tipo
- **Documentos siguientes**: Identifica y propone documentos lógicos como siguientes pasos para extender la documentación del sistema solo cuando no caben en la estructura existente
- **Mejoras de redacción**: Propone mejoras de estilo narrativo, evitando colecciones excesivas de bullet points y promoviendo documentos narrativos
- **Impacto indirecto**: Identifica documentos impactados indirectamente por las respuestas de gaps y propone actualizaciones correspondientes
- **Uso de herramientas MCP**: Todas las operaciones se realizan mediante herramientas MCP de Alejandria

**Responsabilidades**:
- Generar propuestas basadas en gaps resueltos (responded) usando `list_gaps`
- Proponer cómo integrar las respuestas de gaps al contenido principal de la documentación
- Proponer mejoras de redacción y estilo (evitar colecciones de bullet points, promover documentos narrativos, identificar texto out of scope)
- Identificar documentos impactados indirectamente por las respuestas de gaps y proponer actualizaciones correspondientes
- Evaluar calidad, densidad temática y tamaño del documento para informar propuestas estructurales
- Crear propuestas usando `create_proposal` en la base de datos
- Proponer mejoras estructurales (división atómica, consolidación, documentos siguientes) cuando sea necesario
- Validar y actualizar propuestas existentes
- Priorizar acciones de edición del documento analizado sobre propuestas de nuevos documentos
- Sugerir ediciones a documentos existentes antes de proponer nuevos documentos
- Sugerir consolidación de hallazgos en documentos estructurados solo cuando las ediciones no son suficientes
- Proponer división atómica de documentos densos o grandes
- Identificar y proponer documentos lógicos como siguientes pasos solo cuando no caben en la estructura existente
- Mantener trazabilidad entre gaps resueltos y acciones de integración
- **NO editar directamente el documento** usando `write_document` - solo crea propuestas

## Estructura del Skill

Este skill utiliza una estructura modular para facilitar el mantenimiento y la navegación.

### Archivos Principales

- **`SKILL.md`**: Este archivo - Objetivos, principios y resumen del proceso
- **`reference/workflows.md`**: Índice de los pasos del proceso con enlaces a archivos detallados

### Archivos de Proceso (workflows/)

- **`workflows/00-detection.md`**: Detección de propuesta existente usando `list_gaps`
- **`workflows/01-validation.md`**: Validación de vigencia de la propuesta
- **`workflows/02-proposal.md`**: Propuesta de nuevas acciones
- **`workflows/03-creation.md`**: Creación de propuesta usando `create_proposal`
- **`workflows/04-atomic-division.md`**: Propuesta de división atómica
- **`workflows/05-consolidation.md`**: Sugerencia de consolidación
- **`workflows/06-next-documents.md`**: Propuesta de documentos siguientes

### Archivos de Referencia

- **`reference/objectives-principles.md`**: Propósito fundamental, principios de generación y distinción con otros skills
- **`reference/guardrails.md`**: Errores comunes y mejores prácticas específicas de actions-proposal-mcp
- **`reference/templates.md`**: Plantillas de formato para propuestas y validación de propuestas vigentes
- **`reference/idempotency.md`**: Gestión de idempotencia y detección de propuesta existente
- **`reference/io-expectations.md`**: Expectativas de entrada y salida del skill
- **`reference/priorities.md`**: Niveles de prioridad de acciones y criterios de ordenamiento
- **`reference/action-types.md`**: Tipos de acciones (edición documento actual, edición documentos existentes, creación nuevos documentos)
- **`reference/flowchart.md`**: Diagrama de flujo visual del proceso completo
- **`reference/troubleshooting.md`**: Guía de troubleshooting para casos borde
- **`reference/mcp-tools.md`**: Referencia de herramientas MCP disponibles

## Herramientas MCP Utilizadas

Este skill utiliza las siguientes herramientas MCP de Alejandria:

- **`read_document`**: Leer el contenido del documento desde la base de datos (usa document_slug)
- **`list_gaps`**: Obtener gaps existentes para un documento (usa document_slug, filtrar por status=responded)
- **`create_proposal`**: Crear propuestas de mejora en la base de datos (usa gap_slugs, genera proposal_slug automáticamente)
- **`search_similar_documents`**: Buscar documentos similares para identificar impacto indirecto

## Proceso

El proceso sigue un enfoque sistemático organizado en 5 fases:

**Fase 1: Evaluación de Calidad** (Paso 8)
- Evaluación de calidad del documento usando `read_document`
- Evaluación de densidad temática
- Evaluación de tamaño del documento
- Análisis de impacto en calificación (Paso 8b)

**Fase 2: Gestión de Propuesta Existente** (Pasos 0-1)
- Detección de propuesta existente usando `list_gaps`
- Validación de vigencia de la propuesta

**Fase 3: Propuesta de Acciones** (Paso 2)
- Propuesta de acciones para integrar respuestas de gaps resueltos (responded) al contenido principal (incluyendo ediciones del documento actual, ediciones a documentos existentes, y creación de nuevos documentos como último recurso)
- Propuesta de mejoras de redacción y estilo (evitar colecciones de bullet points, promover documentos narrativos, identificar texto out of scope)
- Identificación de documentos impactados indirectamente por las respuestas de gaps y propuesta de actualizaciones correspondientes
- Priorización basada en impacto en calificación del documento

**Fase 4: Creación de la Propuesta** (Paso 3)
- Creación de propuesta usando `create_proposal` con calificación esperada

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
- Se ha validado la vigencia de la propuesta existente (si aplica)
- Se han propuesto acciones para integrar todos los gaps resueltos (responded) al contenido principal, priorizando por impacto en calificación
- Se han propuesto mejoras de redacción y estilo cuando sea necesario
- Se han identificado documentos impactados indirectamente por las respuestas de gaps y se han propuesto actualizaciones correspondientes
- Se ha creado la propuesta usando `create_proposal` con versión incrementada y calificación esperada
- Se ha propuesto división atómica si el documento excede los límites de tamaño recomendados para su tipo
- Se ha sugerido consolidación si aplica
- Se han identificado documentos siguientes lógicos cuando no caben en la estructura existente

### Resumen de Pasos

**Fase 1: Evaluación de Calidad**
0. **Evaluación de Calidad**: Evaluar calidad, densidad y tamaño del documento usando `read_document`
1. **Análisis de Impacto en Calificación**: Analizar cómo cada gap resuelto mejorará la calificación del documento

**Fase 2: Gestión de Propuesta Existente**
2. **Detección de Propuesta Existente**: Determinar si existe una propuesta previa usando `list_gaps`
3. **Validación de Vigencia**: Validar si la propuesta existente sigue siendo vigente dado el estado actual de gaps

**Fase 3: Propuesta de Acciones**
4. **Propuesta de Acciones**: Generar acciones para integrar gaps resueltos (responded) al contenido principal, priorizando por impacto en calificación. Incluye propuestas de mejoras de redacción y estilo, e identificación de documentos impactados indirectamente

**Fase 4: Creación de la Propuesta**
5. **Creación de la Propuesta**: Crear propuesta usando `create_proposal` con versionamiento y calificación esperada

**Fase 5: Propuestas Estructurales**
6. **Propuesta de División Atómica**: Proponer división de documentos densos o grandes en documentos atómicos si el documento excede los límites de tamaño recomendados
7. **Sugerencia de Consolidación**: Proponer organización de hallazgos en documentos estructurados si aplica
8. **Propuesta de Documentos Siguientes**: Identificar y proponer documentos lógicos como siguientes pasos cuando no caben en la estructura existente
9. **Validación Cruzada de Propuestas**: Validar consistencia entre tipos de propuestas estructurales y acciones propuestas

## Gestión de Idempotencia

Para detalles sobre gestión de idempotencia, consultar `reference/idempotency.md`.

## Expectativas de Entrada/Salida

Para detalles sobre expectativas de entrada y salida, consultar `reference/io-expectations.md`.

## Uso

Invoca este skill cuando el documento tiene gaps con estado `responded` (gaps que ya tienen respuestas documentadas) para generar propuestas de mejora de forma idempotente. El skill ayudará a mantener una propuesta vigente y actualizada, evitando generación infinita de propuestas mediante gestión de estado y validación de vigencia. El skill crea propuestas usando `create_proposal` en la base de datos, pero NO edita directamente el documento.

**Entrada esperada**:
- `document_slug`: Slug del documento en Alejandria

**Salida esperada**:
- Propuesta creada en la base de datos usando `create_proposal`
- Gaps asociados a la propuesta

## Instrucción de Lista de Tareas

**ANTES DE COMENZAR**: Debes crear una lista de tareas utilizando la herramienta `todo_list` con cada paso a ejecutar y su descripción. Esta lista debe incluir:

- **Todos los pasos del proceso** (Fase 1-4, pasos 0-6) con descripciones claras
- **Estado inicial**: Marcar el primer paso como "in_progress" y los demás como "pending"
- **Prioridades**: Asignar prioridad "high" a pasos críticos, "medium" a pasos importantes
- **Actualización continua**: Marcar cada tarea como "completed" inmediatamente después de terminarla
- **Visibilidad**: Esto permite tener claro qué se debe hacer antes de empezar y seguimiento del progreso

**Ejemplo de estructura de tareas**:
0. Detección de Propuesta Existente - Determinar si existe una propuesta previa usando list_gaps
1. Validación de Vigencia - Validar si la propuesta existente sigue siendo vigente
2. Propuesta de Acciones - Generar acciones para integrar gaps resueltos al contenido principal
3. Creación de la Propuesta - Crear propuesta usando create_proposal con versionamiento
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
- **Herramientas MCP disponibles**: Consulta `reference/mcp-tools.md`
