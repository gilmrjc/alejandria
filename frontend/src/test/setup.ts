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
);

beforeAll(() => server.listen());
afterEach(() => {
  server.resetHandlers();
  cleanup();
});
afterAll(() => server.close());
