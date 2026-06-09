import api from './api';
import type {
  CreateDocumentDto,
  Document,
  DocumentListItem,
  DocumentListParams,
  DocumentSnapshot,
  FolderTreeItem,
  PaginatedResponse,
  UpdateDocumentDto,
} from '@/types/document';

/**
 * Project-scoped document service.
 * 
 * Routes follow GitHub-style URL structure:
 *   /api/v1/{organization_slug}/{project_slug}/documents
 */
export const projectDocumentsService = {
  async list(
    orgSlug: string,
    projectSlug: string,
    params?: DocumentListParams
  ): Promise<PaginatedResponse<DocumentListItem>> {
    const response = await api.get<PaginatedResponse<DocumentListItem>>(
      `/${orgSlug}/${projectSlug}/documents`,
      { params }
    );
    return response.data;
  },

  async getTree(orgSlug: string, projectSlug: string): Promise<FolderTreeItem[]> {
    const response = await api.get<FolderTreeItem[]>(
      `/${orgSlug}/${projectSlug}/documents/tree`
    );
    return response.data;
  },

  async getBySlug(orgSlug: string, projectSlug: string, slug: string): Promise<Document> {
    const response = await api.get<Document>(
      `/${orgSlug}/${projectSlug}/documents/slug/${slug}`
    );
    return response.data;
  },

  async create(
    orgSlug: string,
    projectSlug: string,
    data: CreateDocumentDto
  ): Promise<Document> {
    const response = await api.post<Document>(
      `/${orgSlug}/${projectSlug}/documents`,
      data
    );
    return response.data;
  },

  async updateBySlug(
    orgSlug: string,
    projectSlug: string,
    slug: string,
    data: UpdateDocumentDto
  ): Promise<Document> {
    const response = await api.put<Document>(
      `/${orgSlug}/${projectSlug}/documents/slug/${slug}`,
      data
    );
    return response.data;
  },

  async deleteBySlug(orgSlug: string, projectSlug: string, slug: string): Promise<void> {
    await api.delete(`/${orgSlug}/${projectSlug}/documents/slug/${slug}`);
  },

  async getSnapshotsBySlug(
    orgSlug: string,
    projectSlug: string,
    slug: string
  ): Promise<PaginatedResponse<DocumentSnapshot>> {
    const response = await api.get<PaginatedResponse<DocumentSnapshot>>(
      `/${orgSlug}/${projectSlug}/documents/slug/${slug}/snapshots`
    );
    return response.data;
  },

  async restoreSnapshotBySlug(
    orgSlug: string,
    projectSlug: string,
    documentSlug: string,
    snapshotId: string
  ): Promise<Document> {
    const response = await api.post<Document>(
      `/${orgSlug}/${projectSlug}/documents/slug/${documentSlug}/snapshots/${snapshotId}/restore`
    );
    return response.data;
  },
};
