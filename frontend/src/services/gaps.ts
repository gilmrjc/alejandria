import api from './api';
import type { Gap, GapListParams } from '@/types/gap';

export const gapsService = {
  async list(params?: GapListParams): Promise<{ items: Gap[]; pagination: { page: number; per_page: number; total: number; total_pages: number } }> {
    const response = await api.get('/gaps', { params });
    return response.data;
  },

  async getBySlug(slug: string): Promise<Gap> {
    const response = await api.get<Gap>(`/gaps/slug/${slug}`);
    return response.data;
  },

  async get(id: string): Promise<Gap> {
    const response = await api.get<Gap>(`/gaps/${id}`);
    return response.data;
  },

  async create(data: { document_id: string; question: string; priority: string; context_missing?: string; role_affected?: string }): Promise<Gap> {
    const response = await api.post<Gap>('/gaps', data);
    return response.data;
  },

  async updateBySlug(slug: string, data: { answer?: string; status?: string }): Promise<Gap> {
    const response = await api.put<Gap>(`/gaps/slug/${slug}`, data);
    return response.data;
  },

  async update(id: string, data: { answer?: string; status?: string }): Promise<Gap> {
    const response = await api.put<Gap>(`/gaps/${id}`, data);
    return response.data;
  },

  async deleteBySlug(slug: string): Promise<void> {
    await api.delete(`/gaps/slug/${slug}`);
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/gaps/${id}`);
  },
};
