import { create } from 'zustand';
import type { Proposal, ProposalListParams } from '@/types/proposal';
import { proposalsService } from '@/services/proposals';

interface ProposalsState {
  proposals: Proposal[];
  total: number;
  page: number;
  loading: boolean;
  error: string | null;
  fetchProposals: (params?: ProposalListParams) => Promise<void>;
  updateProposal: (id: string, data: { status?: string }) => Promise<void>;
}

export const useProposalsStore = create<ProposalsState>((set) => ({
  proposals: [],
  total: 0,
  page: 1,
  loading: false,
  error: null,

  fetchProposals: async (params) => {
    set({ loading: true, error: null });
    try {
      const result = await proposalsService.list(params);
      set({
        proposals: result.items,
        total: result.total,
        page: result.page,
        loading: false,
      });
    } catch {
      set({ error: 'Error al cargar propuestas', loading: false });
    }
  },

  updateProposal: async (id, data) => {
    try {
      const updated = await proposalsService.update(id, data);
      set((state) => ({
        proposals: state.proposals.map((proposal) => (proposal.id === id ? updated : proposal)),
      }));
    } catch {
      set({ error: 'Error al actualizar propuesta' });
    }
  },
}));
