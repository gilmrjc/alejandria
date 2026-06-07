import { describe, it, expect, beforeEach, vi } from 'vitest';
import { projectsService } from '../projects';
import api from '../api';

vi.mock('../api');

describe('projectsService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('list', () => {
    it('debe llamar api.get para obtener proyectos', async () => {
      const mockProjects = [{ id: '1', name: 'Test Project' }];
      vi.mocked(api.get).mockResolvedValue({ data: mockProjects } as any);

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
      const mockProject = { id: '1', name: 'Test Project' };
      vi.mocked(api.get).mockResolvedValue({ data: mockProject } as any);

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
      const mockProject = { id: '1', name: 'New Project' };
      const mockData = { name: 'New Project', slug: 'new-project', organization_id: 'org1' };
      vi.mocked(api.post).mockResolvedValue({ data: mockProject } as any);

      const result = await projectsService.create(mockData as any);

      expect(api.post).toHaveBeenCalledWith('/projects', mockData);
      expect(result).toEqual(mockProject);
    });

    it('debe manejar error en create', async () => {
      vi.mocked(api.post).mockRejectedValue(new Error('Validation Error'));
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      await expect(projectsService.create({ name: 'Test' } as any)).rejects.toThrow('Validation Error');
      expect(consoleSpy).toHaveBeenCalledWith('Error al crear proyecto:', expect.any(Error));

      consoleSpy.mockRestore();
    });
  });
});
