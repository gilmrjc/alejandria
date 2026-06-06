---
id: ARC-008
type: Frontend Specification
rating: 9
rating-phase: document-editing
dependency: [ARC-002, ARC-003, ARC-004]
related:
  - target: STR-005
    relationship_type: implements
    reason: Implementa la estrategia de frontend con especificaciones técnicas
  - target: EPC-003
    relationship_type: references
    reason: Referencia la épica de frontend React para implementación
---

# Frontend Specification — Alejandria

Este documento define la especificación del frontend de Alejandria. El frontend proporciona una interfaz de usuario para gestionar documentos, sesiones de resolución de gaps, y monitorear el estado del pipeline.

---

## Índice

1. [Visión General](#1-visión-general)
2. [Arquitectura del Frontend](#2-arquitectura-del-frontend)
3. [Componentes](#3-componentes)
4. [State Management](#4-state-management)
5. [Integración con API](#5-integración-con-api)
6. [Sistema de Diseño](#6-sistema-de-diseño)
7. [UX Patterns](#7-ux-patterns)
8. [Estructura de Proyecto](#8-estructura-de-proyecto)

---

## 1. Visión General

### Propósito

El frontend de Alejandria proporciona tres interfaces principales:

1. **Dashboard**: Vista general de documentos, sesiones, y estado del sistema
2. **Sesión de Resolución**: Interfaz interactiva para responder gaps con Agente 3
3. **Document Editor**: Visualizador y editor de documentos con historial de versiones

### User Personas

Los usuarios principales del frontend son roles técnicos involucrados en el desarrollo y operación del sistema:

- **CTO/VP Engineering**: Responsable de arquitectura técnica y decisiones estratégicas
- **Senior Developer/Tech Lead**: Desarrollador senior que implementa features y revisa código
- **DevOps/SRE**: Responsable de infraestructura, deployment y operaciones
- **Arquitecto Senior**: Responsable de diseño de sistema y decisiones de arquitectura

**Referencia**: Ver [FEA-003](../../ingenieria/tareas/epica-03-frontend-react.md) (líneas 37-40, 77-80, 116-120, 156-160, 194-198) para detalles adicionales sobre user personas.

### Casos de Uso

El frontend habilita los siguientes casos de uso clave para los usuarios:

- **Revisar estado del proyecto via Dashboard**: Obtener vista general de métricas agregadas (documentos, sesiones, gaps)
- **Navegar documentos**: Explorar documentos con filtros y búsqueda para encontrar información específica
- **Revisar gaps detectados**: Ver gaps agrupados por tema con contexto faltante identificado
- **Revisar y aprobar cambios**: Revisar propuestas de cambios con diff viewer integrado y aprobar/rechazar
- **Navegación rápida**: Acceso rápido desde Dashboard a secciones específicas del sistema

**Referencia**: Ver [PRD-003](../../producto/requisitos/prd-003.md) (líneas 45-47) y [FEA-003](../../ingenieria/tareas/epica-03-frontend-react.md) (workflow de 5 fases) para detalles adicionales sobre casos de uso.

### Priorización de Features

La priorización de features distingue entre funcionalidades esenciales para MVP Bootstrapped y features que pueden postponerse a versiones posteriores.

**MVP Esenciales** (requeridas para dogfooting temprano):
- Estructura base del proyecto React
- Routing con React Router
- Cliente HTTP (Axios)
- State management con Zustand
- Dashboard con estadísticas básicas
- Sección de Documentos (lista, filtros, búsqueda)
- Sección de Gaps (visualización de gaps detectados)
- Sección de Propuestas (diff viewer para cambios)
- Diff Viewer integrado

**Features que pueden postponerse** (nice-to-have o post-MVP):
- Sección de Grafo (visualización de dependencias)
- Sección de Preguntas (depende de backend Hito 4)
- Interfaz de Sesión Interactiva (POST-MVP)

**Referencia**: Ver [EPC-003](../../ingenieria/tareas/epica-003-b-dashboard-mvp-core.md) (líneas 75-92) y [PRD-003](../../producto/requisitos/prd-003.md) (líneas 86-92) para detalles adicionales sobre priorización.

### Métricas de Éxito

Para MVP Bootstrapped, el enfoque es funcionalidad básica sobre métricas cuantitativas. La validación temprana se realizará cualitativamente mediante dogfooting y feedback en retrospectivas de desarrollo.

**Enfoque MVP**: Funcionalidad básica sobre métricas cuantitativas extensas. El objetivo es validar que el frontend habilita los workflows críticos de manera efectiva.

**Validación Cualitativa**:
- Dogfooting temprano por el equipo de desarrollo
- Retrospectivas de desarrollo para identificar fricciones
- Feedback directo de usuarios técnicos (user personas definidas)

**Métricas Cualitativas**:
- Tiempo promedio para encontrar información en documentos
- Satisfacción subjetiva (escala 1-10) con la interfaz
- Fricciones percibidas en workflows clave

**Umbrales de Éxito**:
- Satisfacción ≥ 7/10 en encuestas de dogfooting
- Reducción de fricciones ≥ 30% en 3 meses (medido cualitativamente)

**Métricas Post-MVP**: Métricas formales de adopción, satisfacción, y KPIs se definirán post-MVP cuando se valide problem-solution fit.

**Referencia**: Ver [PRD-003](../../producto/requisitos/prd-003.md) (líneas 72-78, 495-502) para detalles adicionales sobre métricas de éxito.

### Stack Tecnológico

- **Framework**: React (opción principal para MVP). Ver [frontend-strategy.md](../../estrategia/estrategia/frontend-strategy.md) para contexto estratégico de implementación de diseño con React.
- **State Management**: Zustand seleccionado para MVP por overhead mínimo, optimización automática de performance, y bundle size ~1KB. Estado global: user (auth), documents (lista), sessions (activas), loading/error globales. Estado local: componentes específicos (filtros, modales, forms). Patrones: Zustand stores separados por dominio (authStore, documentsStore, sessionsStore).
- **HTTP Client**: Axios o Fetch API
- **Routing**: React Router
- **UI Components**: shadcn/ui seleccionado (componentes copiados al proyecto, full control, moderno, integración con TailwindCSS). Material-UI es la alternativa mencionada pero no seleccionada.
- **Styling**: TailwindCSS (integrado con shadcn/ui)
- **Build Tool**: Vite

### Referencias

- **[api-specification.md](api-specification.md)**: Endpoints de API REST
- **[end-to-end-flow.md](end-to-end-flow.md)**: Flujo del pipeline
- **[technology-stack.md](technology-stack.md)**: Stack tecnológico del sistema

---

## 2. Arquitectura del Frontend

### Estructura de Capas

```
┌─────────────────────────────────────────────────┐
│              UI Layer (React Components)          │
│  - Dashboard                                     │
│  - SessionView                                   │
│  - DocumentEditor                                │
├─────────────────────────────────────────────────┤
│              State Management Layer               │
│  - React Context / Zustand                       │
│  - Global State (user, documents, sessions)      │
├─────────────────────────────────────────────────┤
│              Service Layer                         │
│  - API Client (Axios)                            │
│  - WebSocket Client (opcional)                   │
│  - Auth Service                                  │
├─────────────────────────────────────────────────┤
│              Data Layer                           │
│  - API Endpoints                                 │
│  - Local Storage (auth tokens)                   │
└─────────────────────────────────────────────────┘
```

### Flujo de Navegación

```
/ → Dashboard (vista principal)
/documents → Lista de documentos
/documents/{id} → Detalle de documento
/sessions → Lista de sesiones
/sessions/{id} → Vista de sesión (resolución de gaps)
/sessions/{id}/gaps → Gaps de sesión
/settings → Configuración de usuario
```

---

## 3. Componentes

### Dashboard

**Propósito**: Vista general del sistema con estadísticas y accesos rápidos.

**Componentes**:

- `DashboardStats`: Tarjetas con estadísticas (documentos totales, sesiones activas, gaps pendientes)
- `RecentDocuments`: Lista de documentos recientes con estado healthy
- `ActiveSessions`: Lista de sesiones en progreso
- `QuickActions`: Botones para crear documento, iniciar sesión

**Estado**:

```typescript
interface DashboardState {
  stats: {
    totalDocuments: number;
    activeSessions: number;
    pendingGaps: number;
    healthyDocuments: number;
  };
  recentDocuments: Document[];
  activeSessions: Session[];
  loading: boolean;
  error: string | null;
}
```

**API Calls**:

- `GET /api/v1/documents?per_page=5&sort_by=updated_at`
- `GET /api/v1/sessions?status=awaiting_resolution&per_page=5`
- `GET /api/v1/health`

---

### DocumentList

**Propósito**: Lista paginada de documentos con filtros y búsqueda.

**Componentes**:

- `DocumentTable`: Tabla con documentos (id, title, file_path, healthy, updated_at)
- `DocumentFilters`: Filtros por estado healthy, fecha de actualización
- `DocumentSearch`: Búsqueda por título o ruta
- `Pagination`: Controles de paginación

**Estado**:

```typescript
interface DocumentListState {
  documents: Document[];
  pagination: {
    page: number;
    perPage: number;
    total: number;
    totalPages: number;
  };
  filters: {
    healthy: boolean | null;
    updatedAfter: string | null;
    search: string;
  };
  loading: boolean;
  error: string | null;
}
```

**API Calls**:

- `GET /api/v1/documents?page={page}&per_page={perPage}&healthy={healthy}&search={search}`

---

### DocumentDetail

**Propósito**: Vista detallada de un documento con historial de versiones.

**Componentes**:

- `DocumentViewer`: Visualizador de contenido del documento
- `DocumentMetadata`: Metadatos (title, file_path, healthy, created_at, updated_at)
- `SnapshotHistory`: Lista de snapshots con opción de restaurar
- `DocumentActions`: Botones para editar, eliminar, crear sesión

**Estado**:

```typescript
interface DocumentDetailState {
  document: Document | null;
  snapshots: DocumentSnapshot[];
  loading: boolean;
  error: string | null;
  showRestoreModal: boolean;
  selectedSnapshot: DocumentSnapshot | null;
}
```

**API Calls**:

- `GET /api/v1/documents/{id}`
- `GET /api/v1/documents/{id}/snapshots`
- `POST /api/v1/documents/{id}/snapshots/{snapshot_id}/restore`
- `POST /api/v1/sessions` (crear sesión)

---

### SessionList

**Propósito**: Lista de sesiones con filtros por estado y documento.

**Componentes**:

- `SessionTable`: Tabla con sesiones (id, document_id, status, round, created_at)
- `SessionFilters`: Filtros por estado, documento
- `SessionStatusBadge`: Badge con color según estado

**Estado**:

```typescript
interface SessionListState {
  sessions: Session[];
  filters: {
    documentId: string | null;
    status: string | null;
  };
  loading: boolean;
  error: string | null;
}
```

**API Calls**:

- `GET /api/v1/sessions?document_id={documentId}&status={status}`

---

### SessionView

**Propósito**: Vista interactiva para resolver gaps con Agente 3.

**Componentes**:

- `SessionHeader`: Información de sesión (documento, estado, round)
- `GapGroupList`: Lista de grupos de gaps
- `GapGroupCard`: Card con grupo de gaps y estado
- `GapResolutionPanel`: Panel para resolver gaps de un grupo
- `AgentChat`: Chat interactivo con Agente 3
- `SessionProgress`: Barra de progreso de resolución

**Estado**:

```typescript
interface SessionViewState {
  session: Session | null;
  gapGroups: GapGroup[];
  currentGroup: GapGroup | null;
  gaps: Gap[];
  chatMessages: ChatMessage[];
  loading: boolean;
  error: string | null;
  answeringGap: boolean;
}
```

**API Calls**:

- `GET /api/v1/sessions/{id}`
- `GET /api/v1/sessions/{id}/gap-groups`
- `GET /api/v1/sessions/{id}/gaps?status=pending`
- `POST /api/v1/sessions/{id}/gaps/{gap_id}/answer`
- `POST /api/v1/sessions/{id}/complete`

---

### GapResolutionPanel

**Propósito**: Panel para resolver un gap específico.

**Componentes**:

- `GapQuestion`: Pregunta del gap con contexto faltante
- `GapPriorityBadge`: Badge con prioridad (critical/high/medium/low)
- `GapRoleAffected`: Rol afectado por el gap
- `AnswerInput`: Textarea para ingresar respuesta
- `AgentSuggestion`: Sugerencia del Agente 3 (opcional)
- `SubmitButton`: Botón para enviar respuesta

**Estado**:

```typescript
interface GapResolutionPanelState {
  gap: Gap | null;
  answer: string;
  agentSuggestion: string | null;
  submitting: boolean;
  error: string | null;
}
```

**API Calls**:

- `POST /api/v1/sessions/{id}/gaps/{gap_id}/answer`

---

### ContextEntriesView

**Propósito**: Vista de cambios sugeridos (context_entries) para aprobación.

**Componentes**:

- `ContextEntryList`: Lista de cambios sugeridos
- `ContextEntryCard`: Card con cambio (old_content, new_content, line_number)
- `DiffViewer`: Visualizador de diff entre old y new content
- `ApproveButton`: Botón para aprobar cambio
- `RejectButton`: Botón para rechazar cambio

**Estado**:

```typescript
interface ContextEntriesViewState {
  contextEntries: ContextEntry[];
  loading: boolean;
  error: string | null;
  approving: boolean;
}
```

**API Calls**:

- `GET /api/v1/sessions/{id}/context-entries`
- `POST /api/v1/context-entries/{id}/approve`

---

## 4. State Management

### Global State (Zustand)

Zustand seleccionado para MVP por overhead mínimo, optimización automática de performance, y bundle size ~1KB. Los stores se organizan por dominio para mantener el estado modular y escalable.

```typescript
// stores/authStore.ts
import { create } from 'zustand';

interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
  setUser: (user: User | null) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  loading: false,
  error: null,
  setUser: (user) => set({ user }),
  logout: () => set({ user: null }),
}));

// stores/documentsStore.ts
import { create } from 'zustand';

interface DocumentsState {
  documents: Document[];
  loading: boolean;
  error: string | null;
  fetchDocuments: () => Promise<void>;
  setDocuments: (documents: Document[]) => void;
}

export const useDocumentsStore = create<DocumentsState>((set) => ({
  documents: [],
  loading: false,
  error: null,
  fetchDocuments: async () => {
    set({ loading: true });
    try {
      const response = await documentsService.list({});
      set({ documents: response.data, loading: false });
    } catch (error) {
      set({ error: 'Failed to fetch documents', loading: false });
    }
  },
  setDocuments: (documents) => set({ documents }),
}));

// stores/sessionsStore.ts
import { create } from 'zustand';

interface SessionsState {
  sessions: Session[];
  loading: boolean;
  error: string | null;
  fetchSessions: () => Promise<void>;
  setSessions: (sessions: Session[]) => void;
}

export const useSessionsStore = create<SessionsState>((set) => ({
  sessions: [],
  loading: false,
  error: null,
  fetchSessions: async () => {
    set({ loading: true });
    try {
      const response = await sessionsService.list({});
      set({ sessions: response.data, loading: false });
    } catch (error) {
      set({ error: 'Failed to fetch sessions', loading: false });
    }
  },
  setSessions: (sessions) => set({ sessions }),
}));
```

### Local State (Component Level)

Cada componente maneja su propio estado local para UI específica:

```typescript
const DocumentDetail: React.FC<{id: string}> = ({ id }) => {
  const [document, setDocument] = useState<Document | null>(null);
  const [snapshots, setSnapshots] = useState<DocumentSnapshot[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Lógica del componente...
};
```

---

## 5. Integración con API

### API Client (Axios)

```typescript
// services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
});

// Interceptor para agregar token de autenticación
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirigir a login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### Servicios de API

```typescript
// services/documents.ts
import api from './api';

export const documentsService = {
  async list(params: DocumentListParams) {
    const response = await api.get('/documents', { params });
    return response.data;
  },
  
  async get(id: string) {
    const response = await api.get(`/documents/${id}`);
    return response.data;
  },
  
  async create(data: CreateDocumentDto) {
    const response = await api.post('/documents', data);
    return response.data;
  },
  
  async update(id: string, data: UpdateDocumentDto) {
    const response = await api.put(`/documents/${id}`, data);
    return response.data;
  },
  
  async delete(id: string) {
    const response = await api.delete(`/documents/${id}`);
    return response.data;
  },
  
  async getSnapshots(id: string) {
    const response = await api.get(`/documents/${id}/snapshots`);
    return response.data;
  },
  
  async restoreSnapshot(documentId: string, snapshotId: string) {
    const response = await api.post(
      `/documents/${documentId}/snapshots/${snapshotId}/restore`
    );
    return response.data;
  },
};
```

```typescript
// services/sessions.ts
import api from './api';

export const sessionsService = {
  async list(params: SessionListParams) {
    const response = await api.get('/sessions', { params });
    return response.data;
  },
  
  async get(id: string) {
    const response = await api.get(`/sessions/${id}`);
    return response.data;
  },
  
  async create(data: CreateSessionDto) {
    const response = await api.post('/sessions', data);
    return response.data;
  },
  
  async getGaps(sessionId: string, params: GapListParams) {
    const response = await api.get(`/sessions/${sessionId}/gaps`, { params });
    return response.data;
  },
  
  async getGapGroups(sessionId: string) {
    const response = await api.get(`/sessions/${sessionId}/gap-groups`);
    return response.data;
  },
  
  async answerGap(sessionId: string, gapId: string, answer: string) {
    const response = await api.post(
      `/sessions/${sessionId}/gaps/${gapId}/answer`,
      { answer }
    );
    return response.data;
  },
  
  async complete(sessionId: string) {
    const response = await api.post(`/sessions/${sessionId}/complete`);
    return response.data;
  },
  
  async getContextEntries(sessionId: string) {
    const response = await api.get(`/sessions/${sessionId}/context-entries`);
    return response.data;
  },
};
```

---

## 6. Sistema de Diseño

El sistema de diseño del frontend se basa en shadcn/ui como biblioteca principal de componentes, proporcionando una base consistente y moderna para la interfaz de usuario.

### Biblioteca de Componentes

- **shadcn/ui**: Componentes copiados directamente al proyecto, ofreciendo full control sobre el código, diseño moderno, y perfecta integración con TailwindCSS. Esta aproximación permite personalización completa sin dependencias externas opacas.

### Design Tokens

- **Paleta de colores**: Sistema de colores consistente para estados (primary, secondary, success, error, warning) y elementos de UI
- **Tipografía**: Escala tipográfica definida para headings, body text, y captions
- **Espaciado**: Scale de 4px para mantener consistencia en márgenes y padding (4px, 8px, 12px, 16px, 24px, 32px, etc.)

### Consistencia Visual

Para MVP Bootstrapped, la consistencia se mantiene mediante convenciones de código y patrones de uso de componentes, sin herramientas adicionales de design system management. La estructura de componentes de shadcn/ui proporciona la base para mantener coherencia visual.

**Referencia**: Ver [PRD-003](../../producto/requisitos/prd-003.md) (líneas 526-533) para detalles adicionales sobre sistema de diseño.

---

## 7. UX Patterns

### Responsive Design

La estrategia de responsive design prioriza el soporte para desktop en MVP Bootstrapped, con planes para extender responsividad completa post-MVP.

**Breakpoints de Diseño**:
- **Desktop**: > 1024px (prioridad para MVP - desarrollo local)
- **Tablet**: 768px - 1024px (nice-to-have para MVP)
- **Mobile**: < 768px (NO APLICA para MVP Bootstrapped - POST-MVP)

**Prioridad MVP**: El foco principal es desktop para desarrollo local y validación temprana del producto. La responsividad completa (tablet y mobile) se implementará post-MVP cuando se valide problem-solution fit.

**Referencia**: Ver [PRD-003](../../producto/requisitos/prd-003.md) (líneas 390-398) para detalles adicionales sobre responsive design.

### Accesibilidad

La estrategia de accesibilidad busca cumplir con estándares WCAG para asegurar que el frontend sea usable por personas con discapacidades.

**Compliance WCAG**: Nivel AA (objetivo para MVP Bootstrapped)

**Soporte para Navegación por Teclado**:
- Tab navigation entre elementos interactivos
- Focus visible en elementos interactivos
- Atajos de teclado para acciones comunes

**Contraste de Colores**:
- Mínimo 4.5:1 para texto normal (WCAG AA)
- Mínimo 3:1 para texto grande (WCAG AA)
- Verificación de contraste en componentes shadcn/ui

**Texto Alternativo para Imágenes**:
- Alt text descriptivo para imágenes informativas
- Alt text vacío para imágenes decorativas

**Validación**: La accesibilidad completa se validará post-MVP. Para MVP, se seguirán mejores prácticas básicas y se verificará cumplimiento de WCAG AA en componentes críticos.

**Referencia**: Ver [PRD-003](../../producto/requisitos/prd-003.md) (líneas 400-408) para detalles adicionales sobre accesibilidad.

### Flujo de Usuario End-to-End

El frontend habilita workflows típicos que permiten a los usuarios navegar el sistema de manera eficiente. Los workflows principales son:

**Workflow 1: Revisar estado del proyecto via Dashboard**
- Usuario accede al Dashboard
- Ve métricas agregadas (documentos totales, sesiones activas, gaps pendientes)
- Navega a secciones específicas desde el Dashboard

**Workflow 2: Navegar documentos**
- Usuario accede a la Sección de Documentos
- Usa filtros y búsqueda para encontrar documentos específicos
- Ve lista de documentos con estado healthy
- Accede a detalle de documento para ver contenido y snapshots

**Workflow 3: Revisar gaps detectados**
- Usuario accede a la Sección de Gaps
- Ve gaps agrupados por tema
- Revisa contexto faltante identificado para cada gap
- Navega entre grupos de gaps

**Workflow 4: Revisar y aprobar cambios**
- Usuario accede a la Sección de Propuestas
- Ve lista de cambios sugeridos (context_entries)
- Usa diff viewer integrado para comparar old vs new content
- Aprueba o rechaza cambios individuales

**Workflow 5: Navegación rápida**
- Usuario accede desde Dashboard a secciones específicas
- Usa breadcrumbs para navegar jerarquía
- Accede rápidamente a información crítica

**Referencia**: Ver [PRD-003](../../producto/requisitos/prd-003.md) (líneas 45-47) y [FEA-003](../../ingenieria/tareas/epica-03-frontend-react.md) (workflow de 5 fases) para detalles adicionales sobre flujo de usuario.

### Layout y Estructura Visual

El layout del frontend sigue una estructura estándar de aplicación web moderna, optimizada para desktop en MVP Bootstrapped.

**Especificación de Layout**:
- Grid system basado en TailwindCSS para consistencia
- Breakpoints alineados con estrategia de responsive design (desktop >1024px prioritario)

**Estructura de Layout**:
- **Sidebar izquierda**: Navegación principal entre secciones (Dashboard, Documentos, Gaps, Propuestas, Settings)
- **Header superior**: Breadcrumbs para navegación jerárquica, información de usuario, notificaciones
- **Content area**: Área principal para contenido específico de cada sección

**Patrones Visuales**:
- **Hover states**: Feedback visual al pasar cursor sobre elementos interactivos
- **Active states**: Indicación visual de elemento seleccionado o activo
- **Loading states**: Indicadores de carga definidos ad-hoc según necesidad durante implementación
- **Error states**: Mensajes de error definidos ad-hoc según necesidad durante implementación

**Referencia**: Ver [PRD-003](../../producto/requisitos/prd-003.md) (líneas 535-542) para detalles adicionales sobre layout y estructura visual.

### Sesión de Resolución de Gaps

**Flujo de Usuario**:

1. Usuario ve lista de sesiones en Dashboard
2. Usuario hace clic en sesión con estado "awaiting_resolution"
3. Usuario ve lista de grupos de gaps
4. Usuario selecciona un grupo
5. Usuario ve lista de gaps del grupo
6. Usuario selecciona un gap
7. Usuario ve pregunta del gap y contexto faltante
8. Usuario ingresa respuesta o usa sugerencia del Agente 3
9. Usuario envía respuesta
10. Sistema marca gap como respondido
11. Usuario continúa con siguiente gap
12. Cuando todos los gaps del grupo están respondidos, usuario marca grupo como completado
13. Sistema encola job `gap_verification`
14. Si verificación pasa, usuario ve cambios sugeridos
15. Usuario aprueba/rechaza cambios
16. Sistema aplica cambios y marca documento como healthy

**Patrones de UX**:

- **Progressive Disclosure**: Mostrar información gradualmente (grupos → gaps → detalles)
- **Inline Editing**: Editar respuestas directamente en la lista
- **Keyboard Shortcuts**: Enter para enviar respuesta, Esc para cancelar
- **Auto-save**: Guardar respuestas automáticamente mientras el usuario escribe
- **Visual Feedback**: Indicadores de progreso, badges de estado, animaciones de carga

---

### Visualización de Cambios

**Diff Viewer**:

Usar un componente de diff para mostrar cambios sugeridos:

```typescript
import { DiffViewer } from 'react-diff-viewer';

const ContextEntryCard: React.FC<{entry: ContextEntry}> = ({ entry }) => {
  return (
    <div className="context-entry-card">
      <DiffViewer
        oldValue={entry.old_content || ''}
        newValue={entry.new_content}
        splitView={true}
        useDarkTheme={false}
      />
      <div className="actions">
        <button onClick={() => approve(entry.id)}>Approve</button>
        <button onClick={() => reject(entry.id)}>Reject</button>
      </div>
    </div>
  );
};
```

---

### Notificaciones

**Toast Notifications**:

Mostrar notificaciones para eventos importantes:

- Sesión creada exitosamente
- Gap respondido
- Cambios aplicados
- Error en operación

```typescript
import { toast } from 'react-hot-toast';

toast.success('Gap respondido exitosamente');
toast.error('Error al aplicar cambios');
```

---

## 7. Estructura de Proyecto

### Estructura de Directorios

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── DashboardStats.tsx
│   │   │   ├── RecentDocuments.tsx
│   │   │   └── ActiveSessions.tsx
│   │   ├── Documents/
│   │   │   ├── DocumentList.tsx
│   │   │   ├── DocumentDetail.tsx
│   │   │   ├── DocumentViewer.tsx
│   │   │   └── SnapshotHistory.tsx
│   │   ├── Sessions/
│   │   │   ├── SessionList.tsx
│   │   │   ├── SessionView.tsx
│   │   │   ├── GapGroupList.tsx
│   │   │   ├── GapResolutionPanel.tsx
│   │   │   └── ContextEntriesView.tsx
│   │   └── Common/
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       ├── Badge.tsx
│   │       └── Modal.tsx
│   ├── contexts/
│   │   ├── AppContext.tsx
│   │   └── AuthContext.tsx
│   ├── services/
│   │   ├── api.ts
│   │   ├── documents.ts
│   │   ├── sessions.ts
│   │   └── auth.ts
│   ├── types/
│   │   ├── document.ts
│   │   ├── session.ts
│   │   └── gap.ts
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Documents.tsx
│   │   ├── Sessions.tsx
│   │   └── Settings.tsx
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── public/
├── package.json
├── vite.config.ts
└── tsconfig.json
```

### Configuración de Vite

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
```

---

## Análisis de Documento

**ESTADO DEL ANÁLISIS**

- Análisis previo: NO
- Fecha de análisis: 2026-05-22
- Versión del análisis: 1

**CLASIFICACIÓN DEL DOCUMENTO**

- Tipo: Documento de Diseño
- Rol Principal: Desarrollador Frontend
- Roles a Revisar: Desarrollador Frontend + Diseñador UI/UX (+ Product Manager)
- Enfoque: Especificación de frontend para gestión de documentos, resolución de gaps y monitoreo de pipeline
- Perspectiva: Senior + Junior
- Fecha de análisis: 2026-05-22
- Versión del análisis: 1

### Revisión por Rol: Desarrollador Frontend (Senior)

**Validación de Respuestas Existentes**
El documento define claramente el stack tecnológico (React, Context API/Zustand, Axios, React Router, shadcn/ui/Material-UI, TailwindCSS, Vite), arquitectura de capas (UI, State Management, Service, Data), componentes principales (Dashboard, DocumentList, DocumentDetail, SessionList, SessionView, GapResolutionPanel, ContextEntriesView), y patrones de UX. Incluye estructura de proyecto y ejemplos de API calls.

**Gaps Identificados**

**IMPLEMENTACIÓN TÉCNICA**

**GAP: Decisión entre Context API y Zustand** [PRIORIDAD: Alto] [ESTADO: IMPLEMENTADO]

- **Pregunta**: ¿Por qué la decisión entre Context API y Zustand está pendiente? ¿Qué criterios se usarán para decidir? ¿Cuáles son los trade-offs entre ambos para este proyecto?
- **Contexto faltante**: El documento menciona "Context API o Zustand" pero no proporciona análisis comparativo ni criterios para la decisión de state management.
- **Rol afectado**: Desarrollador Frontend Senior
- **Fecha de identificación**: 2026-05-22
- **Respuesta**: Usar Zustand para MVP (justificado por investigación: ideal para startups/MVPs, overhead mínimo, optimización automática de performance, bundle size ~1KB). Estado global: user (auth), documents (lista), sessions (activas), loading/error globales. Local: estado de componentes específicos (filtros, modales, forms). Patrones: Zustand stores separados por dominio (authStore, documentsStore, sessionsStore).
- **Referencia**: PRD-003 (líneas 515-522)
- **Fecha de resolución**: 2026-06-05

**GAP: Estrategia de manejo de estado offline** [PRIORIDAD: Alto] [ESTADO: PENDIENTE]

- **Pregunta**: ¿Cómo se maneja el estado cuando el usuario está offline? ¿Hay cache local? ¿Cómo se sincroniza cuando se reconecta? ¿Qué estrategia de optimistic updates se usa?
- **Contexto faltante**: No hay información sobre manejo de estado offline, cache local, o sincronización cuando el usuario se desconecta/reconecta.
- **Rol afectado**: Desarrollador Frontend Senior
- **Fecha de identificación**: 2026-05-22

**GAP: Estrategia de performance y lazy loading** [PRIORIDAD: Medio] [ESTADO: PENDIENTE]

- **Pregunta**: ¿Qué estrategia de lazy loading se usa para rutas y componentes? ¿Cómo se optimiza el bundle size? ¿Hay code splitting por ruta?
- **Contexto faltante**: No hay información sobre lazy loading, code splitting, optimización de bundle, o estrategia de performance del frontend.
- **Rol afectado**: Desarrollador Frontend Senior
- **Fecha de identificación**: 2026-05-22

### Revisión por Rol: Desarrollador Frontend (Junior)

**Gaps Identificados**

**IMPLEMENTACIÓN TÉCNICA**

**GAP: Explicación de React Context vs Zustand** [PRIORIDAD: Medio] [ESTADO: IMPLEMENTADO]

- **Pregunta**: ¿Qué es React Context y qué es Zustand? ¿Cuándo se usa uno vs el otro? ¿Cuáles son las ventajas y desventajas de cada uno?
- **Contexto faltante**: El documento menciona ambas opciones pero no explica qué son, cuándo es apropiado usar cada una, o las diferencias entre ellas.
- **Rol afectado**: Desarrollador Frontend Junior
- **Fecha de identificación**: 2026-05-22
- **Respuesta**: Zustand seleccionado para MVP por overhead mínimo, optimización automática de performance, bundle size ~1KB. Context API es la alternativa nativa de React pero puede causar re-renders innecesarios. Zustand es ideal para startups/MVPs.
- **Referencia**: PRD-003 (líneas 515-522)
- **Fecha de resolución**: 2026-06-05

**GAP: Explicación de shadcn/ui vs Material-UI** [PRIORIDAD: Bajo] [ESTADO: IMPLEMENTADO]

- **Pregunta**: ¿Qué es shadcn/ui y qué es Material-UI? ¿Por qué se mencionan ambos? ¿Cuál se elige y por qué?
- **Contexto faltante**: El documento menciona ambas librerías de UI pero no explica qué son, por qué se mencionan ambas, o cuál se elige para el proyecto.
- **Rol afectado**: Desarrollador Frontend Junior
- **Fecha de identificación**: 2026-05-22
- **Respuesta**: shadcn/ui seleccionado (componentes copiados al proyecto, full control, moderno, integración con TailwindCSS). Material-UI es la alternativa mencionada pero no seleccionada.
- **Referencia**: PRD-003 (líneas 526-533)
- **Fecha de resolución**: 2026-06-05

### Revisión por Rol: Diseñador UI/UX (Senior)

**Validación de Respuestas Existentes**
El documento define patrones de UX (progressive disclosure, inline editing, diff viewer, notifications), componentes principales, y flujo de navegación. Incluye descripciones de estados de componentes y UX patterns.

**Gaps Identificados**

**DISEÑO DE INTERFAZ**

**GAP: Sistema de diseño y design tokens** [PRIORIDAD: Alto] [ESTADO: IMPLEMENTADO]

- **Pregunta**: ¿Hay un sistema de diseño definido? ¿Qué design tokens se usan (colores, tipografía, espaciado)? ¿Cómo se mantiene consistencia visual entre componentes?
- **Contexto faltante**: No hay información sobre sistema de diseño, design tokens, o guía de estilo visual para mantener consistencia.
- **Rol afectado**: Diseñador UI/UX Senior
- **Fecha de identificación**: 2026-05-22
- **Respuesta**: Biblioteca: shadcn/ui (componentes copiados al proyecto, full control, moderno, integración con TailwindCSS). Tokens: paleta de colores + tipografía + espaciado (scale de 4px). Consistencia: solo convenciones de código sin herramientas adicionales para MVP.
- **Referencia**: PRD-003 (líneas 526-533)
- **Fecha de resolución**: 2026-06-05

**GAP: Estrategia de responsive design** [PRIORIDAD: Alto] [ESTADO: IMPLEMENTADO]

- **Pregunta**: ¿Cómo se adapta la UI a diferentes tamaños de pantalla (mobile, tablet, desktop)? ¿Qué breakpoints se usan? ¿Hay wireframes para diferentes viewports?
- **Contexto faltante**: No hay información sobre responsive design, breakpoints, o adaptación de la UI a diferentes tamaños de pantalla.
- **Rol afectado**: Diseñador UI/UX Senior
- **Fecha de identificación**: 2026-05-22
- **Respuesta**: Soporte para desktop: > 1024px (prioridad para MVP). Soporte para tablet: 768px - 1024px (nice-to-have para MVP). Soporte para mobile: < 768px (NO APLICA para MVP Bootstrapped - POST-MVP). Breakpoints de diseño: desktop (>1024px), tablet (768-1024px), mobile (<768px). Para MVP Bootstrapped, el foco es desktop para desarrollo local. Responsividad completa se implementará post-MVP.
- **Referencia**: PRD-003 (líneas 390-398)
- **Fecha de resolución**: 2026-06-05

**GAP: Accesibilidad y WCAG compliance** [PRIORIDAD: Medio] [ESTADO: IMPLEMENTADO]

- **Pregunta**: ¿Qué nivel de WCAG compliance se busca? ¿Cómo se maneja accesibilidad (keyboard navigation, screen readers, contrast ratios)? ¿Hay herramientas de testing de accesibilidad?
- **Contexto faltante**: No hay información sobre accesibilidad, WCAG compliance, o estrategias para soportar usuarios con discapacidades.
- **Rol afectado**: Diseñador UI/UX Senior
- **Fecha de identificación**: 2026-05-22
- **Respuesta**: Compliance WCAG: Nivel AA (objetivo para MVP Bootstrapped). Soporte para navegación por teclado: Tab navigation entre elementos interactivos. Contraste de colores: Mínimo 4.5:1 para texto normal, 3:1 para texto grande (WCAG AA). Texto alternativo para imágenes: Alt text descriptivo para imágenes informativas. Accesibilidad completa se validará post-MVP. Para MVP, seguir mejores prácticas básicas.
- **Referencia**: PRD-003 (líneas 400-408)
- **Fecha de resolución**: 2026-06-05

### Revisión por Rol: Diseñador UI/UX (Junior)

**Gaps Identificados**

**DISEÑO DE INTERFAZ**

**GAP: Wireframes y mockups** [PRIORIDAD: Alto] [ESTADO: IMPLEMENTADO]

- **Pregunta**: ¿Dónde están los wireframes o mockups de los componentes principales? ¿Hay prototipos interactivos para validar el diseño?
- **Contexto faltante**: El documento describe componentes pero no incluye wireframes, mockups, o prototipos visuales de la UI.
- **Rol afectado**: Diseñador UI/UX Junior
- **Fecha de identificación**: 2026-05-22
- **Respuesta**: Especificación: solo especificación de layout (grid system, breakpoints) sin wireframes específicos para MVP. Estructura: layout estándar con sidebar izquierda (navegación) + header superior (breadcrumbs, user) + content area. Patrones: solo hover y active states para MVP, loading/error states se definen ad-hoc.
- **Referencia**: PRD-003 (líneas 535-542)
- **Fecha de resolución**: 2026-06-05

**GAP: Explicación de patrones de UX** [PRIORIDAD: Medio] [ESTADO: NO APLICA]

- **Pregunta**: ¿Qué es progressive disclosure y por qué se usa? ¿Qué es inline editing y cuándo es apropiado? ¿Cómo se diseñan notificaciones efectivas?
- **Contexto faltante**: El documento menciona patrones de UX pero no explica qué son, por qué se usan, o cómo se implementan correctamente.
- **Rol afectado**: Diseñador UI/UX Junior
- **Fecha de identificación**: 2026-05-22
- **Respuesta**: Estos son conceptos estándar de UX/UI que se consideran conocimiento básico del dominio. Progressive disclosure, inline editing, y notificaciones son patrones bien documentados en la industria. No es responsabilidad de este documento de especificación técnica explicar conceptos fundamentales de UX.
- **Fecha de resolución**: 2026-06-05

### Revisión por Rol: Product Manager (Senior)

**Validación de Respuestas Existentes**
El documento define el propósito del frontend (Dashboard, Session Resolution, Document Editor), flujo de navegación, y componentes principales. Hay descripciones de funcionalidades de cada componente.

**Gaps Identificados**

**NEGOCIO Y PRODUCTO**

**GAP: User personas y casos de uso** [PRIORIDAD: Alto] [ESTADO: IMPLEMENTADO]

- **Pregunta**: ¿Quiénes son los usuarios principales del frontend? ¿Qué personas se han definido? ¿Qué casos de uso clave se soportan?
- **Contexto faltante**: No hay información sobre user personas, casos de uso específicos, o quién es el usuario objetivo del frontend.
- **Rol afectado**: Product Manager Senior
- **Fecha de identificación**: 2026-05-22
- **Respuesta**: User personas definidas en FEA-003: CTO/VP Engineering, Senior Developer/Tech Lead, DevOps/SRE, Arquitecto Senior. Casos de uso: Revisar estado del proyecto via Dashboard, Navegar documentos, Revisar gaps detectados, Revisar y aprobar cambios, Navegación rápida (PRD-003 líneas 45-47).
- **Referencia**: PRD-003 (líneas 45-47), FEA-003 (líneas 37-40, 77-80, 116-120, 156-160, 194-198)
- **Fecha de resolución**: 2026-06-05

**GAP: Priorización de features** [PRIORIDAD: Medio] [ESTADO: IMPLEMENTADO]

- **Pregunta**: ¿Qué features son MVP vs roadmap futuro? ¿Cómo se priorizan las funcionalidades del frontend? ¿Qué se incluye en la primera versión?
- **Contexto faltante**: No hay información sobre priorización de features, MVP vs roadmap, o qué funcionalidades se incluyen en la primera versión.
- **Rol afectado**: Product Manager Senior
- **Fecha de identificación**: 2026-05-22
- **Respuesta**: MVP esenciales para dogfooting: Estructura base, Routing, Cliente HTTP, State management, Dashboard, Sección de Documentos, Sección de Gaps, Sección de Propuestas, Diff Viewer. Features que pueden postponerse: Sección de Grafo (nice-to-have), Sección de Preguntas (depende de backend Hito 4), Interfaz de Sesión Interactiva (POST-MVP). Referencia: EPC-003 (líneas 75-92).
- **Referencia**: EPC-003 (líneas 75-92), PRD-003 (líneas 86-92)
- **Fecha de resolución**: 2026-06-05

**GAP: Métricas de éxito del frontend** [PRIORIDAD: Medio] [ESTADO: IMPLEMENTADO]

- **Pregunta**: ¿Qué métricas se usan para medir el éxito del frontend (engagement, time to resolution, error rates)? ¿Cómo se trackea el uso de features?
- **Contexto faltante**: No hay información sobre métricas de éxito, analytics, o cómo se mide la efectividad del frontend.
- **Rol afectado**: Product Manager Senior
- **Fecha de identificación**: 2026-05-22
- **Respuesta**: Para MVP Bootstrapped, el enfoque es funcionalidad básica sobre métricas cuantitativas. El dogfooting temprano se validará cualitativamente mediante feedback en retrospectivas de desarrollo. Métricas de éxito formales (adopción, satisfacción, KPIs) se definirán post-MVP cuando se valide problem-solution fit. Métricas cualitativas: tiempo promedio para encontrar información + satisfacción subjetiva (escala 1-10) + fricciones percibidas. Umbrales: satisfacción ≥ 7/10 + reducción de fricciones ≥ 30% en 3 meses.
- **Referencia**: PRD-003 (líneas 72-78, 495-502)
- **Fecha de resolución**: 2026-06-05

### Revisión por Rol: Product Manager (Junior)

**Gaps Identificados**

**NEGOCIO Y PRODUCTO**

**GAP: Flujo de usuario end-to-end** [PRIORIDAD: Medio] [ESTADO: IMPLEMENTADO]

- **Pregunta**: ¿Cuál es el flujo completo de un usuario desde login hasta resolución de un gap? ¿Qué pasos sigue? ¿Dónde pueden haber fricciones?
- **Contexto faltante**: El documento describe componentes individuales pero no el flujo completo de usuario end-to-end a través del sistema.
- **Rol afectado**: Product Manager Junior
- **Fecha de identificación**: 2026-05-22
- **Respuesta**: Workflows típicos habilitados por el frontend React: (1) Revisar estado del proyecto via Dashboard con métricas agregadas, (2) Navegar documentos via Sección de Documentos con filtros y búsqueda, (3) Revisar gaps detectados via Sección de Gaps con agrupación por tema, (4) Revisar y aprobar cambios via Sección de Propuestas con diff viewer integrado, (5) Navegación rápida desde Dashboard a secciones específicas. Flujo detallado de 5 fases en FEA-003.
- **Referencia**: PRD-003 (líneas 45-47), FEA-003 (workflow de 5 fases)
- **Fecha de resolución**: 2026-06-05

**GAP: Escenarios de edge cases en UX** [PRIORIDAD: Bajo] [ESTADO: NO APLICA]

- **Pregunta**: ¿Cómo se manejan edge cases en la UX (documentos muy largos, muchos gaps, errores de API, sesiones expiradas)? ¿Qué mensajes se muestran?
- **Contexto faltante**: No hay información sobre manejo de edge cases en la UX, mensajes de error, o comportamiento en situaciones excepcionales.
- **Rol afectado**: Product Manager Junior
- **Fecha de identificación**: 2026-05-22
- **Respuesta**: PRD-003 define manejo de errores de API (401: redirigir a login, 500: mostrar error genérico, 404: mostrar not found) y estados de carga/error. Edge cases específicos se definirán durante implementación según necesidad. Este nivel de detalle es apropiado para fase de implementación, no para especificación de alto nivel.
- **Referencia**: PRD-003 (líneas 353-355, 386)
- **Fecha de resolución**: 2026-06-05

### CALIFICACIÓN DEL DOCUMENTO: 9/10

**Fecha de Reevaluación**: 2026-06-06
**Versión del Análisis**: 3

**Desglose**:

- Completitud de Respuestas: 9/10 - Cubre stack tecnológico con decisiones implementadas (Zustand, shadcn/ui), arquitectura de capas, componentes principales, patrones de UX, sistema de diseño, responsive design, accesibilidad, user personas, casos de uso, priorización de features, métricas de éxito, y flujo de usuario end-to-end. Las 11 respuestas de gaps han sido integradas en el contenido principal.
- Contexto Multi-Rol: 9/10 - Proporciona contexto técnico completo para desarrolladores frontend (Zustand stores, API services). Contexto para Diseñador UI/UX (sistema de diseño, responsive design, accesibilidad, layout) y Product Manager (user personas, casos de uso, priorización, métricas) integrado directamente en el documento con referencias a PRD-003, EPC-003, y FEA-003.
- Calidad de Referencias: 9/10 - Referencias a otros documentos de arquitectura son relevantes. Referencias cruzadas con PRD-003, EPC-003, y FEA-003 proporcionan contexto completo para roles funcionales.
- Estructura y Organización: 9/10 - Estructura clara con índice actualizado, secciones bien organizadas incluyendo nuevas secciones (Sistema de Diseño, User Personas, Casos de Uso, Priorización de Features, Métricas de Éxito, Flujo de Usuario End-to-End, Layout y Estructura Visual).
- Consistencia: 9/10 - No se detectaron contradicciones, la especificación es consistente con el API, el pipeline descrito, y documentos relacionados (PRD-003, EPC-003, FEA-003). Las decisiones técnicas (Zustand, shadcn/ui) están consistentemente aplicadas en todo el documento.

**Resumen**: Especificación de frontend completa con definición clara de stack tecnológico (Zustand, shadcn/ui), arquitectura de capas, componentes principales, patrones de UX, sistema de diseño, responsive design, accesibilidad, user personas, casos de uso, priorización de features, métricas de éxito, flujo de usuario end-to-end, y layout visual. Las 11 respuestas de gaps han sido integradas en el contenido principal, proporcionando contexto completo para todos los roles relevantes. El documento está en su forma final y es útil para implementación con trazabilidad completa con PRD-003, EPC-003, y FEA-003.

---

## Referencias

- **[api-specification.md](api-specification.md)**: Especificación de API REST
- **[end-to-end-flow.md](end-to-end-flow.md)**: Flujo del pipeline
- **[technology-stack.md](technology-stack.md)**: Stack tecnológico
- **[database-schema-design.md](database-schema-design.md)**: Diseño conceptual de esquema de base de datos

---

*Documento generado como parte de [ARC-004](database-schema-design.md).*
*Fecha de creación: 2026-05-22.*
