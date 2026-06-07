import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useOrganizationsStore } from '../organizationsStore';
import { organizationsService } from '@/services/organizations';

vi.mock('@/services/organizations');

describe('organizationsStore', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debe tener estado inicial correcto', () => {
    const store = useOrganizationsStore.getState();
    expect(store.organizations).toEqual([]);
    expect(store.loading).toBe(false);
    expect(store.error).toBeNull();
  });

  it('debe actualizar organizations al fetch exitoso', async () => {
    const mockOrganizations = [{ id: '1', name: 'Test Org', slug: 'test-org' }];
    vi.mocked(organizationsService.list).mockResolvedValue(mockOrganizations as any);

    const store = useOrganizationsStore.getState();
    await store.fetchOrganizations();
    const updatedStore = useOrganizationsStore.getState();

    expect(organizationsService.list).toHaveBeenCalled();
    expect(updatedStore.organizations).toEqual(mockOrganizations);
    expect(updatedStore.loading).toBe(false);
  });

  it('debe actualizar loading y error al fetch fallido', async () => {
    vi.mocked(organizationsService.list).mockRejectedValue(new Error('API Error'));

    const store = useOrganizationsStore.getState();
    await store.fetchOrganizations();
    const updatedStore = useOrganizationsStore.getState();

    expect(updatedStore.error).toBe('Error al cargar organizaciones');
    expect(updatedStore.loading).toBe(false);
  });

  it('debe agregar organización al create exitoso', async () => {
    const newOrg = { id: '1', name: 'New Org', slug: 'new-org' };
    vi.mocked(organizationsService.create).mockResolvedValue(newOrg as any);

    const store = useOrganizationsStore.getState();
    await store.createOrganization({ name: 'New Org', slug: 'new-org' } as any);
    const updatedStore = useOrganizationsStore.getState();

    expect(organizationsService.create).toHaveBeenCalledWith({ name: 'New Org', slug: 'new-org' });
    expect(updatedStore.organizations).toContainEqual(newOrg);
    expect(updatedStore.loading).toBe(false);
  });

  it('debe actualizar error al create fallido', async () => {
    vi.mocked(organizationsService.create).mockRejectedValue(new Error('API Error'));

    const store = useOrganizationsStore.getState();
    await expect(store.createOrganization({ name: 'Test' } as any)).rejects.toThrow('Error al crear organización');
    const updatedStore = useOrganizationsStore.getState();

    expect(updatedStore.error).toBe('Error al crear organización');
    expect(updatedStore.loading).toBe(false);
  });
});
