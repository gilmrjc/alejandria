# Guardrails y Errores Comunes

## Errores Comunes

### Proporcionar Respuestas en Lugar de Identificar Gaps

- **Error**: El objetivo es encontrar información faltante, no responder las preguntas
- **Correct**: Identificar qué información falta y qué preguntas necesitan ser respondidas

### Agregar Preguntas Redundantes

- **Error**: Agregar preguntas que ya están respondidas en la documentación
- **Correct**: Validar respuestas existentes antes de identificar nuevos gaps

### Ser Demasiado Granular

- **Error**: Preguntas demasiado específicas o enfocadas en detalles de implementación irrelevantes
- **Correct**: Enfocarse en gaps estratégicos que impactan comprensión y decisiones

### Ser Demasiado General

- **Error**: Preguntas vagas que no proporcionan contexto accionable
- **Correct**: Formular preguntas específicas con contexto claro

### Ignorar Contexto de Negocio

- **Error**: Enfocarse solo en aspectos técnicos
- **Correct**: Abordar tanto aspectos técnicos como de negocio/dominio

### No Detectar Información Fuera de Scope

- **Error**: No identificar cuando el documento contiene información que no corresponde a su tipo y propósito
- **Correct**: Detectar y documentar información fuera de scope (ej. detalles de implementación en un PRD, decisiones de negocio en un documento de arquitectura técnica, detalles operacionales en un documento estratégico)

### Omitir Validación

- **Error**: Identificar nuevos gaps sin validar respuestas existentes
- **Correct**: Siempre validar respuestas existentes antes de identificar nuevos gaps

### Olvidar Referencias

- **Error**: Agregar información sin referencia fuente
- **Correct**: Cada pieza de información agregada debe tener una referencia fuente específica

## Cuando la Información No Está Disponible

Si existe código pero no hay documentación que explique el por qué:

- Marcar explícitamente como un gap
- Agregar anotación: `**NOTA**: El código implementa esta funcionalidad pero no hay documentación que explique el por qué de esta implementación.`
- No inventar respuestas
- Priorizar la identificación de necesidades de investigación sobre proporcionar respuestas incompletas

## Manejo de Contradicciones

Cuando las fuentes se contradicen entre sí:

1. **Identificar el conflicto**: Declarar claramente qué contradice qué
   - Ejemplo: "La documentación dice X, pero el código muestra Y"

2. **Priorizar fuentes**: Generalmente, código > documentación reciente > documentación antigua

3. **Documentar la discrepancia**: Agregar una nota explicando la contradicción

4. **Sugerir resolución**: Recomendar qué fuente debe considerarse como autoritativa

5. **Marcar para revisión**: Marcar contradicciones que necesitan revisión humana

### Formato de Contradicción

```text
**DISCREPANCIA**: [Descripción clara del conflicto]
**RECOMENDACIÓN**: [Sugerencia de resolución]
```

### Ejemplo

```text
**DISCREPANCIA**: La documentación establece "cada compañía tiene su propia base de datos" pero el código muestra base de datos compartida con tabla UserCompany.
**RECOMENDACIÓN**: La implementación del código parece ser el estado actual. La documentación puede estar desactualizada.
```

## Mejores Prácticas

- **Sé exhaustivo**: Sé exhaustivo al identificar contexto faltante
- **Siempre proporciona referencias fuente**: Siempre proporciona referencias fuente al agregar información
- **Mantén la estructura original**: Mantén la estructura y formato de la documentación original
- **Enfócate en gaps**: Enfócate en gaps más que en proporcionar respuestas completas
- **Usa fuentes disponibles**: Usa las fuentes disponibles actuales en el workspace
- **Documenta en el mismo archivo**: Las sugerencias, gaps identificados y referencias deben documentarse dentro del mismo archivo analizado
- **Preserva estructura**: Preservar estructura y formato de la documentación original al agregar contexto
- **Documenta contradicciones**: Identificar y documentar contradicciones entre fuentes cuando se identifiquen

## Requisitos de Formato de Referencias

### Para Código

- Usar URLs de GitHub en lugar de rutas de archivos locales
- Formato: `https://github.com/<org>/<repo>/blob/<branch>/<path-to-file>#L<line-number>`
- Ejemplo: `https://github.com/example-org/example-repo/blob/main/src/Service.js#L24`

### Para Commits

- Usar URLs de GitHub con hash de commit
- Incluir números de línea en URLs de GitHub cuando sea aplicable

### General

- Citar fragmentos relevantes cuando sea útil
- Ser específico con las referencias
- Incluir URLs para todas las fuentes externas
