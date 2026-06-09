export type ProposalStatus = 'pending' | 'accepted' | 'rejected' | 'implemented';

export interface ProposalGap {
  id: string;
  slug: string;
  question: string;
  answer: string | null;
  priority: string;
  status: string;
  context_missing: string | null;
  role_affected: string | null;
}

export interface ProposalDocument {
  id: string;
  slug: string;
  title: string;
  rating: number | null;
}

export interface Proposal {
  id: string;
  slug: string;
  name: string;
  description: string;
  status: ProposalStatus;
  created_at: string;
  updated_at: string;
  old_content?: string;
  new_content?: string;
  gaps?: ProposalGap[];
  documents?: ProposalDocument[];
}

export interface ProposalListItem {
  id: string;
  slug: string;
  name: string;
  status: ProposalStatus;
  created_at: string;
}

export interface ProposalListParams {
  page?: number;
  per_page?: number;
  status?: ProposalStatus;
}
