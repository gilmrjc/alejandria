import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { GapsPage } from '../GapsPage';
import { useGapsStore } from '@/stores/gapsStore';

vi.mock('@/stores/gapsStore');
vi.mock('react-router-dom', () => ({
  useNavigate: () => vi.fn(),
}));

describe('GapsPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debe renderizar título y descripción', () => {
    vi.mocked(useGapsStore).mockReturnValue({
      gaps: [],
      loading: false,
      fetchGaps: vi.fn(),
      total: 0,
      page: 1,
      error: null,
    });

    render(<GapsPage />);

    expect(screen.getByText('Gaps')).toBeInTheDocument();
    expect(screen.getByText('Gaps detectados en documentos')).toBeInTheDocument();
  });

  it('debe renderizar GapFilters', () => {
    vi.mocked(useGapsStore).mockReturnValue({
      gaps: [],
      loading: false,
      fetchGaps: vi.fn(),
      total: 0,
      page: 1,
      error: null,
    });

    render(<GapsPage />);

    expect(screen.getByPlaceholderText('Buscar gaps...')).toBeInTheDocument();
  });

  it('debe renderizar GapList', () => {
    vi.mocked(useGapsStore).mockReturnValue({
      gaps: [],
      loading: false,
      fetchGaps: vi.fn(),
      total: 0,
      page: 1,
      error: null,
    });

    render(<GapsPage />);

    expect(screen.getByText('No se encontraron gaps')).toBeInTheDocument();
  });

  it('debe llamar fetchGaps al montar', () => {
    const fetchGaps = vi.fn();
    vi.mocked(useGapsStore).mockReturnValue({
      gaps: [],
      loading: false,
      fetchGaps,
      total: 0,
      page: 1,
      error: null,
    });

    render(<GapsPage />);

    expect(fetchGaps).toHaveBeenCalled();
  });

  it('debe filtrar gaps por búsqueda', () => {
    const mockGaps = [
      { id: '1', question: 'Test Gap', slug: 'test', priority: 'high', status: 'pending', document_id: '1', created_at: '2024-01-01' },
      { id: '2', question: 'Other Gap', slug: 'other', priority: 'medium', status: 'pending', document_id: '1', created_at: '2024-01-01' },
    ];
    vi.mocked(useGapsStore).mockReturnValue({
      gaps: mockGaps,
      loading: false,
      fetchGaps: vi.fn(),
      total: 2,
      page: 1,
      error: null,
    });

    render(<GapsPage />);

    const searchInput = screen.getByPlaceholderText('Buscar gaps...');
    searchInput.dispatchEvent(new Event('change', { bubbles: true }));
    Object.assign(searchInput, { value: 'Test' });
  });
});
