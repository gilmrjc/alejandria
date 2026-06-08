import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { GapList } from '../GapList';
import type { Gap } from '@/types/gap';

describe('GapList', () => {
  it('debe mostrar loading state', () => {
    render(
      <GapList 
        gaps={[]} 
        loading={true} 
        onGapClick={vi.fn()} 
      />
    );

    expect(screen.getByText('Cargando gaps...')).toBeInTheDocument();
  });

  it('debe mostrar empty state cuando no hay gaps', () => {
    render(
      <GapList 
        gaps={[]} 
        loading={false} 
        onGapClick={vi.fn()} 
      />
    );

    expect(screen.getByText('No se encontraron gaps')).toBeInTheDocument();
  });

  it('debe renderizar lista de gaps', () => {
    const mockGaps: Gap[] = [
      { id: '1', document_id: '1', slug: 'gap-1', question: 'Test Question 1', priority: 'high', status: 'pending', context_missing: null, role_affected: null, answer: null, answered_at: null, created_at: '2024-01-01', updated_at: '2024-01-01' },
      { id: '2', document_id: '1', slug: 'gap-2', question: 'Test Question 2', priority: 'medium', status: 'pending', context_missing: null, role_affected: null, answer: null, answered_at: null, created_at: '2024-01-01', updated_at: '2024-01-01' },
    ];

    const onGapClick = vi.fn();
    render(
      <GapList 
        gaps={mockGaps} 
        loading={false} 
        onGapClick={onGapClick} 
      />
    );

    expect(screen.getByText('Test Question 1')).toBeInTheDocument();
    expect(screen.getByText('Test Question 2')).toBeInTheDocument();
  });

  it('debe llamar onGapClick cuando se hace click en un gap', () => {
    const mockGaps: Gap[] = [
      { id: '1', document_id: '1', slug: 'gap-1', question: 'Test Question 1', priority: 'high', status: 'pending', context_missing: null, role_affected: null, answer: null, answered_at: null, created_at: '2024-01-01', updated_at: '2024-01-01' },
    ];

    const onGapClick = vi.fn();
    render(
      <GapList 
        gaps={mockGaps} 
        loading={false} 
        onGapClick={onGapClick} 
      />
    );

    screen.getByText('Test Question 1').click();
    expect(onGapClick).toHaveBeenCalledWith('gap-1');
  });
});
