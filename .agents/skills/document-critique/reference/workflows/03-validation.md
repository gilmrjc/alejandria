# Paso 3: Validación de Respuestas y Consistencia

Para cada rol funcional relevante (mínimo 2-3 roles), realiza la validación de respuestas existentes y consistencia cruzada.

## 3.1 Validar Respuestas Existentes para el Rol

- **Revisar contexto de gaps previos**: Antes de iniciar la validación, revisar las respuestas y justificaciones de gaps con estado `[RESPONDIDO]` y `[NO APLICA]` del Paso 2. Utilizar esta información como contexto base para entender el documento actual.
- Revisa el documento desde la perspectiva del rol funcional actual
- Determina si el documento responde las preguntas que este rol haría según el tipo de documento
- Aplica la perspectiva dual de nivel de experiencia adaptada al contexto:
  - **Senior**: Valida que las decisiones tengan suficiente contexto, razones fundamentales, impacto en el negocio/organización, consideraciones a largo plazo
  - **Junior**: Valida que haya explicaciones de conceptos del dominio, terminología, pros/contras, y procesos paso a paso
- Responde preguntas con información disponible de los recursos del documento
- Confirma que las respuestas existentes son correctas basándote en fuentes disponibles
- Verifica precisión, completitud y consistencia para este rol
- **Considerar gaps previos respondidos/no aplica**: Al evaluar nuevas preguntas, verificar si ya fueron respondidas o marcadas como no aplica en análisis previos para evitar duplicación y aprovechar el contexto acumulado

## 3.2 Validación de Consistencia Cruzada

Antes de identificar contexto faltante para cada rol, realizar validación proactiva de contradicciones:

**Proceso:**

1. **Identificar afirmaciones clave** en el documento actual
2. **Comparar con cada referencia** mencionada:
   - ¿La referencia afirma lo mismo?
   - ¿Hay discrepancias en datos, fechas, decisiones, arquitectura?
   - ¿Hay versiones conflictivas del mismo hecho?
3. **Comparar referencias entre sí**:
   - ¿Las referencias se contradicen entre sí?
   - ¿Hay ADRs que contradicen la documentación?
   - ¿Hay código que contradice la documentación?
4. **Documentar cada contradicción** usando el formato de `reference/guardrails.md`
5. **Generar gap automáticamente** por cada contradicción:
   - Pregunta: "¿Cuál es el dato correcto? [Descripción de contradicción]"
   - Prioridad: Determinada por impacto de la contradicción en decisiones

**Prioridad de fuentes en contradicciones:**

- Código > Documentación reciente > Documentación antigua
- ADRs > Documentación general
- Especificaciones técnicas > Documentación de producto

Para más detalles sobre manejo de contradicciones, consultar `reference/guardrails.md`.
