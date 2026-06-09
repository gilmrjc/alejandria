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
  folder_id: string | null;
  folder_name: string | null;
  folder_path: string | null;
}

export interface FolderTreeItem {
  type: 'folder' | 'document';
  id: string; // UUID for real items, path for virtual folders
  name: string;
  path: string;
  slug: string | null;
  children: FolderTreeItem[];
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
