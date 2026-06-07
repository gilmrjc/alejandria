import api from './api';
import type { DashboardStats } from '@/types/dashboard';

export async function getDashboardMetrics(): Promise<DashboardStats> {
  const response = await api.get<DashboardStats>('/metrics');
  return response.data;
}
