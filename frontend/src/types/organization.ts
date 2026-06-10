export interface Organization {
  id: string;
  name: string;
  slug: string;
  is_personal: boolean;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectMetrics {
  document_count: number;
  gap_count: number;
  pending_gap_count: number;
  avg_rating: number | null;
  healthy_percentage: number;
}

export interface Project {
  id: string;
  organization_id: string;
  name: string;
  slug: string;
  description: string | null;
  created_by: string;
  created_at: string;
  updated_at: string;
  metrics?: ProjectMetrics;
}

export interface CreateOrganizationDto {
  name: string;
  slug: string;
}

export interface CreateProjectDto {
  organization_id: string;
  name: string;
  slug: string;
  description?: string;
}
