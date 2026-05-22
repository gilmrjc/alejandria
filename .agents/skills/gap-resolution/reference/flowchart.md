# Diagrama de Flujo del Proceso

Este documento muestra el flujo visual completo del proceso de resolución de gaps.

## Diagrama de Flujo Principal

```mermaid
flowchart TD
    Start([Inicio]) --> Detect{¿Existe sesión previa?}
    Detect -->|No| InitVersion[Inicializar versión 1]
    Detect -->|Sí| ReadSession[Leer sesión existente]
    ReadSession --> ValidateGaps[Validar vigencia de gaps]
    ValidateGaps --> IncrementVersion[Incrementar versión]
    InitVersion --> Prepare[Preparación de la sesión]
    IncrementVersion --> Prepare

    Prepare --> ReviewGaps[Revisar gaps identificados]
    ReviewGaps --> EstablishOrder[Establecer orden de trabajo]
    EstablishOrder --> DocumentState[Documentar estado inicial]

    DocumentState --> SelectGap[Seleccionar gap prioritario]
    SelectGap --> PresentContext[Presentar contexto del gap]

    PresentContext --> AskQuestions[Formular preguntas clave]
    AskQuestions --> ProvideSuggestions[Proveer sugerencias]
    ProvideSuggestions --> RequestValidation[Solicitar validación]

    RequestValidation --> CheckResponse{Tipo de respuesta}

    CheckResponse -->|Valida| ExpandResponse[Expandir respuesta]
    CheckResponse -->|Modifica| ExpandModified[Expandir modificación]
    CheckResponse -->|Rechaza| OfferAlternatives[Ofrecer alternativas]
    CheckResponse -->|No sabe| SuggestSources[Sugerir fuentes]

    ExpandResponse --> ValidateExpansion[Validar expansión]
    ExpandModified --> ValidateExpansion
    OfferAlternatives --> CheckConsensus{¿Consenso?}
    CheckConsensus -->|Sí| ExpandResponse
    CheckConsensus -->|No| SuggestSources

    ValidateExpansion --> DocumentResponse[Documentar respuesta]
    SuggestSources --> DocumentPersistent[Documentar gap persistente]

    DocumentResponse --> UpdateState[Actualizar estado a RESUELTO]
    DocumentPersistent --> KeepPending[Mantener estado PENDIENTE]

    UpdateState --> MoreGaps{¿Más gaps?}
    KeepPending --> MoreGaps

    MoreGaps -->|Sí| SelectGap
    MoreGaps -->|No| Incorporate[Incorporar respuestas al documento]

    Incorporate --> ValidateIncorporation[Validar incorporación]
    ValidateIncorporation --> DocumentResults[Documentar resultados]
    DocumentResults --> UpdateSessionState[Actualizar estado de sesión]
    UpdateSessionState --> End([Fin])
```

## Resumen de Pasos

1. **Detección de Sesión Previo**: Determinar si existe sesión previa y validar vigencia
2. **Preparación de la Sesión**: Revisar gaps, establecer orden de trabajo, documentar estado inicial
3. **Rondas de Preguntas**: Para cada gap, presentar contexto, formular preguntas, proveer sugerencias
4. **Manejo de Respuestas**: Expandir respuestas validadas, manejar rechazos, documentar gaps persistentes
5. **Documentación de Resultados**: Incorporar respuestas al documento, validar incorporación, actualizar estado de sesión
