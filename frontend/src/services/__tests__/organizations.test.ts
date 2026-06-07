import { describe, it, expect, beforeEach, vi } from 'vitest';
import { organizationsService } from '../organizations';
import api from '../api';

vi.mock('../api');

describe('organizationsService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('list', () => {
    it('debe llamar api.get para obtener organizaciones', async () => {
      const mockOrganizations = [{ id: '1', name: 'Test Org' }];
      vi.mocked(api.get).mockResolvedValue({ data: mockOrganizations } as any);

      const result = await organizationsService.list();

      expect(api.get).toHaveBeenCalledWith('/organizations');
      expect(result).toEqual(mockOrganizations);
    });

    it('debe manejar error en list', async () => {
      vi.mocked(api.get).mockRejectedValue(new Error('API Error'));
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      await expect(organizationsService.list()).rejects.toThrow('API Error');
      expect(consoleSpy).toHaveBeenCalledWith('Error al cargar organizaciones:', expect.any(Error));

      consoleSpy.mockRestore();
    });
  });

  describe('get', () => {
    it('debe llamar api.get para obtener organización por id', async () => {
      const mockOrganization = { id: '1', name: 'Test Org' };
      vi.mocked(api.get).mockResolvedValue({ data: mockOrganization } as any);

      const result = await organizationsService.get('1');

      expect(api.get).toHaveBeenCalledWith('/organizations/1');
      expect(result).toEqual(mockOrganization);
    });

    it('debe manejar error en get', async () => {
      vi.mocked(api.get).mockRejectedValue(new Error('Not Found'));
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      await expect(organizationsService.get('1')).rejects.toThrow('Not Found');
      expect(consoleSpy).toHaveBeenCalledWith('Error al cargar organización 1:', expect.any(Error));

      consoleSpy.mockRestore();
    });
  });

  describe('create', () => {
    it('debe llamar api.post con datos de organización', async () => {
      const mockOrganization = { id: '1', name: 'New Org' };
      const mockData = { name: 'New Org', slug: 'new-org' };
      vi.mocked(api.post).mockResolvedValue({ data: mockOrganization } as any);

      const result = await organizationsService.create(mockData as any);

      expect(api.post).toHaveBeenCalledWith('/organizations', mockData);
      expect(result).toEqual(mockOrganization);
    });

    it('debe manejar error en create', async () => {
      vi.mocked(api.post).mockRejectedValue(new Error('Validation Error'));
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      await expect(organizationsService.create({ name: 'Test' } as any)).rejects.toThrow('Validation Error');
      expect(consoleSpy).toHaveBeenCalledWith('Error al crear organización:', expect.any(Error));

      consoleSpy.mockRestore();
    });
  });
});
