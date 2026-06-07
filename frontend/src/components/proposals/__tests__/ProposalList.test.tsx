import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ProposalList } from '../ProposalList';

describe('ProposalList', () => {
  it('debe mostrar loading state', () => {
    render(
      <ProposalList 
        proposals={[]} 
        loading={true} 
        onProposalClick={vi.fn()} 
      />
    );

    expect(screen.getByText('Cargando propuestas...')).toBeInTheDocument();
  });

  it('debe mostrar empty state cuando no hay propuestas', () => {
    render(
      <ProposalList 
        proposals={[]} 
        loading={false} 
        onProposalClick={vi.fn()} 
      />
    );

    expect(screen.getByText('No se encontraron propuestas')).toBeInTheDocument();
  });

  it('debe renderizar lista de propuestas', () => {
    const mockProposals = [
      { id: '1', name: 'Test Proposal 1', description: 'Description 1', status: 'pending' },
      { id: '2', name: 'Test Proposal 2', description: 'Description 2', status: 'pending' },
    ] as any;

    const onProposalClick = vi.fn();
    render(
      <ProposalList 
        proposals={mockProposals} 
        loading={false} 
        onProposalClick={onProposalClick} 
      />
    );

    expect(screen.getByText('Test Proposal 1')).toBeInTheDocument();
    expect(screen.getByText('Test Proposal 2')).toBeInTheDocument();
  });
});
