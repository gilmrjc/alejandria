---
id: T-008
type: Task
rating: 9.0
rating-phase: document-editing
related:
  - target: T-002
    relationship_type: depends_on
    reason: Depende de la configuración de Docker Compose para verificar Qdrant
---

# T-008: Verificar configuración de Qdrant

**Tipo**: Task
**Prioridad**: Alta
**Estimación**: 2 horas
**Dependencias**: T-002

## Descripción

Verificar que Qdrant está configurado correctamente para búsqueda semántica según ADR-003. Los comandos de verificación siguen la API REST de Qdrant. Las dimensiones de vectores de prueba son 1024 (BGE-M3) con cosine similarity, según ADR-003.

## Criterios de Aceptación

- [ ] Contenedor Qdrant levanta sin errores
- [ ] API HTTP responde en puerto 6333
- [ ] API gRPC responde en puerto 6334
- [ ] Colección de prueba puede crearse vía API
- [ ] Embeddings pueden almacenarse y recuperarse
- [ ] Búsqueda semántica funciona con vectores de prueba
- [ ] Datos persisten después de restart de contenedor
- [ ] Health check de Docker Compose funciona correctamente

## Comandos de Verificación

```bash
# Verificar que Qdrant está corriendo
curl http://localhost:6333/

# Crear colección de prueba
curl -X PUT http://localhost:6333/collections/test_collection \
  -H 'Content-Type: application/json' \
  -d '{
    "vectors": {
      "size": 1024,
      "distance": "Cosine"
    }
  }'

# Insertar vector de prueba
curl -X PUT http://localhost:6333/collections/test_collection/points \
  -H 'Content-Type: application/json' \
  -d '{
    "points": [
      {
        "id": 1,
        "vector": [0.1, 0.2, 0.3, ...],
        "payload": {"text": "test"}
      }
    ]
  }'
```

## Criterios de Éxito

- Búsqueda semántica funciona con vectores de prueba
- Datos persisten después de restart de contenedor
- API HTTP y gRPC responden correctamente
- Colección de prueba puede crearse y eliminarse sin errores

## Referencias

- [TRD - Hito 1](../propuestas/trd-milestone-1-infrastructure.md): RF-004: Qdrant Setup

---

## Troubleshooting

### Contenedor Qdrant no levanta

Si el contenedor Qdrant no inicia:

1. Verificar que el contenedor esté corriendo:

   ```bash
   docker-compose ps qdrant
   ```

2. Si el contenedor no está corriendo, levantarlo:

   ```bash
   docker-compose up -d qdrant
   ```

3. Revisar logs de Qdrant para identificar errores:

   ```bash
   docker-compose logs qdrant
   ```

### API HTTP no responde

Si `curl http://localhost:6333/` no responde:

1. Verificar que el puerto 6333 no esté en uso por otro proceso:

   ```bash
   lsof -i :6333
   ```

2. Si hay conflicto de puertos, cambiar el puerto en docker-compose.yml:

   ```yaml
   qdrant:
     ports:
       - "6334:6333"  # Usar puerto 6334 en host en lugar de 6333
   ```

3. Reiniciar el contenedor Qdrant:

   ```bash
   docker-compose restart qdrant
   ```

### Colección no se puede crear

Si la creación de colección falla:

1. Verificar que Qdrant esté healthy:

   ```bash
   curl http://localhost:6333/health
   ```

2. Verificar que el JSON de la colección sea válido:

   ```bash
   # Validar JSON antes de enviar
   echo '{"vectors": {"size": 1024, "distance": "Cosine"}}' | jq .
   ```

3. Revisar logs de Qdrant para errores de validación:

   ```bash
   docker-compose logs qdrant | grep -i error
   ```

### Datos no persisten después de restart

Si las colecciones se pierden después de reiniciar el contenedor:

1. Verificar que el volume Docker esté montado correctamente:

   ```bash
   docker volume ls | grep qdrant
   ```

2. Verificar que el volume tenga datos:

   ```bash
   docker volume inspect qdrant_qdrant_data
   ```

3. Si el volume está vacío, verificar que la configuración de persistencia en docker-compose.yml sea correcta:

   ```yaml
   qdrant:
     volumes:
       - qdrant_data:/qdrant/storage
   ```

### Latencia alta en búsqueda semántica

Si las búsquedas son lentas:

1. Verificar recursos del sistema (CPU, RAM) con `docker stats`

2. Cerrar otras aplicaciones que puedan estar consumiendo recursos

3. Verificar que no haya contenedores pesados corriendo simultáneamente

4. Para desarrollo local, latencias hasta 100ms son aceptables para búsquedas semánticas

### Búsqueda semántica no funciona

Si la búsqueda no retorna resultados esperados:

1. Verificar que los vectores tengan el número correcto de dimensiones (1024 para BGE-M3):

   ```bash
   # Verificar información de la colección
   curl http://localhost:6333/collections/test_collection
   ```

2. Verificar que el tipo de distancia sea correcto (Cosine):

   ```bash
   # La respuesta debe mostrar "distance": "Cosine"
   curl http://localhost:6333/collections/test_collection
   ```

3. Verificar que los vectores estén normalizados (opcional pero recomendado para cosine similarity)

**Nota:** Para esta fase inicial del proyecto, el troubleshooting manual es suficiente. Herramientas automatizadas de monitoreo y alertas pueden agregarse más adelante si se requiere para producción.
