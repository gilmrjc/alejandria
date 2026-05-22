# Gestión de Idempotencia

## Detección de Análisis Previo

El skill detecta automáticamente si existe un análisis previo buscando:

- Sección **ESTADO DEL ANÁLISIS**
- Sección **CLASIFICACIÓN DEL DOCUMENTO** con fecha y versión
- Gaps con estados: `[PENDIENTE]`, `[RESPONDIDO]`, `[NO APLICA]`, `[OBSOLETO]`
- Sección **PLAN DE TRABAJO**

## Validación de Gaps Existentes

Para cada gap con estado `[PENDIENTE]`:

1. Validar si sigue siendo relevante dado el estado actual del documento
2. Buscar nueva información en referencias que pueda responder el gap
3. Actualizar estado a `[RESPONDIDO]` si se encontró respuesta
4. Marcar como `[OBSOLETO]` si ya no es relevante
5. Mantener como `[PENDIENTE]` si sigue vigente

Para gaps con estado `[RESPONDIDO]` o `[NO APLICA]`:

1. Revisar las respuestas y justificaciones proporcionadas
2. Utilizar esta información como contexto para evaluaciones posteriores
3. Validar que las respuestas sigan siendo correctas dado el estado actual del documento

## Deduplicación de Nuevos Gaps

Al identificar nuevos gaps:

1. **Verificar campo "related"**: Revisar el frontmatter del documento para identificar archivos relacionados
2. **Consultar gaps_resueltos**: Para cada archivo relacionado, verificar los gaps listados en `gaps_resueltos`
3. **Deduplicación por relaciones**: Si un gap ya fue resuelto en un archivo relacionado, NO volver a identificarlo
4. **Comparar con gaps existentes**: Comparar con gaps existentes en el documento actual (título, pregunta, contexto)
5. **Actualizar en lugar de crear**: Si existe un gap similar, actualizar el existente en lugar de crear uno nuevo
6. **Documentar referencias cruzadas**: Cuando se use información de archivos relacionados, documentar la referencia explícitamente
7. **Documentar actualización**: Documentar la actualización con fecha y versión del análisis

**Proceso de deduplicación mediante relaciones**:

1. Antes de investigar, revisar el campo `related` del frontmatter
2. Durante la investigación, consultar los archivos relacionados
3. Al identificar gaps, verificar si ya están en `gaps_resueltos` de algún archivo relacionado
4. Si se detecta duplicación, eliminar el gap duplicado y documentar la referencia al archivo relacionado

Esto asegura que:

- Las relaciones entre documentos estén explícitamente documentadas
- No se duplique el trabajo de investigación
- Los gaps resueltos previamente no se vuelvan a identificar
- Se mantenga trazabilidad de la información entre archivos

## Versionamiento del Análisis

- Cada análisis incrementa la versión del análisis
- La fecha del análisis se registra en la clasificación
- El estado del análisis documenta la versión anterior y cambios
