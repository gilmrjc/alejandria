import { create } from 'zustand';
import type { Gap, GapListParams } from '@/types/gap';
import { gapsService } from '@/services/gaps';

interface GapsState {
  gaps: Gap[];
  total: number;
  page: number;
  loading: boolean;
  error: string | null;
  fetchGaps: (params?: GapListParams) => Promise<void>;
  updateGap: (slug: string, data: { answer?: string; status?: string }) => Promise<void>;
}

export const useGapsStore = create<GapsState>((set) => ({
  gaps: [],
  total: 0,
  page: 1,
  loading: false,
  error: null,

  fetchGaps: async (params) => {
    set({ loading: true, error: null });
    try {
      const result = await gapsService.list(params);
      set({
        gaps: result.items,
        total: result.pagination.total,
        page: result.pagination.page,
        loading: false,
      });
    } catch {
      set({ error: 'Error al cargar gaps', loading: false });
    }
  },

  updateGap: async (slug, data) => {
    try {
      const updated = await gapsService.updateBySlug(slug, data);
      set((state) => ({
        gaps: state.gaps.map((gap) => (gap.slug === slug ? updated : gap)),
      }));
    } catch {
      set({ error: 'Error al actualizar gap' });
    }
  },
}));
