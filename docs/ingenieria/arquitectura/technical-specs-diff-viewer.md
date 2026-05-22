---
id: TS-005
type: Technical Specification
related-features: [FEAT-008]
related-adrs: []
dependency: [FEAT-008, FEAT-006, REQ-012]
related:
  - target: FEAT-008
    relationship_type: implements
    reason: Implementa la especificación técnica detallada del feature de diff viewer
  - target: REQ-012
    relationship_type: implements
    reason: Implementa los requisitos del diff viewer
---

# Especificación Técnica: Diff Viewer

Especificación técnica detallada para el diff viewer de Alejandría.

---

## Índice

1. [Visión General](#1-visión-general)
2. [Comparación Visual](#2-comparación-visual)
3. [Navegación](#3-navegación)
4. [Revisión de Cambios](#4-revisión-de-cambios)
5. [Requisitos No Funcionales](#5-requisitos-no-funcionales)

---

## 1. Visión General

**Propósito:**

Permitir a los usuarios revisar y entender qué cambiará antes de aprobar propuestas de edición.

**Contexto:**

Herramienta de comparación visual que muestra cambios propuestos antes de su aplicación.

**Referencias:**

- [FEAT-008](../../producto/funcionalidades/diff-viewer.md): Diff Viewer
- [FEAT-006](../../producto/funcionalidades/versioning-documentos.md): Versioning de Documentos
- [REQ-012](../../producto/requisitos/.archived/requisitos-diff-viewer.md): Requisitos archivados

---

## 2. Comparación Visual

### Motor de Comparación de Texto

**Algoritmo:** Myers diff algorithm (implementación estándar)

**Librería recomendada:**

- JavaScript: `diff` (npm package) o `jsdiff`
- Python: `difflib` (built-in) o `diff-match-patch`

**Granularidad de diff:**

- Línea por línea (default)
- Palabra por palabra (opcional)
- Carácter por carácter (opcional para debugging)

### Algoritmo de Diff

**Línea por línea:**

- Comparación basada en líneas completas
- Eficiente para documentos largos
- Buen balance entre precisión y performance

**Palabra por palabra:**

- Comparación dentro de líneas
- Útil para detectar cambios pequeños en líneas largas
- Más computacionalmente intensivo

**Carácter por carácter:**

- Comparación a nivel de carácter
- Útil para debugging de cambios sutiles
- No recomendado para uso general

### Esquema de Colores

**Adiciones (verde):**

- Color: `#10B981` (Tailwind green-500)
- Background: `#D1FAE5` (Tailwind green-100)
- Prefijo: `+`

**Eliminaciones (rojo):**

- Color: `#EF4444` (Tailwind red-500)
- Background: `#FEE2E2` (Tailwind red-100)
- Prefijo: `-`

**Modificaciones (amarillo):**

- Color: `#F59E0B` (Tailwind amber-500)
- Background: `#FEF3C7` (Tailwind amber-100)
- Prefijo: `~`

**Sin cambios:**

- Color: `#374151` (Tailwind gray-700)
- Background: Transparente
- Sin prefijo

### Sincronización de Scroll Entre Paneles

**Implementación:**

- Dos paneles lado a lado (left: versión anterior, right: versión nueva)
- Event listener de scroll en ambos paneles
- Cuando un panel scrollea, el otro scrollea proporcionalmente
- Cálculo de posición: `scrollTop_other = (scrollTop_current / scrollHeight_current) * scrollHeight_other`

**UX:**

- Botón de toggle para scroll sincronizado (default: activado)
- Scroll independiente disponible para comparación detallada
- Highlight de línea activa en ambos paneles
- Scroll suave (smooth scrolling) para mejor UX

### Resaltado de Cambios en Contexto

**Líneas adyacentes:**

- Mostrar 3 líneas antes y después de cada cambio
- Background sutil para contexto (ej: `#F3F4F6` para gray-100)
- Líneas de contexto no resaltadas con colores de cambio

**Opciones de configuración:**

- Número de líneas de contexto (default: 3, configurable: 1-10)
- Opción de "mostrar todo" (sin contexto limitado)
- Opción de "solo cambios" (sin contexto)

---

## 3. Navegación

### Navegación por Bloques de Cambios

**Definición de bloque:**

- Secuencia contigua de líneas con cambios
- Separado por al menos 3 líneas sin cambios

**Implementación:**

- Índice pre-calculado de bloques de cambios
- Cada bloque tiene: start_line, end_line, change_type
- Panel lateral con lista de bloques clickeables

**UX:**

- Click en bloque en panel lateral → scroll al bloque en diff
- Highlight del bloque activo en panel lateral
- Contador de bloques (ej: "15 bloques de cambios")

### Salto al Siguiente/Anterior Cambio

**Atajos de teclado:**

- Siguiente cambio: `Ctrl+G` o `Cmd+G`
- Anterior cambio: `Ctrl+Shift+G` o `Cmd+Shift+G`

**Botones en UI:**

- Botón "Siguiente" (icono: flecha abajo)
- Botón "Anterior" (icono: flecha arriba)
- Ubicación: header del diff viewer

**Comportamiento:**

- Scroll al siguiente/anterior bloque de cambios
- Highlight del bloque activo
- Focus en primera línea del bloque

### Contador de Cambios Totales

**Métricas mostradas:**

- Líneas agregadas: X
- Líneas eliminadas: Y
- Líneas modificadas: Z
- Total de cambios: X + Y + Z

**Ubicación:** Header del diff viewer

**Formato:** "15 cambios: +5 líneas, -3 líneas, ~7 líneas"

### Resumen Estadístico de Cambios

**Estadísticas adicionales:**

- Porcentaje de documento cambiado: `(líneas cambiadas / líneas totales) * 100`
- Archivos afectados: N (para propuestas multi-archivo)
- Tamaño de cambio: KB

**Visualización:**

- Barra de progreso mostrando porcentaje cambiado
- Color de barra: verde (< 10%), amarillo (10-30%), rojo (> 30%)

---

## 4. Revisión de Cambios

### Botones de Aprobar/Rechazar Propuesta desde Diff Viewer

**Botones principales:**

- "Aprobar cambios" (botón primario, verde)
- "Rechazar cambios" (botón secundario, rojo)

**Ubicación:** Footer del diff viewer

**Comportamiento:**

- Aprobar: Enqueue job de aplicación de cambios
- Rechazar: Marcar propuesta como rejected, registrar motivo
- Confirmación requerida para ambas acciones (modal)

### Capacidad de Editar Propuesta Antes de Aprobar

**Botón "Editar propuesta":**

- Ubicación: Footer del diff viewer (entre aprobar y rechazar)
- Transforma botón "Aprobar" en "Validar"

**Edición de propuesta:**

- Campo de texto editable con plan de acción
- Edición en línea (inline edit)
- Soporte para Markdown

**Validación:**

- Al hacer click en "Validar":
  - Sistema verifica consistencia con gaps resueltos
  - Si consistente: Reactiva botón "Aprobar"
  - Si inconsistente: Genera nuevo plan con modificaciones consistentes

### Comentarios sobre Cambios Específicos

**Implementación:**

- Click derecho en línea → "Agregar comentario"
- Panel lateral con lista de comentarios
- Comentarios asociados a línea específica

**Tipos de comentarios:**

- Pregunta (para discusión)
- Concern (para expresar preocupación)
- Sugerencia (para proponer mejora)

**Workflow:**

- Comentarios deben resolverse antes de aprobar
- Resolución: "Resuelto", "No aplica", "Aceptado"

### Historial de Revisiones de Propuesta

**Registro de revisiones:**

- Tabla `proposal_reviews` con:
  - `proposal_id`
  - `reviewer_id`
  - `reviewed_at`
  - `action` (approved, rejected, requested_changes)
  - `comments` (JSON array)

**Visualización:**

- Timeline de revisiones en panel lateral
- Cada revisión muestra: reviewer, fecha, acción
- Click en revisión → ver diff en ese momento

---

## 5. Requisitos No Funcionales

### Performance

**Tiempo máximo para generar diff:**

- Documentos < 10KB: 50ms
- Documentos 10KB - 100KB: 200ms
- Documentos 100KB - 1MB: 1s
- Documentos > 1MB: 5s

**Tiempo máximo para renderizar diff visual:**

- < 100 líneas: 100ms
- 100-500 líneas: 300ms
- 500-1000 líneas: 500ms
- > 1000 líneas: 1s

**Tiempo máximo para navegar entre cambios:**

- Salto a siguiente/anterior: 50ms
- Scroll a bloque específico: 100ms

**Capacidad máxima de tamaño de documento para diff:**

- Límite duro: 10MB
- Límite blando: 1MB (alerta si excede)
- Para documentos > 1MB: diff por chunks con paginación

### Usabilidad

**Claridad de presentación de cambios:**

- Colores intuitivos (verde = adición, rojo = eliminación)
- Prefijos claros (+, -, ~)
- Resaltado de contexto para orientación
- Tipografía legible (monospace para código)

**Facilidad de navegación entre cambios:**

- Atajos de teclado documentados
- Botones prominentes en UI
- Panel lateral con índice de cambios
- Scroll suave para mejor UX

**Intuitividad de resaltado visual:**

- Contraste suficiente para accesibilidad (WCAG AA)
- Background sutil para contexto
- Highlight de línea activa
- Indicadores visuales de bloques de cambios

**Responsividad:**

- Mobile: Paneles apilados verticalmente
- Tablet: Paneles lado a lado con scroll horizontal
- Desktop: Paneles lado a lado completos

### Compatibilidad

**Soporte para múltiples formatos de documento:**

- Markdown (default)
- Código (syntax highlighting)
- Texto plano
- JSON/YAML (syntax highlighting)

**Soporte para syntax highlighting en diff:**

- Librería: Prism.js o Highlight.js
- Lenguajes soportados: Python, JavaScript, Go, Rust, Java, SQL, YAML, JSON
- Configuración automática basada en extensión de archivo

**Soporte para diff de archivos binarios (si aplica):**

- Detección de archivos binarios
- Mensaje: "Archivo binario, diff no disponible"
- Opción de descargar ambas versiones para comparación externa

---

## Referencias

- [FEAT-008](../../producto/funcionalidades/diff-viewer.md): Diff Viewer
- [FEAT-006](../../producto/funcionalidades/versioning-documentos.md): Versioning de Documentos
- [REQ-012](../../producto/requisitos/.archived/requisitos-diff-viewer.md): Requisitos archivados

---

*Documento generado integrando requisitos técnicos archivados con especificación de feature actual.*
