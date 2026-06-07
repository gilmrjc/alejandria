---
id: ARC-020
type: Architecture
related:
  - target: ADR-009
    relationship_type: references
    reason: Referencia la estrategia de testing Python para alineación de objetivos
  - target: ARC-008
    relationship_type: implements
    reason: Implementa la estrategia de testing para el frontend especificado en frontend-specification.md
  - target: ARC-018
    relationship_type: extends
    reason: Extiende la testing-strategy.md general con detalles específicos de frontend
---

# Frontend Testing Strategy — Alejandria

Este documento define la estrategia de testing para el frontend de Alejandria (React + Vitest + React Testing Library).

## Contexto y Problema

El frontend de Alejandria requiere una estrategia de testing para asegurar calidad del código mientras se mantiene un ciclo de desarrollo rápido. El sistema necesita:

- Cobertura de código alta para asegurar calidad de componentes React
- Testing de componentes con estado y hooks complejos
- Testing de integración con API backend
- Testing de routing y navegación
- Ejecución rápida de tests para desarrollo iterativo

El stack incluye React con hooks, Zustand para state management, y Axios para API calls, lo que requiere una estrategia de testing adaptada a estos componentes.

## Decisiones

**Decisión**: Usar estrategia de testing híbrida con Vitest, React Testing Library, y mocks para servicios externos.

**Stack de testing**:

- **Vitest**: Framework de testing principal (compatible con Vite)
- **React Testing Library**: Testing de componentes React
- **@testing-library/jest-dom**: Matchers mejorados para DOM
- **@testing-library/user-event**: Simulación de eventos de usuario
- **vitest-coverage-v8**: Medición de cobertura de código

**Distribución de tests**:

- **Unit tests (70%)**: Lógica de hooks, servicios, stores sin dependencias externas
- **Component tests (20%)**: Componentes React con mocks de servicios y stores
- **Integration tests (10%)**: Flujos completos con routing y navegación

**Cobertura objetivo**: 80%+ (vs 90%+ para backend Python, ya que UI es más dinámica y tiene más branches visuales)

**Configuración Vitest** (`vitest.config.ts`):

```typescript
coverage: {
  provider: 'v8',
  include: ['src/**/*.{ts,tsx}'],
  reporter: ['text', 'json', 'html'],
  exclude: [
    'node_modules/',
    'src/test/',
    '**/*.d.ts',
    '**/*.config.*',
    '**/mockData.ts',
    'src/**/*.test.{ts,tsx}',
    'src/**/*.stories.{ts,tsx}',
    'src/main.tsx',
    'src/vite-env.d.ts',
  ],
  thresholds: {
    lines: 80,
    functions: 80,
    branches: 75,
    statements: 80
  }
}
```

## Justificación

### Ventajas de la Estrategia Propuesta

**Enfoque híbrido**:

- Unit tests rápidos (<100ms cada uno) para feedback rápido en desarrollo
- Component tests con RTL para validar comportamiento de UI
- Integration tests limitados a flujos críticos sin overhead excesivo

**Testing de componentes React**:

- React Testing Library promueve testing de comportamiento vs implementación
- Testing de hooks personalizados con @testing-library/react-hooks
- Mocking de servicios y stores para aislar componentes

**Cobertura alta (80%+)**:

- Asegura que la mayoría del código está testeado
- vitest-coverage-v8 genera reportes detallados de cobertura
- CI/CD puede fallar si cobertura cae debajo de 80%
- Objetivo más bajo que backend (90%+) por naturaleza más dinámica de UI

### Testing por Componente

**Servicios (src/services/)**:

- Unit tests: métodos con mocks de axios
- Testing de error handling y retry logic
- Testing de interceptors (auth, error responses)

**Stores (src/stores/)**:

- Unit tests: actions con mocks de servicios
- Testing de state transitions (loading → success/error)
- Testing de localStorage persistence (authStore)

**Componentes UI (src/components/)**:

- Component tests: render con props, user interactions
- Mocking de stores y servicios
- Testing de loading, error, and empty states

**Páginas (src/pages/)**:

- Component tests: render con routing
- Mocking de stores y navigation
- Testing de protected routes (RequireAuth)

**Hooks (src/hooks/)**:

- Unit tests: hooks con @testing-library/react-hooks
- Testing de return values y side effects

### Alineación con ADR-009

**Stack Python vs Frontend**:

- ADR-009 define pytest para backend con 90%+ cobertura
- Esta estrategia define Vitest para frontend con 80%+ cobertura
- Diferencia justificada por naturaleza más dinámica de UI y branches visuales
- Ambos enfatizan unit tests rápidos y coverage alta

**Patrones similares**:

- Ambos usan mocks para dependencias externas
- Ambos priorizan unit tests sobre integration tests
- Ambos configuran CI/CD para fallar si cobertura cae debajo del umbral

## Trade-offs

### Desventajas

- **Tiempo de ejecución**: Component tests con RTL son más lentos que unit tests puros
- **Curva de aprendizaje**: React Testing Library requiere aprender patrones específicos

### Mitigación

- **Ejecución selectiva**: Permitir ejecutar solo unit tests en desarrollo rápido
- **Documentación de patrones**: Documentar patrones de testing en este documento

## Detalles de Implementación

### Unit Tests

**Características**:

- <100ms de ejecución por test
- Mocks de todas las dependencias externas (axios, stores, services)
- Testing de lógica pura (hooks, servicios, stores)

**Ejemplo de unit test para servicio**:

```typescript
// src/services/__tests__/documents.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { documentsService } from '../documents';
import api from './api';

vi.mock('./api');

describe('documentsService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debe llamar api.get con parámetros correctos en list', async () => {
    const mockResponse = { data: { items: [], total: 0 } };
    vi.mocked(api.get).mockResolvedValue(mockResponse);

    await documentsService.list({ page: 1, per_page: 10 });

    expect(api.get).toHaveBeenCalledWith('/documents', { params: { page: 1, per_page: 10 } });
  });

  it('debe manejar error en list', async () => {
    vi.mocked(api.get).mockRejectedValue(new Error('API Error'));

    await expect(documentsService.list({})).rejects.toThrow('API Error');
  });
});
```

**Ejemplo de unit test para store**:

```typescript
// src/stores/__tests__/documentsStore.test.ts
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useDocumentsStore } from '../documentsStore';
import { documentsService } from '@/services/documents';

vi.mock('@/services/documents');

describe('documentsStore', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debe tener estado inicial correcto', () => {
    const store = useDocumentsStore.getState();
    expect(store.documents).toEqual([]);
    expect(store.loading).toBe(false);
    expect(store.error).toBeNull();
  });

  it('debe actualizar loading a true al llamar fetchDocuments', async () => {
    vi.mocked(documentsService.list).mockImplementation(() => new Promise(() => {}));

    const store = useDocumentsStore.getState();
    const fetchPromise = store.fetchDocuments();
    const updatedStore = useDocumentsStore.getState();
    
    expect(updatedStore.loading).toBe(true);

    // Clean up
    vi.mocked(documentsService.list).mockResolvedValue({ items: [], total: 0 });
    await fetchPromise.catch(() => {});
  });

  it('debe actualizar documents al fetch exitoso', async () => {
    const mockResponse = { items: [{ id: '1', title: 'Test' }], total: 1 };
    vi.mocked(documentsService.list).mockResolvedValue(mockResponse);

    const store = useDocumentsStore.getState();
    await store.fetchDocuments();
    const updatedStore = useDocumentsStore.getState();

    expect(updatedStore.documents).toEqual(mockResponse.items);
    expect(updatedStore.loading).toBe(false);
  });
});
```

### Component Tests

**Características**:

- Testing de comportamiento de componentes (render, user interactions)
- Mocks de stores y servicios
- Testing de loading, error, and empty states
- Usar React Testing Library patterns (queries, userEvent)

**Ejemplo de component test**:

```typescript
// src/components/documents/__tests__/DocumentFilters.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { DocumentFilters } from '../DocumentFilters';

describe('DocumentFilters', () => {
  it('debe renderizar input de búsqueda con placeholder correcto', () => {
    render(<DocumentFilters search="" onSearchChange={vi.fn()} onClear={vi.fn()} />);
    expect(screen.getByPlaceholderText('Buscar documentos...')).toBeInTheDocument();
  });

  it('debe llamar onSearchChange cuando input cambia', () => {
    const onSearchChange = vi.fn();
    render(<DocumentFilters search="" onSearchChange={onSearchChange} onClear={vi.fn()} />);
    
    const input = screen.getByPlaceholderText('Buscar documentos...');
    fireEvent.change(input, { target: { value: 'test' } });
    
    expect(onSearchChange).toHaveBeenCalledWith('test');
  });
});
```

### Integration Tests

**Características**:

- Flujos completos con routing y navegación
- Mocking de API responses
- Testing de protected routes
- 10% del total de tests

**Ejemplo de integration test**:

```typescript
// src/pages/__tests__/integration/login-flow.test.tsx
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { App } from '@/App';
import { useAuthStore } from '@/stores/authStore';

vi.mock('@/services/auth');

describe('Login Flow Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    useAuthStore.setState({ user: null, loading: false, error: null });
  });

  it('debe redirigir a login cuando no hay usuario', async () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(window.location.pathname).toBe('/login');
    });
  });
});
```

## Convenciones de Testing

### Nomenclatura

- **Archivos de test**: `__tests__/nombre.test.ts` o `nombre.test.tsx`
- **Descripciones**: En español, claro y descriptivo
- **Patrón**: "debe [acción] cuando [condición]"

```typescript
it('debe actualizar loading a true al llamar fetchDocuments', async () => { ... });
it('debe mostrar mensaje de error cuando fetch falla', async () => { ... });
it('debe renderizar lista de documentos cuando hay datos', () => { ... });
```

### Estructura de Tests

```typescript
describe('Componente/Funcionalidad', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Reset stores si es necesario
  });

  it('debe tener estado inicial correcto', () => { ... });

  it('debe actualizar loading state', async () => { ... });

  it('debe manejar éxito', async () => { ... });

  it('debe manejar error', async () => { ... });
});
```

### Mocking

```typescript
// Mock de servicios
vi.mock('@/services/documents');

// Mock de stores
vi.mock('@/stores/authStore');

// Mock de axios
vi.mock('axios');
```

## Alternativas Consideradas

### Solo Component Tests

**Ventaja**: Testing de comportamiento real de UI

**Desventaja**: Más lento, no aísla lógica de negocio

**Decisión**: Rechazada porque unit tests de servicios/stores son más rápidos y aíslan mejor lógica

### Jest en lugar de Vitest

**Ventaja**: Más maduro, más plugins

**Desventaja**: No integrado nativamente con Vite, configuración más compleja

**Decisión**: Rechazada porque Vitest es nativo de Vite y más rápido

## Consecuencias

### Impacto Positivo

- **Cobertura alta**: 80%+ asegura calidad de código
- **Feedback rápido**: Unit tests <100ms permiten desarrollo iterativo
- **Patrones consistentes**: Convenciones claras facilitan onboarding
- **Integración con Vite**: Vitest es nativo y rápido

### Impacto Negativo

- **Curva de aprendizaje**: React Testing Library requiere aprender patrones específicos
- **Tiempo de setup**: Configuración inicial de mocks y fixtures

### Requerimientos de Implementación

- Configurar Vitest con thresholds de cobertura (80%+)
- Crear estructura de directorios de tests (src/**/__tests__/)
- Implementar tests para servicios (prioridad alta)
- Implementar tests para stores (prioridad alta)
- Implementar tests para componentes (prioridad media)
- Implementar tests para páginas (prioridad media)
- Documentar patrones de testing en este documento
- Configurar CI/CD para ejecutar tests con coverage

## Referencias

- ADR-009: Python Testing Strategy (para alineación de objetivos)
- ARC-008: Frontend Specification (stack tecnológico)
- Vitest documentation: <https://vitest.dev/>
- React Testing Library documentation: <https://testing-library.com/react>
