# Paso 6: Propuesta de División Atómica

## Objetivo

Proponer división de documentos densos o excesivamente grandes en archivos atómicos cuando el documento cumpla con los criterios de tamaño y densidad establecidos.

## Detección de Candidatos para División

Aplicar los siguientes criterios para determinar si el documento es candidato para división atómica:

1. **Más de 5 secciones principales sin estructura clara**
   - Contar secciones de nivel 1 (#) o nivel 2 (##)
   - Si hay más de 5 secciones principales sin agrupación lógica, considerar división

2. **Densidad de información alta**
   - Calcular ratio de líneas de texto vs líneas de estructura (títulos, listas, código)
   - Si el ratio texto/estructura > 80%, indica alta densidad que podría beneficiarse de división

3. **Palabras clave repetidas en múltiples secciones**
   - Identificar palabras clave que aparecen en más de 3 secciones diferentes
   - Esto indica temas mezclados que podrían separarse

4. **Longitud del documento**
   - Contar líneas totales del documento **IMPORTANTE: Contar solo el contenido principal, ignorando reportes, análisis, secciones de gaps, y cualquier contenido metadatos**
   - Si excede 300 líneas sin justificación clara (ej. documento de referencia extenso), considerar división

5. **Mezcla de tipos de contenido**
   - Detectar si el documento mezcla tipos de contenido incompatibles
   - Ejemplo: Detalles técnicos en un documento de estrategia, requisitos de usuario en un documento técnico

## Criterios de División

El documento requiere división si cumple al menos 2 de los 5 criterios anteriores (secciones, densidad, palabras clave, longitud, mezcla de tipos).

## Proceso de Propuesta de División

1. **Analizar temas identificados**: Revisar la lista de temas del documento
2. **Determinar estructura atómica**: Proponer archivos atómicos basados en los temas
3. **Validar autonomía**: Asegurar que cada archivo propuesto pueda existir de forma aislada
4. **Evitar archivos tipo índice**: Cada archivo debe tener contenido sustantivo propio
5. **Considerar tipo de documento**: ADR, PRD, especificación, etc. según corresponda

## Criterios de Autonomía

Para cada archivo atómico propuesto, validar cualitativamente:

- **Objetivo independiente**: El documento tiene un propósito propio y completo
  - El documento responde a una pregunta o necesidad específica por sí mismo
  - No depende de otros documentos para tener sentido
  - Ejemplo válido: Un ADR sobre "Selección de base de datos" tiene propósito independiente
  - Ejemplo inválido: Un índice que solo lista otros documentos sin contenido propio

- **Contexto autosuficiente**: Contiene suficiente contexto introductorio
  - Un lector nuevo puede entender el propósito del documento sin consultar otros
  - Tiene introducción que explica el contexto y motivo del documento
  - Ejemplo válido: "Este documento decide qué base de datos usar para el proyecto X porque..."
  - Ejemplo inválido: "Ver documento de arquitectura para contexto" sin introducción propia

- **Contenido sustantivo**: Tiene contenido propio y significativo
  - La mayoría del contenido es original y no referencias a otros documentos
  - El documento aporta valor propio más allá de redirigir a otros
  - Ejemplo válido: Documento con análisis, decisiones y justificaciones propias
  - Ejemplo inválido: Documento que es 80% citas o referencias a otros documentos

- **Estructura completa**: Tiene introducción, desarrollo y conclusión propios
  - El documento tiene un inicio claro, desarrollo del tema y cierre
  - No requiere secciones de otros documentos para ser completo
  - Ejemplo válido: Documento con "Contexto → Análisis → Decisión → Impacto"
  - Ejemplo inválido: Documento que termina abruptamente o requiere otro documento para cerrar

- **Lectura independiente**: Un lector puede obtener valor sin consultar otros documentos
  - El documento es comprensible y útil por sí mismo
  - No requiere lectura previa de otros documentos para ser útil
  - Ejemplo válido: Un desarrollador puede entender el ADR sin leer toda la arquitectura
  - Ejemplo inválido: Documento que asume conocimiento previo de otros documentos sin explicarlo

## Criterios para Evitar División Inapropiada

NO proponer división cuando:

- La división resultaría en archivos tipo índice o resumen sin contenido sustantivo
- Los archivos resultantes no serían autónomos
- Los temas están tan interrelacionados que separarlos fragmentaría el contexto
- El documento tendría que repetir el mismo contexto en múltiples archivos
- La división forzaría a crear archivos "puente"

## Formato de Propuesta

```markdown
**PROPUESTA DE DIVISIÓN ATÓMICA**
- Documento origen: [nombre del documento]
- Razón de división: [densidad excesiva / tamaño excesivo / ambos]
- Temas identificados: [lista de temas]

**Archivos atómicos propuestos**:

1. [Archivo atómico 1]:
   - Tipo: [tipo de documento]
   - Contenido: [temas a incluir]
   - Objetivo: [propósito del archivo]
   - Tamaño estimado: [líneas]
   - Validación de autonomía:
     - Objetivo independiente: [cumple/no cumple]
     - Contexto autosuficiente: [cumple/no cumple]
     - Contenido sustantivo: [cumple/no cumple]
     - Estructura completa: [cumple/no cumple]
     - Lectura independiente: [cumple/no cumple]

2. [Archivo atómico 2]:
   - Tipo: [tipo de documento]
   - Contenido: [temas a incluir]
   - Objetivo: [propósito del archivo]
   - Tamaño estimado: [líneas]
   - Validación de autonomía:
     - Objetivo independiente: [cumple/no cumple]
     - Contexto autosuficiente: [cumple/no cumple]
     - Contenido sustantivo: [cumple/no cumple]
     - Estructura completa: [cumple/no cumple]
     - Lectura independiente: [cumple/no cumple]
...
```

## Recomendación de Acción

Priorizar ediciones del archivo actual sobre proponer división. Proponer división solo cuando:

1. **Se cumplan los criterios de densidad/tamaño**: El documento es demasiado denso o grande según los criterios establecidos
2. **Las ediciones no resuelven el problema**: El documento es intrínsecamente denso, no por falta de contenido específico
3. **La división mejoraría la calidad**: La división resultaría en archivos más enfocados, claros y mantenibles
4. **Los archivos resultantes serían autónomos**: Cada archivo propuesto tiene contenido sustantivo y puede existir de forma aislada

## Evaluación de Calidad y Densidad

Antes de proponer división, evaluar si la división realmente mejoraría la calidad de la documentación:

- **¿El documento es difícil de navegar?** Si hay muchos temas mezclados que dificultan encontrar información específica
- **¿El documento es difícil de mantener?** Si cambios en un tema requieren revisar múltiples secciones no relacionadas
- **¿El documento es difícil de entender?** Si un lector nuevo se pierde por la cantidad de temas diferentes
- **¿La división mejoraría la claridad?** Si separar temas en archivos específicos haría cada uno más claro y enfocado

Si la respuesta a estas preguntas es afirmativa, la división está justificada por mejoras en calidad de documentación.

## Salida

- **Propuesta de división atómica**: Estructura de archivos atómicos propuesta si aplica
- **Validación de autonomía**: Evaluación de cada archivo propuesto
