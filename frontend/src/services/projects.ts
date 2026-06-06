import api from './api';
import type { CreateProjectDto, Project } from '@/types/organization';

export const projectsService = {
  async list(): Promise<Project[]> {
    try {
      const response = await api.get<Project[]>('/projects');
      return response.data;
    } catch (error) {
      console.error('Error al cargar proyectos:', error);
      throw error;
    }
  },

  async get(id: string): Promise<Project> {
    try {
      const response = await api.get<Project>(`/projects/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error al cargar proyecto ${id}:`, error);
      throw error;
    }
  },

  async create(data: CreateProjectDto): Promise<Project> {
    try {
      const response = await api.post<Project>('/projects', data);
      return response.data;
    } catch (error) {
      console.error('Error al crear proyecto:', error);
      throw error;
    }
  },
};
