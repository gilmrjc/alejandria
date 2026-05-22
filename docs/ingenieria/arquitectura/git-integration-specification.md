---
id: ARC-010
type: Integration Specification
rating:
rating-phase:
dependency: [ESTR-STR-002, ARC-011, ARC-003]
related:
  - target: STR-002
    relationship_type: implements
    reason: Implementa la estrategia tecnológica con especificación de integración Git
  - target: ARC-011
    relationship_type: implements
    reason: Implementa el architecture overview con detalles de integración Git
---

## Especificación de Integración Git — Alejandria

Este documento define los detalles técnicos de integración con Git para el Hito 7 del roadmap técnico de Alejandria.

---

## Propósito de la Integración Git

Recuperar un repositorio usando su branch principal (main, master u otro) y generar un grafo de relaciones usando treesitter y análisis AST. Este grafo se apunta a los distintos documentos existentes para poder:

- Recuperar la relación entre código y decisiones tomadas
- Entender por qué el código existente tiene la forma y arquitectura en base a documentación real
- Encontrar gaps de código sin referencia como muestra posible de gaps existentes

---

## Patón General de Integración

Fuente externa → documentos

Git para código-documentos (implementación actual). Otros sistemas (Jira para tareas-documentos, Notion para documentos externos-documentos, etc.) se definirán en fase posterior según necesidades de validación.

---

## Justificación

Git es universal en proyectos de desarrollo, por lo que es la integración más apropiada para MVP bootstrapped. Los otros sistemas (Jira, Notion, Confluence) dependen mucho de los equipos y pueden tener más variación, por lo que se dejan para una fase posterior.

---

## Componentes de la Integración

### Recuperación de Repositorio

- **Branch principal**: main, master u otro (configurable)
- **Autenticación**: PENDIENTE - método de autenticación por definir (SSH, HTTPS, token)
- **Clonado local**: PENDIENTE - estrategia de clonado y actualización
- **Manejo de repositorios grandes**: PENDIENTE - estrategia para repositorios con muchos archivos

### Análisis AST con Treesitter

- **Parser**: Treesitter para análisis de código fuente
- **Lenguajes soportados**: PENDIENTE - lista de lenguajes por definir (Python, JavaScript, etc.)
- **Extracción de estructuras**: PENDIENTE - qué estructuras se extraen (funciones, clases, imports, etc.)
- **Mapeo a documentos**: PENDIENTE - cómo se mapea el AST a documentos existentes

### Generación de Grafo de Relaciones

- **Nodos del grafo**: PENDIENTE - qué representa cada nodo (archivos, funciones, clases, documentos)
- **Aristas del grafo**: PENDIENTE - qué relaciones se representan (imports, llamadas, referencias)
- **Almacenamiento del grafo**: PENDIENTE - formato de almacenamiento (base de datos, archivo)
- **Actualización del grafo**: PENDIENTE - cuándo y cómo se actualiza el grafo

### Integración con Pipeline de 5 Fases

- **Fase de detección**: PENDIENTE - cómo se usa el grafo para detectar gaps
- **Fase de resolución**: PENDIENTE - cómo se usa el grafo para responder gaps
- **Fase de aplicación**: PENDIENTE - cómo se aplican cambios al código si aplica

---

## Referencias

- **[../../estrategia/estrategia/technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md)**: Roadmap técnico, Hito 7
- **[architecture-overview.md](architecture-overview.md)**: Decisiones de diseño arquitectónico
- **[../arquitectura/technology-stack.md](../arquitectura/technology-stack.md)**: Stack tecnológico

---

## Información Pendiente de Definir

Las siguientes secciones están marcadas como PENDIENTE y se definirán en fase de implementación:

- Método de autenticación con Git
- Estrategia de clonado y actualización de repositorios
- Lista de lenguajes soportados por Treesitter
- Estructuras AST a extraer por lenguaje
- Estrategia de mapeo AST → documentos
- Definición de nodos y aristas del grafo
- Formato de almacenamiento del grafo
- Estrategia de actualización del grafo
- Integración específica con cada fase del pipeline
