---
id: T-012
type: Task
rating: 9.0
rating-phase: document-editing
related:
  - target: T-011
    relationship_type: depends_on
    reason: Depende del README con instrucciones para crear script automatizado
  - target: TRD-001
    relationship_type: implements
    reason: Implementa el requisito RF-008 de documentación
---

# T-012: Crear script de setup automatizado

**Tipo**: Task
**Prioridad**: Baja
**Estimación**: 2 horas
**Dependencias**: T-011

## Descripción

Crear script `scripts/dev-setup.sh` que automatiza el setup inicial para nuevos desarrolladores según ADR-003.

La estimación de 2 horas es razonable para implementar script automatizado con verificaciones, manejo de errores y output claro. Variables sensibles: POSTGRES_PASSWORD. Output claro: mensajes de progreso con timestamps y colores. Manejo de errores gracefully: mensajes de error específicos con sugerencias de solución, exit codes apropiados. Script debe ser idempotente según ADR-003.

## Criterios de Aceptación

- [ ] Script `scripts/dev-setup.sh` creado
- [ ] Script verifica que Docker Desktop esté instalado
- [ ] Script verifica que Git esté instalado
- [ ] Script crea archivo `.env` desde `.env.example`
- [ ] Script solicita configuración de variables sensibles (POSTGRES_PASSWORD)
- [ ] Script levanta stack con Docker Compose
- [ ] Script ejecuta health checks
- [ ] Script tiene output claro con progreso de setup (Mensajes de progreso con timestamps y colores)
- [ ] Script maneja errores gracefully (Mensajes de error específicos con sugerencias de solución, exit codes apropiados)
- [ ] Script es idempotente (puede ejecutarse múltiples veces)

## Criterios de Éxito

- Script es idempotente (puede ejecutarse múltiples veces sin efectos adversos)
- Setup completo en menos de 15 minutos (asumiendo Docker Desktop pre-instalado)
- Manejo de errores graceful con mensajes específicos y sugerencias
- Output claro con progreso visible (timestamps, colores)

### Validación de Idempotencia

Se usa validación manual por el desarrollador ejecutando el script múltiples veces.

**Proceso de validación:**

- El desarrollador ejecuta `./scripts/dev-setup.sh` múltiples veces (ej: 3 veces)
- Verificar que no hay errores en cada ejecución
- Verificar que no se crean recursos duplicados
- Verificar que el estado final es el mismo después de cada ejecución
- Ejecutar `./scripts/health-check.sh` al final para validar que todos los servicios están operativos

**Justificación:** Para desarrollo local, la validación manual es suficiente. Pruebas automatizadas que ejecuten el script múltiples veces pueden agregarse más adelante si se requiere para CI/CD.

## Referencias

- [TRD - Hito 1](../propuestas/trd-milestone-1-infrastructure.md): RF-008: Documentation

---

## Dependencias con Otras Tareas

Esta tarea (T-012) depende de:

- **T-011** (README): Requiere README con instrucciones para crear script automatizado que lo referencia
- **T-010** (Health check): Requiere health check funcional para verificar estado después de setup

Esta tarea (T-012) es prerequisito para:

- No aplica - Esta es la última tarea de la épica de infraestructura base

---

## Mantenimiento

### Estrategia de Actualización del Script

Se usa actualización del script según necesidad por el desarrollador.

**Cambios que requieren actualización del script:**

- Variables de entorno (nuevas variables, cambios de nombres)
- Servicios en docker-compose.yml (nuevos servicios, cambios de configuración)
- Comandos de setup (nuevos comandos, cambios en sintaxis)
- Procedimientos de verificación (nuevos health checks, cambios en validaciones)

**Proceso:**

- El desarrollador actualiza el script cuando hace cambios relevantes
- Verificar que el script sigue siendo idempotente después de cambios
- Documentar cambios en el commit message para rastreo

**Justificación:** Para desarrollo local, la actualización según necesidad es suficiente. Procesos formales de revisión periódica o validación automatizada pueden agregarse más adelante si el proyecto crece. Consistente con la estrategia del README (T-012).
