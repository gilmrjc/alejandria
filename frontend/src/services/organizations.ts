import api from './api';
import type { CreateOrganizationDto, Organization } from '@/types/organization';

export const organizationsService = {
  async list(): Promise<Organization[]> {
    try {
      const response = await api.get<Organization[]>('/organizations');
      return response.data;
    } catch (error) {
      console.error('Error al cargar organizaciones:', error);
      throw error;
    }
  },

  async get(id: string): Promise<Organization> {
    try {
      const response = await api.get<Organization>(`/organizations/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error al cargar organización ${id}:`, error);
      throw error;
    }
  },

  async create(data: CreateOrganizationDto): Promise<Organization> {
    try {
      const response = await api.post<Organization>('/organizations', data);
      return response.data;
    } catch (error) {
      console.error('Error al crear organización:', error);
      throw error;
    }
  },
};
