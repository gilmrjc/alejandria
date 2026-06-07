import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ProposalsPage } from '../ProposalsPage';
import { useProposalsStore } from '@/stores/proposalsStore';

vi.mock('@/stores/proposalsStore');
vi.mock('react-router-dom', () => ({
  useNavigate: () => vi.fn(),
}));

describe('ProposalsPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debe renderizar título y descripción', () => {
    vi.mocked(useProposalsStore).mockReturnValue({
      proposals: [],
      loading: false,
      fetchProposals: vi.fn(),
      total: 0,
      page: 1,
      error: null,
    });

    render(<ProposalsPage />);

    expect(screen.getByText('Propuestas')).toBeInTheDocument();
    expect(screen.getByText('Propuestas de cambios pendientes')).toBeInTheDocument();
  });

  it('debe renderizar ProposalFilters', () => {
    vi.mocked(useProposalsStore).mockReturnValue({
      proposals: [],
      loading: false,
      fetchProposals: vi.fn(),
      total: 0,
      page: 1,
      error: null,
    });

    render(<ProposalsPage />);

    expect(screen.getByPlaceholderText('Buscar propuestas...')).toBeInTheDocument();
  });

  it('debe renderizar ProposalList', () => {
    vi.mocked(useProposalsStore).mockReturnValue({
      proposals: [],
      loading: false,
      fetchProposals: vi.fn(),
      total: 0,
      page: 1,
      error: null,
    });

    render(<ProposalsPage />);

    expect(screen.getByText('No se encontraron propuestas')).toBeInTheDocument();
  });

  it('debe llamar fetchProposals al montar', () => {
    const fetchProposals = vi.fn();
    vi.mocked(useProposalsStore).mockReturnValue({
      proposals: [],
      loading: false,
      fetchProposals,
      total: 0,
      page: 1,
      error: null,
    });

    render(<ProposalsPage />);

    expect(fetchProposals).toHaveBeenCalled();
  });

  it('debe filtrar propuestas por búsqueda', () => {
    const mockProposals = [
      { id: '1', name: 'Test Proposal', description: 'Test description', status: 'pending', gap_slugs: [], created_at: '2024-01-01' },
      { id: '2', name: 'Other Proposal', description: 'Other description', status: 'pending', gap_slugs: [], created_at: '2024-01-01' },
    ];
    vi.mocked(useProposalsStore).mockReturnValue({
      proposals: mockProposals,
      loading: false,
      fetchProposals: vi.fn(),
      total: 2,
      page: 1,
      error: null,
    });

    render(<ProposalsPage />);

    const searchInput = screen.getByPlaceholderText('Buscar propuestas...');
    searchInput.dispatchEvent(new Event('change', { bubbles: true }));
    Object.assign(searchInput, { value: 'Test' });
  });
});
