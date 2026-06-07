import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useProjectsStore } from '../projectsStore';
import { projectsService } from '@/services/projects';

vi.mock('@/services/projects');

describe('projectsStore', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debe tener estado inicial correcto', () => {
    const store = useProjectsStore.getState();
    expect(store.projects).toEqual([]);
    expect(store.loading).toBe(false);
    expect(store.error).toBeNull();
  });

  it('debe actualizar projects al fetch exitoso', async () => {
    const mockProjects = [{ id: '1', name: 'Test Project', slug: 'test-project' }];
    vi.mocked(projectsService.list).mockResolvedValue(mockProjects as any);

    const store = useProjectsStore.getState();
    await store.fetchProjects();
    const updatedStore = useProjectsStore.getState();

    expect(projectsService.list).toHaveBeenCalled();
    expect(updatedStore.projects).toEqual(mockProjects);
    expect(updatedStore.loading).toBe(false);
  });

  it('debe actualizar error al fetch fallido', async () => {
    vi.mocked(projectsService.list).mockRejectedValue(new Error('API Error'));

    const store = useProjectsStore.getState();
    await store.fetchProjects();
    const updatedStore = useProjectsStore.getState();

    expect(updatedStore.error).toBe('Error al cargar proyectos');
    expect(updatedStore.loading).toBe(false);
  });

  it('debe agregar proyecto al create exitoso', async () => {
    const newProject = { id: '1', name: 'New Project', slug: 'new-project' };
    vi.mocked(projectsService.create).mockResolvedValue(newProject as any);

    const store = useProjectsStore.getState();
    await store.createProject({ name: 'New Project', slug: 'new-project' } as any);
    const updatedStore = useProjectsStore.getState();

    expect(projectsService.create).toHaveBeenCalledWith({ name: 'New Project', slug: 'new-project' });
    expect(updatedStore.projects).toContainEqual(newProject);
    expect(updatedStore.loading).toBe(false);
  });

  it('debe actualizar error al create fallido', async () => {
    vi.mocked(projectsService.create).mockRejectedValue(new Error('API Error'));

    const store = useProjectsStore.getState();
    await expect(store.createProject({ name: 'Test' } as any)).rejects.toThrow('Error al crear proyecto');
    const updatedStore = useProjectsStore.getState();

    expect(updatedStore.error).toBe('Error al crear proyecto');
    expect(updatedStore.loading).toBe(false);
  });
});
