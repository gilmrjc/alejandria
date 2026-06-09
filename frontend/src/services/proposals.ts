import api from './api';
import type { Proposal, ProposalListParams } from '@/types/proposal';

export const proposalsService = {
  async list(params?: ProposalListParams): Promise<{ items: Proposal[]; total: number; page: number; per_page: number; total_pages: number }> {
    const response = await api.get('/proposals', { params });
    return response.data;
  },

  async get(id: string): Promise<Proposal> {
    const response = await api.get<Proposal>(`/proposals/${id}/view`);
    return response.data;
  },

  async create(data: { name: string; description: string }): Promise<Proposal> {
    const response = await api.post<Proposal>('/proposals', data);
    return response.data;
  },

  async update(id: string, data: { status?: string }): Promise<Proposal> {
    const response = await api.put<Proposal>(`/proposals/${id}`, data);
    return response.data;
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/proposals/${id}`);
  },
};
