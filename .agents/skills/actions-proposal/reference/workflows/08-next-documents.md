# Paso 8: Propuesta de Documentos Siguientes

## Objetivo

Identificar y proponer documentos lógicos como siguientes pasos para extender la documentación del sistema, basándose en dependencias naturales y la estructura existente del proyecto.

## Descubrimiento de la Estructura de Documentación

El primer paso es descubrir la estructura de documentación del proyecto actual.

### Análisis de la Estructura Existente

Explorar el directorio de documentación del proyecto (usualmente `docs/` o similar) para identificar:

1. **Directorios principales**: Identificar las áreas de alto nivel (ej. estrategia, ingeniería, producto, etc.)
2. **Subdirectorios**: Identificar las subáreas dentro de cada área principal
3. **Archivos existentes**: Listar los documentos ya creados en cada área
4. **Patrones de nomenclatura**: Identificar cómo se nombran los archivos en cada área
5. **Tipos de documentos**: Clasificar los documentos por tipo (ADRs, especificaciones, PRDs, etc.)

### Mapeo de la Estructura

Documentar la estructura descubierta en el siguiente formato:

```markdown
**ESTRUCTURA DE DOCUMENTACIÓN DEL PROYECTO**

[Directorio principal 1]:
  - [Subdirectorio 1.1]: [descripción del tipo de documentos]
  - [Subdirectorio 1.2]: [descripción del tipo de documentos]
  - Archivos existentes: [lista de archivos]

[Directorio principal 2]:
  - [Subdirectorio 2.1]: [descripción del tipo de documentos]
  - Archivos existentes: [lista de archivos]
...
```

## Criterios para Identificar Documentos Siguientes

Para proponer documentos siguientes, considera:

1. **Dependencia lógica**: ¿Qué documentos naturalmente seguirían al actual basándose en el flujo de desarrollo?
   - Después de un documento de requisitos (PRD), sigue una especificación técnica
   - Después de una decisión arquitectónica (ADR), sigue una especificación de implementación
   - Después de una estrategia, siguen políticas o guías de implementación

2. **Completitud de área**: ¿Qué áreas relacionadas aún no tienen documentación?
   - Si hay especificaciones de un componente pero no de componentes relacionados, proponer especificaciones complementarias
   - Si hay arquitectura de alto nivel pero no decisiones arquitectónicas específicas, proponer ADRs

3. **Flujo de desarrollo**: ¿Qué documentos son necesarios para el siguiente paso del desarrollo?
   - Después de especificaciones técnicas, proponer guías de implementación o onboarding
   - Después de requisitos de producto, proponer casos de negocio o análisis de riesgos

4. **Cobertura de dominio**: ¿Qué aspectos del dominio aún no están documentados?
   - Si hay estrategia pero no políticas operativas, proponer políticas
   - Si hay requisitos funcionales pero no investigación de usuarios, proponer user research

## Proceso de Identificación

1. **Analizar el documento actual**: Determinar su tipo, área y propósito
2. **Descubrir estructura existente**: Usar el script `discover_structure.py` para identificar áreas, subáreas y documentos existentes con depth 2
3. **Analizar campo 'related'**: Leer el campo `related` del frontmatter para identificar dependencias declaradas
4. **Identificar gaps lógicos**: Determinar qué documentos faltan basándose en dependencias naturales, la estructura descubierta y las relaciones declaradas
5. **Validar duplicados**: Verificar sistemáticamente si los documentos propuestos ya existen
6. **Priorizar propuestas**: Ordenar propuestas por relevancia y urgencia para el desarrollo

## Validación de Duplicados

Para cada documento propuesto, verificar si ya existe en la estructura:

1. **Búsqueda por nombre similar**: Buscar documentos con nombres similares al propuesto
   - Comparar palabras clave en el nombre
   - Verificar variaciones de nomenclatura (ej. singular/plural, guiones vs espacios)

2. **Búsqueda por propósito similar**: Buscar documentos con propósito similar al propuesto
   - Revisar títulos y descripciones de documentos existentes
   - Comparar objetivos declarados en frontmatter

3. **Búsqueda por ubicación similar**: Buscar documentos en la misma ubicación o subárea
   - Verificar si ya existe un documento en el directorio propuesto
   - Revisar subdirectorios cercanos con contenido similar

4. **Decisión**:
   - Si existe duplicado con alto solapamiento: Sugerir edición al existente en lugar de crear nuevo
   - Si no existe duplicado o el solapamiento es bajo: Proceder con propuesta

## Uso del Campo 'related' para Detectar Dependencias

El campo `related` del frontmatter contiene dependencias declaradas explícitamente. Usarlo como fuente adicional:

1. **Leer campo 'related'**: Extraer la lista de documentos relacionados del frontmatter actual
2. **Analizar dependencias**: Para cada documento relacionado, identificar:
   - ¿Qué información falta en ese documento relacionado?
   - ¿Qué documento sería el siguiente lógico después del relacionado?
3. **Proponer basado en dependencias**: Sugerir documentos siguientes que extiendan o complementen las dependencias declaradas
4. **Combinar con análisis de estructura**: Usar las dependencias declaradas como fuente adicional al análisis de estructura general

## Formato de Propuesta de Documentos Siguientes

```markdown
**PROPUESTA DE DOCUMENTOS SIGUIENTES**

**ESTRUCTURA DE DOCUMENTACIÓN DEL PROYECTO**:
[Resultado del mapeo de estructura]

**Análisis del documento actual**:
- Tipo: [tipo de documento]
- Área: [área identificada en la estructura del proyecto]
- Subárea: [subárea identificada en la estructura del proyecto]
- Propósito: [descripción del propósito]

**Documentos existentes en áreas relacionadas**:
- [Área 1]: [lista de documentos existentes]
- [Área 2]: [lista de documentos existentes]
...

**Documentos siguientes propuestos** (ordenados por prioridad):

1. **[Nombre del documento propuesto]**
   - Tipo: [tipo de documento]
   - Ubicación sugerida: [ruta basada en la estructura del proyecto]
   - Propósito: [descripción del propósito]
   - Justificación: [por qué es el siguiente paso lógico]
   - Dependencia: [documento(s) existente(s) que justifican esta propuesta]

2. **[Nombre del documento propuesto]**
   - Tipo: [tipo de documento]
   - Ubicación sugerida: [ruta basada en la estructura del proyecto]
   - Propósito: [descripción del propósito]
   - Justificación: [por qué es el siguiente paso lógico]
   - Dependencia: [documento(s) existente(s) que justifican esta propuesta]
...
```

## Patrones Comunes de Propuestas

- **Patrón de requisitos a especificaciones**: Después de un documento de requisitos (PRD, brief de producto), proponer especificaciones técnicas de los componentes mencionados
- **Patrón de arquitectura a decisiones**: Después de un documento de arquitectura de alto nivel, proponer ADRs para decisiones arquitectónicas específicas
- **Patrón de decisiones a implementación**: Después de un ADR o decisión arquitectónica, proponer especificaciones de implementación o guías técnicas
- **Patrón de estrategia a políticas**: Después de un documento de estrategia, proponer políticas operativas o guías de implementación
- **Patrón de especificaciones complementarias**: Después de una especificación técnica (ej. API), proponer especificaciones de componentes relacionados (ej. base de datos, frontend)
- **Patrón de producto a negocio**: Después de requisitos de producto, proponer casos de negocio o análisis de riesgos
- **Patrón de implementación a onboarding**: Después de especificaciones técnicas, proponer guías de implementación o documentación de onboarding

## Recomendación de Acción

Priorizar ediciones del archivo actual y ediciones a archivos existentes sobre crear nuevos documentos. Proponer documentos siguientes solo cuando representen el siguiente paso lógico para el desarrollo del sistema y no caben en la estructura existente.

## Salida

- **Propuesta de documentos siguientes**: Documentos lógicos como siguientes pasos cuando no caben en la estructura existente
- **Estructura del proyecto**: Mapeo de la estructura de documentación actual
