import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { DocumentMetadata } from '../DocumentMetadata';

describe('DocumentMetadata', () => {
  const mockDocument = {
    id: '1',
    title: 'Test Document',
    filename: 'test.md',
    rating: 8.5,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-02T00:00:00Z',
    project_id: 'proj-1',
    organization_id: 'org-1',
    slug: 'test-doc',
    content: 'content',
    created_by: 'user1',
    updated_by: 'user1',
  };

  it('debe renderizar metadatos del documento', () => {
    render(<DocumentMetadata document={mockDocument} />);
    
    expect(screen.getByText('Metadatos')).toBeInTheDocument();
    expect(screen.getByText('Test Document')).toBeInTheDocument();
    expect(screen.getByText('test.md')).toBeInTheDocument();
  });

  it('debe mostrar calificación cuando existe', () => {
    render(<DocumentMetadata document={mockDocument} />);
    
    expect(screen.getByText('8.5')).toBeInTheDocument();
  });

  it('debe mostrar "Sin calificar" cuando no hay rating', () => {
    const docWithoutRating = { ...mockDocument, rating: null };
    render(<DocumentMetadata document={docWithoutRating} />);
    
    expect(screen.getByText('Sin calificar')).toBeInTheDocument();
  });

  it('debe mostrar badge Healthy cuando rating >= 9', () => {
    const docWithHighRating = { ...mockDocument, rating: 9.5 };
    render(<DocumentMetadata document={docWithHighRating} />);
    
    expect(screen.getByText('Healthy')).toBeInTheDocument();
  });

  it('no debe mostrar badge Healthy cuando rating < 9', () => {
    render(<DocumentMetadata document={mockDocument} />);
    
    expect(screen.queryByText('Healthy')).not.toBeInTheDocument();
  });

  it('debe mostrar fechas formateadas', () => {
    render(<DocumentMetadata document={mockDocument} />);
    
    expect(screen.getByText(/Creado/)).toBeInTheDocument();
    expect(screen.getByText(/Actualizado/)).toBeInTheDocument();
  });
});
