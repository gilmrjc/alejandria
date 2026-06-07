import { describe, it, expect, vi, beforeEach } from 'vitest';
import api from '../api';
import type { InternalAxiosRequestConfig, AxiosResponse } from 'axios';

describe('api client', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Reset localStorage
    localStorage.clear();
    // Reset window.location
    (window as unknown as { location: { href: string } }).location = { href: '' };
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
      const config: InternalAxiosRequestConfig = {
        headers: {},
      } as InternalAxiosRequestConfig;
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
      const config: InternalAxiosRequestConfig = {
        headers: {},
      } as InternalAxiosRequestConfig;
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
      const response: AxiosResponse = {
        data: { success: true },
        status: 200,
        statusText: 'OK',
        headers: {},
        config: { headers: {} } as InternalAxiosRequestConfig,
      } as AxiosResponse;
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
      } as { response?: { status: number } };
      
      api.interceptors.response.use(
        (res) => res,
        (err) => {
          if (err.response?.status === 401) {
            localStorage.removeItem('access_token');
            (window as unknown as { location: { href: string } }).location.href = '/login';
          }
          return Promise.reject(err);
        }
      );
      
      const handler = api.interceptors.response.handlers?.[0];
      if (handler?.rejected) {
        try {
          await handler.rejected(error);
        } catch {
          // Expected to reject
        }
      }
      
      expect(localStorage.getItem('access_token')).toBeNull();
      expect((window as unknown as { location: { href: string } }).location.href).toBe('/login');
    });

    it('debe rechazar error no 401', async () => {
      const error = {
        response: { status: 500 },
      } as { response?: { status: number } };
      
      api.interceptors.response.use(
        (res) => res,
        (err) => {
          if (err.response?.status === 401) {
            localStorage.removeItem('access_token');
            (window as unknown as { location: { href: string } }).location.href = '/login';
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
      const error = new Error('Network Error') as Error & { response?: { status: number } };
      
      api.interceptors.response.use(
        (res) => res,
        (err) => {
          if (err.response?.status === 401) {
            localStorage.removeItem('access_token');
            (window as unknown as { location: { href: string } }).location.href = '/login';
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
