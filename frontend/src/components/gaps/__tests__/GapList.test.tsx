import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { GapList } from '../GapList';

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
    const mockGaps = [
      { id: '1', slug: 'gap-1', question: 'Test Question 1', priority: 'high', status: 'pending' },
      { id: '2', slug: 'gap-2', question: 'Test Question 2', priority: 'medium', status: 'pending' },
    ] as any;

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
});
