---
id: T-007
type: Task
rating: 9
rating-phase: document-editing
related:
  - target: T-002
    relationship_type: depends_on
    reason: Depende de la configuración de Docker Compose para verificar Redis
  - target: ADR-003
    relationship_type: implements
    reason: Implementa la verificación de configuración de Redis según ADR-003
---

# T-007: Verificar configuración de Redis

**Tipo**: Task
**Prioridad**: Alta
**Estimación**: 1 hora
**Dependencias**: T-002

## Descripción

Verificar que Redis está configurado correctamente como broker y cache según ADR-003. Redis ofrece operaciones en memoria con baja latencia (<10ms) para cache del sistema.

**Contexto de AOF (Append Only File):** AOF es un mecanismo de persistencia que registra cada operación de escritura en un archivo log, permitiendo recuperación de datos después de un crash. Esto es crítico para Redis como broker de Celery y cache del sistema. Según ADR-003, Redis 7.4.9-alpine se configura con AOF habilitado para durabilidad de datos.

## Criterios de Aceptación

- [ ] Contenedor Redis levanta sin errores
- [ ] Comando `redis-cli ping` responde `PONG`
- [ ] AOF persistencia habilitada (verificar en redis.conf)
- [ ] Datos persisten después de restart de contenedor
- [ ] Performance de Redis aceptable (<10ms para commands simples)
- [ ] Health check de Docker Compose funciona correctamente

## Comandos de Verificación

```bash
# Verificar que Redis está corriendo
docker-compose exec redis redis-cli ping

# Verificar configuración de AOF
docker-compose exec redis redis-cli CONFIG GET appendonly

# Verificar persistencia
docker-compose exec redis redis-cli SET test_key "test_value"
docker-compose restart redis
docker-compose exec redis redis-cli GET test_key

# Medir latencia de Redis (ejecutar por ~30 segundos para obtener muestra representativa)
docker-compose exec redis redis-cli --latency
```

## Criterios de Éxito

- Redis responde con latencia <10ms para commands simples
- Datos persisten después de restart de contenedor
- AOF persistencia habilitada y funcionando
- Health check de Docker Compose funciona correctamente

## Referencias

- [TRD - Hito 1](../propuestas/trd-milestone-1-infrastructure.md): RF-003: Redis Setup
- [ADR-003](../decisiones/adr-003-local-infrastructure-docker-compose.md): Local Infrastructure with Docker Compose

---

## Troubleshooting

### Comandos de verificación fallan

Si `redis-cli ping` no responde:

1. Verificar que el contenedor esté corriendo:

   ```bash
   docker-compose ps redis
   ```

2. Si el contenedor no está corriendo, levantarlo:

   ```bash
   docker-compose up -d redis
   ```

3. Revisar logs de Redis para identificar errores:

   ```bash
   docker-compose logs redis
   ```

### AOF no está habilitado

Si `CONFIG GET appendonly` retorna `no` en lugar de `yes`:

1. Verificar que el comando `redis-server --appendonly yes` esté configurado en docker-compose.yml (línea 102 de T-002)

2. Reiniciar el contenedor Redis:

   ```bash
   docker-compose restart redis
   ```

3. Verificar nuevamente la configuración

### Datos no persisten después de restart

Si `GET test_key` retorna `(nil)` después del restart:

1. Verificar que el volume Docker esté montado correctamente:

   ```bash
   docker volume ls | grep redis
   ```

2. Verificar que AOF esté habilitado (ver troubleshooting anterior)

3. Revisar logs de Redis para errores de escritura:

   ```bash
   docker-compose logs redis | grep -i error
   ```

### Latencia > 10ms

Si `redis-cli --latency` muestra latencias consistentemente > 10ms:

1. Verificar recursos del sistema (CPU, RAM) con `docker stats`
2. Cerrar otras aplicaciones que puedan estar consumiendo recursos
3. Verificar que no haya contenedores pesados corriendo simultáneamente
4. Si el problema persiste, puede ser normal en máquinas con recursos limitados; para desarrollo local, latencias hasta 20ms son aceptables
