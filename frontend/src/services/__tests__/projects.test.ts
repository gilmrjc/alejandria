import { describe, it, expect, beforeEach, vi } from 'vitest';
import { projectsService } from '../projects';
import api from '../api';
import type { Project, CreateProjectDto } from '@/types/organization';

vi.mock('../api');

describe('projectsService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('list', () => {
    it('debe llamar api.get para obtener proyectos', async () => {
      const mockProjects: Project[] = [{ id: '1', name: 'Test Project', slug: 'test-project', description: null, organization_id: 'org1', created_by: 'user1', created_at: '2024-01-01', updated_at: '2024-01-01' }];
      vi.mocked(api.get).mockResolvedValue({ data: mockProjects });

      const result = await projectsService.list();

      expect(api.get).toHaveBeenCalledWith('/projects');
      expect(result).toEqual(mockProjects);
    });

    it('debe manejar error en list', async () => {
      vi.mocked(api.get).mockRejectedValue(new Error('API Error'));
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      await expect(projectsService.list()).rejects.toThrow('API Error');
      expect(consoleSpy).toHaveBeenCalledWith('Error al cargar proyectos:', expect.any(Error));

      consoleSpy.mockRestore();
    });
  });

  describe('get', () => {
    it('debe llamar api.get para obtener proyecto por id', async () => {
      const mockProject: Project = { id: '1', name: 'Test Project', slug: 'test-project', description: null, organization_id: 'org1', created_by: 'user1', created_at: '2024-01-01', updated_at: '2024-01-01' };
      vi.mocked(api.get).mockResolvedValue({ data: mockProject });

      const result = await projectsService.get('1');

      expect(api.get).toHaveBeenCalledWith('/projects/1');
      expect(result).toEqual(mockProject);
    });

    it('debe manejar error en get', async () => {
      vi.mocked(api.get).mockRejectedValue(new Error('Not Found'));
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      await expect(projectsService.get('1')).rejects.toThrow('Not Found');
      expect(consoleSpy).toHaveBeenCalledWith('Error al cargar proyecto 1:', expect.any(Error));

      consoleSpy.mockRestore();
    });
  });

  describe('create', () => {
    it('debe llamar api.post con datos de proyecto', async () => {
      const mockProject: Project = { id: '1', name: 'New Project', slug: 'new-project', description: null, organization_id: 'org1', created_by: 'user1', created_at: '2024-01-01', updated_at: '2024-01-01' };
      const mockData: CreateProjectDto = { name: 'New Project', slug: 'new-project', organization_id: 'org1' };
      vi.mocked(api.post).mockResolvedValue({ data: mockProject });

      const result = await projectsService.create(mockData);

      expect(api.post).toHaveBeenCalledWith('/projects', mockData);
      expect(result).toEqual(mockProject);
    });

    it('debe manejar error en create', async () => {
      vi.mocked(api.post).mockRejectedValue(new Error('Validation Error'));
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      const mockData: CreateProjectDto = { name: 'Test', slug: 'test', organization_id: 'org1' };
      await expect(projectsService.create(mockData)).rejects.toThrow('Validation Error');
      expect(consoleSpy).toHaveBeenCalledWith('Error al crear proyecto:', expect.any(Error));

      consoleSpy.mockRestore();
    });
  });
});
