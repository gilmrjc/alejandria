# Paso 1: Estructura de Rondas de Preguntas

Para cada gap, realiza una o múltiples rondas de preguntas según la complejidad.

## Clasificación del Gap

Antes de iniciar las rondas, clasificar el gap según `reference/gap-classification.md`:

- **Tipo**: Definición, Razonamiento, Estrategia, o Implementación
- **Modo**: Rápido, Profundo, o Diferido
- **Roles involucrados**: Roles funcionales relevantes para este gap
- **Perspectiva**: Senior + Junior

Declarar la clasificación al inicio de la ronda.

## Formato de una Ronda

Cada ronda sigue esta estructura:

### Presentación del Contexto

- Describe el gap específico que será abordado
- Explica por qué es importante resolverlo (impacto, rol afectado, consecuencias)
- Menciona el rol funcional afectado
- Indica la prioridad del gap
- Muestra la categoría temática explícitamente

### Preguntas Principales

- Formula 2-4 preguntas clave relacionadas con el gap
- Las preguntas deben ser específicas y accionables
- Incluye el tipo de respuesta esperada (definición, razonamiento, decisión)

### Apoyo y Sugerencias

- Provee contexto o marco de referencia para ayudar al usuario
- Sugiere posibles direcciones o enfoques
- Ofrece ejemplos o analogías si es aplicable
- Presenta alternativas o trade-offs cuando corresponda
- Basar sugerencias en gaps similares resueltos previamente si aplica

### Solicitud de Validación

- Pide explícitamente al usuario que valide o refute las sugerencias
- Solicita que el usuario agregue su perspectiva o conocimientos
- Invita a modificar o mejorar las propuestas

**Ejemplo de ronda:**

```text
**GAP: [Título del gap] [PRIORIDAD]**

**Contexto**: Este gap afecta a [rol] y es importante porque [razón].

**Preguntas**:
1. ¿Cuál es la definición precisa de [concepto] en este contexto?
2. ¿Qué razonamiento justifica esta decisión?

**Sugerencias**:
- Podríamos definir [concepto] como [propuesta de definición]
- El razonamiento podría basarse en [marco de referencia]
- Alternativa: [otro enfoque posible]

**Validación**: ¿Estás de acuerdo con estas sugerencias? ¿Agregarías o modificarías algo?
```

## Tipos de Rondas Según el Gap

### Rondas de Definición (para gaps de terminología o conceptos)

- Enfocarse en clarificar términos y conceptos
- Proveer definiciones iniciales como punto de partida
- Solicitar ejemplos concretos del contexto del proyecto
- Validar que la definición sea aplicable al dominio

### Rondas de Razonamiento (para gaps de por qué/cómo)

- Enfocarse en establecer la lógica detrás de decisiones
- Proveer marcos de razonamiento posibles
- Explorar trade-offs y alternativas consideradas
- Documentar el proceso de toma de decisiones

### Rondas de Estrategia (para gaps de planeamiento o roadmap)

- Enfocarse en definir enfoques estratégicos
- Proveer opciones con pros y contras
- Considerar dependencias y riesgos
- Validar alineación con objetivos de negocio

### Rondas de Implementación (para gaps técnicos)

- Enfocarse en detalles de cómo implementar
- Sugerir patrones o enfoques técnicos
- Considerar restricciones y dependencias
- Validar factibilidad técnica
