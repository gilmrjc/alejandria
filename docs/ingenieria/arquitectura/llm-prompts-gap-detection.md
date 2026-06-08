---
id: ARC-014
type: LLM Prompt Specification
rating: 9.0
rating-phase: document-editing
related:
  - target: EPC-004
    relationship_type: implements
    reason: Implementa la especificación de prompts para gap_detection en Épica 4
  - target: ARC-036
    relationship_type: references
    reason: Referencia MCP tools specification para contexto de tools disponibles
  - target: ARC-013
    relationship_type: references
    reason: Referencia llm-evals-guide para estrategia de evaluación
---

# LLM Prompts Specification - Gap Detection

Este documento define la especificación detallada de prompts de LLM para detección de gaps en documentos. Para la arquitectura general de jobs, ver [job-implementation-guide.md](./job-implementation-guide.md). Para evals de LLM, ver [llm-evals-guide.md](./llm-evals-guide.md).

---

## 1. Prompt Base para Gap Detection

### 1.1 Contexto y Rol

```
You are an expert technical documentation analyst specializing in identifying gaps, inconsistencies, and missing information in technical documentation. Your role is to analyze documents and identify areas where information is incomplete, unclear, or contradictory.

You have access to the following MCP tools:
- read_document: Read document content and metadata
- list_gaps: List existing gaps for a document
- create_gap: Create a new gap with metadata

Your analysis should focus on:
1. Missing critical information (how, why, implementation details)
2. Inconsistencies between sections
3. Ambiguous statements that need clarification
4. Missing context or prerequisites
5. Unclear technical specifications
```

### 1.2 Variables de Contexto

El prompt debe incluir las siguientes variables dinámicas:

```python
context = {
    "document_title": str,
    "document_content": str,
    "document_type": str,  # technical-brief, architecture, requirements, etc.
    "existing_gaps": List[Dict],  # Gaps ya identificados para evitar duplicados
    "focus_areas": List[str],  # Áreas específicas a analizar (opcional)
    "role_affected": str,  # Rol afectado por el gap (developer, architect, product, etc.)
}
```

### 1.3 Prompt Template

```
Analyze the following document for gaps, inconsistencies, and missing information.

## Document Information
- Title: {document_title}
- Type: {document_type}
- Role affected: {role_affected}

## Document Content
{document_content}

## Existing Gaps (avoid duplicates)
{existing_gaps_summary}

## Analysis Instructions
1. Identify gaps where critical information is missing (how, why, implementation details)
2. Look for inconsistencies between different sections
3. Find ambiguous statements that need clarification
4. Check for missing context or prerequisites
5. Identify unclear technical specifications

For each gap identified, provide:
- Question: A clear, specific question about the missing information
- Context missing: Description of what information is missing
- Type: Type of gap (implementation, clarification, consistency, prerequisite)
- Severity: Impact level (low, medium, high, critical)
- Role affected: Who needs this information (developer, architect, product, etc.)

## Output Format
Return a JSON array of gaps with the following structure:
[
  {
    "question": "string",
    "context_missing": "string",
    "type": "implementation|clarification|consistency|prerequisite",
    "severity": "low|medium|high|critical",
    "role_affected": "developer|architect|product|stakeholder|other"
  }
]
```

---

## 2. Estrategia de Few-Shot Learning

### 2.1 Ejemplos de Input/Output

**Example 1: Technical Document**

**Input:**
```
Document: "API Authentication System"
Content: "The system uses JWT tokens for authentication. Tokens expire after 8 hours."
```

**Output:**
```json
[
  {
    "question": "How are JWT tokens generated and validated?",
    "context_missing": "Missing information about token generation algorithm, secret key management, and validation process",
    "type": "implementation",
    "severity": "high",
    "role_affected": "developer"
  },
  {
    "question": "What happens when a token expires? Is there a refresh mechanism?",
    "context_missing": "Missing information about token refresh flow and user experience on expiration",
    "type": "implementation",
    "severity": "medium",
    "role_affected": "developer"
  }
]
```

**Example 2: Architecture Document**

**Input:**
```
Document: "Microservices Architecture"
Content: "Services communicate via REST APIs. Database is PostgreSQL."
```

**Output:**
```json
[
  {
    "question": "How is service discovery implemented?",
    "context_missing": "Missing information about how services find and communicate with each other",
    "type": "implementation",
    "severity": "high",
    "role_affected": "architect"
  },
  {
    "question": "What is the data consistency strategy across services?",
    "context_missing": "Missing information about transaction management and data synchronization",
    "type": "consistency",
    "severity": "high",
    "role_affected": "architect"
  }
]
```

### 2.2 Negative Examples

**Example of BAD gap detection:**
```json
[
  {
    "question": "What is the color of the UI buttons?",
    "context_missing": "UI color scheme not specified",
    "type": "clarification",
    "severity": "low",
    "role_affected": "designer"
  }
]
```
**Why it's bad:** Too trivial, not critical for technical implementation.

**Example of GOOD gap detection:**
```json
[
  {
    "question": "How are API rate limits enforced and what are the limits?",
    "context_missing": "Missing information about rate limiting strategy and specific limits",
    "type": "implementation",
    "severity": "medium",
    "role_affected": "developer"
  }
]
```
**Why it's good:** Specific, actionable, critical for implementation.

---

## 3. Manejo de Edge Cases

### 3.1 Documentos Vacíos o Muy Cortos

**Strategy:** Si el documento tiene menos de 100 caracteres, retornar un gap específico:

```json
[
  {
    "question": "This document appears to be empty or incomplete. What content should be added?",
    "context_missing": "Document content is minimal or missing",
    "type": "prerequisite",
    "severity": "critical",
    "role_affected": "author"
  }
]
```

### 3.2 Documentos con Formato Incorrecto

**Strategy:** Si el documento no tiene estructura clara (headers, sections), identificar gap de estructura:

```json
[
  {
    "question": "This document lacks clear structure. What sections should be added?",
    "context_missing": "Document structure is unclear or missing standard sections",
    "type": "clarification",
    "severity": "medium",
    "role_affected": "author"
  }
]
```

### 3.3 Duplicación de Gaps Existentes

**Strategy:** Antes de crear un nuevo gap, verificar si ya existe un gap similar:

```python
def is_duplicate_gap(new_gap, existing_gaps):
    for existing in existing_gaps:
        similarity = calculate_similarity(new_gap["question"], existing["question"])
        if similarity > 0.8:  # 80% similarity threshold
            return True
    return False
```

---

## 4. Iteración y Mejora Basada en Evals

### 4.1 Métricas de Calidad

**Precision:** Porcentaje de gaps identificados que son válidos y útiles
```
precision = (valid_gaps / total_gaps_identified) * 100
```

**Recall:** Porcentaje de gaps reales que fueron identificados
```
recall = (gaps_identified / total_real_gaps) * 100
```

**F1 Score:** Balance entre precision y recall
```
f1 = 2 * (precision * recall) / (precision + recall)
```

### 4.2 Dataset de Prueba

Crear un dataset de documentos con gaps pre-identificados manualmente:

```
test_documents/
  ├── technical_brief_1.md (with 5 known gaps)
  ├── architecture_doc_1.md (with 3 known gaps)
  ├── requirements_doc_1.md (with 4 known gaps)
  └── ...
```

### 4.3 Estrategia de Iteración

1. **Baseline:** Ejecutar prompt actual en dataset de prueba
2. **Evaluar:** Calcular precision, recall, F1 score
3. **Analizar errores:** Identificar tipos de gaps no detectados
4. **Ajustar prompt:** Agregar ejemplos few-shot para tipos de gaps faltantes
5. **Repetir:** Ejecutar nuevamente y comparar métricas

**Ejemplo de iteración:**

**Iteración 1:**
- Precision: 70%
- Recall: 60%
- F1: 0.65
- **Issue:** No detectando gaps de consistencia

**Iteración 2 (ajuste):** Agregar ejemplo few-shot de consistencia
- Precision: 75%
- Recall: 75%
- F1: 0.75
- **Improvement:** +15% en recall

---

## 5. Integración con Job de Celery

### 5.1 Flujo de Ejecución

```python
@celery_app.task(bind=True, name='gap_detection')
def gap_detection_task(self, document_id: str):
    # 1. Leer documento
    document = read_document(document_id)
    
    # 2. Leer gaps existentes
    existing_gaps = list_gaps(document_id, status='pending')
    
    # 3. Construir contexto
    context = {
        "document_title": document.title,
        "document_content": document.content,
        "document_type": document.metadata.get('type'),
        "existing_gaps": existing_gaps,
        "role_affected": "developer"  # Default, can be parameterized
    }
    
    # 4. Ejecutar prompt LLM
    gaps = execute_llm_prompt(context)
    
    # 5. Filtrar duplicados
    new_gaps = filter_duplicates(gaps, existing_gaps)
    
    # 6. Crear gaps en base de datos
    for gap in new_gaps:
        create_gap(document_id, gap)
    
    return {"gaps_created": len(new_gaps)}
```

### 5.2 Manejo de Timeouts y Errores

```python
try:
    gaps = execute_llm_prompt(context, timeout=300)  # 5 minutos
except TimeoutError:
    logger.error(f"LLM timeout for document {document_id}")
    retry_task(self)  # Reintentar con backoff
except LLMError as e:
    logger.error(f"LLM error for document {document_id}: {e}")
    mark_document_as_failed(document_id)
```

---

## 6. Referencias

- [mcp-tools-specification.md](./mcp-tools-specification.md): MCP tools disponibles
- [llm-evals-guide.md](./llm-evals-guide.md): Guía de evaluación de LLM
- [job-implementation-guide.md](./job-implementation-guide.md): Guía de implementación de jobs
- [epica-04-deteccion-agrupacion.md](../tareas/epica-04-deteccion-agrupacion.md): Épica 4 - T-044

---

*Fin del documento de especificación de prompts LLM para gap detection.*
