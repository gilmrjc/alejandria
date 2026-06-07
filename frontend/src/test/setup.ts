import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach, beforeAll, afterAll } from 'vitest';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

// MSW server for API mocking
export const server = setupServer(
  // Health check endpoint
  http.get('http://localhost:8000/api/v1/health', () => {
    return HttpResponse.json({ status: 'healthy' });
  }),
  // Document detail endpoints
  http.get('http://localhost:8000/api/v1/documents/123', () => {
    return HttpResponse.json({
      id: '123',
      title: 'Test Document',
      slug: 'test-doc',
      content: 'Test content',
      filename: 'test.md',
      rating: 8.5,
      project_id: 'proj-1',
      organization_id: 'org-1',
      created_by: 'user1',
      updated_by: 'user1',
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    });
  }),
  http.get('http://localhost:8000/api/v1/documents/123/snapshots', () => {
    return HttpResponse.json({
      items: [],
      pagination: { page: 1, per_page: 10, total: 0, total_pages: 0 },
    });
  }),
  // Gap detail endpoint
  http.get('http://localhost:8000/api/v1/gaps/slug/test-gap', () => {
    return HttpResponse.json({
      id: '1',
      slug: 'test-gap',
      question: 'Test question',
      context_missing: 'Test context',
      priority: 'high',
      status: 'pending',
      role_affected: 'developer',
      document_id: 'doc-1',
      answer: null,
      answered_at: null,
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    });
  }),
  // Proposal detail endpoint
  http.get('http://localhost:8000/api/v1/proposals/123', () => {
    return HttpResponse.json({
      id: '123',
      name: 'Test Proposal',
      slug: 'test-proposal',
      description: 'Test description',
      status: 'pending',
      gap_slugs: [],
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    });
  }),
);

beforeAll(() => server.listen());
afterEach(() => {
  server.resetHandlers();
  cleanup();
});
afterAll(() => server.close());
