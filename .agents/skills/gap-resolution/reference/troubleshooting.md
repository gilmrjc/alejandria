# Guía de Troubleshooting

Este documento proporciona soluciones para casos borde y situaciones especiales durante las sesiones de resolución de gaps.

## Casos Comunes

### El Usuario No Sabe o No Tiene Información

**Síntoma**: El usuario indica que no tiene información para responder un gap.

**Solución**:

1. Documentar la situación explícitamente
2. Sugerir fuentes de investigación o stakeholders a consultar
3. Proponer posponer la resolución del gap
4. Crear un plan de acción claro para abordar el gap en el futuro
5. Marcar el gap como persistente con estado `[PENDIENTE]`

**Preventivo**: En la preparación de la sesión, enviar lista de gaps con anticipación para que el usuario pueda investigar.

### El Usuario Rechaza Todas las Sugerencias

**Síntoma**: El usuario rechaza consistentemente todas las sugerencias propuestas.

**Solución**:

1. Preguntar al usuario qué dirección prefiere
2. Ofrecer un enfoque completamente diferente
3. Solicitar al usuario que proponga alternativas
4. Si no hay consenso, documentar como gap persistente con plan de acción

**Preventivo**: Adaptar las sugerencias según el feedback del usuario en iteraciones anteriores.

### Sesión Demasiado Larga

**Síntoma**: La sesión está tomando más tiempo del planeado, el usuario muestra fatiga.

**Solución**:

1. Implementar sesiones por lotes (batch sessions)
2. Agrupar gaps por temática para sesiones focales
3. Establecer límite de gaps por sesión (ej. máximo 5 gaps críticos)
4. Permitir pausas programadas entre gaps complejos
5. Posponer gaps de menor prioridad para sesión futura

**Preventivo**: En la preparación, estimar tiempo requerido y ajustar el alcance de la sesión.

### Contradicciones en Respuestas del Usuario

**Síntoma**: El usuario proporciona respuestas que se contradicen entre sí o con información existente.

**Solución**:

1. Identificar explícitamente la contradicción
2. Pedir al usuario que clarifique o resuelva el conflicto
3. Documentar ambas perspectivas si no hay resolución inmediata
4. Sugerir revisión con stakeholders adicionales
5. Marcar como gap persistente si requiere investigación adicional

**Preventivo**: Validar cada respuesta con el usuario antes de documentar, especialmente cuando hay cambios de dirección.

### El Usuario Pide Pausa

**Síntoma**: El usuario solicita interrumpir la sesión temporalmente.

**Solución**:

1. Documentar estado actual de la sesión
2. Proponer punto de reanudación lógico
3. Guardar contexto de gaps abordados y pendientes
4. No forzar continuación si el usuario necesita tiempo

**Preventivo**: Establecer expectativas de duración al inicio de la sesión.

### Gaps Persistentes Recurrentes

**Síntoma**: El mismo gap aparece como persistente en múltiples sesiones.

**Solución**:

1. Revisar planes de acción de sesiones anteriores
2. Verificar si hay nueva información disponible
3. Consultar con el usuario si el plan de acción sigue siendo válido
4. Considerar re-priorizar el gap o asignar recursos específicos
5. Sugerir involucrar stakeholders adicionales

**Preventivo**: Crear sistema de seguimiento de gaps persistentes con responsables y fechas límite.

### Respuestas Textuales vs Expandidas

**Síntoma**: El usuario responde con referencias textuales ("la opción 2", "la sugerencia A") en lugar de respuestas completas.

**Solución**:

1. Aplicar el proceso de expansión descrito en `workflows/02-response-handling.md`
2. Validar con el usuario que la expansión captura correctamente su intención
3. Documentar la respuesta expandida como auto-contenida
4. Incluir contexto necesario (por qué, para qué, alternativas consideradas)

**Preventivo**: En cada ronda, solicitar respuestas completas y no solo referencias a opciones.

### Falta de Contexto Compartido

**Síntoma**: El usuario no entiende por qué un gap es importante o su impacto.

**Solución**:

1. Incluir el "por qué" de cada gap en la presentación (impacto, rol afectado, consecuencias)
2. Proveer ejemplos concretos de cómo el gap afecta el documento o proyecto
3. Mostrar prioridad y categoría temática explícitamente antes de cada ronda
4. Adaptar el lenguaje al nivel del usuario

**Preventivo**: En la preparación, incluir contexto de impacto para cada gap.

## Errores Comunes y Prevención

### Generar Demasiadas Sugerencias

**Prevención**:

- Limitar a 2-4 sugerencias por ronda
- Enfocarse en sugerencias de alta calidad sobre cantidad
- Adaptar sugerencias según el feedback del usuario

### Ser Demasiado Directivo

**Prevención**:

- Usar lenguaje de sugerencia ("podríamos", "una opción podría ser")
- Dejar que el usuario tome la decisión final
- Validar cada propuesta antes de avanzar

### Perder Foco del Gap

**Prevención**:

- Mantenerse en el gap específico durante la ronda
- No derivar en otros temas no relacionados
- Si el usuario deriva, redirigir suavemente al gap actual

### Documentar Sin Validar

**Prevención**:

- Nunca incorporar contenido al documento sin validación explícita
- Confirmar cada respuesta con el usuario antes de documentar
- Validar expansiones de respuestas textuales

### Ignorar Prioridades

**Prevención**:

- Seguir el orden de trabajo establecido en la preparación
- No abordar gaps de baja prioridad antes de críticos y altos
- Respetar las prioridades asignadas en el proceso de identificación de gaps

## Recursos Adicionales

Para más información sobre:

- **Proceso detallado**: Consultar `reference/workflows/`
- **Errores comunes y mejores prácticas**: Consultar `reference/guardrails.md`
- **Transiciones de estado**: Consultar `reference/state-transitions.md`
- **Plantillas de formato**: Consultar `reference/templates.md`
