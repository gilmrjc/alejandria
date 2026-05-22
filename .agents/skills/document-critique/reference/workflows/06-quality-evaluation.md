# Paso 6: Evaluación de Calidad y Decisión de Adición de Gaps

Evalúa la calidad del documento y determina si los gaps identificados deben agregarse al archivo durante esta revisión.

## Criterios de Calificación

Para criterios detallados de calificación por nivel (1-10), consultar `references/quality-criteria.md`.

## Decisión de Adición de Gaps

### Si calificación ≥ 9

- Solo proporcionar resumen de la revisión
- No agregar sección de gaps al archivo
- Documento se considera completo para el propósito actual
- Los gaps identificados se documentan solo en el análisis de revisión, no en el archivo original
- **IMPORTANTE: Eliminar completamente toda la sección de análisis del documento** - Dado que la calificación es ≥ 9, no hay gaps que trabajar, por lo tanto toda la sección de análisis (incluyendo cualquier nota, texto temporal, o hallazgos documentados durante el proceso de revisión) debe ser eliminada del contenido del archivo original

### Si calificación < 9

- Proporcionar resumen de la revisión
- Agregar sección de gaps al archivo original con el formato de `references/templates.md`
- Incluir gaps críticos y de alta prioridad con referencias cuando estén disponibles
- Documentar contradicciones identificadas
- Sugerir consolidación temática si aplica

Formato de calificación:

```markdown
**CALIFICACIÓN DEL DOCUMENTO: X/10**

**Desglose**:
- Completitud de Respuestas: X/10 - [justificación]
- Contexto Multi-Rol: X/10 - [justificación]
- Calidad de Referencias: X/10 - [justificación]
- Estructura y Organización: X/10 - [justificación]
- Consistencia: X/10 - [justificación]

**Resumen**: [breve resumen de la evaluación general]
```

## Actualización del Frontmatter del Documento

Después de calificar el documento, actualizar el frontmatter del archivo procesado agregando los siguientes campos:

- **rating**: La calificación numérica (1-10)
- **rating-phase**: El nombre del skill que realizó la calificación (document-critique)

Ejemplo de actualización de frontmatter:

```yaml
---
rating: 7
rating-phase: document-critique
---
```

Si el frontmatter del documento ya existe, agregar estos campos al frontmatter existente. Si no existe frontmatter, crearlo con estos campos.
