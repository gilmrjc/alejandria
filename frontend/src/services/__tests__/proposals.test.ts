import { describe, it, expect, beforeEach } from 'vitest';
import { proposalsService } from '../proposals';
import { http, HttpResponse } from 'msw';
import { server } from '@/test/setup';

describe('proposalsService', () => {
  beforeEach(() => {
    // MSW handlers are reset in test/setup.ts afterEach
  });

  describe('list', () => {
    it('debe llamar API GET /proposals con params', async () => {
      const mockResponse = {
        items: [{ id: '1', name: 'Test' }],
        total: 1,
        page: 1,
        per_page: 10,
        total_pages: 1,
      };
      
      server.use(
        http.get('http://localhost:8000/api/v1/proposals', ({ request }) => {
          const url = new URL(request.url);
          expect(url.searchParams.get('page')).toBe('1');
          return HttpResponse.json(mockResponse);
        })
      );

      const result = await proposalsService.list({ page: 1 });
      expect(result).toEqual(mockResponse);
    });

    it('debe propagar error de API', async () => {
      server.use(
        http.get('http://localhost:8000/api/v1/proposals', () => {
          return HttpResponse.json({ error: 'API Error' }, { status: 500 });
        })
      );

      await expect(proposalsService.list()).rejects.toThrow();
    });
  });

  describe('get', () => {
    it('debe llamar API GET /proposals/:id', async () => {
      const mockProposal = { id: '1', name: 'Test' };
      
      server.use(
        http.get('http://localhost:8000/api/v1/proposals/1', () => {
          return HttpResponse.json(mockProposal);
        })
      );

      const result = await proposalsService.get('1');
      expect(result).toEqual(mockProposal);
    });
  });

  describe('create', () => {
    it('debe llamar API POST /proposals con datos', async () => {
      const mockProposal = { id: '1', name: 'New Proposal' };
      const mockData = { name: 'New Proposal', description: 'Description' };
      
      server.use(
        http.post('http://localhost:8000/api/v1/proposals', async ({ request }) => {
          const body = await request.json();
          expect(body).toEqual(mockData);
          return HttpResponse.json(mockProposal);
        })
      );

      const result = await proposalsService.create(mockData);
      expect(result).toEqual(mockProposal);
    });
  });

  describe('update', () => {
    it('debe llamar API PUT /proposals/:id con datos', async () => {
      const mockProposal = { id: '1', name: 'Updated' };
      const mockData = { status: 'approved' };
      
      server.use(
        http.put('http://localhost:8000/api/v1/proposals/1', async ({ request }) => {
          const body = await request.json();
          expect(body).toEqual(mockData);
          return HttpResponse.json(mockProposal);
        })
      );

      const result = await proposalsService.update('1', mockData);
      expect(result).toEqual(mockProposal);
    });
  });

  describe('delete', () => {
    it('debe llamar API DELETE /proposals/:id', async () => {
      server.use(
        http.delete('http://localhost:8000/api/v1/proposals/1', () => {
          return new HttpResponse(null, { status: 204 });
        })
      );

      await proposalsService.delete('1');
    });
  });
});
