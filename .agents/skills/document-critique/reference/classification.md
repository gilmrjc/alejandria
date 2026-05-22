# Referencia de Clasificación

## Tipos de Documentos

Categorizar los documentos en uno de los siguientes tipos:

### Documentos Estratégicos

- **Documento Estratégico**: Planeamiento a largo plazo, items de roadmap, decisiones estratégicas, visión organizacional
- **Documento de Negocio**: Análisis de mercado, propuestas de negocio, casos de negocio, planes de crecimiento
- **Documento de Cultura**: Valores, principios, manifiestos, guías culturales

### Documentos de Producto

- **Product Requirements Document (PRD)**: Requisitos de negocio, user stories, features de producto
- **Especificación de Requisitos**: Requisitos funcionales y no funcionales detallados
- **Documento de Roadmap**: Planificación temporal de features y entregas
- **Documento de User Research**: Investigación de usuarios, personas, journey maps

### Documentos Técnicos

- **Especificación Técnica**: Documento con detalles de implementación, contratos de API, restricciones técnicas
- **Documento de Arquitectura**: Diseño de sistema, interacciones de componentes, decisiones de diseño
- **Architecture Decision Record (ADR)**: Decisiones arquitectónicas, trade-offs técnicos
- **Documento de Diseño**: Diseño de UI/UX, wireframes, prototipos

### Documentos de Operaciones

- **Documento de Proceso**: Workflows, procedimientos, guías operacionales
- **Manual de Operaciones**: Guías de despliegue, monitoreo, escalas
- **Documento de Incidentes**: Post-mortems, análisis de incidentes, planes de recuperación
- **Documento de Seguridad**: Políticas de seguridad, procedimientos de cumplimiento

### Documentos de Usuario

- **Manual de Usuario**: Guías para usuarios finales, tutoriales, documentación de uso
- **Guía de Onboarding**: Documentación para nuevos usuarios o empleados
- **FAQ**: Preguntas frecuentes y respuestas
- **Documentación de Soporte**: Guías de troubleshooting, resolución de problemas

### Documentos de Gestión

- **Documento de Políticas**: Políticas organizacionales, procedimientos estándar
- **Documento de Compliance**: Requisitos legales, regulaciones, estándares de cumplimiento
- **Documento de Proyecto**: Plan de proyecto, cronogramas, recursos, riesgos
- **Documento de Recursos Humanos**: Manuales de empleados, políticas de RRHH

### Documentos de Referencia

- **Glosario/Terminología**: Definiciones de términos y conceptos del dominio
- **Documento de Estándares**: Estándares técnicos, guías de estilo, convenciones
- **Documento de API**: Documentación de APIs, endpoints, ejemplos de uso

### Otros

- **Otro**: Cualquier otro tipo no clasificado en las categorías anteriores

## Roles Funcionales

Determinar el rol funcional principal basado en el tipo de documento y su contenido:

### Roles de Negocio y Estrategia

- **Ejecutivo/Liderazgo**: Visión estratégica, decisiones de alto nivel, impacto en negocio, KPIs, objetivos organizacionales
- **Product Manager/Owner**: Requisitos de negocio, user stories, features, roadmap, decisiones de producto, contexto de negocio
- **Business Analyst**: Análisis de requisitos, procesos de negocio, casos de uso, análisis de viabilidad
- **Stakeholder de Negocio**: Interesados del negocio, sponsors, clientes internos, departamentos funcionales

### Roles Técnicos

- **Desarrollador/Ingeniero**: Detalles de implementación, arquitectura, trade-offs técnicos, contratos de API, evaluación de código y decisiones técnicas
- **Arquitecto**: Decisiones de diseño de alto nivel, patrones arquitectónicos, integraciones de sistemas, consideraciones de escalabilidad
- **QA/Tester**: Criterios de aceptación, casos de prueba, escenarios de validación, requisitos de calidad
- **DevOps/SRE**: Workflows de despliegue, monitoreo, infraestructura, procedimientos operacionales, configuración de sistemas
- **Diseñador UI/UX**: Diseño de interfaz, experiencia de usuario, wireframes, prototipos

### Roles de Operaciones

- **Operaciones/DevOps/SRE**: Workflows de despliegue, monitoreo, infraestructura, procedimientos operacionales, configuración de sistemas
- **Gerente de Proyecto**: Planificación, cronogramas, recursos, riesgos, seguimiento de entregas
- **Gerente de Operaciones**: Procesos operacionales, eficiencia, métricas de operaciones
- **Especialista en Seguridad**: Políticas de seguridad, procedimientos de cumplimiento, análisis de riesgos

### Roles de Usuario y Soporte

- **Usuario Final**: Usabilidad, claridad de instrucciones, experiencia de uso, facilidad de aprendizaje
- **Soporte Técnico**: Troubleshooting, guías de resolución de problemas, FAQ, documentación para usuarios finales
- **Cliente Externo**: Requisitos del cliente, expectativas, casos de uso desde perspectiva del cliente

### Roles de Gestión y Cumplimiento

- **Recursos Humanos**: Políticas de empleados, onboarding, cultura organizacional, procedimientos de RRHH
- **Legal/Compliance**: Requisitos legales, regulaciones, estándares de cumplimiento, políticas de privacidad
- **Finanzas**: Presupuestos, análisis de costos, ROI, proyecciones financieras
- **Auditor**: Requisitos de auditoría, controles, documentación de cumplimiento

### Roles Mixtos

- **Mixto**: Múltiples roles funcionales con secciones diferenciadas

## Combinaciones de Roles por Tipo de Documento

Mínimo 2-3 roles para revisar por tipo de documento. El agente debe adaptar las combinaciones según el contexto específico del documento:

### Combinaciones para Documentos Estratégicos

- **Documento Estratégico**: Ejecutivo + Product Manager (+ Stakeholder de Negocio si aplica)
- **Documento de Negocio**: Business Analyst + Ejecutivo (+ Product Manager si aplica)
- **Documento de Cultura**: Liderazgo + Recursos Humanos (+ Todos los empleados si aplica)

### Combinaciones para Documentos de Producto

- **PRD**: Product Manager + Desarrollador (+ Usuario Final si aplica)
- **Especificación de Requisitos**: Business Analyst + Product Manager (+ Desarrollador si aplica)
- **Documento de Roadmap**: Product Manager + Ejecutivo (+ Stakeholder de Negocio si aplica)
- **Documento de User Research**: Product Manager + Diseñador UI/UX (+ Usuario Final si aplica)

### Combinaciones para Documentos Técnicos

- **Especificación Técnica**: Desarrollador + Arquitecto (+ QA si aplica)
- **Documento de Arquitectura**: Arquitecto + Desarrollador (+ Operations si aplica)
- **ADR**: Arquitecto + Desarrollador
- **Documento de Diseño**: Diseñador UI/UX + Product Manager (+ Desarrollador si aplica)

### Combinaciones para Documentos de Operaciones

- **Documento de Proceso**: Operaciones + Soporte (+ Desarrollador si aplica)
- **Manual de Operaciones**: Operaciones + DevOps/SRE (+ Gerente de Operaciones si aplica)
- **Documento de Incidentes**: DevOps/SRE + Arquitecto (+ Gerente de Proyecto si aplica)
- **Documento de Seguridad**: Especialista en Seguridad + Legal/Compliance (+ DevOps/SRE si aplica)

### Combinaciones para Documentos de Usuario

- **Manual de Usuario**: Usuario Final + Soporte Técnico (+ Diseñador UI/UX si aplica)
- **Guía de Onboarding**: Recursos Humanos + Usuario Final (+ Gerente de Proyecto si aplica)
- **FAQ**: Soporte Técnico + Usuario Final
- **Documentación de Soporte**: Soporte Técnico + Usuario Final (+ Desarrollador si aplica)

### Combinaciones para Documentos de Gestión

- **Documento de Políticas**: Legal/Compliance + Recursos Humanos (+ Liderazgo si aplica)
- **Documento de Compliance**: Legal/Compliance + Auditor (+ Gerente de Proyecto si aplica)
- **Documento de Proyecto**: Gerente de Proyecto + Stakeholder de Negocio (+ Desarrollador si aplica)
- **Documento de Recursos Humanos**: Recursos Humanos + Liderazgo (+ Todos los empleados si aplica)

### Combinaciones para Documentos de Referencia

- **Glosario/Terminología**: Todos los roles relevantes al dominio
- **Documento de Estándares**: Arquitecto + Desarrollador (+ QA si aplica)
- **Documento de API**: Desarrollador + Arquitecto (+ Usuario Final si aplica)

### Combinaciones para Otros Tipos

- **Otro**: Adaptar roles según el contenido y propósito del documento

## Nivel de Detalle y Profundidad del Documento

Al clasificar un documento, es crítico detectar el nivel de detalle y profundidad que trata según el tipo de texto y contexto. Esto evita falsos positivos en la detección de gaps.

### Principios de Alineación de Nivel

**Evitar gaps fuera de alcance según el tipo de documento:**

- **Documentos de producto**: No buscar gaps de detalles técnicos de implementación. Enfocarse en requisitos, user stories, features, y decisiones de producto. Los detalles técnicos pertenecen a especificaciones técnicas o código.
- **Documentos de arquitectura**: No buscar gaps de implementación específica (código). Enfocarse en decisiones de diseño, patrones, trade-offs arquitectónicos, e interacciones de componentes. La implementación detallada pertenece al código.
- **Documentos de estrategia**: No buscar gaps de detalles operacionales granulares. Enfocarse en visión, decisiones de alto nivel, impacto en negocio, y KPIs.
- **Documentos MVP**: No buscar gaps de datos importantes para productos enterprise (ej. compliance complejo, escalabilidad masiva). Enfocarse en lo esencial para el MVP actual.
- **Documentos técnicos**: No buscar gaps de decisiones de negocio o estrategia de producto a menos que estén directamente relacionadas con decisiones técnicas.

### Ejemplos de Falsos Positivos a Evitar

| Tipo de Documento      | Gap Falso Positivo (NO buscar)                                 | Enfoque Correcto                                                |
|:-----------------------|:---------------------------------------------------------------|:----------------------------------------------------------------|
| PRD                    | "¿Cómo está implementado el endpoint X?"                       | "¿Qué requisitos de negocio satisface el feature X?"            |
| Arquitectura           | "¿Qué línea de código maneja el error?"                        | "¿Qué patrón de manejo de errores se usa en el sistema?"        |
| Estrategia             | "¿Qué herramienta de CI/CD se usa?"                            | "¿Qué objetivos estratégicos guían la selección de tecnología?" |
| MVP                    | "¿Cómo se maneja compliance GDPR enterprise?"                  | "¿Qué datos mínimos se necesitan para el lanzamiento?"          |
| Especificación Técnica | "¿Por qué esta característica es prioritaria para el negocio?" | "¿Qué restricciones técnicas afectan la implementación?"        |

### Criterios para Determinar el Nivel Apropiado

Al evaluar si un gap es apropiado para el tipo de documento:

1. **Revisar el propósito declarado** del documento
2. **Identificar el público objetivo** principal
3. **Verificar el nivel de abstracción** del contenido (alto vs bajo)
4. **Considerar el contexto del proyecto** (MVP vs enterprise, prototipo vs producción)
5. **Preguntar**: ¿Esta información debería estar en este documento o en otro tipo de documento?

### Detección de Información Fuera de Scope en el Documento

Además de evitar generar gaps fuera de alcance, es crítico detectar cuando el documento **contiene** información que no corresponde a su tipo y propósito.

**Criterios para identificar información fuera de scope**:

1. **Revisar el tipo de documento clasificado**
2. **Verificar si el contenido incluye detalles que pertenecen a otros tipos de documentos**
3. **Evaluar si la información es apropiada para el público objetivo del documento**
4. **Considerar si la información debería estar en un documento separado**

**Ejemplos de información fuera de scope por tipo de documento**:

| Tipo de Documento      | Información Fuera de Scope (Detectar)                                    | Debería Estar En          |
|:-----------------------|:-------------------------------------------------------------------------|:--------------------------|
| PRD                    | Detalles de implementación, código, configuración técnica                | Especificación Técnica    |
| Arquitectura           | Justificación de negocio, análisis de mercado, roadmap de producto       | Documento Estratégico/PRD |
| Estrategia             | Configuración de CI/CD, scripts de despliegue, procedimientos granulares | Manual de Operaciones     |
| Especificación Técnica | User stories, criterios de aceptación de usuario, journey maps           | PRD                       |
| Documento de Proceso   | Decisiones arquitectónicas, trade-offs técnicos                          | ADR/Arquitectura          |
| Manual de Usuario      | Justificación de negocio, análisis de mercado, roadmap                   | Documento Estratégico/PRD |

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

### Adaptación por Contexto de Proyecto

**Proyectos MVP/Early Stage**:

- Enfocarse en funcionalidad esencial y time-to-market
- Evitar gaps de escalabilidad masiva, compliance enterprise, optimización prematura
- Priorizar gaps que bloquean el lanzamiento

**Proyectos Enterprise/Production**:

- Considerar gaps de compliance, seguridad, escalabilidad
- Incluir gaps de optimización y rendimiento
- Considerar gaps de gobernanza y procesos

**Proyectos Legacy**:

- Enfocarse en gaps de deuda técnica y modernización
- Considerar gaps de compatibilidad y migración
- Balancear gaps de innovación vs estabilidad

## Perspectivas de Nivel de Experiencia

Aplicar ambas perspectivas a cada rol funcional:

### Perspectiva Senior

Enfocarse en decisiones y contexto estratégico:

- Entender las razones fundamentales detrás de las decisiones tomadas
- Identificar el impacto en el negocio y consideraciones de largo plazo
- Evaluar trade-offs y alternativas consideradas
- Validar que el contexto estratégico esté documentado
- Enfocarse en gaps que impidan la toma de decisiones informadas

### Perspectiva Junior

Enfocarse en entendimiento fundamental y onboarding:

- Entender las razones desde un punto más fundamental: pros y contras
- Obtener explicaciones claras de conceptos de dominio y terminología usada
- Tener un paso a paso de los procesos a implementar para entender cómo funcionan
- Validar que haya suficiente contexto para entender el sistema sin investigación adicional
- Enfocarse en gaps que dificulten el aprendizaje y el entendimiento del sistema

## Formato de Declaración de Clasificación

Al inicio del análisis, declarar:

```text
**CLASIFICACIÓN DEL DOCUMENTO**
- Tipo: [Tipo de archivo]
- Rol Principal: [Rol funcional principal]
- Roles a Revisar: [Rol 1] + [Rol 2] (+ [Rol 3] si aplica)
- Enfoque: [Descripción del enfoque de revisión]
- Perspectiva: Senior + Junior
```
