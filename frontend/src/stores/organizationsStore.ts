import { create } from 'zustand';
import type { Organization, CreateOrganizationDto } from '@/types/organization';
import { organizationsService } from '@/services/organizations';

interface OrganizationsState {
  organizations: Organization[];
  loading: boolean;
  error: string | null;
  fetchOrganizations: () => Promise<void>;
  createOrganization: (data: CreateOrganizationDto) => Promise<void>;
}

export const useOrganizationsStore = create<OrganizationsState>((set) => ({
  organizations: [],
  loading: false,
  error: null,

  fetchOrganizations: async () => {
    set({ loading: true, error: null });
    try {
      const organizations = await organizationsService.list();
      set({ organizations, loading: false });
    } catch {
      set({ error: 'Error al cargar organizaciones', loading: false });
    }
  },

  createOrganization: async (data) => {
    set({ loading: true, error: null });
    try {
      const newOrg = await organizationsService.create(data);
      set((state) => ({
        organizations: [...state.organizations, newOrg],
        loading: false,
      }));
    } catch {
      set({ error: 'Error al crear organización', loading: false });
      throw new Error('Error al crear organización');
    }
  },
}));
