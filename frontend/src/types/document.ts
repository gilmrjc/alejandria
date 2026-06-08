export interface Document {
  id: string;
  title: string;
  slug: string;
  filename: string;
  content: string;
  rating: number | null;
  created_at: string;
  updated_at: string;
  created_by: string | null;
  updated_by: string | null;
}

export interface DocumentListItem {
  id: string;
  title: string;
  slug: string;
  filename: string;
  rating: number | null;
  created_at: string;
  updated_at: string;
}

export interface DocumentSnapshot {
  id: string;
  document_id: string;
  old_content: string | null;
  new_content: string;
  diff_type: 'full' | 'diff';
  rating: number | null;
  created_at: string;
  created_by: string | null;
}

export interface DocumentListParams {
  page?: number;
  per_page?: number;
  updated_after?: string | null;
  sort_by?: string;
  order?: 'asc' | 'desc';
}

export interface CreateDocumentDto {
  title: string;
  filename: string;
  content: string;
}

export interface UpdateDocumentDto {
  title?: string;
  filename?: string;
  content?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  pagination: {
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
  };
}
