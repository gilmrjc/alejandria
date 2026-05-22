# Paso 5: Actualización del Plan de Trabajo

## Objetivo

Actualizar el plan de trabajo existente o crear uno nuevo. **Este paso SÍ escribe el plan de trabajo en el archivo analizado.**

## Caso A: Actualización de Plan Existente

Si el plan requiere actualización:

1. **Incrementar versión**: Aumentar el número de versión del plan
2. **Remover acciones obsoletas**: Eliminar acciones para gaps que ya no existen o están `[OBSOLETO]`
3. **Agregar nuevas acciones**: Incorporar acciones para gaps nuevos identificados
4. **Actualizar estados de gaps**: Marcar los gaps con nuevas acciones propuestas como `[PLANEADO]`
5. **Actualizar prioridades**: Ajustar prioridades si han cambiado
6. **Documentar cambios**: Agregar una nota de cambios al inicio del plan

## Caso B: Creación de Nuevo Plan

Si no existe plan o se requiere un plan completamente nuevo:

1. **Inicializar versión**: Establecer versión del plan en 1
2. **Generar todas las acciones**: Crear acciones de integración para todos los gaps `[RESUELTO]`
3. **Actualizar estados de gaps**: Marcar los gaps con acciones propuestas como `[PLANEADO]`
4. **Organizar por prioridad**: Agrupar acciones por prioridad (Crítica, Alta, Media)
5. **Documentar el plan**: Usar el formato completo de plantilla

## Documentación de Cambios

Al actualizar un plan existente, agregar:

```markdown
**HISTORIAL DE CAMBIOS**
- Versión [número]: [YYYY-MM-DD] - [Descripción de cambios]
- Versión [número-1]: [YYYY-MM-DD] - Creación inicial del plan
```

## Escritura en el Archivo

Este es el único paso del skill que escribe en el archivo analizado:

- Escribir el plan de trabajo completo en el archivo
- Actualizar estados de gaps de `[RESUELTO]` a `[PLANEADO]` para gaps con acciones propuestas
- NO realizar otras ediciones (no integrar respuestas al contenido principal, no actualizar otros estados de gaps)
- Mantener el formato y estructura del archivo original

## Salida

- **Plan de trabajo actualizado**: Plan escrito en el archivo con versión incrementada
- **Historial de cambios**: Registro de modificaciones si es actualización
