# Plantillas de Formato para Gap Resolution

## Plantilla de Estado de la Sesión

Usar al inicio de la sesión:

```markdown
**ESTADO DE LA SESIÓN**
- Fecha: [YYYY-MM-DD]
- Versión de sesión: [número incremental]
- Gaps a resolver: [cantidad]
- Gaps pendientes: [cantidad]
- Gaps resueltos: [cantidad]
```

## Plantilla de Preparación de la Sesión

Usar al preparar la sesión:

```markdown
**PREPARACIÓN DE LA SESIÓN**

**Gaps identificados**:
1. [Gap 1]: [descripción breve] - Prioridad: [Alta/Media/Baja]
2. [Gap 2]: [descripción breve] - Prioridad: [Alta/Media/Baja]
...

**Orden de trabajo**:
1. [Gap 1] - [razón de prioridad]
2. [Gap 2] - [razón de prioridad]
...
```

## Plantilla de Ronda de Preguntas

Usar durante cada ronda de preguntas:

```markdown
**RONDA DE PREGUNTAS: [Título del Gap]**

**Contexto**:
[Descripción del contexto del gap]

**Preguntas**:
1. [Pregunta 1]
2. [Pregunta 2]
...

**Sugerencias**:
- [Sugerencia 1]
- [Sugerencia 2]
...
```

## Plantilla de Respuesta Validada

Usar cuando el usuario valida una respuesta:

```markdown
**RESPUESTA VALIDADA**
- Gap: [Título del gap]
- Fecha: [YYYY-MM-DD]
- Respuesta: [Contenido de la respuesta validada - debe ser auto-contenida y expandida]
- Referencias: [Fuentes consultadas si aplica]
- Estado: [RESUELTO]
```

**Importante**: La respuesta debe ser auto-contenida y expandida, NO textual.

### Ejemplo de Respuesta Expandida

**Respuesta del usuario**: "La opción 2"

**Respuesta documentada (expandida)**:

```markdown
**RESPUESTA VALIDADA**
- Gap: Selección de base de datos
- Fecha: 2026-05-26
- Respuesta: Usaremos PostgreSQL como base de datos principal porque ofrece mejor soporte para consultas complejas, tiene una comunidad más activa que las alternativas evaluadas (MySQL y MongoDB), y el equipo ya tiene experiencia previa con esta tecnología.
- Referencias: docs/arquitectura/decisiones/adr-001.md
- Estado: [RESUELTO]
```

## Plantilla de Respuesta Modificada

Usar cuando el usuario modifica una sugerencia:

```markdown
**RESPUESTA MODIFICADA**
- Gap: [Título del gap]
- Fecha: [YYYY-MM-DD]
- Sugerencia original: [Sugerencia propuesta]
- Modificación del usuario: [Descripción de la modificación]
- Respuesta final: [Contenido de la respuesta final - debe ser auto-contenida y expandida]
- Estado: [RESUELTO]
```

**Importante**: La respuesta final debe ser auto-contenida y expandida, combinando la sugerencia original con la modificación del usuario.

### Ejemplo de Respuesta Modificada Expandida

**Sugerencia original**: "Usar PostgreSQL porque tiene mejor soporte para consultas complejas"

**Modificación del usuario**: "La opción 2, pero también porque el equipo ya tiene experiencia con PostgreSQL"

**Respuesta documentada (expandida)**:

```markdown
**RESPUESTA MODIFICADA**
- Gap: Selección de base de datos
- Fecha: 2026-05-26
- Sugerencia original: Usar PostgreSQL porque tiene mejor soporte para consultas complejas
- Modificación del usuario: Agregar que el equipo ya tiene experiencia con PostgreSQL
- Respuesta final: Usaremos PostgreSQL como base de datos principal por dos razones principales: (1) ofrece mejor soporte para consultas complejas que las alternativas evaluadas (MySQL y MongoDB), y (2) el equipo ya tiene experiencia previa con PostgreSQL, lo que reduce la curva de aprendizaje y acelera el desarrollo inicial.
- Estado: [RESUELTO]
```

## Plantilla de Respuesta Rechazada

Usar cuando el usuario rechaza una sugerencia:

```markdown
**RESPUESTA RECHAZADA**
- Gap: [Título del gap]
- Fecha: [YYYY-MM-DD]
- Sugerencia propuesta: [Sugerencia rechazada]
- Razón del rechazo: [Explicación del usuario]
- Estado: [PENDIENTE]
- Plan de acción: [Cómo abordar este gap en el futuro]
```

## Plantilla de Definición Establecida

Usar cuando se establece una definición o concepto:

```markdown
**DEFINICIÓN ESTABLECIDA**
- Término/Concepto: [Nombre]
- Fecha: [YYYY-MM-DD]
- Definición: [Contenido de la definición]
- Contexto: [Contexto de uso]
- Estado: [DEFINIDO]
```

## Plantilla de Razonamiento Documentado

Usar cuando se establece un razonamiento o justificación:

```markdown
**RAZONAMIENTO DOCUMENTADO**
- Decisión/Concepto: [Descripción]
- Fecha: [YYYY-MM-DD]
- Razonamiento: [Contenido del razonamiento]
- Alternativas consideradas: [Lista de alternativas]
- Justificación: [Por qué se eligió esta opción]
- Estado: [DOCUMENTADO]
```

## Plantilla de Gap Persistente

Usar cuando un gap no se resuelve en la sesión:

```markdown
**GAP PERSISTENTE**
- Gap: [Título del gap]
- Fecha: [YYYY-MM-DD]
- Razón de persistencia: [Por qué no se pudo resolver]
- Plan de acción: [Cómo abordar este gap en el futuro]
- Responsable sugerido: [Rol funcional]
- Estado: [PENDIENTE]
```

## Plantilla de Resultados de la Sesión

Usar al finalizar la sesión:

```markdown
**RESULTADOS DE LA SESIÓN**

**Gaps resueltos**: [cantidad]
- [Gap 1]: [resumen de la respuesta]
- [Gap 2]: [resumen de la respuesta]
...

**Definiciones establecidas**: [cantidad]
- [Término 1]: [resumen de la definición]
- [Término 2]: [resumen de la definición]
...

**Razonamientos documentados**: [cantidad]
- [Razonamiento 1]: [resumen]
- [Razonamiento 2]: [resumen]
...

**Gaps persistentes**: [cantidad]
- [Gap 1]: [plan de acción]
- [Gap 2]: [plan de acción]
...
```

## Plantilla de Documentación de Resultados

Usar al incorporar resultados al documento original:

```markdown
**DOCUMENTACIÓN DE RESULTADOS**

**Respuestas incorporadas**:
[Sección del documento donde se incorporaron las respuestas]

**Definiciones agregadas**:
[Sección del documento donde se agregaron las definiciones]

**Razonamientos agregados**:
[Sección del documento donde se agregaron los razonamientos]

**Gaps pendientes documentados**:
[Sección del documento donde se documentaron los gaps persistentes]
```
