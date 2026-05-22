# Diagrama de Flujo del Proceso

## Flujo Visual

```text
INICIO
   │
   ▼
┌─────────────────────────────────────┐
│ Paso 0: Detección de Plan Existente │
│ - Buscar secciones de plan de trabajo│
│ - Identificar versión y fecha       │
└─────────────────────────────────────┘
   │
   ├─────────────────┐
   │                 │
   ▼                 ▼
Sin Plan        Con Plan Existente
   │                 │
   │                 ▼
   │        ┌─────────────────────────┐
   │        │ Paso 1: Validación de    │
   │        │ Vigencia del Plan        │
   │        │ - Comparar gaps actuales │
   │        │ - Identificar cambios    │
   │        └─────────────────────────┘
   │                 │
   │                 ▼
   │        ┌─────────────────────────┐
   │        │ ¿Plan es vigente?       │
   │        └─────────────────────────┘
   │                 │
   │        ┌────────┴────────┐
   │        │                 │
   │        ▼                 ▼
   │     Vigente      Requiere Actualización
   │        │                 │
   │        └────────┬────────┘
   │                 │
   └─────────────────┤
                     ▼
          ┌─────────────────────────┐
          │ Paso 2: Propuesta de    │
          │ Nuevas Acciones         │
          │ - Identificar gaps sin  │
          │   acción asignada       │
          │ - Generar acciones      │
          │ - Aplicar jerarquía de  │
          │   tipos de acción       │
          └─────────────────────────┘
                     │
                     ▼
          ┌─────────────────────────┐
          │ Paso 3: Actualización   │
          │ del Plan de Trabajo     │
          │ - Escribir plan en file │
          │ - Incrementar versión   │
          │ - Documentar cambios    │
          └─────────────────────────┘
                     │
                     ▼
          ┌─────────────────────────┐
          │ Paso 4: Propuesta de    │
          │ División Atómica        │
          │ - Evaluar criterios     │
          │ - Proponer archivos     │
          │   atómicos si aplica    │
          └─────────────────────────┘
                     │
                     ▼
          ┌─────────────────────────┐
          │ Paso 5: Sugerencia de   │
          │ Consolidación           │
          │ - Evaluar criterios     │
          │ - Proponer consolidación │
          │   si aplica             │
          └─────────────────────────┘
                     │
                     ▼
          ┌─────────────────────────┐
          │ Paso 6: Propuesta de    │
          │ Documentos Siguientes   │
          │ - Descubrir estructura  │
          │ - Identificar gaps      │
          │   lógicos               │
          │ - Proponer documentos   │
          └─────────────────────────┘
                     │
                     ▼
          ┌─────────────────────────┐
          │ Paso 7: Validación      │
          │ Cruzada de Propuestas   │
          │ - Detectar contradicciones│
          │ - Priorizar propuestas  │
          │ - Ajustar inconsistencias│
          └─────────────────────────┘
                     │
                     ▼
                   FIN
```

## Decisiones Clave

### Detección de Plan (Paso 0)

- **¿Existe plan?** → Si: Validar vigencia. No: Crear nuevo plan.

### Validación de Vigencia (Paso 1)

- **¿Plan es vigente?** → Si: Mantener plan. No: Actualizar plan.

### Propuesta de Acciones (Paso 2)

- **¿Gap tiene acción asignada?** → Si: Omitir. No: Proponer acción.
- **¿Tipo de acción?** → Priorizar: archivo actual > archivos existentes > nuevo archivo.

### División Atómica (Paso 4)

- **¿Cumple criterios?** → Si: Proponer división. No: Omitir.

### Consolidación (Paso 5)

- **¿Cumple criterios?** → Si: Proponer consolidación. No: Omitir.

### Documentos Siguientes (Paso 6)

- **¿Es siguiente lógico?** → Si: Proponer documento. No: Omitir.

### Validación Cruzada (Paso 7)

- **¿Hay contradicciones?** → Si: Resolver y priorizar. No: Finalizar.

## Puntos de Salida

El proceso puede terminar en diferentes puntos:

1. **Después de Paso 1**: Si el plan es vigente y no hay gaps nuevos.
2. **Después de Paso 3**: Si no hay propuestas estructurales que aplicar.
3. **Después de Paso 7**: Finalización normal del proceso.

## Iteraciones

El proceso es idempotente:

- Ejecuciones múltiples no generan planes duplicados
- Cada ejecución valida y actualiza según sea necesario
- El versionamiento permite rastrear cambios
