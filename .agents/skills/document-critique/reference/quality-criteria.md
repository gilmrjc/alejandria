# Criterios de Calificación de Documentos

Este documento describe los criterios detallados para calificar documentos en una escala de 1-10.

## Parámetros de Calificación

La calificación combina densidad de gaps (relativa al tamaño) con factores adicionales:

1. **Densidad de gaps** (gaps / secciones significativas)
2. **Claridad del texto** (legibilidad, estructura, coherencia)
3. **Densidad de contradicciones** (contradicciones / afirmaciones clave)
4. **Calidad de referencias** (especificidad, actualidad, relevancia)
5. **Profundidad de contexto** (superficial vs profundo)
6. **Accionabilidad de gaps** (claridad de cómo resolverlos)

**Definición de afirmación clave**: Afirmaciones sustantivas que requieren respaldo (decisiones, arquitectura, requisitos, valores, etc.)

## Niveles de Calificación

### 10/10 - Documento Excepcional

- **Densidad de gaps**: 0%
- **Texto**: Excepcionalmente claro, estructura impecable
- **Densidad de contradicciones**: 0%
- **Referencias**: Exhaustivas (URLs específicas con números de línea, commits con hash, múltiples fuentes corroborativas)
- **Contexto**: Profundo (explica no solo el qué sino el por qué, alternativas consideradas, trade-offs)

### 9/10 - Documento Completo

- **Densidad de gaps**: 0%
- **Texto**: Claro y bien estructurado
- **Densidad de contradicciones**: 0%
- **Referencias**: Completas (URLs específicas, commits, al menos una fuente por afirmación clave)
- **Contexto**: Sólido (explica el qué y el por qué, algunas alternativas mencionadas)

### 8/10 - Documento Bueno con Gaps Menores

- **Densidad de gaps**: 1-10% (gaps dispersos, no concentrados)
- **Texto**: Claro
- **Densidad de contradicciones**: 1-5% (contradicciones aisladas)
- **Referencias**: Adecuadas (URLs específicas para la mayoría de afirmaciones clave)
- **Contexto**: Razonable (explica el qué, por qué parcialmente explicado)
- **Gaps accionables**: Gaps tienen sugerencias de investigación

### 6-7/10 - Documento Aceptable con Gaps Significativos

- **Densidad de gaps**: 11-25% (gaps en múltiples secciones)
- **Texto**: Aceptable con áreas mejorables
- **Densidad de contradicciones**: 6-15% (contradicciones en múltiples secciones)
- **Referencias**: Parciales (URLs genéricas o faltan referencias para algunas afirmaciones)
- **Contexto**: Superficial (explica el qué, por qué poco explicado)
- **Gaps accionables**: Algunos gaps tienen sugerencias vagas

### 4-5/10 - Documento Deficiente

- **Densidad de gaps**: 26-50% (gaps en la mayoría de secciones)
- **Texto**: Confuso o desestructurado
- **Densidad de contradicciones**: 16-30% (contradicciones frecuentes)
- **Referencias**: Insuficientes (pocas o ninguna referencia específica)
- **Contexto**: Mínimo (solo describe el qué sin contexto)
- **Gaps accionables**: Gaps sin sugerencias de resolución

### 1-3/10 - Documento Muy Deficiente

- **Densidad de gaps**: >50% (más de la mitad del documento tiene gaps)
- **Texto**: Incoherente
- **Densidad de contradicciones**: >30% (ej. contradice la mayoría de sus afirmaciones clave)
- **Referencias**: Sin referencias (no hay referencias o son irrelevantes)
- **Contexto**: Sin contexto (solo afirma sin explicar)
- **Gaps accionables**: Gaps indefinidos (sin claridad de qué se necesita)

## Decisión de Adición de Gaps

### Si calificación ≥ 9

- Solo proporcionar resumen de la revisión
- No agregar sección de gaps al archivo
- Documento se considera completo para el propósito actual
- Los gaps identificados se documentan solo en el análisis de revisión, no en el archivo original

### Si calificación < 9

- Proporcionar resumen de la revisión
- Agregar sección de gaps al archivo original con el formato de `references/templates.md`
- Incluir gaps críticos y de alta prioridad con referencias cuando estén disponibles
- Documentar contradicciones identificadas
- Sugerir consolidación temática si aplica

## Formato de Calificación

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
