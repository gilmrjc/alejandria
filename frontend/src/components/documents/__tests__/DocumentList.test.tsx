import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { DocumentList } from '../DocumentList';
import type { DocumentListItem } from '@/types/document';

describe('DocumentList', () => {
  const mockDocuments: DocumentListItem[] = [
    {
      id: '1',
      title: 'Test Document',
      slug: 'test-document',
      filename: 'test.md',
      rating: 9.5,
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-02T00:00:00Z',
      folder_id: null,
      folder_name: null,
      folder_path: null,
    },
  ];

  it('renders documents when not loading', () => {
    render(
      <DocumentList
        documents={mockDocuments}
        loading={false}
        onDocumentClick={vi.fn()}
      />
    );
    expect(screen.getByText('Test Document')).toBeInTheDocument();
  });

  it('shows loading state', () => {
    render(
      <DocumentList
        documents={[]}
        loading={true}
        onDocumentClick={vi.fn()}
      />
    );
    expect(screen.getByText('Cargando documentos...')).toBeInTheDocument();
  });

  it('shows empty state when no documents', () => {
    render(
      <DocumentList
        documents={[]}
        loading={false}
        onDocumentClick={vi.fn()}
      />
    );
    expect(screen.getByText('No se encontraron documentos')).toBeInTheDocument();
  });

  it('calls onDocumentClick when document is clicked', () => {
    const handleClick = vi.fn();
    render(
      <DocumentList
        documents={mockDocuments}
        loading={false}
        onDocumentClick={handleClick}
      />
    );
    
    screen.getByText('Test Document').click();
    expect(handleClick).toHaveBeenCalled();
  });
});
