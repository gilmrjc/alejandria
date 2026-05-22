# Paso 0: Evaluación de Calidad, Densidad y Tamaño

## Objetivo

Evaluar el documento para determinar si requiere mejoras estructurales (división atómica, consolidación, documentos siguientes) basándose en su calidad, densidad y tamaño. Esta evaluación informa las propuestas estructurales en los pasos 6-8.

**NOTA IMPORTANTE**: Este paso NO genera una nueva calificación del documento. La calificación inicial debe provenir de una evaluación previa de calidad del documento (generada durante el proceso de identificación de gaps y preguntas críticas). Actions-proposal solo usa la calificación existente para informar propuestas estructurales y calcular la calificación esperada después de implementar el plan.

## Evaluación de Calidad del Documento

### Lectura de Calificación Existente

**ANTES de evaluar**, verificar si ya existe una calificación del documento generada previamente:

1. **Buscar calificación existente**: Buscar en el documento una sección de calificación (usualmente con formato "CALIFICACIÓN DEL DOCUMENTO: X/10")
2. **Si existe calificación**: Usar esa calificación como base para el análisis de impacto
3. **Si NO existe calificación**: Solo en este caso, realizar una evaluación de calidad para informar propuestas estructurales

### Criterios de Calidad (Solo si NO existe calificación previa)

Si es necesario evaluar, usar los siguientes criterios:

#### Estructura (25%)

- **Alineación con objetivo**: ¿Cada sección contribuye directamente al objetivo del documento?
- **Flujo lógico**: ¿El orden de secciones facilita la comprensión del contenido?
- **Completitud**: ¿Faltan secciones necesarias para el objetivo?
- **Organización**: ¿La estructura es clara y fácil de navegar?

#### Contenido (45%)

- **Calidad explicativa**: ¿Hay suficiente texto explicativo para dar contexto?
- **Contexto para senior**: ¿Se explican razones fundamentales, impacto, trade-offs?
- **Contexto para junior**: ¿Se explican pros/contras, conceptos de dominio, terminología?
- **Balance texto/listas**: ¿Hay equilibrio entre texto explicativo y listas organizativas?
- **Lenguaje que permite seguir ideas**: ¿El texto fluye lógicamente con conectores y transiciones?

#### Densidad (15%)

- **Número de temas**: ¿Cuántos temas distintos trata el documento?
- **Cohesión temática**: ¿Los temas están relacionados o son dispersos?
- **Necesidad de división**: ¿El documento sería más claro dividido?

#### Tamaño (10%)

- **Número de líneas**: ¿Cuántas líneas tiene el documento? **IMPORTANTE: Contar solo el contenido principal, ignorando reportes, análisis, secciones de gaps, y cualquier contenido metadatos**
- **Justificación de tamaño**: Si excede 300 líneas, ¿hay una razón sólida?
- **Necesidad de división**: ¿El tamaño afecta la navegación o mantenibilidad?

#### Perspectiva Dual (5%)

- **Cobertura senior**: ¿Se atienden las necesidades de perspectiva senior?
- **Cobertura junior**: ¿Se atienden las necesidades de perspectiva junior?
- **Balance**: ¿Ambas perspectivas están equilibradas?

### Escala de Calificación 1-10

- **1-3**: Documento muy deficiente. Sin estructura clara, contenido mínimo, sin contexto para ningún nivel, muy denso.
- **4-5**: Documento deficiente. Estructura desalineada, contenido insuficiente, contexto faltante para uno o ambos niveles, denso.
- **6-7**: Documento aceptable pero con mejoras necesarias. Estructura básica, contenido con gaps significativos, contexto parcial, puede ser denso.
- **8**: Documento bueno con mejoras menores. Estructura alineada, contenido decente con algunos gaps, contexto razonable, densidad aceptable.
- **9**: Documento alineado y útil (objetivo esperado). Estructura correcta, contenido sólido con contexto para ambos niveles, densidad aceptable.
- **10**: Documento excelente pero esfuerzo no justificado en práctica. Estructura perfecta, contenido completo, contexto excepcional, atomicidad perfecta.

### Formato de Calificación

```markdown
**EVALUACIÓN DE CALIDAD**

**Calificación: X/10**

**Desglose**:
- Estructura: X/10 - [justificación]
- Contenido: X/10 - [justificación]
- Densidad: X/10 - [justificación]
- Tamaño: X/10 - [justificación]
- Perspectiva Dual: X/10 - [justificación]

**Resumen**: [breve resumen de la evaluación general]
```

## Evaluación de Densidad

### Identificación de Temas

Un tema es:

- Un área funcional distinta (ej. arquitectura, negocio, operaciones)
- Un dominio de problema separado (ej. autenticación, autorización, auditoría)
- Un tipo de contenido diferente (ej. especificación técnica, guía de proceso, estrategia)
- Un conjunto de decisiones que pueden vivir independientemente

**IMPORTANTE**: Al identificar temas, considerar solo el contenido principal del documento. Ignorar reportes, análisis, secciones de gaps, y cualquier contenido metadatos para esta evaluación.

### Criterios de Densidad

- **Menos de 3 temas**: Densidad aceptable, documento puede mantenerse unificado
- **3 temas**: Límite aceptable, considerar si los temas están relacionados
- **Más de 3 temas**: Documento muy denso, marcar como candidato para división en archivos atómicos

### Formato de Evaluación de Densidad

```markdown
**EVALUACIÓN DE DENSIDAD**
- Temas identificados: X temas
- Lista de temas:
  1. [Tema 1]: [descripción breve]
  2. [Tema 2]: [descripción breve]
  3. [Tema 3]: [descripción breve]
  ...
- Densidad: [aceptable/muy densa]
- Candidato para división: [SÍ/NO]
```

## Evaluación de Tamaño

### Criterios de Tamaño

- **Contar líneas totales**: Determinar el número de líneas del documento actual **IMPORTANTE: Contar solo el contenido principal, ignorando reportes, análisis, secciones de gaps, y cualquier contenido metadatos**
- **Criterio de tamaño ideal**: Máximo 300 líneas por documento
- **Evaluación del tamaño**:
  - **Menos de 200 líneas**: Tamaño óptimo, documento conciso y enfocado
  - **200-300 líneas**: Tamaño aceptable, dentro del rango ideal
  - **300-400 líneas**: Tamaño límite, requiere justificación del por qué es necesario este tamaño
  - **Más de 400 líneas**: Tamaño excesivo, debe proponerse división en documentos más pequeños

### Justificación de Tamaño

Si el documento excede 300 líneas, justificar por qué es necesario mantenerlo unificado:

- Tema complejo que requiere profundidad
- Interdependencia crítica de secciones
- Necesidad de contexto compartido
- Referencia extenso que requiere ser unificado

Si no hay justificación sólida, marcar como candidato para división.

### Formato de Evaluación de Tamaño

```markdown
**EVALUACIÓN DE TAMAÑO**
- Líneas totales (contenido principal solo): X líneas
- Estado de tamaño: [óptimo/aceptable/límite/excesivo]
- Candidato para división: [SÍ/NO]
- Justificación del tamaño (si excede 300 líneas): [razón por la que es necesario este tamaño]
```

## Conclusión de Evaluación

### Criterios para Propuestas Estructurales

Basándose en la evaluación de calidad, densidad y tamaño:

- **División atómica**: Se propone si:
  - Densidad > 3 temas O tamaño > 300 líneas sin justificación
  - La calificación de calidad es < 8 debido a densidad/tamaño
  - Los temas pueden separarse en archivos autónomos

- **Consolidación**: Se propone si:
  - Hay múltiples gaps dispersos que podrían agruparse
  - Los gaps superan 10 por tema o 30% del documento
  - Existe un dominio funcional diferente que requiere documento separado

- **Documentos siguientes**: Se propone si:
  - La estructura existente no puede acomodar nuevas extensiones
  - Hay dependencias lógicas que no están documentadas
  - El flujo de desarrollo requiere documentos específicos

### Formato de Conclusión

```markdown
**CONCLUSIÓN DE EVALUACIÓN**
- Requiere división atómica: [SÍ/NO]
- Requiere consolidación: [SÍ/NO]
- Requiere documentos siguientes: [SÍ/NO]
- Razón: [explicación basada en evaluación de calidad, densidad y tamaño]
```

## Salida

- **Evaluación de calidad**: Calificación del documento con desglose por criterios
- **Evaluación de densidad**: Diagnóstico de densidad temática
- **Evaluación de tamaño**: Diagnóstico de tamaño del documento
- **Conclusión**: Recomendaciones sobre propuestas estructurales necesarias
