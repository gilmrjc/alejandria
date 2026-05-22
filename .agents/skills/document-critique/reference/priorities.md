# Referencia de Prioridades y Categorización

## Niveles de Prioridad

Asignar prioridad a cada gap identificado basándose en la matriz de decisión de factores.

### Matriz de Asignación de Prioridad

Asignar prioridad basándose en la combinación de factores:

**Factores a evaluar:**

1. **Impacto en negocio**: Alto (bloquea decisiones estratégicas) / Medio (afecta ejecución) / Bajo (contexto adicional)
2. **Riesgo**: Alto (puede causar errores críticos o pérdidas) / Medio (afecta calidad) / Bajo (nice-to-have)
3. **Costo de no resolver**: Alto (retrabajo significativo) / Medio (fricción operacional) / Bajo (inconveniente menor)
4. **Bloqueante**: Alto (3+ documentos dependen indirectamente) / Medio (1-2 documentos dependen) / Bajo (ningún documento depende)

**Tabla de decisión:**

| Factores "Alto" | Factores "Medio" | Bloqueante Alto | Prioridad |
|:----------------|:-----------------|:----------------|:----------|
| 3+              | Cualquiera       | Cualquiera      | Crítico   |
| Cualquiera      | Cualquiera       | Sí + 1 Alto     | Crítico   |
| 2               | Cualquiera       | No              | Alto      |
| 1               | 1+               | No              | Alto      |
| 1               | 0                | No              | Medio     |
| 0               | 2+               | No              | Medio     |
| 0               | 0-1              | No              | Bajo      |

**Reglas simplificadas:**

- **Crítico**: 3+ factores Alto, o Bloqueante Alto + 1+ factor Alto
- **Alto**: 2 factores Alto, o 1 factor Alto + 1+ factor Medio
- **Medio**: 1 factor Alto, o 2+ factores Medio
- **Bajo**: 0-1 factor Medio, sin factores Alto

### Descripciones de Niveles

### Crítico

- Bloquea decisiones importantes (de negocio o técnicas)
- Representa riesgo alto para el negocio
- Bloquea desarrollo/entrega de features

### Alto

- Impacta significativamente la comprensión o toma de decisiones (de negocio o técnicas)
- Afecta capacidad de ejecución técnica

### Medio

- Proporciona contexto útil pero no es esencial para decisiones actuales
- No bloquea desarrollo

### Bajo

- Información nice-to-have
- Detalles granulares o contexto de referencia

## Categorías Temáticas

Agrupar gaps por categorías temáticas naturales, adaptando según el tipo de documento:

### Categorías para Documentos Estratégicos

- **Visión y Estrategia**: Visión organizacional, dirección estratégica, objetivos a largo plazo
- **Negocio y Mercado**: Análisis de mercado, casos de negocio, propuestas de negocio
- **Stakeholders**: Identificación de stakeholders, roles, responsabilidades
- **KPIs y Métricas**: Definición de KPIs, métricas de éxito, medición de impacto
- **Cultura y Valores**: Valores organizacionales, principios, cultura corporativa

### Categorías para Documentos de Producto

- **Requisitos**: Requisitos funcionales y no funcionales, user stories, features
- **Usuario y Experiencia**: Personas, journey maps, experiencia de usuario
- **Roadmap**: Planificación temporal, priorización de features, entregas
- **Mercado**: Análisis de mercado, competencia, posicionamiento
- **Validación**: User research, feedback de usuarios, pruebas de concepto

### Categorías para Documentos Técnicos

- **Arquitectura y Diseño**: Decisiones arquitectónicas, patrones de diseño, trade-offs técnicos, interacciones de componentes
- **Implementación Técnica**: Detalles de código, contratos de API, dependencias, configuración técnica
- **Operaciones y Despliegue**: Workflows de despliegue, infraestructura, monitoreo, procedimientos operacionales
- **Dominio y Terminología**: Conceptos del dominio, definiciones, glosario de términos
- **Procesos y Workflows**: Procedimientos operacionales, guías, flujos de trabajo

### Categorías para Documentos de Operaciones

- **Procesos**: Workflows, procedimientos, guías operacionales
- **Infraestructura**: Configuración de sistemas, recursos, escalabilidad
- **Monitoreo**: Métricas, alertas, dashboards
- **Incidentes**: Post-mortems, análisis de incidentes, planes de recuperación
- **Seguridad**: Políticas de seguridad, procedimientos de cumplimiento, análisis de riesgos

### Categorías para Documentos de Usuario

- **Usabilidad**: Facilidad de uso, experiencia de usuario, accesibilidad
- **Instrucciones**: Claridad de instrucciones, tutoriales, guías paso a paso
- **Troubleshooting**: Resolución de problemas, diagnóstico de errores, FAQ
- **Onboarding**: Guías para nuevos usuarios, recursos de aprendizaje
- **Soporte**: Canales de soporte, documentación de ayuda, recursos adicionales

### Categorías para Documentos de Gestión

- **Políticas**: Políticas organizacionales, procedimientos estándar, reglamentos
- **Compliance**: Requisitos legales, regulaciones, estándares de cumplimiento
- **Recursos**: Gestión de recursos, presupuestos, asignación de personal
- **Proyectos**: Plan de proyecto, cronogramas, riesgos, seguimiento de entregas
- **Recursos Humanos**: Políticas de empleados, onboarding, cultura organizacional, procedimientos de RRHH

### Categorías para Documentos de Referencia

- **Definiciones**: Conceptos del dominio, términos, glosario
- **Estándares**: Estándares técnicos, guías de estilo, convenciones
- **APIs**: Documentación de APIs, endpoints, ejemplos de uso
- **Best Practices**: Mejores prácticas, patrones recomendados, guías de implementación

### Categorías Genéricas

- **Otro**: Cualquier otra categoría temática relevante según el documento

## Formato de Documentación de Gaps

```text
**[CATEGORÍA TEMÁTICA]**

**GAP: [Título del gap]** [PRIORIDAD: Crítico/Alto/Medio/Bajo]
- **Pregunta**: [Pregunta específica]
- **Contexto faltante**: [Descripción del contexto faltante]
- **Rol afectado**: [Roles funcionales afectados]
- **Referencia**: [Si aplica, referencia a fuente parcial]
```

## Prioridad de Fuentes

Al investigar información, priorizar fuentes en este orden:

1. **Documentación técnica** > Código > Comentarios en código
2. **Documentación reciente** > Documentación antigua
3. **Referencias internas del proyecto** > Referencias externas

## Tipos de Documentos Recomendados para Consolidación

Al sugerir consolidación, usar tipos de documentos apropiados según el tipo de gaps:

### Para Gaps Estratégicos

- **Documento Estratégico**: Planeamiento a largo plazo, decisiones estratégicas, visión organizacional
- **Documento de Negocio**: Análisis de mercado, propuestas de negocio, casos de negocio
- **Documento de Cultura**: Valores, principios, manifiestos, guías culturales

### Para Gaps de Producto

- **PRD**: Requisitos de negocio y features de producto
- **Especificación de Requisitos**: Requisitos funcionales y no funcionales detallados
- **Documento de Roadmap**: Planificación temporal de features y entregas
- **Documento de User Research**: Investigación de usuarios, personas, journey maps

### Para Gaps Técnicos

- **ADR**: Decisiones arquitectónicas y trade-offs técnicos
- **Documento de Arquitectura**: Diseño de sistema y especificaciones técnicas
- **Especificación Técnica**: Detalles de implementación y contratos de API
- **Documento de Diseño**: Diseño de UI/UX, wireframes, prototipos

### Para Gaps de Operaciones

- **Documento de Proceso**: Workflows y procedimientos operacionales
- **Manual de Operaciones**: Guías de despliegue, monitoreo, escalas
- **Documento de Incidentes**: Post-mortems, análisis de incidentes, planes de recuperación
- **Documento de Seguridad**: Políticas de seguridad, procedimientos de cumplimiento

### Para Gaps de Usuario

- **Manual de Usuario**: Guías para usuarios finales, tutoriales, documentación de uso
- **Guía de Onboarding**: Documentación para nuevos usuarios o empleados
- **FAQ**: Preguntas frecuentes y respuestas
- **Documentación de Soporte**: Guías de troubleshooting, resolución de problemas

### Para Gaps de Gestión

- **Documento de Políticas**: Políticas organizacionales, procedimientos estándar
- **Documento de Compliance**: Requisitos legales, regulaciones, estándares de cumplimiento
- **Documento de Proyecto**: Plan de proyecto, cronogramas, recursos, riesgos
- **Documento de Recursos Humanos**: Manuales de empleados, políticas de RRHH

### Para Gaps de Referencia

- **Glosario**: Definiciones de términos del dominio
- **Documento de Estándares**: Estándares técnicos, guías de estilo, convenciones
- **Documento de API**: Documentación de APIs, endpoints, ejemplos de uso

## Criterios de Consolidación

Crear nuevos documentos solo cuando:

- Hay más de 10 gaps relacionados con un tema específico
- El contenido excede el 30% del tamaño actual del documento
- El contenido pertenece a un dominio funcional diferente (ej. gaps de arquitectura en un PRD)

De lo contrario, preferir editar el documento actual en lugar de crear nuevos.
