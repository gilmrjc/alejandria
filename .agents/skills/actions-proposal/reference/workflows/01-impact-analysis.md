# Paso 1: Análisis de Impacto en Calificación

## Objetivo

Analizar cómo cada gap resuelto ([RESUELTO]) contribuirá a mejorar la calificación del documento, priorizando gaps basándose en su impacto en los criterios de calidad (estructura, contenido, densidad, tamaño, perspectiva dual).

## Contexto

Este paso se ejecuta después de la evaluación de calidad (Paso 0) y antes de proponer acciones (Paso 4). El objetivo es asegurar que el plan de trabajo esté enfocado en mejorar la calificación del documento, no solo en integrar respuestas de gaps.

**NOTA IMPORTANTE**: La calificación inicial debe obtenerse de una evaluación previa de calidad del documento si existe. Actions-proposal NO genera la calificación inicial, solo calcula la calificación esperada después de implementar el plan.

## Proceso de Análisis

### 1. Recuperar Calificación Actual

Obtener la calificación actual del documento del Paso 0:

**Preferencia**: Usar la calificación generada en una evaluación previa de calidad si existe en el documento.

- Calificación total: X/10
- Desglose por criterios:
  - Estructura: X/10
  - Contenido: X/10
  - Densidad: X/10
  - Tamaño: X/10
  - Perspectiva Dual: X/10

### 2. Analizar Cada Gap Resuelto

Para cada gap con estado `[RESUELTO]`:

1. **Leer la respuesta del gap**: Entender qué información proporciona la respuesta
2. **Identificar el criterio de calidad impactado**: Determinar qué criterio(s) mejorará con esta respuesta
3. **Calcular el impacto esperado**: Estimar cuánto mejorará el criterio (ej. de 5/10 a 7/10)
4. **Justificar el impacto**: Explicar por qué esta respuesta mejorará el criterio
5. **Identificar tipo de acción requerida**: Determinar qué tipo de acción es necesaria para integrar la respuesta

### 3. Criterios de Impacto por Tipo de Gap

#### Gaps que Mejoran Estructura

- Gaps sobre organización de secciones
- Gaps sobre flujo lógico del documento
- Gaps sobre completitud de secciones necesarias
- Gaps sobre claridad de navegación

**Impacto esperado**: +1 a +3 puntos en el criterio de Estructura

#### Gaps que Mejoran Contenido

- Gaps sobre contexto explicativo faltante
- Gaps sobre razones fundamentales (senior)
- Gaps sobre pros/contras y conceptos de dominio (junior)
- Gaps sobre balance texto/listas
- Gaps sobre flujo narrativo y conectores

**Impacto esperado**: +1 a +4 puntos en el criterio de Contenido

#### Gaps que Mejoran Densidad

- Gaps sobre temas mezclados que pueden separarse
- Gaps sobre cohesión temática
- Gaps sobre necesidad de división

**Impacto esperado**: +1 a +2 puntos en el criterio de Densidad

#### Gaps que Mejoran Tamaño

- Gaps sobre información redundante que puede removerse
- Gaps sobre información que puede moverse a otros archivos
- Gaps sobre consolidación de contenido disperso

**Impacto esperado**: +1 a +2 puntos en el criterio de Tamaño

#### Gaps que Mejoran Perspectiva Dual

- Gaps sobre contexto para senior faltante
- Gaps sobre contexto para junior faltante
- Gaps sobre balance entre perspectivas

**Impacto esperado**: +1 a +2 puntos en el criterio de Perspectiva Dual

### 4. Priorización Basada en Impacto en Calificación

Priorizar gaps según su impacto en la calificación total del documento:

#### Prioridad Crítica (Impacto Alto + Gap de Alta Prioridad)

- Gaps que mejoran el criterio más deficiente del documento
- Gaps con impacto esperado de +3 o más puntos
- Gaps marcados con prioridad "Crítica" en el documento

#### Prioridad Alta (Impacto Alto o Gap de Alta Prioridad)

- Gaps con impacto esperado de +2 puntos
- Gaps marcados con prioridad "Alta" en el documento
- Gaps que mejoran criterios con calificación < 6/10

#### Prioridad Media (Impacto Medio)

- Gaps con impacto esperado de +1 punto
- Gaps marcados con prioridad "Media" en el documento
- Gaps que mejoran criterios con calificación ≥ 6/10

#### Prioridad Baja (Impacto Bajo)

- Gaps con impacto esperado de < +1 punto
- Gaps marcados con prioridad "Baja" en el documento
- Gaps que no contribuyen significativamente a mejorar la calificación

### 5. Cálculo de Calificación Esperada

Calcular la calificación esperada después de implementar todas las acciones propuestas:

1. **Sumar impactos por criterio**: Para cada criterio, sumar los impactos de todos los gaps que lo mejoran
2. **Aplicar límite máximo**: Ningún criterio puede exceder 10/10
3. **Calcular calificación total**: Usar los pesos de los criterios (Estructura 25%, Contenido 45%, Densidad 15%, Tamaño 10%, Perspectiva Dual 5%)
4. **Documentar mejora esperada**: Mostrar la mejora de calificación actual a esperada

### 6. Identificación de Gaps sin Impacto Significativo

Identificar gaps resueltos que no contribuyen significativamente a mejorar la calificación:

- Gaps con impacto esperado < +0.5 puntos
- Gaps que resuelven problemas menores
- Gaps que duplican información ya existente

**Acción**: Considerar si estos gaps deben incluirse en el plan o si pueden omitirse temporalmente.

## Formato de Análisis de Impacto

```markdown
**ANÁLISIS DE IMPACTO EN CALIFICACIÓN**

**Calificación actual**: X/10
- Estructura: X/10
- Contenido: X/10
- Densidad: X/10
- Tamaño: X/10
- Perspectiva Dual: X/10

**Análisis por gap resuelto**:

### Gap: [Título del gap]
- **Criterio impactado**: [Estructura/Contenido/Densidad/Tamaño/Perspectiva Dual]
- **Impacto esperado**: [X/10 → Y/10] (+Z puntos)
- **Justificación**: [por qué esta respuesta mejorará el criterio]
- **Tipo de acción requerida**: [Edición del archivo actual / Edición a archivo existente / Creación de nuevo archivo]
- **Prioridad basada en impacto**: [Crítica/Alta/Media/Baja]

### Gap: [Título del gap]
- **Criterio impactado**: [Estructura/Contenido/Densidad/Tamaño/Perspectiva Dual]
- **Impacto esperado**: [X/10 → Y/10] (+Z puntos)
- **Justificación**: [por qué esta respuesta mejorará el criterio]
- **Tipo de acción requerida**: [Edición del archivo actual / Edición a archivo existente / Creación de nuevo archivo]
- **Prioridad basada en impacto**: [Crítica/Alta/Media/Baja]
...

**Calificación esperada después del plan**: Y/10
- Estructura: X/10 → Y/10 (+Z puntos)
- Contenido: X/10 → Y/10 (+Z puntos)
- Densidad: X/10 → Y/10 (+Z puntos)
- Tamaño: X/10 → Y/10 (+Z puntos)
- Perspectiva Dual: X/10 → Y/10 (+Z puntos)

**Mejora total**: +Z puntos (X/10 → Y/10)

**Gaps sin impacto significativo** (considerar omitir):
- [Lista de gaps con impacto < +0.5 puntos]
```

## Salida

- **Análisis de impacto por gap**: Evaluación de cómo cada gap resuelto mejorará la calificación
- **Priorización basada en impacto**: Gaps ordenados por su impacto en la calificación del documento
- **Calificación esperada**: Calificación total esperada después de implementar el plan
- **Gaps sin impacto significativo**: Lista de gaps que pueden omitirse temporalmente
