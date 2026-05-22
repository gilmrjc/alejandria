# Paso 2: Propuesta de Nuevas Acciones

## Objetivo

Generar acciones para integrar gaps resueltos ([RESUELTO]) al contenido principal de la documentación, incluyendo propuestas de mejoras de redacción y estilo, e identificación de archivos impactados indirectamente por las respuestas de gaps.

## Identificación de Gaps Resueltos

1. Listar todos los gaps con estado `[RESUELTO]` (gaps que tienen respuestas pero aún no tienen acción de integración planeada)
2. Comparar con el plan de trabajo existente (si aplica)
3. Identificar gaps resueltos que no tienen acción de integración asignada
4. Ignorar gaps con estado `[PLANEADO]` (ya tienen acción de integración propuesta)

## Generación de Acciones

Para cada gap resuelto sin acción de integración asignada:

1. **Analizar la respuesta**: Entender la respuesta proporcionada al gap y el contexto
2. **Determinar la acción de integración**: Definir cómo integrar la respuesta al contenido principal
3. **Priorizar tipo de acción**: Aplicar el orden jerárquico estricto:
   - **Primero**: Ediciones del archivo analizado (siempre priorizar esto)
   - **Segundo**: Ediciones a archivos existentes (si las ediciones del archivo actual no son suficientes)
   - **Tercero**: Creación de nuevos archivos (solo como último recurso)
4. **Asignar prioridad**: Basarse en la prioridad del gap (Crítico/Alto/Medio/Bajo)
5. **Sugerir responsable**: Asignar el rol funcional más apropiado
6. **Identificar referencias**: Listar fuentes necesarias para ejecutar la acción
7. **Definir resultado esperado**: Describir qué resultado se espera de la acción

## Criterios para Decidir Entre Edición del Archivo Actual vs Archivos Existentes

**Priorizar siempre ediciones del archivo actual**. Solo considerar ediciones a archivos existentes cuando se cumpla AL MENOS UNO de los siguientes criterios:

### Criterios que Justifican Ediciones a Archivos Existentes

1. **Contexto fuera del tipo de documento actual**: El gap requiere información que no pertenece al tipo de documento actual
   - Ejemplo: Detalles técnicos de implementación en un PRD (Product Requirements Document)
   - Ejemplo: Decisiones de negocio en un documento de arquitectura técnica
   - Ejemplo: Justificación de producto en un manual de operaciones

2. **Información ya existe parcialmente en otro archivo**: La información que resolvería el gap ya está parcialmente documentada en otro archivo y sería mejor consolidarla allí
   - Verificar si el contenido ya existe en otro archivo relacionado
   - Si existe, sugerir edición a ese archivo en lugar de duplicar información

3. **Tamaño del archivo actual excesivo**: La edición requeriría más de 50 líneas adicionales al archivo actual
   - Evaluar si el archivo actual ya está cerca de su tamaño óptimo
   - Si agregar 50+ líneas haría el archivo demasiado denso, considerar archivo existente

4. **Archivo actual excede tamaño óptimo para su tipo**: El archivo actual ya excede el tamaño recomendado para su tipo de documento
   - PRDs: > 200 líneas
   - Especificaciones técnicas: > 300 líneas
   - ADRs: > 100 líneas
   - Manuales de usuario: > 400 líneas
   - Documentos de estrategia: > 150 líneas

### Proceso de Validación

Al considerar ediciones a archivos existentes:

1. **Evaluar contra criterios**: Verificar si se cumple al menos uno de los criterios anteriores
2. **Buscar archivos relevantes**: Identificar archivos existentes que puedan contener la información
3. **Validar existencia**: Confirmar que los archivos existan y sean accesibles
4. **Comparar opciones**: Evaluar si edición a archivo existente es mejor que edición del archivo actual
5. **Documentar justificación**: Si se elige edición a archivo existente, documentar claramente por qué

## Proceso para Ediciones a Archivos Existentes

Cuando el tipo de acción priorizado sea "Ediciones a archivos existentes":

1. **Analizar el gap**: Determinar qué tipo de documento o archivo podría contener la información faltante
2. **Explorar estructura del proyecto**: Identificar archivos existentes relacionados con el gap
3. **Evaluar relevancia**: Determinar si el archivo existente es el lugar apropiado para la información
4. **Validar existencia**: Confirmar que el archivo existe y es accesible
5. **Documentar la propuesta**: Usar el formato de ediciones a archivos existentes

## Formato de Propuesta de Ediciones a Archivos Existentes

```markdown
**EDICIONES A ARCHIVOS EXISTENTES PROPUESTAS**

### Archivo: [ruta del archivo]
- **Gap relacionado**: [Título del gap]
- **Acción propuesta**: [Descripción de la edición a realizar]
- **Justificación**: [Por qué este archivo es el lugar apropiado]
- **Referencias necesarias**: [fuentes a consultar]
- **Resultado esperado**: [descripción del resultado]
```

## Formato de Acciones

Usar el formato de `references/templates.md`:

```markdown
**PLAN DE TRABAJO**
- Fecha de creación: [YYYY-MM-DD]
- Versión del plan: [número incremental]
- Gaps a resolver: [cantidad]
- Prioridad de ejecución: [orden de prioridad]

## Acciones Prioritarias

### Prioridad 1: Crítica
- **Gap**: [Título del gap]
- **Acción**: [Descripción de la acción a tomar - PRIORIZAR EDICIONES DEL ARCHIVO ACTUAL]
- **Tipo de acción**: [Edición del archivo actual / Edición a archivo existente / Creación de nuevo archivo]
- **Responsable sugerido**: [Rol funcional]
- **Referencias necesarias**: [fuentes a consultar]
- **Resultado esperado**: [descripción del resultado]

### Prioridad 2: Alta
- **Gap**: [Título del gap]
- **Acción**: [Descripción de la acción a tomar - PRIORIZAR EDICIONES DEL ARCHIVO ACTUAL]
- **Tipo de acción**: [Edición del archivo actual / Edición a archivo existente / Creación de nuevo archivo]
- **Responsable sugerido**: [Rol funcional]
- **Referencias necesarias**: [fuentes a consultar]
- **Resultado esperado**: [descripción del resultado]

### Prioridad 3: Media
- **Gap**: [Título del gap]
- **Acción**: [Descripción de la acción a tomar - PRIORIZAR EDICIONES DEL ARCHIVO ACTUAL]
- **Tipo de acción**: [Edición del archivo actual / Edición a archivo existente / Creación de nuevo archivo]
- **Responsable sugerido**: [Rol funcional]
- **Referencias necesarias**: [fuentes a consultar]
- **Resultado esperado**: [descripción del resultado]
```

## Validación de Consistencia entre Respuesta del Gap y Acción de Integración

Para cada acción de integración propuesta, validar que sea consistente con la respuesta del gap:

1. **Implementación directa**: ¿La acción de integración implementa directamente la respuesta del gap en el contenido principal?
   - Verificar que la acción no sea genérica sino específica a la respuesta
   - Confirmar que la acción integre el contexto proporcionado en la respuesta

2. **Ejecutabilidad con referencias**: ¿La acción es ejecutable con las referencias proporcionadas en la respuesta?
   - Verificar que las referencias necesarias para la acción estén disponibles
   - Confirmar que las referencias sean suficientes para ejecutar la acción

3. **Correspondencia de resultado**: ¿El resultado esperado de la acción corresponde a la respuesta del gap?
   - Verificar que el resultado esperado describa el estado después de implementar la respuesta
   - Confirmar que el resultado sea medible y verificable

4. **Responsable apropiado**: ¿La acción tiene un responsable claro y apropiado para el tipo de respuesta?
   - Verificar que el rol funcional sugerido sea apropiado para el tipo de respuesta
   - Confirmar que el responsable tenga la autoridad para ejecutar la acción

Si alguna validación falla, revisar y ajustar la acción propuesta antes de continuar.

## Deduplicación de Acciones

Al generar nuevas acciones:

1. Verificar si ya existe una acción similar para el mismo gap
2. Si existe, actualizar la acción existente en lugar de crear una nueva
3. Documentar la actualización con fecha y versión

## Actualización de Estados

Al generar acciones de integración para gaps `[RESUELTO]`, estos gaps deben marcarse como `[PLANEADO]` para indicar que tienen una acción de integración propuesta. Esta actualización de estado se realiza en el Paso 5 (Actualización del Plan) al escribir el plan de trabajo en el archivo.

**Transición de estado**: `[RESUELTO]` → `[PLANEADO]`

## Propuestas de Mejoras de Redacción y Estilo

Además de las acciones de integración de gaps, el skill debe proponer mejoras de redacción y estilo para mejorar la calidad del documento:

### Criterios para Identificar Mejoras de Redacción

1. **Colecciones excesivas de bullet points**: Identificar secciones que consisten principalmente de listas sin contexto narrativo
   - Si una sección tiene más de 10 bullet points consecutivos sin texto explicativo
   - Si el documento tiene más del 40% de su contenido en formato de lista
   - Proponer convertir a formato narrativo con párrafos explicativos

2. **Falta de contexto narrativo**: Identificar información que está presentada de forma aislada sin flujo narrativo
   - Secciones que presentan hechos sin explicar el "por qué" o el contexto
   - Información técnica sin justificación o impacto
   - Proponer agregar contexto narrativo para conectar ideas

3. **Texto fuera de scope**: Identificar información que no corresponde al tipo de documento
   - Detalles de implementación en documentos de estrategia o PRDs
   - Decisiones de negocio en documentos de arquitectura técnica
   - Justificaciones de producto en manuales de operaciones
   - Proponer mover esta información a archivos más apropiados

4. **Densidad de información sin estructura**: Identificar secciones con información densa sin organización clara
   - Párrafos muy largos (>10 líneas) que mezclan múltiples ideas
   - Falta de conectores y transiciones entre ideas
   - Proponer reestructuración con párrafos más cortos y conectores

### Proceso de Propuesta de Mejoras de Redacción

1. **Analizar el documento actual**: Revisar el documento buscando los criterios anteriores
2. **Identificar áreas de mejora**: Marcar secciones específicas que requieren mejoras
3. **Proponer cambios específicos**: Describir exactamente qué cambios de redacción se necesitan
4. **Priorizar mejoras**: Asignar prioridad basándose en el impacto en la calidad del documento
5. **Documentar justificación**: Explicar por qué cada mejora es necesaria

### Formato de Propuestas de Mejoras de Redacción

```markdown
**MEJORAS DE REDACCIÓN Y ESTILO PROPUESTAS**

### Prioridad 1: Crítica
- **Sección**: [nombre de la sección]
- **Problema identificado**: [descripción del problema]
- **Mejora propuesta**: [descripción específica del cambio]
- **Justificación**: [por qué esta mejora es necesaria]
- **Resultado esperado**: [cómo mejorará la calidad del documento]

### Prioridad 2: Alta
- **Sección**: [nombre de la sección]
- **Problema identificado**: [descripción del problema]
- **Mejora propuesta**: [descripción específica del cambio]
- **Justificación**: [por qué esta mejora es necesaria]
- **Resultado esperado**: [cómo mejorará la calidad del documento]
```

## Identificación de Archivos Impactados Indirectamente

Las respuestas de gaps pueden impactar archivos que no son el archivo analizado directamente. El skill debe identificar estos impactos:

### Criterios para Identificar Impacto Indirecto

1. **Dependencias declaradas**: Revisar el campo `related` del frontmatter para identificar archivos relacionados
2. **Referencias cruzadas**: Identificar archivos que hacen referencia al contenido que se está modificando
3. **Consistencia de información**: Identificar archivos que contienen información relacionada que debe mantenerse consistente
4. **Documentación de impacto**: Archivos que documentan el mismo sistema o componente desde otra perspectiva

### Proceso de Identificación de Impacto Indirecto

1. **Analizar el campo `related`**: Extraer la lista de archivos relacionados del frontmatter
2. **Revisar referencias cruzadas**: Buscar referencias al archivo actual en otros documentos
3. **Evaluar consistencia**: Determinar si la respuesta del gap impacta la información en archivos relacionados
4. **Proponer actualizaciones**: Sugerir ediciones a archivos existentes para mantener consistencia
5. **Documentar trazabilidad**: Mantener trazabilidad entre gaps resueltos y archivos impactados

### Formato de Propuesta de Impacto Indirecto

```markdown
**ARCHIVOS IMPACTADOS INDIRECTAMENTE**

### Archivo: [ruta del archivo]
- **Gap relacionado**: [Título del gap]
- **Tipo de impacto**: [consistencia/referencia/dependencia]
- **Actualización propuesta**: [descripción de la edición necesaria]
- **Justificación**: [por qué este archivo debe actualizarse]
- **Referencias necesarias**: [fuentes a consultar]
- **Resultado esperado**: [descripción del resultado]
```

## Salida

- **Lista de acciones de integración propuestas**: Acciones para integrar gaps resueltos al contenido principal
- **Ediciones a archivos existentes**: Propuestas específicas para archivos existentes
- **Mejoras de redacción y estilo**: Propuestas para mejorar la calidad narrativa del documento
- **Archivos impactados indirectamente**: Propuestas de actualizaciones para mantener consistencia
- **Gaps a marcar como [PLANEADO]**: Lista de gaps para los que se generaron acciones de integración
