export type ProposalStatus = 'pending' | 'accepted' | 'rejected' | 'implemented';

export interface Proposal {
  id: string;
  slug: string;
  name: string;
  description: string;
  status: ProposalStatus;
  created_at: string;
  updated_at: string;
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
