# Prioridades de Acciones

## Niveles de Prioridad

Las acciones se organizan en tres niveles de prioridad basándose en la prioridad de los gaps que resuelven:

### Prioridad 1: Crítica

- Gaps marcados como **Crítico** (prioridad más alta)
- Bloquean el desarrollo o toma de decisiones
- Requieren atención inmediata
- Impacto directo en la viabilidad del proyecto

### Prioridad 2: Alta

- Gaps marcados como **Alto** (prioridad alta)
- Importantes pero no bloqueantes
- Deben resolverse pronto
- Impacto significativo en calidad o eficiencia

### Prioridad 3: Media

- Gaps marcados como **Medio** (prioridad media)
- Mejoras deseables
- Pueden postponerse temporalmente
- Impacto moderado en calidad o eficiencia

## Criterios de Ordenamiento

Dentro de cada nivel de prioridad, las acciones se ordenan por:

1. **Tipo de acción** (orden jerárquico):
   - Ediciones del archivo actual (primero)
   - Ediciones a archivos existentes (segundo)
   - Creación de nuevos archivos (tercero, último recurso)

2. **Dependencias entre acciones**:
   - Acciones que desbloquean otras acciones van primero
   - Acciones independientes pueden ejecutarse en paralelo

3. **Complejidad de ejecución**:
   - Acciones más simples primero (menor riesgo)
   - Acciones más complejas después (mayor riesgo)

## Mapeo de Prioridad de Gap a Prioridad de Acción

| Prioridad del Gap | Prioridad de la Acción               |
|-------------------|--------------------------------------|
| Crítico           | Prioridad 1: Crítica                 |
| Alto              | Prioridad 2: Alta                    |
| Medio             | Prioridad 3: Media                   |
| Bajo              | No genera acción (considerar omitir) |

## Ajuste de Prioridad

En casos excepcionales, la prioridad de una acción puede ajustarse si:

- La acción requiere recursos no disponibles (bajar prioridad)
- La acción tiene dependencias críticas no resueltas (bajar prioridad)
- La acción resuelve múltiples gaps de alta prioridad (subir prioridad)
- La acción tiene impacto sistémico positivo (subir prioridad)

Cualquier ajuste de prioridad debe documentarse con justificación clara en el plan de trabajo.
