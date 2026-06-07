import api from './api';
import type {
  CreateDocumentDto,
  Document,
  DocumentListItem,
  DocumentListParams,
  DocumentSnapshot,
  PaginatedResponse,
  UpdateDocumentDto,
} from '@/types/document';

export const documentsService = {
  async list(params?: DocumentListParams): Promise<PaginatedResponse<DocumentListItem>> {
    const response = await api.get<PaginatedResponse<DocumentListItem>>('/documents', { params });
    return response.data;
  },

  async getBySlug(slug: string): Promise<Document> {
    const response = await api.get<Document>(`/documents/slug/${slug}`);
    return response.data;
  },

  async get(id: string): Promise<Document> {
    const response = await api.get<Document>(`/documents/${id}`);
    return response.data;
  },

  async create(data: CreateDocumentDto): Promise<Document> {
    const response = await api.post<Document>('/documents', data);
    return response.data;
  },

  async updateBySlug(slug: string, data: UpdateDocumentDto): Promise<Document> {
    const response = await api.put<Document>(`/documents/slug/${slug}`, data);
    return response.data;
  },

  async update(id: string, data: UpdateDocumentDto): Promise<Document> {
    const response = await api.put<Document>(`/documents/${id}`, data);
    return response.data;
  },

  async deleteBySlug(slug: string): Promise<void> {
    await api.delete(`/documents/slug/${slug}`);
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/documents/${id}`);
  },

  async getSnapshotsBySlug(slug: string): Promise<PaginatedResponse<DocumentSnapshot>> {
    const response = await api.get<PaginatedResponse<DocumentSnapshot>>(
      `/documents/slug/${slug}/snapshots`
    );
    return response.data;
  },

  async getSnapshots(id: string): Promise<PaginatedResponse<DocumentSnapshot>> {
    const response = await api.get<PaginatedResponse<DocumentSnapshot>>(
      `/documents/${id}/snapshots`
    );
    return response.data;
  },

  async restoreSnapshotBySlug(documentSlug: string, snapshotId: string): Promise<Document> {
    const response = await api.post<Document>(
      `/documents/slug/${documentSlug}/snapshots/${snapshotId}/restore`
    );
    return response.data;
  },

  async restoreSnapshot(documentId: string, snapshotId: string): Promise<Document> {
    const response = await api.post<Document>(
      `/documents/${documentId}/snapshots/${snapshotId}/restore`
    );
    return response.data;
  },
};
