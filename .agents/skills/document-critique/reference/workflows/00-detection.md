# Paso 0: Detección de Análisis Previo

Antes de iniciar la revisión, determinar si el documento ya contiene un análisis previo.

## Criterios de Detección

Buscar en el documento las siguientes secciones:

- **ESTADO DEL ANÁLISIS**: Indica que existe un análisis previo
- **CLASIFICACIÓN DEL DOCUMENTO**: Con fecha y versión de análisis
- Secciones de gaps con estados: `[PENDIENTE]`, `[RESPONDIDO]`, `[OBSOLETO]`
- **PLAN DE TRABAJO**: Indica que ya se han propuesto acciones

## Caso A: Sin Análisis Previo

Si no se detectan secciones de análisis previo:

- Proceder con análisis completo desde cero
- Inicializar versión del análisis en 1
- Documentar estado del análisis como "Análisis previo: NO"
- Continuar con Paso 1: Preparación y Clasificación

## Caso B: Con Análisis Previo

Si se detectan secciones de análisis previo:

- Leer el estado del análisis existente
- Validar la vigencia de los gaps existentes
- Determinar si requiere actualización
- Incrementar versión del análisis
- Documentar estado del análisis con información del análisis previo
- Continuar con Paso 1: Preparación y Clasificación
