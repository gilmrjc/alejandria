# Plan de Mejora de Cobertura de Tests - Frontend

## Estado Actual

**Cobertura Global:** 8.36% (objetivo: 80%+)

### Cobertura por Área
- **Servicios (src/services/):** 0% (tests existen pero no generan cobertura)
- **Stores (src/stores/):** 0% (tests existen pero no generan cobertura)
- **Componentes (src/components/):** 30.43% promedio
  - DocumentList: 100%
  - GapCard: 100%
  - ProposalCard: 100%
  - GapPriorityBadge: 100%
  - Badge: 100%
  - Button: 66.66%
  - Card: 88.88%
  - DocumentFilters: 0%
  - GapFilters: 0%
  - ProposalFilters: 0%
  - GapList: 0%
  - ProposalList: 0%
  - GapResolutionPanel: 0%
  - ProposalActions: 0%
  - DocumentMetadata: 0%
  - SnapshotHistory: 0%
  - AppLayout: 0%
- **Páginas (src/pages/):** 0%
- **Hooks (src/hooks/):** 0%
- **UI Components (src/components/ui/):** 74.19% promedio
  - Input: 0%
  - Textarea: 0%

## Contradicciones y Ambigüedades Detectadas

### 1. Tests Existentes con 0% Cobertura
**Problema:** Los tests para servicios y stores existen pero reportan 0% cobertura en el reporte.

**Archivos afectados:**
- `src/services/__tests__/api.test.ts` (existe, 0% cobertura)
- `src/services/__tests__/auth.test.ts` (existe, 0% cobertura)
- `src/services/__tests__/documents.test.ts` (existe, 0% cobertura)
- `src/services/__tests__/gaps.test.ts` (existe, 0% cobertura)
- `src/services/__tests__/organizations.test.ts` (existe, 0% cobertura)
- `src/services/__tests__/projects.test.ts` (existe, 0% cobertura)
- `src/services/__tests__/proposals.test.ts` (existe, 0% cobertura)
- `src/stores/__tests__/authStore.test.ts` (existe, 0% cobertura)
- `src/stores/__tests__/documentsStore.test.ts` (existe, 0% cobertura)
- `src/stores/__tests__/gapsStore.test.ts` (existe, 0% cobertura)
- `src/stores/__tests__/organizationsStore.test.ts` (existe, 0% cobertura)
- `src/stores/__tests__/projectsStore.test.ts` (existe, 0% cobertura)
- `src/stores/__tests__/proposalsStore.test.ts` (existe, 0% cobertura)

**Acción requerida:** Investigar por qué los tests no generan cobertura. Posibles causas:
- Configuración incorrecta de vitest.config.ts
- Los tests no se están ejecutando
- Problema con el provider de cobertura v8
- Los archivos de test no están siendo detectados por el coverage tool

### 2. Diferencia en Thresholds de Branches
**Documentación ARC-019:** Especifica 75% para branches
**vitest.config.ts actual:** Configurado con 85% para branches

**Recomendación:** Alinear con la documentación (75%) o actualizar la documentación si el 85% es intencional.

### 3. Duplicación de ID en Documentación
**Lint warning:** ID duplicado "ARC-019" encontrado en 2 documentos:
- `docs/ingenieria/arquitectura/concurrency-control-strategy.md`
- `docs/ingenieria/arquitectura/frontend-testing-strategy.md`

**Acción requerida:** Corregir el ID duplicado en uno de los documentos.

## Plan de Mejora Priorizado

### Fase 1: Investigación y Corrección de Issues Críticos (Prioridad ALTA)

#### 1.1 Investigar Tests con 0% Cobertura
**Objetivo:** Determinar por qué los tests existentes no generan cobertura

**Acciones:**
1. Verificar que los tests se ejecutan correctamente sin coverage
2. Revisar configuración de vitest.config.ts
3. Verificar que los archivos de test están en el path correcto
4. Revisar si hay algún problema con el provider v8
5. Considerar cambiar a provider 'istanbul' si v8 tiene problemas

**Tiempo estimado:** 2-3 horas

#### 1.2 Corregir ID Duplicado en Documentación
**Objetivo:** Resolver el warning de lint sobre ID duplicado ARC-019

**Acciones:**
1. Revisar ambos documentos con ID ARC-019
2. Asignar un ID único al documento correcto
3. Actualizar referencias si es necesario

**Tiempo estimado:** 30 minutos

#### 1.3 Alinear Thresholds con Documentación
**Objetivo:** Decidir y aplicar el threshold correcto para branches

**Acciones:**
1. Decidir si usar 75% (documentación) o 85% (config actual)
2. Actualizar vitest.config.ts según decisión
3. Documentar la decisión en ARC-019 si se cambia a 85%

**Tiempo estimado:** 30 minutos

### Fase 2: Tests de Servicios (Prioridad ALTA)

**Objetivo:** Alcanzar 90%+ cobertura en servicios (documentado en ARC-019 como prioridad alta)

**Archivos a testear:**
- `src/services/api.ts` (0% → 90%+)
- `src/services/auth.ts` (0% → 90%+)
- `src/services/documents.ts` (0% → 90%+)
- `src/services/gaps.ts` (0% → 90%+)
- `src/services/organizations.ts` (0% → 90%+)
- `src/services/projects.ts` (0% → 90%+)
- `src/services/proposals.ts` (0% → 90%+)

**Estrategia:**
1. Si los tests existentes funcionan después de Fase 1.1, mejorarlos para alcanzar 90%+
2. Si no, crear nuevos tests siguiendo los patrones de ARC-019
3. Mockear axios correctamente
4. Testear todos los métodos: success, error, edge cases

**Patrón de test (según ARC-019):**
```typescript
describe('nombreServicio', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debe llamar api con parámetros correctos', async () => { ... });
  it('debe manejar error', async () => { ... });
  it('debe manejar response vacío', async () => { ... });
});
```

**Tiempo estimado:** 8-10 horas

### Fase 3: Tests de Stores (Prioridad ALTA)

**Objetivo:** Alcanzar 90%+ cobertura en stores (documentado en ARC-019 como prioridad alta)

**Archivos a testear:**
- `src/stores/authStore.ts` (0% → 90%+)
- `src/stores/documentsStore.ts` (0% → 90%+)
- `src/stores/gapsStore.ts` (0% → 90%+)
- `src/stores/organizationsStore.ts` (0% → 90%+)
- `src/stores/projectsStore.ts` (0% → 90%+)
- `src/stores/proposalsStore.ts` (0% → 90%+)

**Estrategia:**
1. Si los tests existentes funcionan después de Fase 1.1, mejorarlos para alcanzar 90%+
2. Si no, crear nuevos tests siguiendo los patrones de ARC-019
3. Mockear servicios correctamente
4. Testear state transitions: loading → success/error
5. Testear localStorage persistence

**Patrón de test (según ARC-019):**
```typescript
describe('nombreStore', () => {
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

**Tiempo estimado:** 8-10 horas

### Fase 4: Tests de Hooks (Prioridad MEDIA)

**Objetivo:** Alcanzar 80%+ cobertura en hooks

**Archivos a testear:**
- `src/hooks/useBreadcrumbs.ts` (0% → 80%+)

**Estrategia:**
1. Usar @testing-library/react-hooks para testing de hooks
2. Testear diferentes rutas y casos edge
3. Mockear useLocation de react-router-dom

**Tiempo estimado:** 2-3 horas

### Fase 5: Tests de Componentes UI (Prioridad MEDIA)

**Objetivo:** Alcanzar 80%+ cobertura en componentes UI

**Archivos a testear:**
- `src/components/ui/input.tsx` (0% → 80%+)
- `src/components/ui/textarea.tsx` (0% → 80%+)
- `src/components/ui/button.tsx` (66.66% → 80%+)
- `src/components/ui/card.tsx` (88.88% → 90%+)

**Estrategia:**
1. Component tests con React Testing Library
2. Testear render con diferentes props
3. Testear user interactions
4. Testear variantes y estados

**Tiempo estimado:** 4-5 horas

### Fase 6: Tests de Componentes de Dominio (Prioridad MEDIA)

**Objetivo:** Alcanzar 80%+ cobertura en componentes de dominio

**Archivos a testear:**
- `src/components/documents/DocumentFilters.tsx` (0% → 80%+)
- `src/components/gaps/GapFilters.tsx` (0% → 80%+)
- `src/components/proposals/ProposalFilters.tsx` (0% → 80%+)
- `src/components/gaps/GapList.tsx` (0% → 80%+)
- `src/components/proposals/ProposalList.tsx` (0% → 80%+)
- `src/components/gaps/GapResolutionPanel.tsx` (0% → 80%+)
- `src/components/proposals/ProposalActions.tsx` (0% → 80%+)
- `src/components/documents/DocumentMetadata.tsx` (0% → 80%+)
- `src/components/documents/SnapshotHistory.tsx` (0% → 80%+)

**Estrategia:**
1. Component tests con React Testing Library
2. Mockear stores y servicios
3. Testear loading, error, and empty states
4. Testear user interactions

**Tiempo estimado:** 10-12 horas

### Fase 7: Tests de Layout (Prioridad BAJA)

**Objetivo:** Alcanzar 70%+ cobertura en layout

**Archivos a testear:**
- `src/components/layout/AppLayout.tsx` (0% → 70%+)

**Estrategia:**
1. Component tests con React Testing Library
2. Mockear useAuthStore y useBreadcrumbs
3. Testear navegación y breadcrumbs
4. Testear logout

**Tiempo estimado:** 3-4 horas

### Fase 8: Tests de Páginas (Prioridad BAJA)

**Objetivo:** Alcanzar 70%+ cobertura en páginas

**Archivos a testear:**
- `src/pages/DashboardPage.tsx` (0% → 70%+)
- `src/pages/LoginPage.tsx` (0% → 70%+)
- `src/pages/DocumentsPage.tsx` (0% → 70%+)
- `src/pages/GapsPage.tsx` (0% → 70%+)
- `src/pages/ProposalsPage.tsx` (0% → 70%+)
- `src/pages/DocumentDetailPage.tsx` (0% → 70%+)
- `src/pages/GapDetailPage.tsx` (0% → 70%+)
- `src/pages/ProposalDetailPage.tsx` (0% → 70%+)
- `src/pages/NotFoundPage.tsx` (0% → 70%+)

**Estrategia:**
1. Component tests con React Testing Library
2. Mockear stores, servicios y routing
3. Testear render con diferentes estados
4. Testear navegación

**Tiempo estimado:** 12-15 horas

### Fase 9: Tests de Integración (Prioridad BAJA)

**Objetivo:** Implementar 10% de tests de integración según ARC-019

**Estrategia:**
1. Crear tests de flujos completos (login → dashboard → documents)
2. Mockear API responses
3. Testear routing y navegación
4. Testear protected routes

**Tiempo estimado:** 8-10 horas

## Resumen de Tiempos

| Fase | Descripción | Tiempo Estimado |
|------|-------------|-----------------|
| 1 | Investigación y corrección crítica | 3-4 horas |
| 2 | Tests de servicios | 8-10 horas |
| 3 | Tests de stores | 8-10 horas |
| 4 | Tests de hooks | 2-3 horas |
| 5 | Tests de componentes UI | 4-5 horas |
| 6 | Tests de componentes de dominio | 10-12 horas |
| 7 | Tests de layout | 3-4 horas |
| 8 | Tests de páginas | 12-15 horas |
| 9 | Tests de integración | 8-10 horas |
| **Total** | | **58-83 horas** |

## Recomendaciones de Implementación

### Orden Sugerido
1. **Comenzar con Fase 1** (crítico para desbloquear el resto)
2. **Fases 2 y 3 en paralelo** (servicios y stores son independientes)
3. **Fases 4, 5, 6 en paralelo** (hooks, UI, y componentes de dominio)
4. **Fases 7, 8, 9 al final** (layout, páginas, e integración son menos críticos)

### Métricas de Éxito
- Cobertura global: 80%+ (lines, functions, statements)
- Cobertura branches: 75%+ (o 85%+ si se decide mantener el threshold actual)
- Todos los tests pasando
- CI/CD configurado para ejecutar tests con coverage
- Tiempo de ejecución de tests < 30 segundos

### Próximos Pasos Inmediatos
1. Investigar por qué los tests existentes no generan cobertura
2. Corregir el ID duplicado en documentación
3. Decidir y aplicar el threshold correcto para branches
4. Comenzar con Fase 2 (servicios) una vez resueltos los issues críticos
