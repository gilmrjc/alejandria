import { describe, it, expect, beforeEach } from 'vitest';
import { documentsService } from '../documents';
import { http, HttpResponse } from 'msw';
import { server } from '@/test/setup';

describe('documentsService', () => {
  beforeEach(() => {
    // MSW handlers are reset in test/setup.ts afterEach
  });

  describe('list', () => {
    it('debe llamar API GET /documents con params', async () => {
      const mockResponse = {
        items: [{ id: '1', title: 'Test' }],
        pagination: { page: 1, per_page: 10, total: 1, total_pages: 1 },
      };
      
      server.use(
        http.get('http://localhost:8000/api/v1/documents', ({ request }) => {
          const url = new URL(request.url);
          expect(url.searchParams.get('page')).toBe('1');
          return HttpResponse.json(mockResponse);
        })
      );

      const result = await documentsService.list({ page: 1 });
      expect(result).toEqual(mockResponse);
    });

    it('debe llamar API GET /documents sin params', async () => {
      const mockResponse = {
        items: [],
        pagination: { page: 1, per_page: 10, total: 0, total_pages: 0 },
      };
      
      server.use(
        http.get('http://localhost:8000/api/v1/documents', () => {
          return HttpResponse.json(mockResponse);
        })
      );

      const result = await documentsService.list();
      expect(result).toEqual(mockResponse);
    });

    it('debe propagar error de API', async () => {
      server.use(
        http.get('http://localhost:8000/api/v1/documents', () => {
          return HttpResponse.json({ error: 'API Error' }, { status: 500 });
        })
      );

      await expect(documentsService.list()).rejects.toThrow();
    });
  });

  describe('get', () => {
    it('debe llamar API GET /documents/:id', async () => {
      const mockDocument = { id: '1', title: 'Test' };
      
      server.use(
        http.get('http://localhost:8000/api/v1/documents/1', () => {
          return HttpResponse.json(mockDocument);
        })
      );

      const result = await documentsService.get('1');
      expect(result).toEqual(mockDocument);
    });
  });

  describe('getBySlug', () => {
    it('debe llamar API GET /documents/slug/:slug', async () => {
      const mockDocument = { id: '1', slug: 'test', title: 'Test' };
      
      server.use(
        http.get('http://localhost:8000/api/v1/documents/slug/test', () => {
          return HttpResponse.json(mockDocument);
        })
      );

      const result = await documentsService.getBySlug('test');
      expect(result).toEqual(mockDocument);
    });
  });

  describe('create', () => {
    it('debe llamar API POST /documents con datos', async () => {
      const mockDocument = { id: '1', title: 'New Doc' };
      const mockData = { title: 'New Doc', content: 'Content', filename: 'test.md' };
      
      server.use(
        http.post('http://localhost:8000/api/v1/documents', async ({ request }) => {
          const body = await request.json();
          expect(body).toEqual(mockData);
          return HttpResponse.json(mockDocument);
        })
      );

      const result = await documentsService.create(mockData);
      expect(result).toEqual(mockDocument);
    });
  });

  describe('update', () => {
    it('debe llamar API PUT /documents/:id con datos', async () => {
      const mockDocument = { id: '1', title: 'Updated' };
      const mockData = { title: 'Updated' };
      
      server.use(
        http.put('http://localhost:8000/api/v1/documents/1', async ({ request }) => {
          const body = await request.json();
          expect(body).toEqual(mockData);
          return HttpResponse.json(mockDocument);
        })
      );

      const result = await documentsService.update('1', mockData as { title: string });
      expect(result).toEqual(mockDocument);
    });
  });

  describe('updateBySlug', () => {
    it('debe llamar API PUT /documents/slug/:slug con datos', async () => {
      const mockDocument = { id: '1', slug: 'test', title: 'Updated' };
      const mockData = { title: 'Updated' };
      
      server.use(
        http.put('http://localhost:8000/api/v1/documents/slug/test', async ({ request }) => {
          const body = await request.json();
          expect(body).toEqual(mockData);
          return HttpResponse.json(mockDocument);
        })
      );

      const result = await documentsService.updateBySlug('test', mockData as { title: string });
      expect(result).toEqual(mockDocument);
    });
  });

  describe('delete', () => {
    it('debe llamar API DELETE /documents/:id', async () => {
      server.use(
        http.delete('http://localhost:8000/api/v1/documents/1', () => {
          return new HttpResponse(null, { status: 204 });
        })
      );

      await documentsService.delete('1');
    });
  });

  describe('deleteBySlug', () => {
    it('debe llamar API DELETE /documents/slug/:slug', async () => {
      server.use(
        http.delete('http://localhost:8000/api/v1/documents/slug/test', () => {
          return new HttpResponse(null, { status: 204 });
        })
      );

      await documentsService.deleteBySlug('test');
    });
  });

  describe('getSnapshots', () => {
    it('debe llamar API GET /documents/:id/snapshots', async () => {
      const mockResponse = {
        items: [{ id: '1', content: 'Snapshot' }],
        pagination: { page: 1, per_page: 10, total: 1, total_pages: 1 },
      };
      
      server.use(
        http.get('http://localhost:8000/api/v1/documents/1/snapshots', () => {
          return HttpResponse.json(mockResponse);
        })
      );

      const result = await documentsService.getSnapshots('1');
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getSnapshotsBySlug', () => {
    it('debe llamar API GET /documents/slug/:slug/snapshots', async () => {
      const mockResponse = {
        items: [{ id: '1', content: 'Snapshot' }],
        pagination: { page: 1, per_page: 10, total: 1, total_pages: 1 },
      };
      
      server.use(
        http.get('http://localhost:8000/api/v1/documents/slug/test/snapshots', () => {
          return HttpResponse.json(mockResponse);
        })
      );

      const result = await documentsService.getSnapshotsBySlug('test');
      expect(result).toEqual(mockResponse);
    });
  });

  describe('restoreSnapshot', () => {
    it('debe llamar API POST /documents/:id/snapshots/:snapshotId/restore', async () => {
      const mockDocument = { id: '1', title: 'Restored' };
      
      server.use(
        http.post('http://localhost:8000/api/v1/documents/1/snapshots/snap1/restore', () => {
          return HttpResponse.json(mockDocument);
        })
      );

      const result = await documentsService.restoreSnapshot('1', 'snap1');
      expect(result).toEqual(mockDocument);
    });
  });

  describe('restoreSnapshotBySlug', () => {
    it('debe llamar API POST /documents/slug/:slug/snapshots/:snapshotId/restore', async () => {
      const mockDocument = { id: '1', slug: 'test', title: 'Restored' };
      
      server.use(
        http.post('http://localhost:8000/api/v1/documents/slug/test/snapshots/snap1/restore', () => {
          return HttpResponse.json(mockDocument);
        })
      );

      const result = await documentsService.restoreSnapshotBySlug('test', 'snap1');
      expect(result).toEqual(mockDocument);
    });
  });
});
