# Paso 3: Manejo de Respuestas del Usuario

## Principio Fundamental: Expansión y Auto-Contención

Todas las respuestas documentadas deben ser auto-contenidas y no textuales:

- **NO usar respuestas textuales**: Si el usuario dice "la opción 2" o "la sugerencia A", NO documentar eso literalmente
- **Expandir referencias**: Si el usuario hace referencia a una opción o parte de una sugerencia, expandir la referencia para que sea una respuesta completa
- **Respuestas auto-contenidas**: La respuesta debe ser entendible por sí misma sin necesidad de ver las sugerencias originales
- **Incluir contexto**: Agregar el contexto necesario para que la respuesta sea clara fuera de la sesión

## Si el usuario valida las sugerencias

### Proceso de Expansión

1. **Identificar la referencia**: Determinar qué opción o sugerencia está validando el usuario
2. **Recuperar contenido**: Obtener el contenido completo de esa opción/sugerencia
3. **Expandir con contexto**: Agregar el razonamiento y contexto proporcionado por el usuario
4. **Formular respuesta completa**: Crear una respuesta auto-contenida y clara
5. **Validar expansión**: Confirmar con el usuario que la expansión es correcta
6. **Documentar**: Incorporar la respuesta expandida en la sección de gaps

### Ejemplo

**Respuesta del usuario**: "La opción 2"

**Respuesta documentada (expandida)**:

```markdown
**Respuesta**: Usaremos PostgreSQL como base de datos principal porque ofrece mejor soporte para consultas complejas y tiene una comunidad más activa que las alternativas evaluadas (MySQL y MongoDB).
```

### Acciones

- Documentar la respuesta validada en formato expandido
- Incorporar al campo "Respuesta" en la sección de gaps del documento
- Actualizar estado del gap a `[RESUELTO]`
- Avanzar a la siguiente pregunta o gap

## Si el usuario modifica las sugerencias

### Proceso de Expansión

1. **Capturar modificación**: Entender qué parte de la sugerencia el usuario modificó
2. **Combinar con original**: Integrar la modificación con el contenido original de la sugerencia
3. **Expandir con contexto**: Agregar el razonamiento de la modificación
4. **Formular respuesta completa**: Crear una respuesta auto-contenida que refleje la modificación
5. **Validar expansión**: Confirmar con el usuario que la expansión captura correctamente su modificación
6. **Documentar**: Incorporar la respuesta expandida en la sección de gaps

### Ejemplo

**Sugerencia original**: "Usar PostgreSQL porque tiene mejor soporte para consultas complejas"

**Modificación del usuario**: "La opción 2, pero también porque el equipo ya tiene experiencia con PostgreSQL"

**Respuesta documentada (expandida)**:

```markdown
**Respuesta**: Usaremos PostgreSQL como base de datos principal por dos razones principales: (1) ofrece mejor soporte para consultas complejas que las alternativas evaluadas, y (2) el equipo ya tiene experiencia previa con PostgreSQL, lo que reduce la curva de aprendizaje y acelera el desarrollo.
```

### Acciones

- Documentar la versión modificada en formato expandido
- Solicitar confirmación final de la expansión
- Incorporar al campo "Respuesta" en la sección de gaps del documento
- Actualizar estado del gap a `[RESUELTO]`
- Avanzar

## Si el usuario rechaza las sugerencias

### Proceso

1. **Solicitar dirección**: Preguntar al usuario qué dirección prefiere
2. **Ofrecer alternativas**: Proveer nuevas sugerencias basadas en su feedback
3. **Iterar**: Continuar el proceso hasta alcanzar consenso
4. **Expandir respuesta**: Cuando se alcance consenso, aplicar el proceso de expansión
5. **Validar**: Confirmar con el usuario que la expansión es correcta
6. **Documentar**: Incorporar la respuesta expandida en la sección de gaps

### Acciones

- Si se alcanza consenso: Documentar respuesta expandida y actualizar estado a `[RESUELTO]`
- Si no se alcanza consenso: Documentar como gap persistente con plan de acción
- Avanzar

## Si el usuario no sabe o no tiene información

### Proceso

1. **Documentar situación**: Registrar que el usuario no tiene información
2. **Sugerir fuentes**: Proponer fuentes de investigación o stakeholders a consultar
3. **Proponer posposición**: Sugerir posponer la resolución del gap
4. **Crear plan de acción**: Documentar un plan claro para abordar el gap en el futuro
5. **Marcar como persistente**: Actualizar estado del gap a `[PENDIENTE]` (persistente)

### Acciones

- Marcar el gap como persistente
- Documentar plan de acción específico
- Sugerir responsables o fuentes a consultar
- Documentar el estado actual en la sección de gaps
- Avanzar

## Si el usuario proporciona una respuesta directa

### Proceso de Expansión

1. **Capturar respuesta**: Entender la respuesta directa del usuario
2. **Evaluar completitud**: Determinar si la respuesta es auto-contenida
3. **Expandir si necesario**: Si la respuesta requiere contexto, agregarlo
4. **Validar**: Confirmar con el usuario que la expansión es correcta
5. **Documentar**: Incorporar la respuesta expandida en la sección de gaps

### Ejemplo

**Respuesta directa del usuario**: "Usaremos microservicios"

**Respuesta documentada (expandida)**:

```markdown
**Respuesta**: La arquitectura del sistema se basará en microservicios para permitir escalabilidad independiente, despliegue ágil y separación de responsabilidades por dominio funcional. Cada microservicio será responsable de un contexto delimitado específico del negocio.
```

### Acciones

- Documentar la respuesta en formato expandido
- Validar con el usuario que la expansión captura correctamente su intención
- Incorporar al campo "Respuesta" en la sección de gaps del documento
- Actualizar estado del gap a `[RESUELTO]`
- Avanzar
