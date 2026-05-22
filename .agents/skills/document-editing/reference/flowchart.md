# Diagrama de Flujo del Proceso

## Resumen Visual

```text
INICIO
  │
  ▼
┌─────────────────────────────────────┐
│ Paso 0: Lectura y Validación del Plan│
│ - Localizar plan de trabajo         │
│ - Leer encabezado                   │
│ - Revisar acciones                  │
│ - Identificar tipos y documentos    │
│ - Verificar referencias             │
│ - Validar plan                      │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ Paso 1: Ejecución de Acciones       │
│ - Por prioridad (Crítica > Alta > Media)│
│ - Por tipo (actual > existentes > nuevos)│
│ - Aplicar ediciones                 │
│ - Verificar cambios                 │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ Paso 2: Integración de Respuestas   │
│ - Identificar gaps con respuestas   │
│ - Leer respuestas                   │
│ - Determinar punto de integración   │
│ - Aplicar integración               │
│ - Eliminar respuestas originales    │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ Paso 3: Documentos Relacionados     │
│ - Identificar documentos relacionados│
│ - Leer acciones para relacionados   │
│ - Validar existencia                │
│ - Aplicar cambios                   │
│ - Verificar consistencia            │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ Paso 4: Actualización de Calificación│
│ - Leer calificación original         │
│ - Leer calificación esperada        │
│ - Evaluar estado actual             │
│ - Calcular nueva calificación       │
│ - Comparar con esperada             │
│ - Actualizar en frontmatter         │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ Paso 5: Estados y Limpieza          │
│ - Actualizar gaps a [IMPLEMENTADO]  │
│ - Documentar fecha y acción         │
│ - Eliminar plan de trabajo          │
│ - Eliminar secciones temporales     │
│ - Verificar forma final             │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ Paso 6: Validación Final            │
│ - Verificar completitud acciones    │
│ - Validar integración               │
│ - Validar estados                   │
│ - Validar calificación              │
│ - Validar documentos relacionados   │
│ - Validar forma final               │
│ - Validar calidad general           │
└─────────────────────────────────────┘
  │
  ▼
FIN
```

## Transiciones de Estados

### Estados de Gaps

```text
[RESUELTO] → [PLANEADO] (por el proceso de generación de planes)
[PLANEADO] → [IMPLEMENTADO] (por document-editing)
```

### Estados del Documento

```text
Con plan de trabajo → En ejecución → Forma final
```

## Puntos de Decisión

### 1. Validación del Plan (Paso 0)

- **Plan válido**: Continuar a Paso 1
- **Plan inválido**: Documentar problema, solicitar aclaración

### 2. Ejecución de Acciones (Paso 1)

- **Acción completada**: Continuar con siguiente acción
- **Acción falla**: Documentar problema, continuar con otras acciones

### 3. Integración de Respuestas (Paso 2)

- **Integración exitosa**: Continuar con siguiente gap
- **Integración falla**: Revisar punto de integración, documentar problema

### 4. Documentos Relacionados (Paso 3)

- **Documento existe**: Aplicar cambios
- **Documento no existe**: Documentar problema, continuar

### 5. Calificación (Paso 4)

- **Calificación ≥ esperada**: Proceso exitoso
- **Calificación < esperada**: Documentar discrepancia, continuar

### 6. Validación Final (Paso 6)

- **Validación exitosa**: Documento listo para producción
- **Validación falla**: Documentar problemas, requerir atención
