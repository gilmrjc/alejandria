---
id: EPC-004-CHK
type: Validation Checklist
rating: 9.0
rating-phase: document-editing
related:
  - target: EPC-004
    relationship_type: validates
    reason: Checklist de validación para Épica 4
  - target: ARC-015
    relationship_type: references
    reason: Referencia celery-implementation-guide para validación de Celery
  - target: ARC-014
    relationship_type: references
    reason: Referencia llm-prompts-gap-detection para validación de prompts
---

# Checklist de Validación - Épica 4: Detección y Agrupación

Este documento proporciona un checklist completo para validar la implementación de Épica 4. Para la especificación de la épica, ver [epica-04-deteccion-agrupacion.md](./epica-04-deteccion-agrupacion.md).

---

## 1. Validación de T-040: Configurar Celery para Jobs

### 1.1 Configuración de Celery App
- [ ] `backend/jobs/celery_app.py` existe y está configurado
- [ ] Broker configurado con Redis URL correcta
- [ ] Backend configurado con Redis URL correcta
- [ ] Include apunta a `["jobs.tasks"]`
- [ ] Task serializer configurado como "json"
- [ ] Timezone configurado como "UTC"
- [ ] Task time limit configurado (30 minutos)
- [ ] Task soft time limit configurado (25 minutos)
- [ ] Retry strategy configurada (task_max_retries=5)
- [ ] Task default retry delay configurado (60 segundos)

### 1.2 Configuración de Workers
- [ ] Servicio `celery-worker` agregado a `docker-compose.yml`
- [ ] Worker command configurado: `celery -A jobs.celery_app worker --loglevel=info`
- [ ] Worker depende de servicios: redis, postgresql, qdrant
- [ ] Variables de entorno configuradas (REDIS_URL, DATABASE_URL, Qdrant_URL, OLLAMA_URL)
- [ ] Worker conecta a Redis exitosamente
- [ ] Worker registra tasks disponibles

### 1.3 Validación de Comandos
```bash
# Verificar configuración de Celery
docker-compose exec celery-worker celery -A jobs.celery_app inspect ping

# Verificar tasks registrados
docker-compose exec celery-worker celery -A jobs.celery_app inspect registered

# Verificar workers activos
docker-compose exec celery-worker celery -A jobs.celery_app inspect active
```

---

## 2. Validación de T-041: Implementar Job gap_detection

### 2.1 Implementación del Task
- [ ] `backend/jobs/tasks/gap_detection.py` existe
- [ ] Task decorado con `@celery_app.task(bind=True, name='gap_detection')`
- [ ] Task acepta `document_id` como parámetro
- [ ] Task usa DocumentService para leer documento
- [ ] Task usa GapService para leer gaps existentes
- [ ] Task usa OllamaClient para detectar gaps
- [ ] Task filtra gaps duplicados
- [ ] Task crea gaps nuevos en base de datos
- [ ] Task retorna dict con `gaps_created`

### 2.2 Manejo de Errores
- [ ] Task maneja DocumentNotFoundError
- [ ] Task maneja LLM errors con retry
- [ ] Task usa backoff exponencial para retries
- [ ] Task loguea errores correctamente
- [ ] Task marca documento como failed si falla después de max_retries

### 2.3 Idempotencia
- [ ] Task usa celery_once para locks distribuidos
- [ ] Task filtra gaps duplicados basado en similitud
- [ ] Task no crea gaps duplicados en ejecuciones múltiples
- [ ] Lock expira después de tiempo razonable

### 2.4 Validación de Comandos
```bash
# Ejecutar task manualmente
docker-compose exec celery-worker celery -A jobs.celery_app call gap_detection --args='["doc-1"]'

# Verificar resultado en logs
docker-compose logs celery-worker | grep "gap_detection"
```

---

## 3. Validación de T-042: Implementar Job vector_sync

### 3.1 Implementación del Task
- [ ] `backend/jobs/tasks/vector_sync.py` existe
- [ ] Task decorado con `@celery_app.task(bind=True, name='vector_sync')`
- [ ] Task acepta `document_id` como parámetro
- [ ] Task usa DocumentService para leer documento
- [ ] Task implementa chunking con max_tokens=512, overlap=50
- [ ] Task usa OllamaClient para generar embeddings
- [ ] Task usa QdrantService para upsert vectors
- [ ] Task retorna dict con `vectors_synced`

### 3.2 Estrategia de Chunking
- [ ] Chunking divide por párrafos
- [ ] Chunking agrupa párrafos hasta ~512 tokens
- [ ] Chunking mantiene 50 tokens de superposición
- [ ] Chunking preserva estructura de secciones en metadata
- [ ] Chunking maneja párrafos largos correctamente

### 3.3 Validación de Comandos
```bash
# Ejecutar task manualmente
docker-compose exec celery-worker celery -A jobs.celery_app call vector_sync --args='["doc-1"]'

# Verificar vectores en Qdrant
curl http://localhost:6333/collections/documents/points/count
```

---

## 4. Validación de T-043: Implementar Job question_generation

### 4.1 Implementación del Task
- [ ] `backend/jobs/tasks/question_generation.py` existe
- [ ] Task decorado con `@celery_app.task(bind=True, name='question_generation')`
- [ ] Task acepta `gap_id` y `answer` como parámetros
- [ ] Task usa GapService para leer gap
- [ ] Task usa OllamaClient para generar embedding de respuesta
- [ ] Task usa QdrantService para upsert vector de respuesta
- [ ] Task retorna dict con `answer_vectorized`

### 4.2 Validación de Comandos
```bash
# Ejecutar task manualmente
docker-compose exec celery-worker celery -A jobs.celery_app call question_generation --args='["gap-1", "Test answer"]'
```

---

## 5. Validación de T-044: Implementar Agente LLM para análisis de documentos

### 5.1 Implementación del Agente
- [ ] `shared/llm/ollama_client.py` existe o se extiende
- [ ] Método `detect_gaps` implementado
- [ ] Método acepta document_content, document_title, existing_gaps
- [ ] Método usa prompt definido en llm-prompts-gap-detection.md
- [ ] Método retorna lista de gaps con metadata completa
- [ ] Método maneja timeouts de Ollama
- [ ] Método maneja errores de conexión

### 5.2 Validación de Prompts
- [ ] Prompt base sigue especificación en llm-prompts-gap-detection.md
- [ ] Prompt incluye contexto y rol del LLM
- [ ] Prompt incluye variables dinámicas (document_title, document_content, etc.)
- [ ] Prompt define formato de salida JSON
- [ ] Prompt incluye ejemplos few-shot
- [ ] Prompt maneja edge cases (documentos vacíos, formato incorrecto)

### 5.3 Validación de Comandos
```bash
# Testear agente LLM manualmente
python -c "
from shared.llm.ollama_client import OllamaClient
client = OllamaClient()
gaps = client.detect_gaps('Test content', 'Test Title', [])
print(gaps)
"
```

---

## 6. Validación de T-045: Implementar Sistema de metadata de gaps

### 6.1 Schema de Base de Datos
- [ ] Tabla `gaps` existe con campos correctos
- [ ] Tabla `gap_tags` existe para tags
- [ ] Índices creados en document_id, status, severity, type
- [ ] Constraints CHECK implementados para enums
- [ ] Foreign key a documents implementado

### 6.2 API Endpoints
- [ ] GET /api/v1/gaps implementado
- [ ] GET /api/v1/gaps/{gap_id} implementado
- [ ] POST /api/v1/gaps implementado
- [ ] PATCH /api/v1/gaps/{gap_id} implementado
- [ ] DELETE /api/v1/gaps/{gap_id} implementado
- [ ] Filtros por document_id, status, severity, type funcionan
- [ ] Paginación implementada

### 6.3 Pydantic Schemas
- [ ] GapCreate schema implementado
- [ ] GapResponse schema implementado
- [ ] Validación de enums (GapType, GapSeverity, GapStatus, GapRole)
- [ ] Validación de longitud de campos

### 6.4 Validación de Comandos
```bash
# Testear endpoint de gaps
curl http://localhost:8000/api/v1/gaps

# Crear gap manualmente
curl -X POST http://localhost:8000/api/v1/gaps \
  -H "Content-Type: application/json" \
  -d '{"document_id": "doc-1", "question": "Test", "context_missing": "Test", "type": "implementation", "severity": "high", "role_affected": "developer"}'
```

---

## 7. Validación de T-046: Implementar Sistema de agrupación por tema

### 7.1 Agrupación por Tags
- [ ] Gaps pueden agruparse por tema usando tags
- [ ] Tags de tema, subtema, prioridad implementados
- [ ] Agrupación por similitud semántica usando Qdrant funciona
- [ ] Metadata de tags se muestra en respuestas

### 7.2 Validación de Comandos
```bash
# Testear agrupación por tema
curl "http://localhost:8000/api/v1/gaps/grouped?group_by=theme"
```

---

## 8. Validación de T-047: Implementar API Endpoints para Dashboard de Gaps

### 8.1 Dashboard Metrics
- [ ] GET /api/v1/gaps/dashboard implementado
- [ ] Endpoint retorna métricas agregadas
- [ ] Métricas por status implementadas
- [ ] Métricas por severidad implementadas
- [ ] Métricas por tipo implementadas
- [ ] Métricas por tema implementadas
- [ ] Métricas por rol afectado implementadas
- [ ] Resolution rate calculado correctamente
- [ ] Avg resolution time calculado correctamente

### 9.2 Filtros y Agrupación
- [ ] Filtros por tema, priority, status, type funcionan
- [ ] Agrupación por tema funciona
- [ ] Metadata de tags incluida en respuestas
- [ ] Paginación implementada

### 9.3 Validación de Comandos
```bash
# Testear dashboard metrics
curl http://localhost:8000/api/v1/gaps/dashboard

# Testear con filtros
curl "http://localhost:8000/api/v1/gaps/dashboard?theme=authentication&status=pending"
```

---

## 9. Validación de Testing

### 9.1 Tests Unitarios
- [ ] Tests para gap_detection task implementados
- [ ] Tests para vector_sync task implementados
- [ ] Tests para question_generation task implementados
- [ ] Tests para chunking implementados
- [ ] Tests para OllamaClient implementados
- [ ] Mocks de dependencias externas implementados

### 92 Tests de Idempotencia
- [ ] Tests de locks distribuidos implementados
- [ ] Tests de filtrado de duplicados implementados
- [ ] Tests de ejecuciones múltiples implementados

### 10.3 Tests de Retry Strategy
- [ ] Tests de retry on failure implementados
- [ ] Tests de backoff exponencial implementados
- [ ] Tests de max_retries implementados

### 10 Coverage
- [ ] Coverage de jobs tasks > 80%
- [ ] Coverage de services > 75%
- [ ] Coverage de LLM client > 70%
- [ ] Coverage overall > 70%

### 100.5 Validación de Comandos
```bash
# Ejecutar tests
pytest backend/tests/test_jobs/ -v

# Ejecutar tests con coverage
pytest backend/tests/test_jobs/ --cov=jobs --cov-report=html

# Ver reporte de coverage
open htmlcov/index.html
```

---

## 11. Validación de Integración

### 11.1 Integración con Redis
- [ ] Celery workers conectan a Redis
- [ ] Tasks se encolan correctamente
- [ ] Results se almacenan en Redis
- [ ] Locks distribuidos funcionan

### 11.2 Integración con PostgreSQL
- [ ] Tasks leen/escriben en base de datos
- [ ] Transacciones manejadas correctamente
- [ ] Connection pooling funciona
- [ ] Migrations aplicadas correctamente

### 10.3 Integración con Qdrant
- [ ] Vector sync upserta vectores correctamente
- [ ] Search por similitud funciona
- [ ] Collections creadas correctamente
- [ ] Metadata de vectores preservada

### 10.4 Integración con Ollama
- [ ] OllamaClient conecta a Ollama
- [ ] Embeddings generados correctamente
- [ ] Gap detection funciona con LLM
- [ ] Timeouts manejados correctamente

### 10.5 Validación de Comandos
```bash
# Verificar integración end-to-end
# 1. Crear documento
curl -X POST http://localhost:8000/api/v1/documents -H "Content-Type: application/json" -d '{"title": "Test", "content": "Test content"}'

# 2. Ejecutar gap_detection
docker-compose exec celery-worker celery -A jobs.celery_app call gap_detection --args='["doc-1"]'

# 3. Verificar gaps creados
curl http://localhost:8000/api/v1/gaps?document_id=doc-1

# 4. Ejecutar vector_sync
docker-compose exec celery-worker celery -A jobs.celery_app call vector_sync --args='["doc-1"]'

# 5. Verificar vectores en Qdrant
curl http://localhost:6333/collections/documents/points/count
```

---

## 12. Validación de Documentación

### 12.1 Documentación Técnica
- [ ] llm-prompts-gap-detection.md creado y completo
- [ ] celery-implementation-guide.md creado y completo
- [ ] api-specification-gaps-metadata.md creado y completo
- [ ] vector-chunking-strategy.md creado y completo
- [ ] celery-testing-guide.md creado y completo
- [ ] epica-04-checklist-validacion.md creado y completo

### 12.2 Actualización de Documentos Existentes
- [ ] epica-01-infraestructura-base.md actualizado a COMPLETADO
- [ ] epica-003-a-infraestructura-frontend-base.md actualizado a EN PROGRESO
- [ ] epica-04-deteccion-agrupacion.md actualizado con T-047 y T-048
- [ ] Referencias cruzadas actualizadas

---

## 13. Sign-off Criteria

La Épica 4 se considerará completada cuando se cumplan los siguientes criterios:

### 12.1 Criterios Funcionales
- [ ] Todos los tasks de Celery (T-040 a T-043) implementados y funcionando
- [ ] Agente LLM (T-044) detecta gaps correctamente
- [ ] Sistema de metadata de gaps (T-045) operativo
- [ ] Sistema de agrupación por tema (T-046) funcional
- [ ] API endpoints de dashboard (T-047) funcionando

### 12.2 Criterios de Calidad
- [ ] Coverage de tests > 70%
- [ ] Todos los tests unitarios pasan
- [ ] Todos los tests de integración pasan
- [ ] Idempotencia validada
- [ ] Retry strategy validada

### 12.3 Criterios de Documentación
- [ ] Todos los documentos técnicos creados
- [ ] Documentación de estado actualizada
- [ ] Referencias cruzadas correctas
- [ ] Ejemplos de uso proporcionados

### 12.4 Criterios de Operación
- [ ] Workers de Celery levantan correctamente
- [ ] Tasks se ejecutan sin errores
- [ ] Integración con servicios externos funciona
- [ ] Logs estructurados implementados
- [ ] Monitoreo configurado (opcional: Flower)

---

## 13. Troubleshooting

### 14.1 Workers no procesan tasks
- [ ] Verificar que worker está conectado: `celery -A jobs.celery_app inspect active`
- [ ] Verificar que tasks están registrados: `celery -A jobs.celery_app inspect registered`
- [ ] Revisar logs del worker: `docker-compose logs celery-worker`

### 13.2 Tasks fallan con timeout
- [ ] Aumentar task_soft_time_limit en celery_app.py
- [ ] Optimizar task para ser más rápido
- [ ] Dividir tasks largos en sub-tasks

### 14.3 LLM no responde
- [ ] Verificar que Ollama está accesible: `curl http://localhost:11434/api/version`
- [ ] Verificar que modelo Qwen está instalado: `ollama list`
- [ ] Aumentar timeout de OllamaClient

### 14.4 Qdrant no sincroniza vectores
- [ ] Verificar que Qdrant está accesible: `curl http://localhost:6333/`
- [ ] Verificar que collection existe: `curl http://localhost:6333/collections/documents`
- [ ] Revisar logs de vector_sync task

---

## 14. Referencias

- [epica-04-deteccion-agrupacion.md](./epica-04-deteccion-agrupacion.md): Especificación de Épica 4 (T-040 a T-047)
- [llm-prompts-gap-detection.md](../arquitectura/llm-prompts-gap-detection.md): Prompts de LLM
- [celery-implementation-guide.md](../arquitectura/celery-implementation-guide.md): Guía de Celery
- [api-specification-gaps-metadata.md](../arquitectura/api-specification-gaps-metadata.md): Especificación de API
- [vector-chunking-strategy.md](../arquitectura/vector-chunking-strategy.md): Estrategia de chunking
- [celery-testing-guide.md](../arquitectura/celery-testing-guide.md): Guía de testing

---

*Fin del checklist de validación para Épica 4.*
