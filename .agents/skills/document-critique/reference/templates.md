# Plantillas de Formato

## Plantilla de Declaración de Clasificación

Usar al inicio del análisis:

```markdown
**CLASIFICACIÓN DEL DOCUMENTO**
- Tipo: [Tipo de archivo]
- Rol Principal: [Rol funcional principal]
- Roles a Revisar: [Rol 1] + [Rol 2] (+ [Rol 3] si aplica)
- Enfoque: [Descripción del enfoque de revisión]
- Perspectiva: Senior + Junior
- Fecha de análisis: [YYYY-MM-DD]
- Versión del análisis: [número incremental]
```

## Plantilla de Campo "related" en Frontmatter

Usar cuando un gap se resuelve mediante un archivo relacionado. Para detalles completos sobre cuándo y cómo usar este campo, consultar `workflows/04-investigation.md`.

```yaml
---
related:
  - archivo: "ruta/al/archivo-relacionado.md"
    razon: "Describe la relación y qué información proporciona"
    gaps_resueltos:
      - "Título del gap 1"
      - "Título del gap 2"
---
```

**Ejemplo práctico**:

```yaml
---
related:
  - archivo: "docs/arquitectura/decisiones/adr-001.md"
    razon: "Este ADR explica la decisión de usar PostgreSQL como base de datos principal"
    gaps_resueltos:
      - "Justificación de selección de base de datos"
      - "Trade-offs considerados en la elección"
---
```

**Uso crítico para deduplicación**: Este campo es OBLIGATORIO cuando un archivo relacionado resuelve gaps. Se usa para:

- Documentar explícitamente las relaciones entre archivos
- Evitar duplicación de gaps ya resueltos en archivos relacionados
- Mantener trazabilidad de información entre documentos
- Facilitar la investigación futura mediante referencias cruzadas

## Plantilla de Documentación de Relaciones Usadas

Usar al documentar relaciones de archivos usadas durante la investigación:

```markdown
**RELACIONES DE ARCHIVOS USADAS EN INVESTIGACIÓN**

[Archivo relacionado]:
- Relación: [Descripción de la relación]
- Gaps resueltos mediante esta relación: [Lista de gaps]
- Referencia: [Ruta al archivo]
```

## Plantilla de Estado del Análisis

Usar al inicio del análisis para documentar si existe un análisis previo:

```markdown
**ESTADO DEL ANÁLISIS**
- Análisis previo: [SÍ/NO]
- Fecha del último análisis: [YYYY-MM-DD si aplica]
- Versión anterior: [número si aplica]
- Gaps pendientes: [cantidad si aplica]
- Gaps respondidos: [cantidad si aplica]
```

## Plantilla de Hallazgos de Referencia

Usar al documentar respuestas encontradas en archivos de referencia:

```markdown
**RESPUESTAS ENCONTRADAS EN REFERENCIAS PARA [ROL]**

[Nombre del archivo de referencia]:
- [Pregunta]: Respuesta encontrada en [sección/línea específica]
- Referencia: [URL o ruta al archivo]

[Nombre de otro archivo de referencia]:
- [Pregunta]: Respuesta encontrada en [sección/línea específica]
- Referencia: [URL o ruta al archivo]
```

## Plantilla de Documentación de Gaps

Usar al documentar gaps identificados:

```markdown
**[CATEGORÍA TEMÁTICA]**

**GAP: [Título del gap]** [PRIORIDAD: Crítico/Alto/Medio/Bajo] [ESTADO: PENDIENTE/RESPONDIDO/NO APLICA/OBSOLETO]
- **Pregunta**: [Pregunta específica]
- **Contexto faltante**: [Descripción del contexto faltante]
- **Rol afectado**: [Roles funcionales afectados]
- **Referencia**: [Si aplica, referencia a fuente parcial]
- **Depende de**: [IDs o títulos de gaps que deben resolverse primero]
- **Fecha de identificación**: [YYYY-MM-DD]
```

### Estados de Gaps

- **PENDIENTE**: Gap identificado que requiere respuesta o investigación
- **RESPONDIDO**: Gap que ha sido respondido con información válida y referencias
- **NO APLICA**: Gap que no es relevante para el documento o contexto actual (con justificación)
- **OBSOLETO**: Gap que ya no es relevante debido a cambios en el documento o contexto

## Plantilla de Plan de Trabajo

Usar al final del análisis para organizar gaps por prioridad y dependencias:

```markdown
**PLAN DE TRABAJO**

### Gaps Críticos

**[Título del gap]** [PRIORIDAD: Crítico]
- **Acción sugerida**: [Descripción de la acción para resolver el gap]
- **Dependencias**: [Otros gaps o documentos que deben resolverse primero]

### Gaps de Alta Prioridad

**[Título del gap]** [PRIORIDAD: Alto]
- **Acción sugerida**: [Descripción de la acción para resolver el gap]
- **Dependencias**: [Otros gaps o documentos que deben resolverse primero]

### Gaps de Prioridad Media

**[Título del gap]** [PRIORIDAD: Medio]
- **Acción sugerida**: [Descripción de la acción para resolver el gap]
- **Dependencias**: [Otros gaps o documentos que deben resolverse primero]
```

**Nota**: Este plan de trabajo sirve para priorizar y ordenar la resolución de gaps basándose en sus dependencias. Los gaps de prioridad Baja se documentan pero no se incluyen en el plan.

## Plantilla de Gaps No Aplica

Usar al final del análisis para consolidar gaps marcados como no aplicables:

```markdown
**GAPS MARCADOS COMO NO APLICA**

Esta sección documenta gaps que fueron identificados pero determinados como no relevantes para el documento o contexto actual. Sirve como referencia para evitar re-detección en análisis futuros.

**[CATEGORÍA TEMÁTICA]**

**GAP: [Título del gap]**
- **Razón de no aplicación**: [Justificación de por qué este gap no es relevante]
- **Fecha de evaluación**: [YYYY-MM-DD]
- **Versión del análisis**: [número]

**[CATEGORÍA TEMÁTICA]**

**GAP: [Título del gap]**
- **Razón de no aplicación**: [Justificación de por qué este gap no es relevante]
- **Fecha de evaluación**: [YYYY-MM-DD]
- **Versión del análisis**: [número]
```

**Uso en deduplicación**: Antes de identificar un nuevo gap, verificar si ya existe en la sección "No Aplica". Si existe con la misma razón, no re-identificarlo.

## Plantilla de Documentación de Contradicciones

Usar al documentar contradicciones entre fuentes. Para detalles sobre manejo de contradicciones, consultar `references/guardrails.md`.

```markdown
**DISCREPANCIA**: [Descripción clara del conflicto]
**RECOMENDACIÓN**: [Sugerencia de resolución]
```

## Plantilla de Código Sin Documentación

Usar cuando el código existe pero carece de documentación explicativa:

```markdown
**NOTA**: El código implementa esta funcionalidad pero no hay documentación que explique el por qué de esta implementación.
```

## Plantillas de Formato de URL de GitHub

### Para Archivos de Código

```markdown
https://github.com/<org>/<repo>/blob/<branch>/<path-to-file>#L<line-number>
```

Ejemplo:

```markdown
https://github.com/example-org/example-repo/blob/main/src/Service.js#L24
```

### Para Commits

```markdown
https://github.com/<org>/<repo>/commit/<commit-hash>
```

## Categorías Temáticas para Agrupación de Gaps

Usar estas categorías al organizar gaps. Para categorías detalladas por tipo de documento, consultar `references/priorities.md`.

- **Arquitectura y Diseño**: Decisiones arquitectónicas, patrones, trade-offs técnicos
- **Implementación Técnica**: Detalles de código, APIs, dependencias, configuración
- **Negocio y Producto**: Requisitos, user stories, decisiones de producto, roadmap
- **Operaciones y Despliegue**: Workflows, infraestructura, monitoreo, procedimientos
- **Dominio y Terminología**: Conceptos del dominio, definiciones, glosario
- **Procesos y Workflows**: Procedimientos operacionales, guías, flujos de trabajo
- **Otro**: Cualquier otra categoría temática relevante según el documento
