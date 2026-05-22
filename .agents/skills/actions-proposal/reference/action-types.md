# Tipos de Acciones

## Jerarquía de Tipos de Acción

Las acciones se priorizan en el siguiente orden jerárquico estricto:

1. **Ediciones del archivo actual** (siempre priorizar)
2. **Ediciones a archivos existentes** (segunda opción)
3. **Creación de nuevos archivos** (último recurso)

## Tipo 1: Ediciones del Archivo Actual

### Definición

Acciones que modifican el contenido del documento analizado actualmente.

### Cuándo Usar

- Siempre que sea posible
- Cuando el gap puede resolverse agregando contenido al archivo actual
- Cuando la información pertenece al tipo de documento actual

### Ejemplos

- Agregar una sección faltante al PRD
- Explicar un concepto en un documento técnico
- Añadir contexto de negocio a una decisión arquitectónica

### Ventajas

- No requiere navegación entre archivos
- Mantiene la información contextualizada
- Menor complejidad de ejecución

## Tipo 2: Ediciones a Archivos Existentes

### Definición

Acciones que modifican archivos existentes diferentes del archivo analizado.

### Cuándo Usar

Solo cuando se cumple AL MENOS UNO de los siguientes criterios:

1. **Contexto fuera del tipo de documento actual**
   - El gap requiere información que no pertenece al tipo de documento actual
   - Ejemplo: Detalles técnicos de implementación en un PRD
   - Ejemplo: Decisiones de negocio en un documento de arquitectura técnica

2. **Información ya existe parcialmente en otro archivo**
   - La información que resolvería el gap ya está parcialmente documentada en otro archivo
   - Es mejor consolidarla allí que duplicar

3. **Tamaño del archivo actual excesivo**
   - La edición requeriría más de 50 líneas adicionales al archivo actual
   - El archivo actual ya está cerca de su tamaño óptimo

4. **Archivo actual excede tamaño óptimo para su tipo**
   - PRDs: > 200 líneas
   - Especificaciones técnicas: > 300 líneas
   - ADRs: > 100 líneas
   - Manuales de usuario: > 400 líneas
   - Documentos de estrategia: > 150 líneas

### Proceso de Validación

1. Evaluar contra los criterios anteriores
2. Buscar archivos relevantes en la estructura del proyecto
3. Validar que los archivos existan y sean accesibles
4. Comparar opciones: ¿es mejor edición a archivo existente que edición del archivo actual?
5. Documentar justificación si se elige esta opción

### Formato de Propuesta

```markdown
**EDICIONES A ARCHIVOS EXISTENTES PROPUESTAS**

### Archivo: [ruta del archivo]
- **Gap relacionado**: [Título del gap]
- **Acción propuesta**: [Descripción de la edición a realizar]
- **Justificación**: [Por qué este archivo es el lugar apropiado]
- **Referencias necesarias**: [fuentes a consultar]
- **Resultado esperado**: [descripción del resultado]
```

## Tipo 3: Creación de Nuevos Archivos

### Definición

Acciones que crean nuevos documentos en el proyecto.

### Cuándo Usar

Solo como último recurso cuando:

- Las ediciones del archivo actual no son suficientes
- No existen archivos apropiados para editar
- La información requiere un documento independiente
- Se cumplen los criterios de consolidación o documentos siguientes

### Criterios para Creación

1. **Consolidación necesaria**
   - Más de 10 gaps relacionados con un tema específico
   - El contenido de gaps excede el 30% del tamaño del documento actual
   - Gaps pertenecen a un dominio funcional diferente

2. **Documento siguiente lógico**
   - Representa el siguiente paso en el flujo de desarrollo
   - Completa un área de documentación faltante
   - Tiene dependencia natural con el documento actual

3. **División atómica justificada**
   - El documento es intrínsecamente denso o grande
   - La división mejoraría la calidad de la documentación
   - Los archivos resultantes serían autónomos con contenido sustantivo

### Proceso de Validación

1. Verificar que no exista un documento similar
2. Validar que el tipo de documento sea apropiado
3. Confirmar que la ubicación propuesta sea correcta
4. Asegurar que el documento tenga propósito independiente
5. Documentar justificación clara

### Formato de Propuesta

```markdown
**CREACIÓN DE NUEVOS ARCHIVOS PROPUESTOS**

### Archivo: [ruta propuesta]
- **Tipo de documento**: [ADR/PRD/Especificación Técnica/etc.]
- **Gap relacionado**: [Título del gap o lista de gaps]
- **Acción propuesta**: [Descripción del contenido a crear]
- **Justificación**: [Por qué se necesita un nuevo archivo]
- **Referencias necesarias**: [fuentes a consultar]
- **Resultado esperado**: [descripción del resultado]
```

## Reglas de Oro

1. **Siempre priorizar ediciones del archivo actual**
2. **Buscar archivos existentes antes de crear nuevos**
3. **Documentar justificación para cada tipo de acción**
4. **Validar que las acciones sean ejecutables con las referencias disponibles**
5. **Mantener trazabilidad entre gaps y acciones**
