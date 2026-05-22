# Paso 5: Identificación de Contexto Faltante

Para cada rol funcional relevante (mínimo 2-3 roles), identifica el contexto faltante desde la perspectiva del rol.

## 5.1 Recopilar Información para el Rol

Usa fuentes de información disponibles para encontrar respuestas específicas para el rol, adaptando según el tipo de documento:

**Para documentos técnicos**: Documentación existente, repositorios de código, ADRs, especificaciones técnicas
**Para documentos estratégicos**: Documentación estratégica, análisis de mercado, casos de negocio, planes de crecimiento
**Para documentos de producto**: Documentación de producto, user research, datos de mercado, feedback de usuarios
**Para documentos de gestión**: Políticas oficiales, procedimientos internos, documentos de compliance, regulaciones
**Para documentos de usuario**: Tutoriales, guías de soporte, documentación relacionada, FAQs

**Prioridad de Fuentes**: La documentación es la fuente de razones y decisiones. Para documentos técnicos, el código es una implementación y no contiene razones (que son las preguntas fundamentales). El código sirve para entender estructuras y flujos, pero debería tener un rol secundario en las citas. Lo más importante es la documentación.

Si existe código pero no hay documento que explique el código, añade esta anotación:

```markdown
**NOTA**: El código implementa esta funcionalidad pero no hay documentación que explique el por qué de esta implementación.
```

Para documentos no técnicos, si existe información pero no hay documentación que explique las razones/decisiones, añade una anotación similar adaptada al contexto.

## 5.2 Identificar Contexto Faltante para el Rol

El objetivo es encontrar información faltante desde la perspectiva del rol, no proporcionar respuestas. Enfócate en:

- **Claridad de Conceptos**: ¿Están los conceptos usados claramente definidos para este rol según el tipo de documento?
- **Lenguaje Apropiado**: ¿Hay lenguaje claro apropiado para este rol (técnico, de negocio, de usuario, etc.)?
- **Gaps de Contexto**: ¿Se necesita más contexto para determinar la validez de las respuestas para este rol?
- **Adaptación al Tipo de Documento**: Los gaps identificados deben ser relevantes al tipo de documento (ej. para documentos estratégicos: gaps sobre impacto en negocio; para documentos de usuario: gaps sobre usabilidad)

## 5.2.1 Detectar Información Fuera de Scope

Además de identificar contexto faltante, detecta cuando el documento contiene información que no corresponde a su tipo y propósito:

**Criterios para identificar información fuera de scope**:

- Revisar el tipo de documento clasificado en el Paso 1
- Verificar si el contenido incluye detalles que pertenecen a otros tipos de documentos
- Consultar la sección "Nivel de Detalle y Profundidad del Documento" en `references/classification.md` para ejemplos específicos

**Ejemplos comunes de información fuera de scope**:

- **PRD con detalles técnicos**: Implementación específica, código, configuración técnica
- **Documento de arquitectura con decisiones de negocio**: Justificación de negocio, análisis de mercado, roadmap de producto
- **Documento estratégico con detalles operacionales**: Configuración de CI/CD, scripts de despliegue, procedimientos granulares
- **Especificación técnica con requisitos de producto**: User stories, criterios de aceptación de usuario, journey maps

**Formato para documentar información fuera de scope**:

Cuando se detecta información fuera de scope, crear un gap usando la plantilla estándar de documentación de gaps (ver `references/templates.md`):

```markdown
**[CATEGORÍA TEMÁTICA]**

**GAP: Justificación de información fuera de scope: [descripción breve]** [PRIORIDAD: Medio] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Por qué se incluye [descripción de la información fuera de scope] en este documento? Esta información parece corresponder a [tipo de documento sugerido] más que a [tipo de documento actual].
- **Contexto faltante**: Justificación de por qué esta información está incluida en este documento en lugar de en el tipo de documento apropiado.
- **Rol afectado**: [Rol funcional que identifica el problema]
- **Referencia**: [Líneas específicas del documento donde aparece la información fuera de scope]
- **Fecha de identificación**: [YYYY-MM-DD]
```

**Ejemplo**:

```markdown
**Alcance y Propósito del Documento**

**GAP: Justificación de información fuera de scope: detalles de implementación en PRD** [PRIORIDAD: Medio] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Por qué se incluyen los detalles de implementación del endpoint X (líneas 45-60) en este PRD? Esta información parece corresponder a una Especificación Técnica más que a un PRD (Product Requirements Document).
- **Contexto faltante**: Justificación de por qué los detalles de implementación específicos están incluidos en un PRD, que debe enfocarse en requisitos de negocio y funcionalidad del producto.
- **Rol afectado**: Product Manager
- **Referencia**: Líneas 45-60 del documento actual
- **Fecha de identificación**: 2026-05-26
```

## 5.3 Preguntas Clave para el Rol

Aplica el marco de preguntas clave (cómo/por qué/qué/cuándo/quién/dónde) adaptado al rol funcional y al tipo de documento:

- **Cómo**: ¿Cómo funciona esto para este rol? ¿Cómo está implementado/diseñado/ejecutado? ¿Cómo se logra?
- **Por qué**: ¿Por qué se tomó esta decisión? ¿Por qué este enfoque? ¿Por qué no alternativas?
- **Qué**: ¿Qué recursos/tecnologías/procesos se usan? ¿Qué componentes están involucrados? ¿Cuáles son las dependencias/requisitos?
- **Cuándo**: ¿Cuándo se implementó/diseñó esto? ¿Cuándo debería cambiar? ¿Cuándo se usa/aplica?
- **Quién**: ¿Quién tomó esta decisión? ¿Quién es responsable? ¿Quiénes son los stakeholders/afectados?
- **Dónde**: ¿Dónde está el código/documentación/recurso? ¿Dónde está documentado? ¿Dónde se usa/aplica?

**Adaptación por tipo de documento**: Las preguntas específicas varían según el contexto. Por ejemplo:

- Documento estratégico: "¿Por qué esta dirección estratégica?", "¿Quiénes son los stakeholders afectados?"
- Documento de usuario: "¿Cómo se usa esta función?", "¿Dónde está documentado el troubleshooting?"
- Documento técnico: "¿Cómo está implementado?", "¿Dónde está el código?"

Si haces alguna de estas preguntas sobre algo desde la perspectiva del rol, esas preguntas deberían añadirse al archivo de documentación.

## 5.4 Añadir Referencias para el Rol

Al encontrar información que responde una pregunta para el rol:

- Añade citas y referencias a archivos fuente
- **Para código**: Usa URLs de GitHub en lugar de rutas de archivos locales
  - Formato: `https://github.com/<org>/<repo>/blob/<branch>/<path-to-file>#L<line-number>`
  - Ejemplo: `https://github.com/example-org/example-repo/blob/main/src/Service.js#L24`
- **Para commits**: Usa URLs de GitHub con hash de commit
- **Para documentos no técnicos**: Usa URLs apropiadas al tipo de recurso (documentos de Google Drive, sistemas de gestión de proyectos, etc.)
- Incluye números de línea en URLs de GitHub cuando sea aplicable
- Cita fragmentos relevantes cuando sea útil

Consulta `references/guardrails.md` para requisitos detallados de formato de referencias.
