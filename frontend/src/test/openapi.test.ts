/**
 * Tests for OpenAPI schema validation
 * Ensures that the generated TypeScript types match the actual API schema
 */

import { describe, it, expect } from 'vitest';
import { paths, components } from '../types/api';

describe('OpenAPI Schema Validation', () => {
  describe('Metrics Endpoint', () => {
    it('should have metrics endpoint defined in paths', () => {
      // Type check - if this compiles, the path exists
      const metricsPath: paths['/api/v1/metrics'] = {} as unknown as paths['/api/v1/metrics'];
      expect(metricsPath).toBeDefined();
    });

    it('should have DashboardMetricsResponse type defined', () => {
      // Type check - if this compiles, the type exists
      const dashboardMetrics: components['schemas']['DashboardMetricsResponse'] = {} as unknown as components['schemas']['DashboardMetricsResponse'];
      expect(dashboardMetrics).toBeDefined();
    });

    it('should have DocumentStats type with camelCase fields', () => {
      // Type check - if this compiles, the type exists with correct fields
      const docStats: components['schemas']['DocumentStats'] = {
        total: 0,
        avgRating: null,
        healthy: 0,
        needsImprovement: 0,
        noRating: 0,
      };
      expect(docStats.total).toBe(0);
      expect(docStats.avgRating).toBeNull();
      expect(docStats.healthy).toBe(0);
      expect(docStats.needsImprovement).toBe(0);
      expect(docStats.noRating).toBe(0);
    });

    it('should have GapStats type with nested byPriority', () => {
      const gapStats: components['schemas']['GapStats'] = {
        total: 0,
        byPriority: { critical: 0, high: 0, medium: 0, low: 0 },
        byStatus: { pending: 0, responded: 0, rejected: 0 },
        pending: 0,
      };
      expect(gapStats.total).toBe(0);
      expect(gapStats.byPriority.critical).toBe(0);
      expect(gapStats.byStatus.pending).toBe(0);
      expect(gapStats.pending).toBe(0);
    });

    it('should have GapByPriority type with priority levels', () => {
      const gapByPriority: components['schemas']['GapByPriority'] = {
        critical: 0,
        high: 0,
        medium: 0,
        low: 0,
      };
      expect(gapByPriority.critical).toBe(0);
      expect(gapByPriority.high).toBe(0);
      expect(gapByPriority.medium).toBe(0);
      expect(gapByPriority.low).toBe(0);
    });

    it('should have GapByStatus type with status values', () => {
      const gapByStatus: components['schemas']['GapByStatus'] = {
        pending: 0,
        responded: 0,
        rejected: 0,
      };
      expect(gapByStatus.pending).toBe(0);
      expect(gapByStatus.responded).toBe(0);
      expect(gapByStatus.rejected).toBe(0);
    });

    it('should have ProposalStats type with nested byStatus', () => {
      const proposalStats: components['schemas']['ProposalStats'] = {
        total: 0,
        byStatus: { pending: 0, accepted: 0, rejected: 0, implemented: 0 },
        pending: 0,
      };
      expect(proposalStats.total).toBe(0);
      expect(proposalStats.byStatus.pending).toBe(0);
      expect(proposalStats.pending).toBe(0);
    });

    it('should have ProposalByStatus type with status values', () => {
      const proposalByStatus: components['schemas']['ProposalByStatus'] = {
        pending: 0,
        accepted: 0,
        rejected: 0,
        implemented: 0,
      };
      expect(proposalByStatus.pending).toBe(0);
      expect(proposalByStatus.accepted).toBe(0);
      expect(proposalByStatus.rejected).toBe(0);
      expect(proposalByStatus.implemented).toBe(0);
    });

    it('should have ProgressMetrics type with camelCase fields', () => {
      const progressMetrics: components['schemas']['ProgressMetrics'] = {
        gapsResolvedPercentage: 0,
        documentsHealthyPercentage: 0,
        avgResolutionTimeHours: null,
        proposalAcceptanceRate: 0,
      };
      expect(progressMetrics.gapsResolvedPercentage).toBe(0);
      expect(progressMetrics.documentsHealthyPercentage).toBe(0);
      expect(progressMetrics.avgResolutionTimeHours).toBeNull();
      expect(progressMetrics.proposalAcceptanceRate).toBe(0);
    });

    it('should have DashboardMetricsResponse with all required sections', () => {
      const dashboardMetrics: components['schemas']['DashboardMetricsResponse'] = {
        documents: {} as unknown as components['schemas']['DocumentStats'],
        gaps: {} as unknown as components['schemas']['GapStats'],
        proposals: {} as unknown as components['schemas']['ProposalStats'],
        progress: {} as unknown as components['schemas']['ProgressMetrics'],
      };
      expect(dashboardMetrics.documents).toBeDefined();
      expect(dashboardMetrics.gaps).toBeDefined();
      expect(dashboardMetrics.proposals).toBeDefined();
      expect(dashboardMetrics.progress).toBeDefined();
    });
  });
});
