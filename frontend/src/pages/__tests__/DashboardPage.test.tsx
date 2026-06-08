import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { DashboardPage } from '../DashboardPage';

// Mock the useDashboardStats hook
vi.mock('@/hooks/useDashboardStats', () => ({
  useDashboardStats: vi.fn(),
}));

import { useDashboardStats } from '@/hooks/useDashboardStats';

describe('DashboardPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debe renderizar título Dashboard', () => {
    vi.mocked(useDashboardStats).mockReturnValue({
      stats: {
        documents: { total: 0, avgRating: null, healthy: 0, needsImprovement: 0, noRating: 0 },
        gaps: { total: 0, byPriority: { critical: 0, high: 0, medium: 0, low: 0 }, byStatus: { pending: 0, responded: 0, rejected: 0 }, pending: 0 },
        proposals: { total: 0, byStatus: { pending: 0, accepted: 0, rejected: 0, implemented: 0 }, pending: 0 },
        progress: { gapsResolvedPercentage: 0, documentsHealthyPercentage: 0, avgResolutionTimeHours: null, proposalAcceptanceRate: 0 },
      },
      loading: false,
      error: null,
      refresh: vi.fn(),
    });
    render(<DashboardPage />);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
  });

  it('debe renderizar subtítulo', () => {
    vi.mocked(useDashboardStats).mockReturnValue({
      stats: {
        documents: { total: 0, avgRating: null, healthy: 0, needsImprovement: 0, noRating: 0 },
        gaps: { total: 0, byPriority: { critical: 0, high: 0, medium: 0, low: 0 }, byStatus: { pending: 0, responded: 0, rejected: 0 }, pending: 0 },
        proposals: { total: 0, byStatus: { pending: 0, accepted: 0, rejected: 0, implemented: 0 }, pending: 0 },
        progress: { gapsResolvedPercentage: 0, documentsHealthyPercentage: 0, avgResolutionTimeHours: null, proposalAcceptanceRate: 0 },
      },
      loading: false,
      error: null,
      refresh: vi.fn(),
    });
    render(<DashboardPage />);
    expect(screen.getByText('Estado general del sistema')).toBeInTheDocument();
  });

  it('debe renderizar tarjetas de estadísticas', () => {
    vi.mocked(useDashboardStats).mockReturnValue({
      stats: {
        documents: { total: 10, avgRating: 8.5, healthy: 5, needsImprovement: 3, noRating: 2 },
        gaps: { total: 5, byPriority: { critical: 1, high: 2, medium: 1, low: 1 }, byStatus: { pending: 3, responded: 2, rejected: 0 }, pending: 3 },
        proposals: { total: 2, byStatus: { pending: 1, accepted: 0, rejected: 0, implemented: 1 }, pending: 1 },
        progress: { gapsResolvedPercentage: 40, documentsHealthyPercentage: 50, avgResolutionTimeHours: 24, proposalAcceptanceRate: 50 },
      },
      loading: false,
      error: null,
      refresh: vi.fn(),
    });
    render(<DashboardPage />);
    expect(screen.getByText('Total documentos')).toBeInTheDocument();
    expect(screen.getByText('Calificación promedio')).toBeInTheDocument();
    expect(screen.getByText('Gaps pendientes')).toBeInTheDocument();
    expect(screen.getByText('Propuestas pendientes')).toBeInTheDocument();
    expect(screen.getByText('Progreso')).toBeInTheDocument();
  });

  it('debe mostrar datos reales cuando no está cargando', () => {
    vi.mocked(useDashboardStats).mockReturnValue({
      stats: {
        documents: { total: 10, avgRating: 8.5, healthy: 5, needsImprovement: 3, noRating: 2 },
        gaps: { total: 5, byPriority: { critical: 1, high: 2, medium: 1, low: 1 }, byStatus: { pending: 3, responded: 2, rejected: 0 }, pending: 3 },
        proposals: { total: 2, byStatus: { pending: 1, accepted: 0, rejected: 0, implemented: 1 }, pending: 1 },
        progress: { gapsResolvedPercentage: 40, documentsHealthyPercentage: 50, avgResolutionTimeHours: 24, proposalAcceptanceRate: 50 },
      },
      loading: false,
      error: null,
      refresh: vi.fn(),
    });
    render(<DashboardPage />);
    expect(screen.getByText('10')).toBeInTheDocument();
    expect(screen.getByText('8.5')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument();
    expect(screen.getByText('40%')).toBeInTheDocument();
  });

  it('debe mostrar guiones cuando está cargando', () => {
    vi.mocked(useDashboardStats).mockReturnValue({
      stats: {
        documents: { total: 0, avgRating: null, healthy: 0, needsImprovement: 0, noRating: 0 },
        gaps: { total: 0, byPriority: { critical: 0, high: 0, medium: 0, low: 0 }, byStatus: { pending: 0, responded: 0, rejected: 0 }, pending: 0 },
        proposals: { total: 0, byStatus: { pending: 0, accepted: 0, rejected: 0, implemented: 0 }, pending: 0 },
        progress: { gapsResolvedPercentage: 0, documentsHealthyPercentage: 0, avgResolutionTimeHours: null, proposalAcceptanceRate: 0 },
      },
      loading: true,
      error: null,
      refresh: vi.fn(),
    });
    render(<DashboardPage />);
    const dashes = screen.getAllByText('—');
    expect(dashes.length).toBeGreaterThan(0);
  });

  it('debe mostrar mensaje de error cuando hay error', () => {
    vi.mocked(useDashboardStats).mockReturnValue({
      stats: {
        documents: { total: 0, avgRating: null, healthy: 0, needsImprovement: 0, noRating: 0 },
        gaps: { total: 0, byPriority: { critical: 0, high: 0, medium: 0, low: 0 }, byStatus: { pending: 0, responded: 0, rejected: 0 }, pending: 0 },
        proposals: { total: 0, byStatus: { pending: 0, accepted: 0, rejected: 0, implemented: 0 }, pending: 0 },
        progress: { gapsResolvedPercentage: 0, documentsHealthyPercentage: 0, avgResolutionTimeHours: null, proposalAcceptanceRate: 0 },
      },
      loading: false,
      error: 'Error al cargar métricas',
      refresh: vi.fn(),
    });
    render(<DashboardPage />);
    expect(screen.getByText('Error al cargar métricas')).toBeInTheDocument();
  });

  it('debe renderizar estado de infraestructura', () => {
    vi.mocked(useDashboardStats).mockReturnValue({
      stats: {
        documents: { total: 0, avgRating: null, healthy: 0, needsImprovement: 0, noRating: 0 },
        gaps: { total: 0, byPriority: { critical: 0, high: 0, medium: 0, low: 0 }, byStatus: { pending: 0, responded: 0, rejected: 0 }, pending: 0 },
        proposals: { total: 0, byStatus: { pending: 0, accepted: 0, rejected: 0, implemented: 0 }, pending: 0 },
        progress: { gapsResolvedPercentage: 0, documentsHealthyPercentage: 0, avgResolutionTimeHours: null, proposalAcceptanceRate: 0 },
      },
      loading: false,
      error: null,
      refresh: vi.fn(),
    });
    render(<DashboardPage />);
    expect(screen.getByText('Estado de infraestructura')).toBeInTheDocument();
  });

  it('debe mostrar items de infraestructura', () => {
    vi.mocked(useDashboardStats).mockReturnValue({
      stats: {
        documents: { total: 0, avgRating: null, healthy: 0, needsImprovement: 0, noRating: 0 },
        gaps: { total: 0, byPriority: { critical: 0, high: 0, medium: 0, low: 0 }, byStatus: { pending: 0, responded: 0, rejected: 0 }, pending: 0 },
        proposals: { total: 0, byStatus: { pending: 0, accepted: 0, rejected: 0, implemented: 0 }, pending: 0 },
        progress: { gapsResolvedPercentage: 0, documentsHealthyPercentage: 0, avgResolutionTimeHours: null, proposalAcceptanceRate: 0 },
      },
      loading: false,
      error: null,
      refresh: vi.fn(),
    });
    render(<DashboardPage />);
    expect(screen.getByText('Vite + React + TypeScript')).toBeInTheDocument();
    expect(screen.getByText('TailwindCSS + shadcn/ui')).toBeInTheDocument();
    expect(screen.getByText('React Router')).toBeInTheDocument();
    expect(screen.getByText('Axios + JWT interceptors')).toBeInTheDocument();
    expect(screen.getByText('Zustand stores')).toBeInTheDocument();
  });

  it('debe renderizar botón de actualizar', () => {
    vi.mocked(useDashboardStats).mockReturnValue({
      stats: {
        documents: { total: 0, avgRating: null, healthy: 0, needsImprovement: 0, noRating: 0 },
        gaps: { total: 0, byPriority: { critical: 0, high: 0, medium: 0, low: 0 }, byStatus: { pending: 0, responded: 0, rejected: 0 }, pending: 0 },
        proposals: { total: 0, byStatus: { pending: 0, accepted: 0, rejected: 0, implemented: 0 }, pending: 0 },
        progress: { gapsResolvedPercentage: 0, documentsHealthyPercentage: 0, avgResolutionTimeHours: null, proposalAcceptanceRate: 0 },
      },
      loading: false,
      error: null,
      refresh: vi.fn(),
    });
    render(<DashboardPage />);
    expect(screen.getByText('Actualizar')).toBeInTheDocument();
  });

  it('debe llamar a refresh cuando se hace click en actualizar', () => {
    const mockRefresh = vi.fn();
    vi.mocked(useDashboardStats).mockReturnValue({
      stats: {
        documents: { total: 0, avgRating: null, healthy: 0, needsImprovement: 0, noRating: 0 },
        gaps: { total: 0, byPriority: { critical: 0, high: 0, medium: 0, low: 0 }, byStatus: { pending: 0, responded: 0, rejected: 0 }, pending: 0 },
        proposals: { total: 0, byStatus: { pending: 0, accepted: 0, rejected: 0, implemented: 0 }, pending: 0 },
        progress: { gapsResolvedPercentage: 0, documentsHealthyPercentage: 0, avgResolutionTimeHours: null, proposalAcceptanceRate: 0 },
      },
      loading: false,
      error: null,
      refresh: mockRefresh,
    });
    render(<DashboardPage />);
    const refreshButton = screen.getByText('Actualizar');
    refreshButton.click();
    expect(mockRefresh).toHaveBeenCalledTimes(1);
  });

  it('debe mostrar "N/A" cuando avgRating es null', () => {
    vi.mocked(useDashboardStats).mockReturnValue({
      stats: {
        documents: { total: 10, avgRating: null, healthy: 5, needsImprovement: 3, noRating: 2 },
        gaps: { total: 5, byPriority: { critical: 1, high: 2, medium: 1, low: 1 }, byStatus: { pending: 3, responded: 2, rejected: 0 }, pending: 3 },
        proposals: { total: 2, byStatus: { pending: 1, accepted: 0, rejected: 0, implemented: 1 }, pending: 1 },
        progress: { gapsResolvedPercentage: 40, documentsHealthyPercentage: 50, avgResolutionTimeHours: null, proposalAcceptanceRate: 50 },
      },
      loading: false,
      error: null,
      refresh: vi.fn(),
    });
    render(<DashboardPage />);
    expect(screen.getByText('N/A')).toBeInTheDocument();
  });
});
