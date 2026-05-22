# Paso 7: Sugerencia de Consolidación

## Objetivo

Proponer organización de hallazgos en documentos estructurados si aplica.

## Criterios de Consolidación

Evaluar si se requiere consolidación basándose en:

- **Cantidad de gaps por tema**: Más de 10 gaps relacionados con un tema específico
- **Tamaño relativo**: El contenido de gaps excede el 30% del tamaño del documento actual **IMPORTANTE: Calcular el tamaño del documento considerando solo el contenido principal, ignorando reportes, análisis, secciones de gaps, y cualquier contenido metadatos**
- **Dominio funcional diferente**: Gaps pertenecen a un dominio funcional diferente (ej. gaps de arquitectura en un PRD)

## Proceso de Sugerencia

1. **Analizar gaps pendientes**: Agrupar gaps por categoría temática
2. **Identificar patrones**: Buscar temas recurrentes o gaps relacionados
3. **Evaluar criterios**: Aplicar criterios de consolidación
4. **Verificar duplicados**: Buscar en estructura existente documentos que ya contengan el contenido propuesto
5. **Proponer tipo de documento**: Sugerir el tipo de documento más apropiado (ADR, PRD, Especificación Técnica, etc.)
6. **Validar tipo de documento**: Validar que el tipo de documento propuesto sea apropiado para el contenido de los gaps
7. **Justificar la propuesta**: Explicar por qué la consolidación sería beneficiosa

## Verificación de Duplicados

Antes de proponer consolidación, verificar si ya existe un documento que podría contener los gaps:

1. **Buscar documentos del mismo tipo**: Identificar en la estructura existente documentos del mismo tipo propuesto (ADR, PRD, etc.)
2. **Comparar contenido**: Verificar si el contenido propuesto ya está cubierto parcial o totalmente en documentos existentes
3. **Evaluar superposición**: Determinar si los gaps propuestos solapan significativamente con contenido existente
4. **Decisión**:
   - Si existe documento similar con alto solapamiento: Sugerir edición a ese archivo en lugar de crear uno nuevo
   - Si no existe documento similar o el solapamiento es bajo: Proceder con consolidación

## Validación de Tipo de Documento

Validar que el tipo de documento propuesto sea apropiado para el contenido de los gaps:

1. **Verificar tipo contra contenido**: Confirmar que el tipo de documento propuesto sea apropiado para el contenido de los gaps
   - Ejemplo: Gaps de arquitectura técnica → ADR o Documento de Arquitectura (no PRD)
   - Ejemplo: Gaps de requisitos de negocio → PRD o Documento de Negocio (no Especificación Técnica)

2. **Validar contra patrones de nomenclatura**: Verificar que el tipo propuesto siga los patrones de nomenclatura del proyecto
   - Revisar cómo se nombran los documentos del mismo tipo en la estructura existente
   - Asegurar que el nombre propuesto sea consistente

3. **Sugerir alternativas si aplica**: Si el tipo propuesto no es el más apropiado, sugerir tipos alternativos basados en el contenido y propósito de los gaps

## Formato de Sugerencia

Usar el formato de `references/templates.md`:

```markdown
**SUGERENCIA DE CONSOLIDACIÓN**
- Tipo de documento sugerido: [ADR/PRD/Especificación Técnica/etc.]
- Razón: [Justificación de por qué se necesita consolidación]
- Gaps a incluir: [Lista de gaps relacionados]
- Beneficio esperado: [Mejora en organización y accesibilidad]
```

## Recomendación de Acción

Priorizar ediciones del archivo actual y ediciones a archivos existentes sobre crear nuevos documentos. Crea nuevos documentos solo cuando se cumplan los criterios de consolidación y las ediciones no sean suficientes.

## Salida

- **Sugerencia de consolidación**: Recomendación de cómo organizar hallazgos en documentos estructurados si aplica
