import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useProjectsStore } from '../projectsStore';
import { projectsService } from '@/services/projects';
import type { Project, CreateProjectDto } from '@/types/organization';

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
    const mockProjects: Project[] = [{ id: '1', name: 'Test Project', slug: 'test-project', description: null, organization_id: 'org1', created_by: 'user1', created_at: '2024-01-01', updated_at: '2024-01-01' }];
    vi.mocked(projectsService.list).mockResolvedValue(mockProjects);

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
    const newProject: Project = { id: '1', name: 'New Project', slug: 'new-project', description: null, organization_id: 'org1', created_by: 'user1', created_at: '2024-01-01', updated_at: '2024-01-01' };
    vi.mocked(projectsService.create).mockResolvedValue(newProject);

    const store = useProjectsStore.getState();
    const mockData: CreateProjectDto = { name: 'New Project', slug: 'new-project', organization_id: 'org1' };
    await store.createProject(mockData);
    const updatedStore = useProjectsStore.getState();

    expect(projectsService.create).toHaveBeenCalledWith({ name: 'New Project', slug: 'new-project', organization_id: 'org1' });
    expect(updatedStore.projects).toContainEqual(newProject);
    expect(updatedStore.loading).toBe(false);
  });

  it('debe actualizar error al create fallido', async () => {
    vi.mocked(projectsService.create).mockRejectedValue(new Error('API Error'));

    const store = useProjectsStore.getState();
    const mockData: CreateProjectDto = { name: 'Test', slug: 'test', organization_id: 'org1' };
    await expect(store.createProject(mockData)).rejects.toThrow('Error al crear proyecto');
    const updatedStore = useProjectsStore.getState();

    expect(updatedStore.error).toBe('Error al crear proyecto');
    expect(updatedStore.loading).toBe(false);
  });
});
