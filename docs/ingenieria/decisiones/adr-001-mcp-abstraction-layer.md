---
id: ADR-001
type: Architecture Decision Record
rating: 9
rating-phase: document-critique
related:
  - target: STR-001
    relationship_type: implements
    reason: Implementa el principio estratégico de complementar LLMs mediante MCP como capa de abstracción
  - target: STR-002
    relationship_type: implements
    reason: Implementa la decisión tecnológica de MCP como capa de abstracción definida en technology-strategy
  - target: ARC-003
    relationship_type: depends_on
    reason: Depende de la arquitectura general del sistema para integración de MCP
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para almacenar configuración de MCP
  - target: ADR-002
    relationship_type: extends
    reason: Extiende el stack unificado Python al definir la implementación específica de MCP
---

# ADR-001: Uso de MCP como Capa de Abstracción para LLM

## Contexto y Problema

Alejandria requiere comunicación con múltiples proveedores de LLM (Anthropic, OpenAI, Qwen, etc.) para implementar sus agentes de detección, agrupación, resolución y verificación de gaps. Sin una capa de abstracción, el sistema tendría:

- **Vendor lock-in**: Dependencia de un solo proveedor de LLM
- **Código duplicado**: Lógica de integración repetida para cada proveedor
- **Dificultad de cambio**: Costo alto para cambiar de proveedor en el futuro
- **Falta de estandarización**: Tool calling y comunicación no estandarizada entre proveedores

## Decisiones

**Decisión**: Usar MCP (Model Context Protocol) como capa de abstracción para toda comunicación con LLMs, tanto para agentes internos del sistema como para agentes externos de terceros.

**Implementación específica**:

- MCP Server implementado en Python usando FastMCP
- Integración nativa con el stack Python (FastAPI)
- Capacidad de usar tanto agentes internos como externos a través de la misma capa

## Justificación

### Alineación con Principios Estratégicos

Esta decisión implementa directamente el principio de "complementar LLMs, no competir contra ellos" establecido en vision-mission.md:

1. **Cambio de proveedores sin reescribir código**: MCP permite cambiar entre Anthropic, OpenAI u otros proveedores sin modificar la arquitectura. Alejandria no depende de un solo LLM.

2. **Enfoque en valor de dominio**: MCP estandariza tool calling, permitiendo que Alejandria se enfoque en orquestación y detección de gaps (su valor de dominio) en lugar de construir capacidades LLM propias.

3. **Flexibilidad futura**: MCP habilita adoptar nuevos modelos a medida que surjan, reforzando que Alejandria complementa la evolución de LLM.

4. **Interacción simple y estandarizada**: MCP es la forma más simple de interactuar con agentes tanto interactiva como automáticamente, aprovechando que es un estándar.

5. **Apalancamiento de tecnología existente**: MCP es la capa técnica que implementa la decisión estratégica de apalancar tecnología base existente en lugar de desarrollar capacidades desde cero.

### Beneficios Técnicos

- **Componibilidad y testabilidad**: Cada componente puede probarse independientemente
- **Cambio de proveedores sin rewrite**: Reducción de vendor lock-in
- **Ecosistema de herramientas estándar**: Acceso a herramientas preexistentes
- **Interacción simple y estandarizada con agentes**: Menor complejidad en integración

### Alineación con Valores Organizacionales

MCP como capa de abstracción implementa el valor de "Integración Continua" al permitir integración con múltiples herramientas y proveedores sin cambios drásticos en arquitectura.

## Trade-offs

### Desventajas

- **Capa adicional de complejidad**: Añade una capa más a la arquitectura
- **Learning curve para equipo**: El equipo necesita aprender MCP

### Mitigación en Fase Bootstrapped

- Usar FastMCP (framework Python simplificado) para reducir complejidad de implementación
- Comenzar con un solo proveedor LLM (Qwen 3.5 en Ollama) para simplificar configuración inicial
- Documentar claramente el patrón MCP para facilitar onboarding del equipo

## Alternativas Consideradas

### Integración Directa con APIs de Proveedores

**Ventaja inicial**: Menor complejidad arquitectónica, setup más simple, menor learning curve

**Desventaja a largo plazo**: Vendor lock-in, dificultad para cambiar de proveedor, arquitectura menos flexible

**Decisión**: Rechazada porque el costo de cambio futuro (refactorizar de integración directa a MCP) sería más alto que implementar MCP desde el inicio.

### Uso de Frameworks como LangChain

**Ventaja**: Ecosistema amplio de herramientas

**Desventaja**: MCP es más simple y ligero, mejor enfocado en estandarización de comunicación vs framework completo de orquestación

**Decisión**: Rechazada porque MCP es un estándar abierto más simple que proporciona interoperabilidad sin la complejidad de un framework completo.

## Consecuencias

### Impacto Positivo

- Flexibilidad para cambiar de proveedor LLM según evolución del mercado
- Capacidad de usar agentes externos además de los internos
- Estándar abierto que reduce riesgo de obsolescencia tecnológica
- Menor costo de mantenimiento a largo plazo

### Impacto Negativo

- Complejidad inicial adicional en implementación
- Necesidad de capacitación del equipo en MCP

### Requerimientos de Implementación

- MCP Server implementado con FastMCP
- Documentación clara del patrón MCP para el equipo
- Configuración inicial con un solo proveedor (Qwen 3.5 en Ollama)
- Estrategia de testing para validar integración con múltiples proveedores

## Referencias

- vision-mission.md: Principio de "complementar LLMs, no competir contra ellos"
- technology-strategy.md: Sección "MCP como Capa de Abstracción"
- technology-strategy.md: Sección "MCP en Fase Bootstrapped"
