import { describe, it, expect, vi, beforeEach } from 'vitest';
import { getDashboardMetrics } from '../metrics';
import api from '../api';

vi.mock('../api');

describe('metrics service', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debe obtener métricas del dashboard', async () => {
    const mockMetrics = {
      documents: { total: 10, avgRating: 8.5, healthy: 5, needsImprovement: 3, noRating: 2 },
      gaps: { total: 5, byPriority: { critical: 1, high: 2, medium: 1, low: 1 }, byStatus: { pending: 3, responded: 2, rejected: 0 }, pending: 3 },
      proposals: { total: 2, byStatus: { pending: 1, accepted: 0, rejected: 0, implemented: 1 }, pending: 1 },
      progress: { gapsResolvedPercentage: 40, documentsHealthyPercentage: 50, avgResolutionTimeHours: 24, proposalAcceptanceRate: 50 },
    };

    vi.mocked(api.get).mockResolvedValue({ data: mockMetrics });

    const result = await getDashboardMetrics();

    expect(api.get).toHaveBeenCalledWith('/metrics');
    expect(result).toEqual(mockMetrics);
  });

  it('debe manejar errores de API', async () => {
    vi.mocked(api.get).mockRejectedValue(new Error('API Error'));

    await expect(getDashboardMetrics()).rejects.toThrow('API Error');
  });
});
