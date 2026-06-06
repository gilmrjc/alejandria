import { create } from 'zustand';
import type { DocumentListItem, DocumentListParams } from '@/types/document';
import { documentsService } from '@/services/documents';

interface DocumentsState {
  documents: DocumentListItem[];
  total: number;
  page: number;
  loading: boolean;
  error: string | null;
  fetchDocuments: (params?: DocumentListParams) => Promise<void>;
}

export const useDocumentsStore = create<DocumentsState>((set) => ({
  documents: [],
  total: 0,
  page: 1,
  loading: false,
  error: null,

  fetchDocuments: async (params) => {
    set({ loading: true, error: null });
    try {
      const result = await documentsService.list(params);
      set({
        documents: result.items,
        total: result.pagination.total,
        page: result.pagination.page,
        loading: false,
      });
    } catch {
      set({ error: 'Error al cargar documentos', loading: false });
    }
  },
}));
