import { useEffect, useState, useCallback } from 'react';
import { getDashboardMetrics, getProjectMetrics } from '@/services/metrics';
import type { DashboardStats } from '@/types/dashboard';

interface UseDashboardStatsOptions {
  orgSlug?: string;
  projectSlug?: string;
}

export function useDashboardStats(options: UseDashboardStatsOptions = {}) {
  const { orgSlug, projectSlug } = options;
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadStats = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      let data: DashboardStats;

      // If project context is provided, fetch project-specific metrics
      if (orgSlug && projectSlug) {
        console.log(`Fetching project metrics for ${orgSlug}/${projectSlug}`);
        data = await getProjectMetrics(orgSlug, projectSlug);
      } else {
        // Otherwise fetch global metrics
        console.log('Fetching global metrics');
        data = await getDashboardMetrics();
      }

      console.log('Metrics received:', data);
      setStats(data);
    } catch (err) {
      console.error('Error loading dashboard stats:', err);
      setError(err instanceof Error ? err.message : 'Error al cargar métricas');
    } finally {
      setLoading(false);
    }
  }, [orgSlug, projectSlug]);

  useEffect(() => {
    loadStats();

    // Auto-refresh every 5 minutes as per specification
    const interval = setInterval(loadStats, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, [loadStats]);

  return { stats, loading, error, refresh: loadStats };
}
