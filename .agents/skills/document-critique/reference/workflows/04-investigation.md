# Paso 4: Investigación de Referencias

Para cada rol funcional relevante (mínimo 2-3 roles), revisa los archivos de referencia mencionados en el documento.

## 4.1 Identificar Archivos de Referencia Relevantes

Escanea el documento buscando menciones de otros archivos, documentos o recursos relevantes para el rol actual. El tipo de referencias varía según el tipo de documento:

**Para documentos técnicos**: Enlaces a documentación, rutas de archivos, URLs externas, ADRs, PRDs, especificaciones técnicas, código (commits, PRs)
**Para documentos estratégicos**: Referencias a documentos de visión, análisis de mercado, casos de negocio, planes estratégicos
**Para documentos de producto**: Referencias a user research, personas, journey maps, documentos de roadmap
**Para documentos de gestión**: Referencias a políticas legales, procedimientos de RRHH, documentos de compliance
**Para documentos de usuario**: Referencias a tutoriales, guías de soporte, documentación relacionada

## 4.2 Revisar Archivos de Referencia Identificados

Para cada archivo de referencia identificado:

- Lee el contenido del archivo de referencia
- Busca respuestas a preguntas que este rol específico haría según el tipo de documento
- Identifica información relevante que podría responder gaps potenciales para este rol
- Documenta qué respuestas se encontraron en cada referencia
- **Detectar contradicciones**: Compara la información del documento principal con las referencias. Si existen discrepancias, documéntalas usando el formato de contradicción de `references/guardrails.md`

## 4.2.1 Documentación de Relaciones entre Archivos (Campo "related")

**CRÍTICO**: Cuando un gap se resuelve mediante el uso de un archivo relacionado, es OBLIGATORIO documentar esta relación en el frontmatter del documento.

### Cuándo Usar el Campo "related"

El campo `related` en el frontmatter debe usarse cuando:

- Un archivo de referencia proporciona la respuesta a un gap identificado
- El documento actual depende de información contenida en otro archivo
- Existe una relación jerárquica o de dependencia entre documentos
- La comprensión del documento requiere consultar otro archivo relacionado

### Formato del Campo "related"

```yaml
---
related:
  - target: "ID-del-documento-relacionado"
    relationship_type: "depends_on|explains|references|extends"
    reason: "Describe la relación y qué información proporciona"
---
```

**Tipos de relación aplicables a resolución de gaps**:

- `depends_on`: El documento actual depende de información contenida en el target
- `explains`: El documento target explica conceptos o detalles relevantes para el documento actual
- `references`: El documento actual hace referencia a información específica del target
- `extends`: El documento target extiende o profundiza información del documento actual

### Ejemplo

```yaml
---
related:
  - target: "ENG-ARC-001"
    relationship_type: "depends_on"
    reason: "Este ADR explica la decisión de usar PostgreSQL como base de datos principal"
---
```

### Uso del Campo "related" para Evitar Duplicados

**IMPORTANTE**: Cuando un archivo contiene el campo `related` en su frontmatter:

1. **Antes de investigar**: Revisar el campo `related` para identificar archivos relacionados
2. **Durante la investigación**: Consultar los archivos relacionados como parte del proceso de investigación
3. **Referencia cruzada**: Cuando se encuentre información en un archivo relacionado, documentar la referencia cruzada explícitamente

Esto asegura que:

- Las relaciones entre documentos estén explícitamente documentadas
- No se duplique el trabajo de investigación
- Se mantenga trazabilidad de la información entre archivos

## 4.3 Documentar Hallazgos de Referencias

### 4.3.1 Documentación de Relaciones Usadas

Si durante la investigación se usaron archivos relacionados (del campo `related`), documentarlo explícitamente:

```markdown
**RELACIONES DE ARCHIVOS USADAS EN INVESTIGACIÓN**

[Archivo relacionado]:
- Relación: [relationship_type]
- Razón: [reason del campo related]
- Referencia: [ID del documento]
```

### 4.3.2 Documentación de Hallazgos

Añade una sección en el documento analizado con el formato:

```markdown
**RESPUESTAS ENCONTRADAS EN REFERENCIAS PARA [ROL]**

[Nombre del archivo de referencia]:
- [Pregunta]: Respuesta encontrada en [sección/línea específica]
- Referencia: [URL o ruta al archivo]

[Nombre de otro archivo de referencia]:
- [Pregunta]: Respuesta encontrada en [sección/línea específica]
- Referencia: [URL o ruta al archivo]
```

## 4.4 Actualizar Estado de Gaps para el Rol

Si una pregunta en el documento tiene una respuesta en un archivo de referencia:

- Incorpora esa respuesta al análisis actual para este rol
- Marca la pregunta como respondida con la referencia correspondiente
- No la incluyas en la lista de gaps a identificar para este rol

## 4.5 Prioridad de Referencias

Sigue la prioridad de fuentes de `references/priorities.md`, adaptando según el tipo de documento:

**Para documentos técnicos**: Documentación > Código > Comentarios de código
**Para documentos estratégicos**: Documentación estratégica > Análisis de mercado > Referencias externas
**Para documentos de producto**: Documentación de producto > User research > Datos de mercado
**Para documentos de gestión**: Políticas oficiales > Procedimientos internos > Referencias externas

Principio general: Documentación reciente > Documentación antigua, Referencias internas > Referencias externas

Si no existen archivos de referencia, procede directamente con el Paso 5: Identificación de Contexto Faltante.

## 4.6 Verificación de Deduplicación Mediante Relaciones

**Antes de proceder al Paso 5**, verificar:

1. Revisar el campo `related` del frontmatter (si existe)
2. Para cada archivo relacionado, verificar que la información proporcionada en `reason` es relevante
3. Confirmar que no se están identificando gaps que ya están cubiertos por las relaciones documentadas
4. Si se detecta duplicación, eliminar el gap duplicado y documentar la referencia al archivo relacionado

Esta verificación es CRÍTICA para mantener la idempotencia del proceso y evitar generación duplicada de gaps.
