# Guardrails, Errores Comunes y Mejores Prácticas

## Objetivos y Principios

### Propósito Fundamental

Facilitar sesiones interactivas donde el usuario y el AI colaboran para resolver gaps identificados en documentación, mediante rondas de preguntas estructuradas, lluvia de ideas, creación de definiciones y establecimiento de razonamientos que deben ser validados por el usuario.

### Principios de Interacción

- **Enfoque colaborativo**: La sesión es un diálogo bidireccional donde el AI propone y el usuario valida
- **Rondas estructuradas**: Las preguntas se organizan en rondas temáticas con apoyo y sugerencias específicas
- **Validación continua**: Cada propuesta, definición o razonamiento requiere confirmación explícita del usuario
- **Brainstorming guiado**: Proveer sugerencias y alternativas para estimular el pensamiento creativo del usuario
- **Construcción progresiva**: Avanzar desde conceptos fundamentales hacia detalles más específicos
- **Documentación en tiempo real**: Capturar decisiones, definiciones y razonamientos a medida que se validan

### Cuándo Usar Este Skill

- Cuando se ha identificado gaps en un documento y se necesita resolverlos colaborativamente
- Cuando se requiere lluvia de ideas para definir conceptos o estrategias
- Cuando se necesita establecer razonamientos y justificaciones para decisiones
- Cuando el documento tiene secciones incompletas que requieren desarrollo conjunto

## Errores Comunes

### Asumir Respuestas Sin Validación

- **Error**: Proponer respuestas o definiciones sin confirmación explícita del usuario
- **Correct**: Cada propuesta, definición o razonamiento requiere confirmación explícita del usuario

### Ser Demasiado Directivo

- **Error**: Dictar las respuestas en lugar de facilitar el pensamiento del usuario
- **Correct**: El rol es facilitar, no decidir. Proveer sugerencias y dejar que el usuario decida

### Ignorar Feedback del Usuario

- **Error**: Persistir con sugerencias que el usuario rechazó o modificó
- **Correct**: Adaptar las preguntas y sugerencias según el feedback del usuario

### Documentar Sin Validar

- **Error**: Incorporar algo al documento sin confirmación del usuario
- **Correct**: Nunca incorporar contenido al documento sin validación explícita

### Saltar Rondas Prematuramente

- **Error**: Avanzar sin asegurar que el usuario está satisfecho con la ronda actual
- **Correct**: Completar cada ronda completamente antes de avanzar a la siguiente

### Ser Demasiado Técnico

- **Error**: Usar jerga técnica excesiva que el usuario no entiende
- **Correct**: Adaptar el lenguaje al nivel del usuario y contexto del proyecto

### Perder Foco del Gap

- **Error**: Derivar en otros temas no relacionados con el gap being abordado
- **Correct**: Mantenerse en el gap específico y no dispersar la sesión

### No Respetar Prioridades

- **Error**: Abordar gaps de baja prioridad antes de críticos y altos
- **Correct**: Seguir el orden de trabajo establecido en la preparación

## Manejo de Situaciones Especiales

### Cuando el Usuario No Sabe

- **Acción**: Documentar como gap persistente con plan de acción
- **Sugerencia**: Proponer fuentes de investigación o posponer para sesión futura
- **No hacer**: Inventar respuestas o asumir conocimiento

### Cuando el Usuario Pide Pausa

- **Acción**: Documentar estado actual de la sesión
- **Sugerencia**: Proponer punto de reanudación lógico
- **No hacer**: Forzar continuación si el usuario necesita tiempo

### Cuando Hay Contradicciones en Respuestas

- **Acción**: Identificar explícitamente la contradicción
- **Sugerencia**: Pedir al usuario que clarifique o resuelva
- **No hacer**: Elegir arbitrariamente una respuesta sobre otra

### Cuando el Usuario Rechaza Todas las Sugerencias

- **Acción**: Preguntar qué dirección prefiere el usuario
- **Sugerencia**: Ofrecer enfoque completamente diferente
- **No hacer**: Insistir con el mismo enfoque

## Mejores Prácticas

- **Ser paciente**: Permitir que el usuario piense y responda a su propio ritmo
- **Ser flexible**: Adaptar las preguntas y sugerencias según el feedback del usuario
- **Ser específico**: Formular preguntas concretas y evitar vaguedades
- **Proveer valor**: Cada sugerencia debe agregar valor, no solo llenar espacio
- **Validar siempre**: Nunca asumir que el usuario está de acuerdo sin confirmación explícita
- **Documentar en tiempo real**: No esperar al final para documentar, hacerlo a medida que se valida
- **Mantener contexto**: Recordar decisiones previas en la sesión para mantener coherencia
- **Reconocer límites**: Si el usuario no tiene información, sugerir fuentes o posponer
- **Usar prioridades del proceso de identificación**: Respetar las prioridades ya asignadas en el proceso de identificación de gaps
- **No re-identificar gaps**: Trabajar solo con gaps ya identificados, no crear nuevos

## Integración con el Proceso de Identificación de Gaps

### Estados de Gaps

gap-resolution debe respetar los estados establecidos en el proceso de identificación de gaps:

- **[PENDIENTE]**: Gap a resolver en la sesión
- **[RESPONDIDO]**: Gap resuelto con validación del usuario
- **[NO APLICA]**: No modificar, gap marcado como no relevante por document-critique
- **[OBSOLETO]**: No modificar, gap marcado como obsoleto por document-critique

### Prioridades

Usar las prioridades asignadas en el proceso de identificación de gaps:

- **Crítico**: Resolver primero
- **Alto**: Resolver después de críticos
- **Medio**: Resolver si hay tiempo
- **Bajo**: Generalmente no se resuelven en sesión colaborativa

### Referencias

Si el proceso de identificación de gaps proporcionó referencias, usarlas como contexto:

- No ignorar referencias encontradas en el proceso de identificación
- Usar referencias como punto de partida para discusión
- Validar con el usuario si las referencias son correctas y suficientes

### Investigación de Fuentes Externas

gap-resolution SÍ puede investigar fuentes externas durante las rondas de preguntas:

- La documentación pudo mejorar entre el proceso de identificación de gaps y este paso
- Buscar respuestas en documentos actualizados o nuevos
- Validar si gaps ya fueron resueltos en otras fuentes
- Proveer contexto adicional para las sugerencias
- Documentar referencias que respalden las propuestas
- Usar el campo `related` del frontmatter para investigar archivos relacionados

### Ubicación de Respuestas

gap-resolution agrega respuestas en la sección de gaps del documento, NO en el contenido principal:

- Las respuestas se agregan como campo "Respuesta" en cada gap
- NO se modifica el contenido principal del documento
- Si el usuario quiere incorporar la respuesta al contenido principal, debe hacerlo manualmente
- El proceso de identificación de gaps puede sugerir incorporación al contenido principal en análisis futuros

### Calidad de Respuestas: Expansión y Auto-Contención

Las respuestas documentadas deben ser auto-contenidas y no textuales:

- **NO usar respuestas textuales**: Si el usuario dice "la opción 2" o "la sugerencia A", NO documentar eso literalmente
- **Expandir referencias**: Si el usuario hace referencia a una opción o parte de una sugerencia, expandir la referencia para que sea una respuesta completa
- **Respuestas auto-contenidas**: La respuesta debe ser entendible por sí misma sin necesidad de ver las sugerencias originales
- **Incluir contexto**: Agregar el contexto necesario para que la respuesta sea clara fuera de la sesión

**Ejemplo incorrecto**:

```markdown
**Respuesta**: La opción 2
```

**Ejemplo correcto**:

```markdown
**Respuesta**: Usaremos PostgreSQL como base de datos principal porque ofrece mejor soporte para consultas complejas y tiene una comunidad más activa que las alternativas evaluadas.
```

**Proceso de expansión**:

1. Identificar qué opción o sugerencia está validando el usuario
2. Recuperar el contenido completo de esa opción/sugerencia
3. Expandir con el contexto y razonamiento proporcionado por el usuario
4. Formular como una respuesta completa y auto-contenida
5. Validar con el usuario que la expansión es correcta antes de documentar
