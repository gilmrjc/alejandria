import { describe, it, expect, beforeEach, vi } from 'vitest';
import { organizationsService } from '../organizations';
import api from '../api';
import type { Organization, CreateOrganizationDto } from '@/types/organization';

vi.mock('../api');

describe('organizationsService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('list', () => {
    it('debe llamar api.get para obtener organizaciones', async () => {
      const mockOrganizations: Organization[] = [{ id: '1', name: 'Test Org', slug: 'test-org', is_personal: false, created_by: 'user1', created_at: '2024-01-01', updated_at: '2024-01-01' }];
      vi.mocked(api.get).mockResolvedValue({ data: mockOrganizations });

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
      const mockOrganization: Organization = { id: '1', name: 'Test Org', slug: 'test-org', is_personal: false, created_by: 'user1', created_at: '2024-01-01', updated_at: '2024-01-01' };
      vi.mocked(api.get).mockResolvedValue({ data: mockOrganization });

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
      const mockOrganization: Organization = { id: '1', name: 'New Org', slug: 'new-org', is_personal: false, created_by: 'user1', created_at: '2024-01-01', updated_at: '2024-01-01' };
      const mockData: CreateOrganizationDto = { name: 'New Org', slug: 'new-org' };
      vi.mocked(api.post).mockResolvedValue({ data: mockOrganization });

      const result = await organizationsService.create(mockData);

      expect(api.post).toHaveBeenCalledWith('/organizations', mockData);
      expect(result).toEqual(mockOrganization);
    });

    it('debe manejar error en create', async () => {
      vi.mocked(api.post).mockRejectedValue(new Error('Validation Error'));
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      const mockData: CreateOrganizationDto = { name: 'Test', slug: 'test' };
      await expect(organizationsService.create(mockData)).rejects.toThrow('Validation Error');
      expect(consoleSpy).toHaveBeenCalledWith('Error al crear organización:', expect.any(Error));

      consoleSpy.mockRestore();
    });
  });
});
