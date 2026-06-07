import { describe, it, expect, beforeEach } from 'vitest';
import { gapsService } from '../gaps';
import { http, HttpResponse } from 'msw';
import { server } from '@/test/setup';

describe('gapsService', () => {
  beforeEach(() => {
    // MSW handlers are reset in test/setup.ts afterEach
  });

  describe('list', () => {
    it('debe llamar API GET /gaps con params', async () => {
      const mockResponse = {
        items: [{ id: '1', question: 'Test' }],
        pagination: { page: 1, per_page: 10, total: 1, total_pages: 1 },
      };
      
      server.use(
        http.get('http://localhost:8000/api/v1/gaps', () => {
          return HttpResponse.json(mockResponse);
        })
      );

      const result = await gapsService.list({});
      expect(result).toEqual(mockResponse);
    });

    it('debe propagar error de API', async () => {
      server.use(
        http.get('http://localhost:8000/api/v1/gaps', () => {
          return HttpResponse.json({ error: 'API Error' }, { status: 500 });
        })
      );

      await expect(gapsService.list()).rejects.toThrow();
    });
  });

  describe('get', () => {
    it('debe llamar API GET /gaps/:id', async () => {
      const mockGap = { id: '1', question: 'Test' };
      
      server.use(
        http.get('http://localhost:8000/api/v1/gaps/1', () => {
          return HttpResponse.json(mockGap);
        })
      );

      const result = await gapsService.get('1');
      expect(result).toEqual(mockGap);
    });
  });

  describe('getBySlug', () => {
    it('debe llamar API GET /gaps/slug/:slug', async () => {
      const mockGap = { id: '1', slug: 'test', question: 'Test' };
      
      server.use(
        http.get('http://localhost:8000/api/v1/gaps/slug/test', () => {
          return HttpResponse.json(mockGap);
        })
      );

      const result = await gapsService.getBySlug('test');
      expect(result).toEqual(mockGap);
    });
  });

  describe('create', () => {
    it('debe llamar API POST /gaps con datos', async () => {
      const mockGap = { id: '1', question: 'New Gap' };
      const mockData = { document_id: '1', question: 'New Gap', priority: 'high' };
      
      server.use(
        http.post('http://localhost:8000/api/v1/gaps', async ({ request }) => {
          const body = await request.json();
          expect(body).toEqual(mockData);
          return HttpResponse.json(mockGap);
        })
      );

      const result = await gapsService.create(mockData);
      expect(result).toEqual(mockGap);
    });
  });

  describe('update', () => {
    it('debe llamar API PUT /gaps/:id con datos', async () => {
      const mockGap = { id: '1', question: 'Updated' };
      const mockData = { answer: 'Answer' };
      
      server.use(
        http.put('http://localhost:8000/api/v1/gaps/1', async ({ request }) => {
          const body = await request.json();
          expect(body).toEqual(mockData);
          return HttpResponse.json(mockGap);
        })
      );

      const result = await gapsService.update('1', mockData);
      expect(result).toEqual(mockGap);
    });
  });

  describe('updateBySlug', () => {
    it('debe llamar API PUT /gaps/slug/:slug con datos', async () => {
      const mockGap = { id: '1', slug: 'test', question: 'Updated' };
      const mockData = { answer: 'Answer' };
      
      server.use(
        http.put('http://localhost:8000/api/v1/gaps/slug/test', async ({ request }) => {
          const body = await request.json();
          expect(body).toEqual(mockData);
          return HttpResponse.json(mockGap);
        })
      );

      const result = await gapsService.updateBySlug('test', mockData);
      expect(result).toEqual(mockGap);
    });
  });

  describe('delete', () => {
    it('debe llamar API DELETE /gaps/:id', async () => {
      server.use(
        http.delete('http://localhost:8000/api/v1/gaps/1', () => {
          return new HttpResponse(null, { status: 204 });
        })
      );

      await gapsService.delete('1');
    });
  });

  describe('deleteBySlug', () => {
    it('debe llamar API DELETE /gaps/slug/:slug', async () => {
      server.use(
        http.delete('http://localhost:8000/api/v1/gaps/slug/test', () => {
          return new HttpResponse(null, { status: 204 });
        })
      );

      await gapsService.deleteBySlug('test');
    });
  });
});
