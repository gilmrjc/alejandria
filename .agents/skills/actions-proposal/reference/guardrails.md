# Guardrails y Errores Comunes

## Errores Comunes

### Incluir Reportes y Análisis en Evaluación de Tamaño y Densidad

- **Error**: Contar líneas totales del documento incluyendo reportes, análisis, secciones de gaps y metadatos al evaluar tamaño y densidad
- **Correct**: Al evaluar tamaño y densidad, contar solo el contenido principal del documento, ignorando reportes, análisis, secciones de gaps y cualquier contenido metadatos

### Proponer Acciones Sin Validar el Plan Existente

- **Error**: Generar nuevas acciones de integración sin verificar si ya existe un plan de trabajo vigente
- **Correct**: Siempre ejecutar el Paso 0 (Detección) y Paso 1 (Validación) antes de proponer nuevas acciones de integración

### No Priorizar Ediciones del Archivo Actual

- **Error**: Proponer inmediatamente creación de nuevos archivos cuando el gap podría resolverse con ediciones al archivo actual
- **Correct**: Aplicar el orden jerárquico estricto: (1) ediciones del archivo actual, (2) ediciones a archivos existentes, (3) creación de nuevos archivos como último recurso

### Proponer Acciones Duplicadas

- **Error**: Crear múltiples acciones de integración para el mismo gap sin verificar si ya existe una acción similar
- **Correct**: Verificar deduplicación antes de crear nuevas acciones de integración; actualizar acciones existentes en lugar de crear duplicados

### Proponer División Atómica Inapropiada

- **Error**: Proponer división de documentos que resultaría en archivos tipo índice sin contenido sustantivo
- **Correct**: Validar autonomía de cada archivo propuesto; solo proponer división cuando los archivos resultantes sean autónomos con contenido sustantivo

### Proponer Consolidación Innecesaria

- **Error**: Sugerir consolidación cuando las ediciones al archivo actual o archivos existentes serían suficientes
- **Correct**: Priorizar ediciones sobre creación de nuevos documentos; consolidar solo cuando se cumplan los criterios (más de 10 gaps por tema, exceden 30% del documento, dominio funcional diferente)

### Proponer Documentos Siguientes sin Análisis de Estructura

- **Error**: Sugerir nuevos documentos sin explorar la estructura de documentación existente del proyecto
- **Correct**: Siempre descubrir y mapear la estructura existente antes de proponer documentos siguientes

### Realizar Otras Ediciones Además del Plan

- **Error**: Integrar respuestas al contenido principal o actualizar estados de gaps al escribir el plan de trabajo
- **Correct**: El skill SÍ escribe el plan de trabajo (Paso 3), pero NO realiza otras ediciones en el archivo

### Ignorar Referencias en Acciones

- **Error**: Proponer acciones sin identificar las fuentes necesarias para ejecutarlas
- **Correct**: Cada acción debe incluir referencias específicas a fuentes necesarias para su ejecución

### No Asignar Responsables Claros

- **Error**: Proponer acciones sin sugerir roles funcionales responsables
- **Correct**: Cada acción debe incluir un responsable sugerido basado en el rol funcional más apropiado

## Mejores Prácticas

- **Prioriza ediciones del archivo actual**: Siempre priorizar ediciones del archivo analizado sobre propuestas de nuevos archivos
- **Valida planes existentes**: Siempre detectar y validar planes de trabajo existentes antes de proponer nuevas acciones
- **Aplica el orden jerárquico estricto**: Ediciones del archivo actual > Ediciones a archivos existentes > Creación de nuevos archivos
- **Valida autonomía en división atómica**: Asegurar que cada archivo propuesto pueda existir de forma aislada con contenido sustantivo
- **Explora estructura antes de proponer siguientes**: Descubrir la estructura de documentación existente antes de proponer documentos siguientes
- **Incluye referencias específicas**: Cada acción debe incluir referencias a fuentes necesarias para su ejecución
- **Asigna responsables funcionales**: Sugerir roles funcionales apropiados para cada acción
- **Mantén trazabilidad**: Cada acción debe estar claramente vinculada al gap que resuelve
- **Documenta versionamiento**: Incrementar versión del plan y documentar cambios en cada actualización
- **Evita duplicación**: Verificar si ya existe una acción similar antes de crear una nueva

## Requisitos de Formato de Referencias

### Para Código

- Usar URLs de GitHub en lugar de rutas de archivos locales
- Formato: `https://github.com/<org>/<repo>/blob/<branch>/<path-to-file>#L<line-number>`
- Ejemplo: `https://github.com/example-org/example-repo/blob/main/src/Service.js#L24`

### Para Commits

- Usar URLs de GitHub con hash de commit
- Incluir números de línea en URLs de GitHub cuando sea aplicable

### Para Archivos del Proyecto

- Usar rutas relativas desde la raíz del proyecto
- Formato: `docs/ingenieria/arquitectura/database-schema-design.md`
- Incluir números de línea cuando sea relevante

### General

- Citar fragmentos relevantes cuando sea útil
- Ser específico con las referencias
- Incluir URLs para todas las fuentes externas
