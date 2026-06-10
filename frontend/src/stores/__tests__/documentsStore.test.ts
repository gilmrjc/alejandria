import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useDocumentsStore } from '../documentsStore';
import { documentsService } from '@/services/documents';

vi.mock('@/services/documents');

describe('documentsStore', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debe tener estado inicial correcto', () => {
    const store = useDocumentsStore.getState();
    expect(store.documents).toEqual([]);
    expect(store.total).toBe(0);
    expect(store.page).toBe(1);
    expect(store.loading).toBe(false);
    expect(store.error).toBeNull();
  });

  it('debe llamar documentsService.list en fetchDocuments', async () => {
    const mockResponse = {
      items: [{ id: '1', title: 'Test', slug: 'test', filename: 'test.md', rating: 9, created_at: '2024-01-01', updated_at: '2024-01-01', folder_id: null, folder_name: null, folder_path: null }],
      pagination: { page: 1, per_page: 10, total: 1, total_pages: 1 },
    };
    
    vi.mocked(documentsService.list).mockResolvedValue(mockResponse);

    const store = useDocumentsStore.getState();
    await store.fetchDocuments();
    const updatedStore = useDocumentsStore.getState();

    expect(documentsService.list).toHaveBeenCalled();
    expect(updatedStore.documents).toEqual(mockResponse.items);
    expect(updatedStore.total).toBe(1);
  });

  it('debe manejar error en fetchDocuments', async () => {
    vi.mocked(documentsService.list).mockRejectedValue(new Error('API Error'));

    const store = useDocumentsStore.getState();
    await store.fetchDocuments();
    const updatedStore = useDocumentsStore.getState();

    expect(updatedStore.error).not.toBeNull();
  });
});
