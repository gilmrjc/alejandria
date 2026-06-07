import { describe, it, expect, vi, beforeEach } from 'vitest';
import { authService } from '../auth';
import api from '../api';

vi.mock('../api');

describe('authService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('login', () => {
    it('debe llamar api.post con credenciales correctas', async () => {
      const mockTokens = { access_token: 'test-token' };
      vi.mocked(api.post).mockResolvedValue({ data: mockTokens } as { data: { access_token: string } });

      const credentials = { email: 'test@example.com', password: 'password' };
      const result = await authService.login(credentials);

      expect(api.post).toHaveBeenCalledWith('/auth/login', credentials);
      expect(result).toEqual(mockTokens);
    });

    it('debe manejar error en login', async () => {
      vi.mocked(api.post).mockRejectedValue(new Error('Invalid credentials'));

      const credentials = { email: 'test@example.com', password: 'password' };
      await expect(authService.login(credentials)).rejects.toThrow('Invalid credentials');
    });
  });

  describe('me', () => {
    it('debe llamar api.get para obtener usuario', async () => {
      const mockUser = { id: '1', username: 'test', email: 'test@example.com' };
      vi.mocked(api.get).mockResolvedValue({ data: mockUser } as { data: { id: string; username: string; email: string } });

      const result = await authService.me();

      expect(api.get).toHaveBeenCalledWith('/auth/me');
      expect(result).toEqual(mockUser);
    });

    it('debe manejar error en me', async () => {
      vi.mocked(api.get).mockRejectedValue(new Error('Unauthorized'));

      await expect(authService.me()).rejects.toThrow('Unauthorized');
    });
  });

  describe('register', () => {
    it('debe llamar api.post con datos de registro', async () => {
      const mockUser = { id: '1', username: 'test', email: 'test@example.com' };
      vi.mocked(api.post).mockResolvedValue({ data: mockUser } as { data: { id: string; username: string; email: string } });

      const data = { email: 'test@example.com', username: 'test', password: 'password' };
      const result = await authService.register(data);

      expect(api.post).toHaveBeenCalledWith('/auth/register', data);
      expect(result).toEqual(mockUser);
    });

    it('debe manejar error en register', async () => {
      vi.mocked(api.post).mockRejectedValue(new Error('Email already exists'));

      const data = { email: 'test@example.com', username: 'test', password: 'password' };
      await expect(authService.register(data)).rejects.toThrow('Email already exists');
    });
  });
});
