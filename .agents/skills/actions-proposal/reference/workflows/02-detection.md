# Paso 0: Detección de Plan Existente

## Objetivo

Determinar si el documento ya contiene un plan de trabajo previo antes de iniciar la propuesta de acciones.

## Criterios de Detección

Buscar en el documento las siguientes secciones:

- **PLAN DE TRABAJO**: Con versión, fecha y gaps a resolver
- **Acciones Prioritarias**: Secciones con Prioridad 1, 2, 3
- **VALIDACIÓN DE PLAN VIGENTE**: Indica que existe una validación previa

## Caso A: Sin Plan Existente

Si no se detectan secciones de plan de trabajo:

- Proceder con creación de nuevo plan desde cero
- Inicializar versión del plan en 1
- Continuar con Paso 1: Validación de Vigencia (marcar como no aplicable)
- Continuar con Paso 2: Propuesta de Acciones

## Caso B: Con Plan Existente

Si se detectan secciones de plan de trabajo:

- Leer el plan de trabajo existente
- Extraer versión actual y fecha de creación
- Identificar gaps con acciones asignadas
- Continuar con Paso 1: Validación de Vigencia

## Salida

- **Estado de detección**: Plan existente / Sin plan existente
- **Información del plan** (si existe): Versión, fecha, gaps con acciones asignadas
