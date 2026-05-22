# Gestión de Idempotencia

## Detección de Plan Existente

El skill detecta automáticamente si existe un plan de trabajo buscando:

- Sección **PLAN DE TRABAJO** con versión y fecha
- Secciones de **Acciones Prioritarias** con estados
- Sección **VALIDACIÓN DE PLAN VIGENTE** si existe validación previa

## Validación de Plan Vigente

Para validar un plan existente:

1. Comparar gaps pendientes en el plan con gaps actuales en el documento
2. Identificar gaps nuevos que no tienen acción asignada
3. Identificar gaps obsoletos que deben removerse del plan
4. Determinar si el plan requiere actualización
5. Documentar la validación con fecha y versión

## Actualización vs Creación

- **Si el plan es vigente**: Actualizar el plan existente incrementando la versión
- **Si el plan no es vigente**: Crear un nuevo plan con versión 1
- **Si no existe plan**: Crear un nuevo plan con versión 1

## Deduplicación de Acciones

Al proponer nuevas acciones:

1. Verificar si ya existe una acción para el gap específico
2. Si existe, actualizar la acción existente en lugar de crear una nueva
3. Documentar la actualización con fecha y versión del plan

## Versionamiento del Plan

- Cada actualización incrementa la versión del plan
- La fecha de actualización se registra en el plan
- El historial de cambios documenta la versión anterior y modificaciones
