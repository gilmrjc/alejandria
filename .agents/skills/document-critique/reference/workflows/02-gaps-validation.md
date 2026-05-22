# Paso 2: Evaluación de Gaps Previos (si aplica)

Si el documento ya contiene gaps identificados previamente:

## Estados de Gaps

- **[PENDIENTE]**: Gap que requiere respuesta o investigación
- **[RESPONDIDO]**: Gap que ha sido respondido con información válida y referencias
- **[NO APLICA]**: Gap que no es relevante para el documento o contexto actual (con justificación)
- **[OBSOLETO]**: Gap que ya no es relevante debido a cambios en el documento o contexto

## Criterios de Vigencia para Gaps [PENDIENTE]

Un gap `[PENDIENTE]` sigue siendo vigente si NO se cumple ninguno de los siguientes:

### Criterios para marcar como [OBSOLETO]

1. **El documento cambió significativamente** en la sección relacionada con el gap
2. **El contexto de negocio evolucionó** (nuevos requisitos, cambio de estrategia)
3. **La tecnología mencionada fue reemplazada** o deprecated
4. **El rol afectado ya no aplica** (cambio de equipo, reestructuración)
5. **La pregunta ya no tiene sentido** dado el estado actual del proyecto

### Criterios para marcar como [RESPONDIDO]

1. **Se encontró respuesta explícita** en nueva documentación
2. **El código ahora incluye comentarios** que explican el por qué
3. **Se agregó una referencia** que responde la pregunta directamente
4. **Un documento relacionado** fue creado que contiene la respuesta

Si el gap sigue vigente, mantener como `[PENDIENTE]` y agregar nota de revisión con fecha.

## Proceso de Validación

Para cada gap existente con estado `[PENDIENTE]`:

1. **Validar vigencia**: ¿El gap sigue siendo relevante dado el estado actual del documento?
2. **Buscar respuestas**: ¿Existe nueva información en referencias que responda este gap?
3. **Actualizar estado**:
   - Si se encontró respuesta: marcar como `[RESPONDIDO]` y documentar la respuesta
   - Si ya no es relevante: marcar como `[OBSOLETO]` con justificación
   - Si sigue pendiente: mantener como `[PENDIENTE]`

Para cada gap existente con estado `[RESPONDIDO]` o `[NO APLICA]`:

1. **Revisar respuesta/justificación**: Leer la respuesta o justificación proporcionada
2. **Validar vigencia**: ¿La respuesta/justificación sigue siendo correcta dado el estado actual del documento?
3. **Acumular contexto**: Utilizar esta información como contexto para evaluaciones posteriores en el análisis actual
4. **Actualizar estado si necesario**:
   - Si la respuesta ya no es correcta: marcar como `[PENDIENTE]` con justificación
   - Si la justificación de "no aplica" ya no es válida: marcar como `[PENDIENTE]` con justificación
   - Si sigue siendo válida: mantener el estado actual

## Deduplicación

Al identificar nuevos gaps:

1. **Identificar el problema de fondo**: Determinar si el nuevo gap refiere al mismo problema fundamental que un gap existente, aunque esté expresado diferente
2. **Comparar con gaps existentes**: Verificar núcleo problemático, área temática y roles afectados
3. **Si es duplicado**: Actualizar el gap existente incorporando el enfoque/perspectiva que generó esta nueva detección
4. **Documentar la actualización**: Registrar fecha, versión y el punto de vista adicional que motivó la re-detección

## Documentación

Distingue claramente entre gaps previos y gaps recién identificados. Si no existe una sección de gaps previa, procede directamente con el bucle iterativo.
