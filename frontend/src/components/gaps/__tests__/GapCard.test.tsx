import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { GapCard } from '../GapCard';
import type { Gap } from '@/types/gap';

describe('GapCard', () => {
  const mockGap: Gap = {
    id: '1',
    document_id: 'doc-1',
    document_slug: 'doc-1',
    document_title: 'Test Document',
    slug: 'test-gap',
    question: 'What is the purpose?',
    context_missing: 'Purpose statement',
    priority: 'high',
    role_affected: 'Developer',
    status: 'pending',
    answer: null,
    answered_at: null,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  };

  it('renders gap question', () => {
    render(<GapCard gap={mockGap} onClick={vi.fn()} />);
    expect(screen.getByText('What is the purpose?')).toBeInTheDocument();
  });

  it('renders priority badge', () => {
    render(<GapCard gap={mockGap} onClick={vi.fn()} />);
    expect(screen.getByText('Alto')).toBeInTheDocument();
  });

  it('renders context missing', () => {
    render(<GapCard gap={mockGap} onClick={vi.fn()} />);
    expect(screen.getByText(/Contexto faltante/)).toBeInTheDocument();
  });

  it('calls onClick when card is clicked', () => {
    const handleClick = vi.fn();
    render(<GapCard gap={mockGap} onClick={handleClick} />);
    
    screen.getByText('What is the purpose?').click();
    expect(handleClick).toHaveBeenCalled();
  });

  it('renders responded status', () => {
    const respondedGap = { ...mockGap, status: 'responded' as const, answered_at: '2024-01-02T00:00:00Z' };
    render(<GapCard gap={respondedGap} onClick={vi.fn()} />);
    
    expect(screen.getByText('Respondido')).toBeInTheDocument();
    expect(screen.getByText(/Respondido:/)).toBeInTheDocument();
  });

  it('renders rejected status', () => {
    const rejectedGap = { ...mockGap, status: 'rejected' as const };
    render(<GapCard gap={rejectedGap} onClick={vi.fn()} />);
    
    expect(screen.getByText('Rechazado')).toBeInTheDocument();
  });

  it('does not render answered date when not answered', () => {
    render(<GapCard gap={mockGap} onClick={vi.fn()} />);
    
    expect(screen.queryByText(/Respondido:/)).not.toBeInTheDocument();
  });

  it('does not render context missing when null', () => {
    const gapWithoutContext = { ...mockGap, context_missing: null };
    render(<GapCard gap={gapWithoutContext} onClick={vi.fn()} />);
    
    expect(screen.queryByText(/Contexto faltante/)).not.toBeInTheDocument();
  });

  it('falls back to pending status for unknown status', () => {
    const unknownGap = { ...mockGap, status: 'unknown' as 'pending' | 'responded' | 'rejected' };
    render(<GapCard gap={unknownGap} onClick={vi.fn()} />);
    
    expect(screen.getByText('Pendiente')).toBeInTheDocument();
  });
});
