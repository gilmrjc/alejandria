# Gestión de Idempotencia

## Detección de Sesión Previa

El skill detecta automáticamente si existe una sesión previa buscando:

- Sección **ESTADO DE LA SESIÓN** con versión y fecha
- Lista de gaps procesados con estados
- Sección **RESULTADOS DE LA SESIÓN** con respuestas validadas
- Sección **GAPS PERSISTENTES** con planes de acción

## Validación de Gaps Existentes

Para gaps con estado `[PENDIENTE]`:

1. Validar si sigue siendo relevante dado el estado actual del documento
2. Verificar si hubo cambios en el contexto que puedan afectar el gap
3. Mantener como `[PENDIENTE]` si sigue vigente
4. Marcar como `[RESUELTO]` si se encontró respuesta en otra fuente (con validación del usuario)

Para gaps con estado `[RESUELTO]`:

1. Revisar las respuestas y justificaciones proporcionadas
2. Validar que las respuestas sigan siendo correctas dado el estado actual del documento
3. Utilizar esta información como contexto para gaps pendientes

## Integración con document-critique

gap-resolution depende de document-critique para la gestión de idempotencia:

### Estados de Gaps

Los estados de gaps son gestionados por document-critique:

- **[PENDIENTE]**: Gap identificado por document-critique, listo para resolución
- **[RESPONDIDO]**: Gap resuelto (document-critique usa este término, gap-resolution usa [RESUELTO] pero son equivalentes)
- **[NO APLICA]**: Gap marcado como no relevante por document-critique
- **[OBSOLETO]**: Gap marcado como obsoleto por document-critique

### Prioridades

Las prioridades son asignadas por document-critique:

- gap-resolution debe respetar las prioridades ya asignadas
- No re-priorizar gaps durante la sesión
- Seguir el orden de trabajo basado en prioridades de document-critique

### Referencias Cruzadas

Si document-critique identificó relaciones entre archivos:

- Revisar el campo `related` en frontmatter
- Usar gaps_resueltos de archivos relacionados como contexto
- No re-resolver gaps ya resueltos en archivos relacionados
- Investigar archivos relacionados para encontrar respuestas actualizadas

### Investigación de Fuentes Externas

gap-resolution puede investigar fuentes externas durante las rondas de preguntas:

- La documentación pudo mejorar entre el proceso de crítica y este paso
- Buscar respuestas en documentos actualizados o nuevos
- Validar si gaps ya fueron resueltos en otras fuentes
- Proveer contexto adicional para las sugerencias
- Documentar referencias que respalden las propuestas

## Actualización vs Creación

### Si existe sesión previa

- Actualizar la sesión existente incrementando la versión
- Revisar gaps persistentes de la sesión anterior
- Priorizar gaps que no se resolvieron en sesiones anteriores
- Documentar cambios desde la sesión anterior

### Si no existe sesión

- Crear una nueva sesión con versión 1
- Establecer estado inicial de la sesión
- Documentar todos los gaps a resolver

## Versionamiento de la Sesión

- Cada sesión incrementa la versión
- La fecha de la sesión se registra en el estado
- El estado de la sesión documenta la versión anterior y cambios
- Mantener historial de gaps resueltos por sesión

## Deduplicación de Trabajo

### Evitar Re-Resolución

Antes de abordar un gap:

1. Verificar si el gap ya está en estado `[RESUELTO]`
2. Verificar si el gap está en `[NO APLICA]` o `[OBSOLETO]`
3. Verificar si el gap fue resuelto en un archivo relacionado (campo `related`)
4. Si ya está resuelto, omitir y documentar referencia

### Gestión de Gaps Persistentes

Para gaps que persisten entre sesiones:

1. Revisar plan de acción de la sesión anterior
2. Verificar si hay nueva información disponible
3. Consultar con el usuario si el plan de acción sigue siendo válido
4. Actualizar plan de acción si es necesario

## Formato de Estado de Sesión

```markdown
**ESTADO DE LA SESIÓN**
- Fecha: [YYYY-MM-DD]
- Versión de sesión: [número incremental]
- Versión anterior: [número si aplica]
- Gaps a resolver: [cantidad]
- Gaps pendientes: [cantidad]
- Gaps resueltos: [cantidad]
- Cambios desde sesión anterior: [descripción si aplica]
```

## Criterios de Terminación

La sesión termina cuando:

- Se han abordado todos los gaps `[PENDIENTE]` priorizados
- Se han documentado todas las respuestas validadas
- Se han incorporado las respuestas al documento original
- Se han documentado los gaps persistentes con planes de acción
- Se ha actualizado el estado de la sesión con versión y fecha
- Se ha verificado que no hay contradicciones en las respuestas incorporadas
