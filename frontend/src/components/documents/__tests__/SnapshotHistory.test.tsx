import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { SnapshotHistory } from '../SnapshotHistory';

describe('SnapshotHistory', () => {
  const mockSnapshots = [
    {
      id: '1',
      created_at: '2024-01-01T00:00:00Z',
      created_by: 'user1',
      document_id: 'doc-1',
      content: 'content',
    },
    {
      id: '2',
      created_at: '2024-01-02T00:00:00Z',
      created_by: 'user2',
      document_id: 'doc-1',
      content: 'content',
    },
  ];

  it('debe mostrar estado de carga', () => {
    render(<SnapshotHistory snapshots={[]} loading onRestore={vi.fn()} />);
    
    expect(screen.getByText('Cargando historial...')).toBeInTheDocument();
  });

  it('debe mostrar mensaje cuando no hay snapshots', () => {
    render(<SnapshotHistory snapshots={[]} loading={false} onRestore={vi.fn()} />);
    
    expect(screen.getByText('No hay snapshots disponibles')).toBeInTheDocument();
  });

  it('debe renderizar lista de snapshots', () => {
    const onRestore = vi.fn();
    render(<SnapshotHistory snapshots={mockSnapshots} loading={false} onRestore={onRestore} />);
    
    expect(screen.getByText('Historial de Snapshots')).toBeInTheDocument();
    expect(screen.getByText(/user1/)).toBeInTheDocument();
    expect(screen.getByText(/user2/)).toBeInTheDocument();
  });

  it('debe llamar onRestore al hacer click en restaurar', () => {
    const onRestore = vi.fn();
    render(<SnapshotHistory snapshots={mockSnapshots} loading={false} onRestore={onRestore} />);
    
    const restoreButtons = screen.getAllByRole('button');
    restoreButtons[0].click();
    
    expect(onRestore).toHaveBeenCalledWith('1');
  });

  it('debe mostrar fechas formateadas', () => {
    render(<SnapshotHistory snapshots={mockSnapshots} loading={false} onRestore={vi.fn()} />);
    
    expect(screen.getByText(/2024/)).toBeInTheDocument();
  });
});
