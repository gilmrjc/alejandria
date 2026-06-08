import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ProposalList } from '../ProposalList';
import type { Proposal } from '@/types/proposal';

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
    const mockProposals: Proposal[] = [
      { id: '1', slug: 'proposal-1', name: 'Test Proposal 1', description: 'Description 1', status: 'pending', created_at: '2024-01-01', updated_at: '2024-01-01' },
      { id: '2', slug: 'proposal-2', name: 'Test Proposal 2', description: 'Description 2', status: 'pending', created_at: '2024-01-01', updated_at: '2024-01-01' },
    ];

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

  it('debe llamar onProposalClick cuando se hace click en una propuesta', () => {
    const mockProposals: Proposal[] = [
      { id: '1', slug: 'proposal-1', name: 'Test Proposal 1', description: 'Description 1', status: 'pending', created_at: '2024-01-01', updated_at: '2024-01-01' },
    ];

    const onProposalClick = vi.fn();
    render(
      <ProposalList 
        proposals={mockProposals} 
        loading={false} 
        onProposalClick={onProposalClick} 
      />
    );

    screen.getByText('Test Proposal 1').click();
    expect(onProposalClick).toHaveBeenCalledWith('1');
  });
});
