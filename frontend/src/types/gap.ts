export type GapPriority = 'critical' | 'high' | 'medium' | 'low';
export type GapStatus = 'pending' | 'responded' | 'rejected';

export interface ReferenceDocument {
  id: string;
  slug: string;
  title: string;
  filename: string;
}

export interface Gap {
  id: string;
  document_id: string;
  document_slug: string | null;
  document_title: string | null;
  slug: string;
  question: string;
  context_missing: string | null;
  priority: GapPriority;
  role_affected: string | null;
  status: GapStatus;
  answer: string | null;
  answered_at: string | null;
  created_at: string;
  updated_at: string;
  reference_documents?: ReferenceDocument[];
}

export interface GapListParams {
  status?: GapStatus;
  document_id?: string;
}

