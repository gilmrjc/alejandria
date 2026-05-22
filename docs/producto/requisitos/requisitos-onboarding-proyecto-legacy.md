---
id: REQ-007
type: Requirements
rating:
rating-phase:
related:
  - target: FEA-001
    relationship_type: implements
    reason: Implementa el feature de onboarding strategy
  - target: FEAT-005
    relationship_type: implements
    reason: Implementa el feature de integración Git
  - target: TS-006
    relationship_type: references
    reason: Referencia el technical-specs-onboarding-proyecto-legacy para especificación técnica detallada
---

# Requisitos: Onboarding de Proyecto Legacy — Alejandria

Este documento define los requisitos para el onboarding de proyectos legacy.

---

## Índice

1. [Visión General](#1-visión-general)
2. [Requisitos Funcionales](#2-requisitos-funcionales)
3. [Requisitos No Funcionales](#3-requisitos-no-funcionales)

---

## 1. Visión General

**Propósito:**

Generar baseline del estado actual de documentación y priorizar áreas que deben abordarse primero.

**Contexto:**

Proceso de migración gradual para proyectos con historia acumulada y documentación existente.

**Referencias:**

- [FEAT-003](../funcionalidades/onboarding-proyecto-legacy.md): Onboarding de Proyecto Legacy
- [STR-003](../../estrategia/estrategia/technical-roadmap.md): Technical Roadmap (Hito 7)

---

## 2. Requisitos Funcionales

### Análisis de Salud Inicial

**Requisitos Definidos:**

- Al conectar un repositorio con historia, el sistema debe ejecutar análisis de salud completo
- El sistema debe generar calificación global del proyecto
- El sistema debe generar mapa de calor de módulos
- El sistema debe generar priorización inteligente basada en frecuencia de cambios y complejidad

**Requisitos Pendientes:**

- [PENDIENTE] Algoritmo de cálculo de calificación global
- [PENDIENTE] Definición de métricas de salud de documentación
- [PENDIENTE] Generación de mapa de calor por módulo
- [PENDIENTE] Algoritmo de priorización basado en frecuencia de cambios
- [PENDIENTE] Algoritmo de priorización basado en complejidad

### Arqueología de Código

**Requisitos Definidos:**

- El sistema debe realizar arqueología de código analizando commits, pull requests e issues

**Requisitos Pendientes:**

- [PENDIENTE] Extracción de contexto de commits históricos
- [PENDIENTE] Análisis de pull requests para reconstruir decisiones
- [PENDIENTE] Análisis de issues para entender contexto de problemas
- [PENDIENTE] Integración de arqueología con detección de gaps
- [PENDIENTE] Estrategia de límite de análisis ( commits a analizar)

### Flujo de Onboarding

**Requisitos Definidos:**

- El usuario debe poder migrar proyecto existente a Alejandría
- El usuario debe poder evaluar salud de documentación actual
- El usuario debe poder priorizar áreas de mejora documental
- El usuario debe poder recuperar contexto perdido mediante arqueología de código

**Requisitos Pendientes:**

- [PENDIENTE] Pasos del flujo de onboarding para proyectos legacy
- [PENDIENTE] Presentación de resultados de análisis de salud
- [PENDIENTE] Interfaz de priorización de áreas de mejora
- [PENDIENTE] Validación de contexto recuperado por arqueología

---

## 3. Requisitos No Funcionales

### Performance

**Requisitos Pendientes:**

- [PENDIENTE] Tiempo máximo para análisis de salud inicial
- [PENDIENTE] Tiempo máximo para arqueología de código
- [PENDIENTE] Límite de commits a analizar por proyecto

### Escalabilidad

**Requisitos Pendientes:**

- [PENDIENTE] Capacidad máxima de tamaño de repositorio para análisis
- [PENDIENTE] Estrategia de análisis para repositorios muy grandes

### Usabilidad

**Requisitos Pendientes:**

- [PENDIENTE] Tiempo máximo para completar onboarding de proyecto legacy
- [PENDIENTE] Claridad de presentación de resultados de análisis

---

## Referencias

- [FEAT-003](../funcionalidades/onboarding-proyecto-legacy.md): Onboarding de Proyecto Legacy
- [FEAT-005](../funcionalidades/integracion-git.md): Integración con Git
- [STR-003](../../estrategia/estrategia/technical-roadmap.md): Technical Roadmap (Hito 7)
- [REQ-001](requisitos-funcionales.md): Requisitos Funcionales

---

*Documento generado como especificación de requisitos para onboarding de proyectos legacy.*
