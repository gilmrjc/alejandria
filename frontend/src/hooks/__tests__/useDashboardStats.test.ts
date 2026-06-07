import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useDashboardStats } from '../useDashboardStats';
import * as metricsService from '@/services/metrics';

vi.mock('@/services/metrics');

describe('useDashboardStats', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('debe cargar stats inicialmente', async () => {
    const mockStats = {
      documents: { total: 10, avgRating: 8.5, healthy: 5, needsImprovement: 3, noRating: 2 },
      gaps: { total: 20, byPriority: { critical: 5, high: 8, medium: 5, low: 2 }, byStatus: { pending: 10, responded: 8, rejected: 2 }, pending: 10 },
      proposals: { total: 5, byStatus: { pending: 2, accepted: 1, rejected: 1, implemented: 1 }, pending: 2 },
      progress: { gapsResolvedPercentage: 40, documentsHealthyPercentage: 50, avgResolutionTimeHours: 2.5, proposalAcceptanceRate: 20 },
    };

    vi.mocked(metricsService.getDashboardMetrics).mockResolvedValue(mockStats);

    const { result, unmount } = renderHook(() => useDashboardStats());

    expect(result.current.loading).toBe(true);

    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });

    expect(result.current.loading).toBe(false);
    expect(result.current.stats).toEqual(mockStats);
    expect(metricsService.getDashboardMetrics).toHaveBeenCalled();

    unmount();
  });

  it('debe manejar errores en fetch', async () => {
    const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    vi.mocked(metricsService.getDashboardMetrics).mockRejectedValue(new Error('API Error'));

    const { result, unmount } = renderHook(() => useDashboardStats());

    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });

    expect(result.current.error).toBe('Error al cargar métricas');
    expect(result.current.stats).toBeNull();

    consoleErrorSpy.mockRestore();
    unmount();
  });

  it('debe tener función refresh', async () => {
    const mockStats = {
      documents: { total: 10, avgRating: 8.5, healthy: 5, needsImprovement: 3, noRating: 2 },
      gaps: { total: 20, byPriority: { critical: 5, high: 8, medium: 5, low: 2 }, byStatus: { pending: 10, responded: 8, rejected: 2 }, pending: 10 },
      proposals: { total: 5, byStatus: { pending: 2, accepted: 1, rejected: 1, implemented: 1 }, pending: 2 },
      progress: { gapsResolvedPercentage: 40, documentsHealthyPercentage: 50, avgResolutionTimeHours: 2.5, proposalAcceptanceRate: 20 },
    };

    vi.mocked(metricsService.getDashboardMetrics).mockResolvedValue(mockStats);

    const { result, unmount } = renderHook(() => useDashboardStats());

    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });

    expect(metricsService.getDashboardMetrics).toHaveBeenCalledTimes(1);

    act(() => {
      result.current.refresh();
    });

    expect(metricsService.getDashboardMetrics).toHaveBeenCalledTimes(2);

    unmount();
  });
});

