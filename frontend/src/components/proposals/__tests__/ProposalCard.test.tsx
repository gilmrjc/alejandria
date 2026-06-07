import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ProposalCard } from '../ProposalCard';
import type { Proposal } from '@/types/proposal';

describe('ProposalCard', () => {
  const mockProposal: Proposal = {
    id: '1',
    slug: 'test-proposal',
    name: 'Update Documentation',
    description: 'Add missing sections to documentation',
    status: 'pending',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  };

  it('renders proposal name', () => {
    render(<ProposalCard proposal={mockProposal} onClick={vi.fn()} />);
    expect(screen.getByText('Update Documentation')).toBeInTheDocument();
  });

  it('renders proposal description', () => {
    render(<ProposalCard proposal={mockProposal} onClick={vi.fn()} />);
    expect(screen.getByText('Add missing sections to documentation')).toBeInTheDocument();
  });

  it('renders status badge', () => {
    render(<ProposalCard proposal={mockProposal} onClick={vi.fn()} />);
    expect(screen.getByText('Pendiente')).toBeInTheDocument();
  });

  it('calls onClick when card is clicked', () => {
    const handleClick = vi.fn();
    render(<ProposalCard proposal={mockProposal} onClick={handleClick} />);
    
    screen.getByText('Update Documentation').click();
    expect(handleClick).toHaveBeenCalled();
  });
});
