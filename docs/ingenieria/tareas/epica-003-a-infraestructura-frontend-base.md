---
id: EPC-0031
type: Epic Implementation
rating: 9
rating-phase: document-editing
related:
  - target: STR-003
    relationship_type: implements
    reason: Implementa la estrategia técnica de frontend React
  - target: STR-005
    relationship_type: implements
    reason: Implementa la estrategia de frontend
  - target: PRD-003
    relationship_type: implements
    reason: Implementa el PRD de Hito 3 con requisitos de frontend
  - target: ARC-008
    relationship_type: references
    reason: Referencia el frontend-specification para especificación técnica
  - target: EPC-0032
    relationship_type: depends_on
    reason: EPC-0032 depende de la infraestructura base configurada en EPC-0031
  - target: EPC-0033
    relationship_type: depends_on
    reason: EPC-0033 depende de la infraestructura base configurada en EPC-0031
---

## Epica 3-A: Infraestructura Frontend Base

**Estado**: ⏳ PENDIENTE - Técnicas por definir

**Objetivo**: Configurar la base técnica del frontend React y validar que funciona visualmente con un dashboard base.

---

## Referencias

- **[../../estrategia/estrategia/technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md)**: Roadmap técnico, Hito 3
- **[../../estrategia/estrategia/frontend-strategy.md](../../estrategia/estrategia/frontend-strategy.md)**: Estrategia de frontend
- **[../arquitectura/technology-stack.md](../arquitectura/technology-stack.md)**: Stack tecnológico
- **[../arquitectura/frontend-specification.md](../arquitectura/frontend-specification.md)**: Especificación de frontend

---

## Componentes

- Estructura base de proyecto React con Vite
- Configuración de routing y navegación
- Cliente HTTP con autenticación JWT
- State management global con Zustand
- Configuración de build y deployment
- Dashboard base para validación visual
- Storybook para desarrollo de componentes en aislamiento

---

## Recursos y Habilidades Requeridas

**Habilidades Técnicas Requeridas**:
- React + TypeScript (experiencia intermedia-senior, 2+ años)
- State Management (Zustand para MVP)
- HTTP Client (Axios con interceptors JWT)
- Routing (React Router)
- UI Components (shadcn/ui)
- Styling (TailwindCSS)
- Testing (Jest + React Testing Library)
- Build Tool (Vite)
- Storybook

**Asignación de Equipo**:
- 1 desarrollador (Technical Lead) según technology-stack.md que define monorepo con un desarrollador para MVP Bootstrapped

**Dependencias Externas**:
- API endpoints: Ya definidos en Hito 2 (API REST y MCP Server)
- Diseño UI/UX: Usa componentes pre-diseñados (shadcn/ui, no requiere diseñador dedicado)
- LLM Provider: Ollama local (Qwen 3.5, no requiere configuración externa)

**Referencias**:
- [technology-stack.md](../arquitectura/technology-stack.md): Stack de frontend (líneas 95-106, 155, 206-213)
- [frontend-specification.md](../arquitectura/frontend-specification.md): Habilidades requeridas (líneas 44-52)

---

## Priorización de Features

**Esenciales para Infraestructura**:
- T-030: Configurar Estructura Base de Proyecto React
- T-031: Implementar Routing y Navegación
- T-032: Implementar Cliente HTTP y Autenticación
- T-040: Implementar State Management Global
- T-042: Configurar Build y Deployment
- T-033-base: Implementar Dashboard Base (validación visual)
- T-044: Configurar Storybook

**Justificación**:
Esta epica establece la base técnica fundamental para todas las funcionalidades subsiguientes. El dashboard base permite validar visualmente que el routing funciona correctamente antes de implementar componentes complejos. Storybook facilita el desarrollo de componentes en aislamiento para las epicas siguientes.

**Referencias**:
- [technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md): Hito 3 criterios y timeline (líneas 143-174)
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Requisitos de componentes (líneas 145-184, 239-241, 397-402)

---

## Valor de Negocio y Casos de Uso

**Problemas del Usuario Resueltos**:
- Sin infraestructura base, no es posible desarrollar ninguna funcionalidad de frontend
- Sin validación visual temprana, errores de routing pueden descubrirse tarde
- Sin Storybook, el desarrollo de componentes es más lento y propenso a errores

**Casos de Usuario Habilitados**:
1. Validar que la aplicación React funciona correctamente en el entorno local
2. Navegar entre rutas básicas para confirmar el routing
3. Desarrollar componentes UI en aislamiento con Storybook
4. Ver un dashboard base simple que confirma la infraestructura está operativa

**Mejora vs Situación Actual**:
- Infraestructura configurada correctamente vs setup manual propenso a errores
- Validación visual temprana vs descubrir problemas de routing en fases avanzadas
- Desarrollo de componentes en aislamiento vs desarrollo integrado más complejo

**Referencias**:
- [technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md): Valor de Hito 3 (líneas 143-174)
- [frontend-strategy.md](../../estrategia/estrategia/frontend-strategy.md): Objetivos de frontend (líneas 25-28)
- [frontend-specification.md](../arquitectura/frontend-specification.md): Componentes de UI (líneas 104-176)

---

## Técnicas Individuales

### Estimación de Esfuerzo Total

**PENDIENTE**: Estimación total por definir en fase de implementación

Desglose por tarea:

- T-030: Configurar estructura base de proyecto React
- T-031: Implementar routing y navegación
- T-032: Implementar cliente HTTP y autenticación
- T-040: Implementar state management global
- T-042: Configurar build y deployment
- T-033-base: Implementar Dashboard Base (validación visual)
- T-044: Configurar Storybook

### Justificación del Orden de Tareas

El orden de tareas se basa en dependencias secuenciales. T-030 (estructura base) es prerequisito fundamental para todas las demás tareas. T-031 (routing), T-032 (cliente HTTP) y T-040 (state management) son prerequisitos para T-033-base (dashboard base). T-042 (build) y T-044 (Storybook) pueden configurarse en paralelo después de T-030.

T-033-base es el último componente de esta epica porque valida visualmente que toda la infraestructura funciona correctamente antes de pasar a epicas subsiguientes.

### T-030: Configurar Estructura Base de Proyecto React

**Descripción**: Crear estructura base del proyecto React con Vite, configurar dependencias (React, React Router, Axios, shadcn/ui/Material-UI, TailwindCSS), y establecer convenciones de código. Configurar TypeScript y ESLint.

**Criterios de Aceptación**:
- [ ] Estructura de directorios configurada según frontend-specification.md (líneas 619-668)
- [ ] package.json configurado con dependencias (React, React Router, Axios, UI library)
- [ ] Vite configurado para desarrollo local (puerto 3000, proxy a API)
- [ ] TypeScript configurado con strict mode
- [ ] ESLint y Prettier configurados
- [ ] TailwindCSS configurado (si se usa shadcn/ui)
- [ ] README con instrucciones de setup

**Dependencias**: Ninguna

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Estructura de proyecto (líneas 619-668)
- [technology-stack.md](../arquitectura/technology-stack.md): Stack de frontend (líneas 95-106)

**Estado**: PENDIENTE

---

### T-031: Implementar Routing y Navegación

**Descripción**: Configurar React Router para navegación entre secciones. Implementar rutas principales: / (dashboard), /documents, /questions, /gaps, /proposals, /graph. Implementar breadcrumbs o indicador de ubicación.

**Criterios de Aceptación**:
- [ ] React Router configurado con rutas principales
- [ ] Navegación entre secciones funciona correctamente
- [ ] Breadcrumbs o indicador de ubicación implementado
- [ ] Links directos a recursos específicos funcionan
- [ ] 404 page implementada para rutas inexistentes

**Dependencias**: T-030

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Flujo de navegación (líneas 88-98)
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Requisitos de navegación (líneas 247-260)

**Estado**: PENDIENTE

---

### T-032: Implementar Cliente HTTP y Autenticación

**Descripción**: Configurar Axios como cliente HTTP con interceptors para autenticación (JWT) y manejo de errores. Implementar servicios de API para documents, sessions, gaps, proposals. Configurar base URL y timeout.

**Criterios de Aceptación**:
- [ ] Axios configurado con base URL y timeout
- [ ] Interceptor para agregar token JWT en headers
- [ ] Interceptor para manejar errores 401 (redirigir a login)
- [ ] Servicios de API implementados (documents, sessions, gaps, proposals)
- [ ] Manejo de errores de API claro para el usuario
- [ ] Autenticación con API funciona correctamente

**Dependencias**: T-030

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Integración con API (líneas 398-529)
- [api-specification.md](../arquitectura/api-specification.md): Endpoints de API REST
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Interacción con API (líneas 289-302)

**Estado**: PENDIENTE

---

### T-040: Implementar State Management Global

**Descripción**: Configurar state management global con Zustand. Implementar estado global para user (auth), documents (lista), sessions (activas), loading/error globales. Definir Zustand stores separados por dominio (authStore, documentsStore, sessionsStore). Estado local para componentes específicos (filtros, modales, forms).

**Criterios de Aceptación**:
- [ ] Zustand configurado como state management global
- [ ] Estado global implementado (user, documents, sessions, loading, error)
- [ ] Zustand stores separados por dominio implementados (authStore, documentsStore, sessionsStore)
- [ ] Actions para actualizar estado implementadas
- [ ] Integración con componentes funciona correctamente
- [ ] Performance de state management es aceptable

**Dependencias**: T-030

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): State Management (líneas 340-395)
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Mantenibilidad - estado global (líneas 427-430)

**Estado**: PENDIENTE

---

### T-042: Configurar Build y Deployment

**Descripción**: Configurar build de producción con Vite. Configurar optimización de bundle, code splitting, y assets. Configurar deployment local (Docker) y preparación para deployment futuro.

**Criterios de Aceptación**:
- [ ] Build de producción funciona sin errores
- [ ] Bundle optimizado (code splitting, lazy loading)
- [ ] Assets optimizados (imágenes, fonts)
- [ ] Dockerfile para frontend configurado
- [ ] Integración con docker-compose funciona
- [ ] Variables de entorno configuradas

**Dependencias**: T-030

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Configuración de Vite (líneas 670-689)
- [technology-stack.md](../arquitectura/technology-stack.md): Stack de frontend

**Estado**: PENDIENTE

---

### T-033-base: Implementar Dashboard Base

**Descripción**: Implementar versión simplificada del dashboard para validar visualmente que el routing funciona correctamente. Incluir layout base con navegación y un componente simple que muestre "Dashboard funcionando" con datos mock.

**Criterios de Aceptación**:
- [ ] Dashboard base se renderiza correctamente en ruta /
- [ ] Navegación entre rutas funciona visualmente
- [ ] Layout base con navegación implementado
- [ ] Datos mock se muestran correctamente
- [ ] Integración con state management funciona
- [ ] Responsive design básico implementado

**Dependencias**: T-030, T-031, T-032, T-040

**Referencias**:
- [technical-specs-dashboard-general.md](../arquitectura/technical-specs-dashboard-general.md): Especificación técnica detallada
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Componente Dashboard (líneas 83-104)

**Estado**: PENDIENTE

---

### T-044: Configurar Storybook

**Descripción**: Configurar Storybook para desarrollo de componentes en aislamiento. Crear stories iniciales para componentes base (Button, Card, Input). Configurar integración con TailwindCSS y shadcn/ui.

**Criterios de Aceptación**:
- [ ] Storybook configurado y funcionando
- [ ] Stories para componentes base creados
- [ ] Integración con TailwindCSS funciona
- [ ] Integración con shadcn/ui funciona
- [ ] Documentación de componentes en Storybook
- [ ] Hot reload funciona correctamente

**Dependencias**: T-030

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Desarrollo de componentes (líneas 104-176)

**Estado**: PENDIENTE
