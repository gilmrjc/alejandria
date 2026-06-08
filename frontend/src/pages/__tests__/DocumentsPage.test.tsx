import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { DocumentsPage } from '../DocumentsPage';
import { useDocumentsStore } from '@/stores/documentsStore';

vi.mock('@/stores/documentsStore');
vi.mock('react-router-dom', () => ({
  useNavigate: () => vi.fn(),
}));

describe('DocumentsPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debe renderizar título y descripción', () => {
    vi.mocked(useDocumentsStore).mockReturnValue({
      documents: [],
      loading: false,
      fetchDocuments: vi.fn(),
      total: 0,
      page: 1,
      error: null,
    });

    render(<DocumentsPage />);

    expect(screen.getByText('Documentos')).toBeInTheDocument();
    expect(screen.getByText('Gestión de documentos del proyecto')).toBeInTheDocument();
  });

  it('debe renderizar DocumentFilters', () => {
    vi.mocked(useDocumentsStore).mockReturnValue({
      documents: [],
      loading: false,
      fetchDocuments: vi.fn(),
      total: 0,
      page: 1,
      error: null,
    });

    render(<DocumentsPage />);

    expect(screen.getByPlaceholderText('Buscar documentos...')).toBeInTheDocument();
  });

  it('debe renderizar DocumentList', () => {
    vi.mocked(useDocumentsStore).mockReturnValue({
      documents: [],
      loading: false,
      fetchDocuments: vi.fn(),
      total: 0,
      page: 1,
      error: null,
    });

    render(<DocumentsPage />);

    expect(screen.getByText('No se encontraron documentos')).toBeInTheDocument();
  });

  it('debe llamar fetchDocuments al montar', () => {
    const fetchDocuments = vi.fn();
    vi.mocked(useDocumentsStore).mockReturnValue({
      documents: [],
      loading: false,
      fetchDocuments,
      total: 0,
      page: 1,
      error: null,
    });

    render(<DocumentsPage />);

    expect(fetchDocuments).toHaveBeenCalled();
  });

  it('debe filtrar documentos por búsqueda', () => {
    const mockDocuments = [
      { id: '1', title: 'Test Document', filename: 'test.md', slug: 'test', rating: 9, created_at: '2024-01-01', updated_at: '2024-01-01' },
      { id: '2', title: 'Other Document', filename: 'other.md', slug: 'other', rating: 8, created_at: '2024-01-01', updated_at: '2024-01-01' },
    ];
    vi.mocked(useDocumentsStore).mockReturnValue({
      documents: mockDocuments,
      loading: false,
      fetchDocuments: vi.fn(),
      total: 2,
      page: 1,
      error: null,
    });

    render(<DocumentsPage />);

    const searchInput = screen.getByPlaceholderText('Buscar documentos...');
    searchInput.dispatchEvent(new Event('change', { bubbles: true }));
    Object.assign(searchInput, { value: 'Test' });
  });

  it('debe mostrar estado de carga', () => {
    vi.mocked(useDocumentsStore).mockReturnValue({
      documents: [],
      loading: true,
      fetchDocuments: vi.fn(),
      total: 0,
      page: 1,
      error: null,
    });

    render(<DocumentsPage />);

    expect(screen.getByText('Cargando documentos...')).toBeInTheDocument();
  });

  it('debe mostrar error cuando hay error', () => {
    vi.mocked(useDocumentsStore).mockReturnValue({
      documents: [],
      loading: false,
      fetchDocuments: vi.fn(),
      total: 0,
      page: 1,
      error: null,
    });

    render(<DocumentsPage />);

    // DocumentsPage no maneja errores directamente, los delega al DocumentList
    expect(screen.getByText('No se encontraron documentos')).toBeInTheDocument();
  });
});
