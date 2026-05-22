# Guía de Troubleshooting

Este documento proporciona soluciones para casos borde y situaciones especiales durante el proceso de crítica de documentos.

## Casos Comunes

### No se puede clasificar el documento

**Síntoma**: El documento no encaja claramente en ninguno de los tipos definidos en `classification.md`.

**Solución**:

1. Analizar el propósito principal del documento
2. Revisar el contenido predominante (técnico, de negocio, de usuario, etc.)
3. Si el documento tiene múltiples secciones de diferentes tipos, clasificar como "Mixto"
4. Documentar la justificación de la clasificación en la sección de clasificación
5. Adaptar los roles funcionales según el contenido mixto

### No hay referencias disponibles

**Síntoma**: El documento no menciona archivos de referencia, código, o documentos relacionados.

**Solución**:

1. Proceder con el análisis basándose solo en el contenido del documento
2. Identificar gaps que requieren investigación en fuentes externas
3. Marcar estos gaps como `[PENDIENTE]` con sugerencias de dónde buscar información
4. Si es un documento técnico sin código, marcar explícitamente: "No hay código disponible para validar"
5. Documentar la falta de referencias en la calificación del documento

### Documento muy grande (>5000 líneas)

**Síntoma**: El documento es demasiado extenso para analizar en una sola pasada.

**Solución**:

1. Dividir el análisis por secciones lógicas del documento
2. Aplicar el proceso iterativo por sección
3. Mantener consistencia en la clasificación y roles a través de todas las secciones
4. Consolidar gaps por sección al final
5. Sugerir división del documento si tiene múltiples temas independientes

### Documento muy pequeño (<50 líneas)

**Síntoma**: El documento es muy breve y no tiene suficiente contexto.

**Solución**:

1. Analizar si el documento es un fragmento o documento completo
2. Si es un fragmento, buscar el documento principal
3. Si es completo pero breve, identificar gaps de contexto faltante
4. Calificar considerando la brevedad como limitación
5. Sugerir expansión del documento si aplica

### Contradicciones irresolubles

**Síntoma**: Las fuentes se contradicen y no es claro cuál es la correcta.

**Solución**:

1. Documentar todas las contradicciones encontradas
2. Aplicar la jerarquía de fuentes (código > documentación reciente > documentación antigua)
3. Si aún no es claro, marcar para revisión humana
4. Generar gap específico: "¿Cuál es el dato correcto dado el conflicto?"
5. Prioridad: Alto si afecta decisiones críticas

### Gaps duplicados entre roles

**Síntoma**: El mismo gap se identifica desde múltiples perspectivas de rol.

**Solución**:

1. Usar el proceso de deduplicación descrito en `workflows/02-gaps-validation.md` (ahora Paso 2)
2. Consolidar el gap en una sola entrada
3. Documentar todos los roles afectados en el campo "Rol afectado"
4. Incluir notas de las diferentes perspectivas que generaron la detección
5. Actualizar fecha y versión del análisis

### Análisis previo corrupto o incompleto

**Síntoma**: El documento tiene secciones de análisis previo pero están incompletas o inconsistentes.

**Solución**:

1. Leer el estado del análisis existente
2. Identificar qué partes están completas y cuáles faltan
3. Completar las partes faltantes siguiendo el proceso estándar
4. Validar y corregir las partes inconsistentes
5. Documentar en "ESTADO DEL ANÁLISIS" qué se corrigió/completó

### Documento con múltiples tipos mezclados

**Síntoma**: El documento contiene secciones de diferentes tipos (ej. PRD con sección técnica).

**Solución**:

1. Clasificar según el tipo predominante
2. Identificar secciones de tipos diferentes
3. Aplicar roles funcionales que cubran todos los tipos presentes
4. Documentar en la clasificación: "Tipo predominante: [X], con secciones de [Y]"
5. Adaptar las perspectivas según cada sección

### No se puede determinar el rol principal

**Síntoma**: El documento no tiene un rol funcional claro.

**Solución**:

1. Analizar quién es el público objetivo del documento
2. Si el documento es para múltiples roles, clasificar como "Mixto"
3. Seleccionar 2-3 roles más relevantes según el contenido
4. Documentar la justificación en la clasificación
5. Aplicar la perspectiva dual a todos los roles seleccionados

### Calificación ambigua

**Síntoma**: El documento cae entre dos niveles de calificación (ej. entre 7 y 8).

**Solución**:

1. Revisar cada parámetro de calificación individualmente
2. Si hay empate, dar prioridad a la densidad de gaps
3. Si aún empata, dar prioridad a la calidad de referencias
4. Documentar la justificación de la calificación en el desglose
5. Si es muy cercano al siguiente nivel, mencionarlo en el resumen

## Errores Comunes y Prevención

### Generar demasiados gaps

**Prevención**:

- Enfocarse en gaps estratégicos, no en detalles granulares
- Aplicar el criterio de "¿esto bloquea una decisión?"
- Consolidar gaps similares en una sola entrada
- Usar la matriz de prioridad para filtrar gaps de baja prioridad

### No identificar gaps críticos

**Prevención**:

- Aplicar sistemáticamente las preguntas clave (cómo/por qué/qué/cuándo/quién/dónde)
- Revisar desde múltiples perspectivas de rol
- Validar que las decisiones tengan contexto suficiente
- Verificar que haya referencias para afirmaciones clave

### Ignorar el contexto de negocio

**Prevención**:

- Incluir roles de negocio/estrategia cuando corresponda
- Aplicar la perspectiva senior para contexto estratégico
- Identificar gaps de impacto en negocio/KPIs
- Verificar que las decisiones técnicas tengan justificación de negocio

### Sobrecargar el documento original

**Prevención**:

- Seguir el criterio de calificación (≥9 no agregar gaps)
- Sugerir consolidación en documentos separados cuando aplica
- Priorizar gaps críticos y de alta prioridad
- Usar el formato de "PLAN DE TRABAJO" para organizar acciones

## Recursos Adicionales

Para más información sobre:

- **Proceso detallado**: Consultar `reference/workflows/`
- **Criterios de calidad**: Consultar `reference/quality-criteria.md`
- **Transiciones de estado**: Consultar `reference/state-transitions.md`
- **Errores comunes**: Consultar `reference/guardrails.md`
