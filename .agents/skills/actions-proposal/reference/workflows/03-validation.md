# Paso 1: Validación de Vigencia del Plan

## Objetivo

Si existe un plan de trabajo previo, validar si sigue siendo vigente dado el estado actual de gaps.

## Proceso de Validación

1. **Leer gaps actuales**: Identificar todos los gaps con estado `[RESUELTO]` en el documento (gaps que tienen respuesta pero aún no tienen acción de integración planeada)
2. **Comparar con plan**: Comparar gaps resueltos actuales con gaps en el plan existente
3. **Identificar cambios**:
   - Gaps nuevos resueltos: Gaps resueltos que no tienen acción de integración asignada en el plan
   - Gaps obsoletos: Gaps en el plan que ya no existen o están marcados como `[OBSOLETO]`
   - Gaps integrados: Gaps en el plan que ya fueron integrados al contenido principal
   - Gaps planeados: Gaps con estado `[PLANEADO]` que ya tienen acción de integración propuesta (no requieren nueva acción)

## Criterios de Vigencia

El plan requiere actualización si:

- Hay gaps resueltos nuevos sin acción de integración asignada
- Hay gaps obsoletos que deben removerse del plan
- Las prioridades de los gaps han cambiado significativamente
- Han pasado más de 30 días desde la última validación

## Documentación de Validación

Usar el formato de `references/templates.md`:

```markdown
**VALIDACIÓN DE PLAN VIGENTE**
- Fecha de validación: [YYYY-MM-DD]
- Plan original versión: [número]
- Gaps resueltos en plan: [cantidad]
- Gaps resueltos nuevos identificados: [cantidad]
- Gaps obsoletos: [cantidad]
- Gaps planeados existentes: [cantidad]
- Requiere actualización: [SÍ/NO]
- Motivo de actualización: [Descripción si aplica]
```

## Decisión

- **Si el plan es vigente**: Continuar con Paso 2 manteniendo el plan existente
- **Si el plan requiere actualización**: Continuar con Paso 2 y actualizar el plan en Paso 3
- **Si no existe plan**: Marcar validación como no aplicable y continuar con Paso 2

## Salida

- **Estado de validación**: Vigente / Requiere actualización / No aplicable
- **Detalle de cambios**: Gaps resueltos nuevos, gaps obsoletos, gaps integrados, gaps planeados existentes
