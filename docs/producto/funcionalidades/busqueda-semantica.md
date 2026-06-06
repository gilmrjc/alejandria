---
id: FEAT-007
type: Feature Document
rating: 9
rating-phase: document-editing
related:
  - target: REQ-010
    relationship_type: implements
    reason: Implementa los requisitos de búsqueda semántica
  - target: PRD-001
    relationship_type: implements
    reason: Implementa el PRD de Hito 1 con búsqueda semántica
  - target: ARC-003
    relationship_type: implements
    reason: Implementa el Technology Stack con Qdrant para búsqueda vectorial
  - target: TS-001
    relationship_type: references
    reason: Referencia el technical-specs-busqueda-semantica para especificación técnica detallada
  - target: ADR-003
    relationship_type: implements
    reason: Implementa la decisión de Qdrant como base de datos vectorial
  - target: STR-003
    relationship_type: references
    reason: Referencia el technical roadmap para mapeo de features a hitos
  - target: ARC-033
    relationship_type: references
    reason: Referencia la implementación detallada de búsqueda semántica
---

# Búsqueda Semántica

## Descripción
Sistema de búsqueda vectorial que permite encontrar información por intención y contexto, no solo por coincidencia exacta.

## Propósito
Facilitar el encuentro rápido de información relevante en proyectos con grandes volúmenes de documentación.

## User Personas
- Todos los usuarios

## Cómo Funciona
Las respuestas de preguntas se transforman en vectores utilizando el modelo BGE-M3 (BAAI General Embedding) con 1024 dimensiones y cosine similarity como métrica de distancia. Este modelo fue seleccionado por su balance entre performance, tamaño y calidad de embeddings para texto técnico. Los vectores se almacenan en Qdrant con índices HNSW configurados por defecto. Qdrant se seleccionó por su rendimiento (latencias p50 <5ms hasta 1M vectores), facilidad de gestión en ambientes locales (despliegue simple con Docker, API REST y gRPC), y ser open-source sin costos para desarrollo local. Alternativas evaluadas: Pinecone (gestionado/costoso), Weaviate (búsqueda híbrida nativa), pgvector (requiere Postgres dedicado), Milvus (orientado a enterprise).

El texto se divide en chunks de máximo 256 tokens con superposición de 25 tokens (10%) para preservar contexto. El algoritmo divide por párrafos, agrupa hasta alcanzar ~256 tokens, mantiene superposición entre chunks adyacentes y preserva estructura de secciones en metadata.

Cada vector almacena metadata obligatoria (document_id, question_id, author, created_at, updated_at, document_type, module) y opcional (tags, priority, language). Los filtros permiten búsquedas por autor, rango de fechas, tipo de documento y módulo/componente, combinando con lógica AND entre tipos diferentes y OR dentro del mismo tipo.

Cuando los documentos originales cambian, los vectores se actualizan mediante re-indexación incremental. El proceso es transaccional: se eliminan vectores existentes, se aplica chunking al contenido actualizado, se generan embeddings nuevos, se insertan vectores y se actualiza el log de sincronización. Se verifica que el vector correspondiente exista antes de cada búsqueda.

La búsqueda semántica se implementa progresivamente a través de hitos: Hito 1 configura Qdrant (base de datos vectorial), Hito 2 implementa el motor de búsqueda semántica, y Hito 4 añade transformación a vectores para detección y agrupación. La tool MCP `search_similar_documents` está disponible para todos los agentes del pipeline y su uso es determinado por cada agente según necesidad específica durante el procesamiento.

Los usuarios pueden buscar en lenguaje natural (ej: "cómo configuro X") y el sistema utiliza la base de datos vectorial para encontrar documentos relevantes aunque no contengan exactamente los términos de búsqueda.

## Casos de Uso
Los usuarios pueden buscar por intención en lenguaje natural, permitiendo encontrar información sin conocer términos exactos. También es posible buscar por contexto o analogía, aplicando filtros específicos como autor, fecha, tipo de documento y módulo para refinar los resultados.

## Componentes y Referencias
El sistema se compone de la base de datos vectorial Qdrant, la transformación de texto a vectores mediante el modelo BGE-M3, y el motor de búsqueda semántica que permite consultas en lenguaje natural con filtros por metadata.

## Requisitos de Performance
Los requisitos de performance para la búsqueda semántica están definidos para garantizar una experiencia fluida. La transformación de texto a vectores debe completarse en 500ms por chunk de 512 tokens con throughput de 100 chunks/segundo. La búsqueda semántica tiene un tiempo máximo de 200ms (p95) con latencia objetivo de 100ms (p50) y throughput de 500 queries/segundo. La aplicación de filtros adiciona 50ms y la carga de top 20 resultados debe completarse en 100ms.

## Métricas de Éxito
La calidad de la búsqueda semántica se mide mediante métricas de precisión: Precision@10 ≥ 0.85, Recall@20 ≥ 0.90 y MRR (Mean Reciprocal Rank) ≥ 0.75. La estrategia de mejora incluye análisis de click-through rate, feedback explícito (thumbs up/down) y re-ranking basado en feedback histórico. El umbral de similitud mínimo es 0.7, configurable por organización.

## Experiencia de Usuario
La interfaz de búsqueda semántica presenta una caja de texto de buscador global en la parte superior de la barra de navegación. Los resultados se muestran en estilo Google con el título del documento (clickable, lleva al documento completo) y el chunk de contenido que generó el resultado (limitado a 200 palabras). No se muestra el score de similitud numérico. La búsqueda opera en tiempo real mientras el usuario escribe con debounce para optimizar performance.

## Decisiones Relacionadas
Ver ADR-003 para la justificación técnica de la elección de Qdrant como base de datos vectorial.
