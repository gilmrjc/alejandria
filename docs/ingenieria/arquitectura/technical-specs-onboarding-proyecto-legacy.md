---
id: TS-006
type: Technical Specification
related-features: [FEAT-003]
related-adrs: []
related:
  - target: FEAT-005
    relationship_type: depends_on
    reason: Depende de la integración con Git para conectar repositorios y realizar arqueología de código
  - target: REQ-007
    relationship_type: depends_on
    reason: Depende de los requisitos archivados de onboarding legacy como fuente de especificaciones técnicas
---

# Especificación Técnica: Onboarding de Proyecto Legacy

Especificación técnica detallada para el onboarding de proyectos legacy en Alejandría.

---

## Índice

1. [Visión General](#1-visión-general)
2. [Análisis de Salud Inicial](#2-análisis-de-salud-inicial)
3. [Arqueología de Código](#3-arqueología-de-código)
4. [Flujo de Onboarding](#4-flujo-de-onboarding)
5. [Requisitos No Funcionales](#5-requisitos-no-funcionales)

---

## 1. Visión General

**Propósito:**

Generar baseline del estado actual de documentación y priorizar áreas que deben abordarse primero.

**Contexto:**

Proceso de migración gradual para proyectos con historia acumulada y documentación existente.

**Referencias:**

- [FEAT-003](../../producto/funcionalidades/onboarding-proyecto-legacy.md): Onboarding de Proyecto Legacy
- [FEAT-005](../../producto/funcionalidades/integracion-git.md): Integración con Git
- [REQ-007](../../producto/requisitos/.archived/requisitos-onboarding-proyecto-legacy.md): Requisitos archivados

---

## 2. Análisis de Salud Inicial

### Algoritmo de Cálculo de Calificación Global

**Fórmula base:**

```python
calificacion_global = (
    (peso_documentacion * calificacion_documentacion) +
    (peso_completitud * calificacion_completitud) +
    (peso_actualizacion * calificacion_actualizacion) +
    (peso_calidad * calificacion_calidad)
) / (peso_documentacion + peso_completitud + peso_actualizacion + peso_calidad)
```

**Pesos por defecto:**

- `peso_documentacion`: 0.3 (cantidad de documentación)
- `peso_completitud`: 0.3 (completitud de contenido)
- `peso_actualizacion`: 0.2 (recencia de actualizaciones)
- `peso_calidad`: 0.2 (calidad estructural)

**Cálculo de sub-calificaciones:**

- `calificacion_documentacion`: (documentos_tecnico / total_archivos) * 10
- `calificacion_completitud`: promedio de ratings de documentos existentes
- `calificacion_actualizacion`: basado en recencia de commits (últimos 6 meses)
- `calificacion_calidad`: basado en estructura y organización de documentación

### Definición de Métricas de Salud de Documentación

**Métricas principales:**

1. **Ratio documentación/código:**
   - Fórmula: `bytes_documentacion / bytes_codigo`
   - Objetivo: > 0.1 (10% de código es documentación)
   - Calificación: min(ratio * 50, 10)

2. **Cobertura de módulos:**
   - Fórmula: `modulos_documentados / total_modulos`
   - Objetivo: > 0.8 (80% de módulos documentados)
   - Calificación: cobertura * 10

3. **Recencia de actualizaciones:**
   - Fórmula: `commits_documentacion_ultimos_6m / total_commits_ultimos_6m`
   - Objetivo: > 0.2 (20% de commits son de documentación)
   - Calificación: min(ratio * 25, 10)

4. **Profundidad de documentación:**
   - Fórmula: promedio de palabras por documento técnico
   - Objetivo: > 500 palabras
   - Calificación: min(palabras_promedio / 100, 10)

### Generación de Mapa de Calor por Módulo

**Estructura de datos:**

```json
{
  "modules": [
    {
      "name": "auth",
      "health_score": 7.5,
      "documentation_count": 5,
      "code_files_count": 20,
      "last_updated": "2026-01-15"
    },
    {
      "name": "payment",
      "health_score": 3.2,
      "documentation_count": 1,
      "code_files_count": 15,
      "last_updated": "2025-08-20"
    }
  ]
}
```

**Visualización:**

- Heatmap con colores: rojo (< 4), amarillo (4-7), verde (> 7)
- Tamaño de celda proporcional a complejidad del módulo
- Hover muestra métricas detalladas

### Algoritmo de Priorización Basado en Frecuencia de Cambios

**Fórmula de prioridad:**

```python
prioridad = (
    (frecuencia_cambios * peso_frecuencia) +
    (complejidad * peso_complejidad) +
    (impacto_negocio * peso_impacto) -
    (salud_documentacion * peso_salud)
)
```

**Pesos:**

- `peso_frecuencia`: 0.4
- `peso_complejidad`: 0.3
- `peso_impacto`: 0.2
- `peso_salud`: 0.1

**Frecuencia de cambios:**

- Número de commits en último año
- Normalizado: commits / 365
- Rango: 0-1

**Complejidad:**

- Cyclomatic complexity promedio
- Número de dependencias
- Tamaño de módulo (líneas de código)
- Normalizado: 0-1

**Impacto de negocio:**

- Módulos core (auth, payment) = 1.0
- Módulos secundarios = 0.5
- Módulos auxiliares = 0.2

### Algoritmo de Priorización Basado en Complejidad

**Métricas de complejidad:**

1. **Cyclomatic complexity:**
   - Calculado con herramienta (ej: radon para Python)
   - Promedio por módulo
   - Normalizado: 0-1

2. **Dependencias:**
   - Número de imports/dependencias
   - Normalizado: log(dependencias + 1) / log(max_dependencias + 1)

3. **Tamaño:**
   - Líneas de código
   - Normalizado: log(loc + 1) / log(max_loc + 1)

**Score de complejidad:**

```python
complejidad = (
    (cyclomatic * 0.4) +
    (dependencias * 0.3) +
    (tamaño * 0.3)
)
```

---

## 3. Arqueología de Código

### Extracción de Contexto de Commits Históricos

**Análisis de commit messages:**

- Extracción de decisiones técnicas
- Identificación de "why" detrás de cambios
- Detección de patrones (ej: "fix:", "feat:", "refactor:")

**Parsing de commit messages:**

```python
def parse_commit_message(message):
    # Detectar tipo de cambio
    tipo = detectar_tipo(message)  # feat, fix, refactor, etc.
    
    # Extraer decisión técnica
    decision = extraer_decision(message)
    
    # Extraer contexto
    contexto = extraer_contexto(message)
    
    return {
        "tipo": tipo,
        "decision": decision,
        "contexto": contexto
    }
```

**Filtrado de commits relevantes:**

- Excluir commits de "chore", "style", "test"
- Priorizar commits con mensajes detallados (> 50 caracteres)
- Excluir commits de merge

### Análisis de Pull Requests para Reconstruir Decisiones

**Extracción de discusiones:**

- Comentarios en PR
- Review comments
- Approvals con comentarios

**Identificación de decisiones:**

- Palabras clave: "decided", "chose", "agreed", "prefer"
- Frases de justificación: "because", "due to", "reason"
- Trade-offs mencionados: "vs", "instead of", "alternative"

**Almacenamiento de contexto:**

```json
{
  "pr_id": 123,
  "decision": "Use PostgreSQL instead of MongoDB",
  "rationale": "Better ACID compliance for transactions",
  "date": "2025-06-15",
  "participants": ["user1", "user2"]
}
```

### Análisis de Issues para Entender Contexto de Problemas

**Extracción de problemas:**

- Títulos de issues
- Descripciones
- Comentarios de resolución

**Mapeo a documentación:**

- Issue → ADR (si es decisión arquitectónica)
- Issue → Feature (si es funcionalidad)
- Issue → Bug report (si es fix)

**Priorización de issues relevantes:**

- Issues con muchas reacciones/emojis
- Issues etiquetados como "decision", "architecture"
- Issues resueltos recientemente

### Integración de Arqueología con Detección de Gaps

**Generación de gaps basados en arqueología:**

1. Si commit menciona decisión pero no hay ADR → gap de documentación
2. Si PR tiene discusión técnica pero no hay documentación → gap de contexto
3. Si issue resuelve problema complejo sin documentación → gap de lecciones aprendidas

**Ejemplo de gap generado:**

```json
{
  "question": "¿Por qué se eligió PostgreSQL en lugar de MongoDB?",
  "context": "Commit abc123 y PR #456 mencionan la decisión",
  "suggestion": "Basado en PR #456: 'Mejor cumplimiento ACID para transacciones'",
  "source": "archaeology"
}
```

### Estrategia de Límite de Análisis

**Límite por defecto:** Últimos 1000 commits

**Configuración:**

- Mínimo: 100 commits
- Máximo: 10,000 commits
- Por defecto: 1000 commits

**Estrategia de sampling:**

- Para > 1000 commits: sampleo estratificado
- Estratos: commits de feat, fix, refactor (prioridad alta)
- Commits recientes (últimos 6 meses): prioridad máxima

**Performance:**

- 100 commits: 30s
- 1000 commits: 5min
- 10000 commits: 30min (job en background)

---

## 4. Flujo de Onboarding

### Pasos del Flujo de Onboarding para Proyectos Legacy

### Paso 1: Conexión de Repositorio

- Usuario selecciona repositorio Git
- Autenticación con proveedor (GitHub, GitLab, etc.)
- Selección de branch (default: main/master)
- Confirmación de permisos de lectura

### Paso 2: Análisis de Salud Inicial

- Sistema ejecuta análisis de salud completo
- Genera calificación global (0-10)
- Genera mapa de calor por módulo
- Genera priorización de áreas de mejora

### Paso 3: Arqueología de Código

- Sistema analiza commits históricos
- Sistema analiza pull requests
- Sistema analiza issues
- Sistema genera contexto recuperado

### Paso 4: Presentación de Resultados

- Dashboard con:
  - Calificación global
  - Mapa de calor
  - Lista priorizada de módulos
  - Contexto recuperado por arqueología

### Paso 5: Selección de Áreas de Mejora

- Usuario selecciona módulos a documentar primero
- Usuario puede ajustar priorización sugerida
- Usuario puede excluir módulos no relevantes

### Paso 6: Validación de Contexto Recuperado

- Usuario revisa contexto recuperado por arqueología
- Usuario aprueba, modifica o rechaza cada contexto
- Contexto aprobado se integra en documentación

### Paso 7: Inicio de Workflow de 5 Fases

- Sistema crea documentos iniciales basados en contexto
- Sistema inicia detección de gaps
- Workflow normal de 5 fases comienza

### Presentación de Resultados de Análisis de Salud

**Dashboard de onboarding:**

1. **Resumen ejecutivo:**
   - Calificación global (gauge chart)
   - Número de módulos
   - Porcentaje de módulos documentados
   - Deuda documental estimada

2. **Mapa de calor:**
   - Visualización de módulos por salud
   - Colores: rojo (< 4), amarillo (4-7), verde (> 7)
   - Tamaño proporcional a complejidad

3. **Lista priorizada:**
   - Top 10 módulos por prioridad
   - Cada módulo con: nombre, salud, frecuencia de cambios, complejidad
   - Botón "Comenzar documentación" por módulo

4. **Contexto recuperado:**
   - Lista de decisiones técnicas recuperadas
   - Cada decisión con: commit/PR fuente, fecha, participantes
   - Botón "Aprobar" / "Rechazar" por decisión

### Interfaz de Priorización de Áreas de Mejora

**Lista de módulos con prioridad:**

- Drag-and-drop para reordenar
- Toggle para incluir/excluir módulo
- Slider para ajustar peso de prioridad

**Criterios de ordenamiento:**

- Por defecto: prioridad calculada
- Opciones: frecuencia de cambios, complejidad, impacto de negocio
- Combinación de criterios (custom sort)

**Validación:**

- Mínimo 1 módulo seleccionado
- Máximo 10 módulos para primera iteración
- Alerta si se seleccionan módulos con salud > 7

### Validación de Contexto Recuperado por Arqueología

**Interfaz de revisión:**

- Lista de decisiones técnicas recuperadas
- Cada decisión en tarjeta con:
  - Título de decisión
  - Rationale extraído
  - Fuente (commit/PR)
  - Fecha
  - Botones: "Aprobar", "Modificar", "Rechazar"

**Acciones:**

- **Aprobar:** Contexto se integra en documentación
- **Modificar:** Usuario edita rationale antes de aprobar
- **Rechazar:** Contexto se descarta, se registra motivo

**Validación:**

- Mínimo 0 decisiones aprobadas (opcional)
- Alerta si se rechazan decisiones de alta prioridad

---

## 5. Requisitos No Funcionales

### Performance

**Tiempo máximo para análisis de salud inicial:**

- Proyectos < 100 archivos: 30s
- Proyectos 100-1000 archivos: 2min
- Proyectos 1000-10000 archivos: 10min
- Proyectos > 10000 archivos: 30min (job en background)

**Tiempo máximo para arqueología de código:**

- 100 commits: 30s
- 1000 commits: 5min
- 10000 commits: 30min (job en background)

**Límite de commits a analizar por proyecto:**

- Por defecto: 1000 commits
- Máximo: 10000 commits
- Para > 1000: sampling estratégico

### Escalabilidad

**Capacidad máxima de tamaño de repositorio para análisis:**

- Límite duro: 5GB
- Límite blando: 1GB (alerta si excede)
- Para > 1GB: clone shallow

**Estrategia de análisis para repositorios muy grandes:**

- Clone shallow (últimos 100 commits)
- Análisis selectivo (solo archivos principales)
- Job en background con notificación de progreso
- Paginación de resultados

### Usabilidad

**Tiempo máximo para completar onboarding de proyecto legacy:**

- Análisis automático: < 10min (para repositorio típico)
- Revisión manual: < 30min (para usuario)
- **Total:** < 40min

**Claridad de presentación de resultados:**

- Visualización intuitiva (charts, heatmaps)
- Métricas explicadas con tooltips
- Acciones claras (botones prominentes)
- Progreso visible (para jobs en background)

---

## Referencias

- [FEAT-003](../../producto/funcionalidades/onboarding-proyecto-legacy.md): Onboarding de Proyecto Legacy
- [FEAT-005](../../producto/funcionalidades/integracion-git.md): Integración con Git
- [REQ-007](../../producto/requisitos/.archived/requisitos-onboarding-proyecto-legacy.md): Requisitos archivados

---

*Documento generado integrando requisitos técnicos archivados con especificación de feature actual.*
