export interface DashboardStats {
  documents: DocumentStats;
  gaps: GapStats;
  proposals: ProposalStats;
  progress: ProgressMetrics;
}

export interface DocumentStats {
  total: number;
  avgRating: number | null;
  healthy: number;
  needsImprovement: number;
  noRating: number;
}

export interface GapStats {
  total: number;
  byPriority: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  byStatus: {
    pending: number;
    responded: number;
    rejected: number;
  };
  pending: number;
}

export interface ProposalStats {
  total: number;
  byStatus: {
    pending: number;
    accepted: number;
    rejected: number;
    implemented: number;
  };
  pending: number;
}

export interface ProgressMetrics {
  gapsResolvedPercentage: number;
  documentsHealthyPercentage: number;
  avgResolutionTimeHours: number | null;
  proposalAcceptanceRate: number;
}
