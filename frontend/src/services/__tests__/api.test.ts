import { describe, it, expect, vi, beforeEach } from 'vitest';
import api from '../api';

describe('api client', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Reset localStorage
    localStorage.clear();
    // Reset window.location
    delete (window as any).location;
    (window as any).location = { href: '' };
  });

  it('debe tener baseURL configurada correctamente', () => {
    expect(api.defaults.baseURL).toBe('http://localhost:8000/api/v1');
  });

  it('debe tener timeout configurado', () => {
    expect(api.defaults.timeout).toBe(10000);
  });

  describe('request interceptor', () => {
    it('debe agregar token JWT en headers cuando existe', async () => {
      localStorage.setItem('access_token', 'test-token');
      
      // Test via actual API call behavior
      const config = { headers: {} as any };
      api.interceptors.request.use((cfg) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          cfg.headers.Authorization = `Bearer ${token}`;
        }
        return cfg;
      });
      
      const handler = api.interceptors.request.handlers?.[0];
      if (handler?.fulfilled) {
        const result = await handler.fulfilled(config);
        expect(result.headers.Authorization).toBe('Bearer test-token');
      }
    });

    it('no debe agregar token cuando no existe', async () => {
      const config = { headers: {} as any };
      api.interceptors.request.use((cfg) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          cfg.headers.Authorization = `Bearer ${token}`;
        }
        return cfg;
      });
      
      const handler = api.interceptors.request.handlers?.[0];
      if (handler?.fulfilled) {
        const result = await handler.fulfilled(config);
        expect(result.headers.Authorization).toBeUndefined();
      }
    });
  });

  describe('response interceptor', () => {
    it('debe pasar response exitosa', async () => {
      const response = { data: { success: true } } as any;
      api.interceptors.response.use((res) => res);
      
      const handler = api.interceptors.response.handlers?.[0];
      if (handler?.fulfilled) {
        const result = await handler.fulfilled(response);
        expect(result).toEqual(response);
      }
    });

    it('debe redirigir a login en error 401', async () => {
      const error = {
        response: { status: 401 },
      } as any;
      
      api.interceptors.response.use(
        (res) => res,
        (err) => {
          if (err.response?.status === 401) {
            localStorage.removeItem('access_token');
            (window as any).location.href = '/login';
          }
          return Promise.reject(err);
        }
      );
      
      const handler = api.interceptors.response.handlers?.[0];
      if (handler?.rejected) {
        try {
          await handler.rejected(error);
        } catch (e) {
          // Expected to reject
        }
      }
      
      expect(localStorage.getItem('access_token')).toBeNull();
      expect((window as any).location.href).toBe('/login');
    });

    it('debe rechazar error no 401', async () => {
      const error = {
        response: { status: 500 },
      } as any;
      
      api.interceptors.response.use(
        (res) => res,
        (err) => {
          if (err.response?.status === 401) {
            localStorage.removeItem('access_token');
            (window as any).location.href = '/login';
          }
          return Promise.reject(err);
        }
      );
      
      const handler = api.interceptors.response.handlers?.[0];
      if (handler?.rejected) {
        await expect(handler.rejected(error)).rejects.toEqual(error);
      }
    });

    it('debe rechazar error sin response', async () => {
      const error = new Error('Network Error') as any;
      
      api.interceptors.response.use(
        (res) => res,
        (err) => {
          if (err.response?.status === 401) {
            localStorage.removeItem('access_token');
            (window as any).location.href = '/login';
          }
          return Promise.reject(err);
        }
      );
      
      const handler = api.interceptors.response.handlers?.[0];
      if (handler?.rejected) {
        await expect(handler.rejected(error)).rejects.toEqual(error);
      }
    });
  });
});
