import { create } from 'zustand';
import type { Project, CreateProjectDto } from '@/types/organization';
import { projectsService } from '@/services/projects';

interface ProjectsState {
  projects: Project[];
  loading: boolean;
  error: string | null;
  fetchProjects: () => Promise<void>;
  createProject: (data: CreateProjectDto) => Promise<void>;
}

export const useProjectsStore = create<ProjectsState>((set) => ({
  projects: [],
  loading: false,
  error: null,

  fetchProjects: async () => {
    set({ loading: true, error: null });
    try {
      const projects = await projectsService.list();
      set({ projects, loading: false });
    } catch {
      set({ error: 'Error al cargar proyectos', loading: false });
    }
  },

  createProject: async (data) => {
    set({ loading: true, error: null });
    try {
      const newProject = await projectsService.create(data);
      set((state) => ({
        projects: [...state.projects, newProject],
        loading: false,
      }));
    } catch {
      set({ error: 'Error al crear proyecto', loading: false });
      throw new Error('Error al crear proyecto');
    }
  },
}));
