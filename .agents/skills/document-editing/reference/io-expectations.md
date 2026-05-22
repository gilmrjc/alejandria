# Expectativas de Entrada y Salida

## Entrada

### Documento con Plan de Trabajo

El documento debe contener:

- **Plan de trabajo proporcionado**: Sección claramente identificada con:
  - Versión del plan
  - Fecha de creación
  - Calificación esperada después de la implementación
  - Lista de gaps a resolver
  - Acciones organizadas por prioridad (Crítica, Alta, Media)
  - Tipos de acciones (edición archivo actual, edición archivos existentes, creación nuevos archivos)
  - Referencias a fuentes necesarias
  - Roles funcionales responsables sugeridos

- **Gaps en estado [PLANEADO]**: Gaps que tienen acciones propuestas en el plan de trabajo

- **Respuestas documentadas**: Respuestas a gaps que deben integrarse al contenido principal

- **Calificación actual**: Calificación del documento antes de los cambios (en frontmatter o sección de análisis)

### Contexto del Proyecto

Acceso a:

- Estructura del proyecto
- Documentos relacionados especificados en el plan
- Referencias a fuentes necesarias para ejecutar las acciones

## Salida

### Cambios Realizados

- **Lista de ediciones aplicadas**: Todas las acciones del plan que se completaron
- **Archivos modificados**: Lista de archivos que fueron editados o creados
- **Cambios en documentos relacionados**: Lista de cambios aplicados a documentos relacionados

### Estados Actualizados

- **Gaps actualizados**: Lista de gaps que pasaron de `[PLANEADO]` a `[IMPLEMENTADO]`
- **Fecha de implementación**: Fecha en que se ejecutó cada acción
- **Acción ejecutada**: Descripción de la acción que resolvió cada gap

### Calificación Actualizada

- **Nueva calificación (rating)**: Calificación del documento después de los cambios
- **Fase de calificación (rating-phase)**: Fase actual del documento
- **Comparación con esperada**: Diferencia entre calificación esperada y alcanzada
- **Justificación**: Razones de la calificación si es necesario

### Documento en Forma Final

- **Sin secciones temporales**: Plan de trabajo y registro de cambios eliminados
- **Contenido integrado**: Respuestas de gaps integradas al contenido principal
- **Consistencia**: Documento coherente y sin duplicaciones
- **Listo para producción**: Documento en su forma final

### Confirmación

- **Plan de trabajo ejecutado completamente**: Todas las acciones del plan fueron ejecutadas
- **Documentación relacionada mejorada**: Cambios en documentos relacionados implementados
- **Calidad de documentación mejorada**: Mejora orgánica de la calidad completa de la documentación

## Formato de Salida

### Actualización de Gap

```markdown
### [Título del gap]
- Estado: [IMPLEMENTADO]
- Fecha de implementación: [YYYY-MM-DD]
- Acción ejecutada: [descripción de la acción]
```

### Actualización de Calificación

```yaml
---
rating: [nueva calificación]
rating-phase: [fase de calificación]
---
```

## Validación de Salida

Antes de considerar el proceso completo, validar que:

- Todas las acciones del plan fueron ejecutadas
- Todos los gaps relevantes tienen estado `[IMPLEMENTADO]`
- La calificación se actualizó correctamente
- El documento no tiene secciones temporales
- El documento fluye lógicamente
- No hay duplicación de información
- Los documentos relacionados se actualizaron
- La consistencia entre documentos se mantiene
