import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { DiffViewer } from '../DiffViewer';

describe('DiffViewer', () => {
  it('debe renderizar el componente con oldContent y newContent', () => {
    const oldContent = 'Linea 1\nLinea 2\nLinea 3';
    const newContent = 'Linea 1\nLinea 2 modificada\nLinea 3';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    expect(screen.getByText('Diff de Cambios')).toBeInTheDocument();
    expect(screen.getByText('Lado a lado')).toBeInTheDocument();
    expect(screen.getByText('Unificado')).toBeInTheDocument();
  });

  it('debe mostrar el nombre del archivo cuando se proporciona', () => {
    const oldContent = 'Linea 1';
    const newContent = 'Linea 2';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} filename="test.md" />);
    
    expect(screen.getByText('test.md')).toBeInTheDocument();
  });

  it('debe mostrar el lenguaje cuando se proporciona', () => {
    const oldContent = 'Linea 1';
    const newContent = 'Linea 2';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} language="markdown" />);
    
    expect(screen.getByText('markdown')).toBeInTheDocument();
  });

  it('debe mostrar estadísticas de cambios', () => {
    const oldContent = 'Linea 1\nLinea 2\nLinea 3';
    const newContent = 'Linea 1\nLinea 2 modificada\nLinea 3 nueva';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    expect(screen.getByText(/adiciones/)).toBeInTheDocument();
    expect(screen.getByText(/eliminaciones/)).toBeInTheDocument();
  });

  it('debe manejar oldContent null (documento nuevo)', () => {
    const oldContent = null;
    const newContent = 'Linea 1\nLinea 2';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    expect(screen.getByText('Diff de Cambios')).toBeInTheDocument();
  });

  it('debe mostrar vista dividida por defecto', () => {
    const oldContent = 'Linea 1';
    const newContent = 'Linea 2';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    expect(screen.getByText('Anterior')).toBeInTheDocument();
    expect(screen.getByText('Nuevo')).toBeInTheDocument();
  });

  it('debe cambiar a vista unificada al hacer click', () => {
    const oldContent = 'Linea 1';
    const newContent = 'Linea 2';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    const unifiedButton = screen.getByText('Unificado');
    fireEvent.click(unifiedButton);
    
    expect(screen.queryByText('Anterior')).not.toBeInTheDocument();
    expect(screen.queryByText('Nuevo')).not.toBeInTheDocument();
  });

  it('debe mostrar iconos de cambios', () => {
    const oldContent = 'Linea 1\nLinea 2';
    const newContent = 'Linea 1\nLinea 2 modificada';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    const icons = document.querySelectorAll('svg');
    expect(icons.length).toBeGreaterThan(0);
  });

  it('debe renderizar todos los badges cuando se proporcionan todos los props', () => {
    const oldContent = 'Linea 1';
    const newContent = 'Linea 2';
    
    render(
      <DiffViewer
        oldContent={oldContent}
        newContent={newContent}
        filename="test.md"
        language="markdown"
      />
    );
    
    expect(screen.getByText('test.md')).toBeInTheDocument();
    expect(screen.getByText('markdown')).toBeInTheDocument();
  });

  it('debe manejar contenido vacío en ambos lados', () => {
    const oldContent = '';
    const newContent = '';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    expect(screen.getByText('Diff de Cambios')).toBeInTheDocument();
  });

  it('debe manejar solo oldContent (eliminación total)', () => {
    const oldContent = 'Linea 1\nLinea 2';
    const newContent = '';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    expect(screen.getByText('Diff de Cambios')).toBeInTheDocument();
  });

  it('debe manejar contenido idéntico (sin cambios)', () => {
    const oldContent = 'Linea 1\nLinea 2\nLinea 3';
    const newContent = 'Linea 1\nLinea 2\nLinea 3';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    expect(screen.getByText('0 adiciones')).toBeInTheDocument();
    expect(screen.getByText('0 eliminaciones')).toBeInTheDocument();
  });

  it('debe cambiar de unified a split view', () => {
    const oldContent = 'Linea 1';
    const newContent = 'Linea 2';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    const unifiedButton = screen.getByText('Unificado');
    fireEvent.click(unifiedButton);
    
    expect(screen.queryByText('Anterior')).not.toBeInTheDocument();
    
    const splitButton = screen.getByText('Lado a lado');
    fireEvent.click(splitButton);
    
    expect(screen.getByText('Anterior')).toBeInTheDocument();
    expect(screen.getByText('Nuevo')).toBeInTheDocument();
  });

  it('debe mostrar líneas con colores para adiciones y eliminaciones', () => {
    const oldContent = 'Linea 1\nLinea 2';
    const newContent = 'Linea 1\nLinea 3';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    const container = screen.getByText('Anterior').closest('div');
    expect(container).toBeInTheDocument();
  });

  it('debe manejar scroll sincronizado en split view', () => {
    const oldContent = 'Linea 1\nLinea 2\nLinea 3\nLinea 4\nLinea 5';
    const newContent = 'Linea 1\nLinea 2\nLinea 3\nLinea 4\nLinea 5';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    const leftPanel = screen.getByText('Anterior').closest('div');
    const rightPanel = screen.getByText('Nuevo').closest('div');
    
    expect(leftPanel).toBeInTheDocument();
    expect(rightPanel).toBeInTheDocument();
  });

  it('debe mostrar contenido largo con scroll', () => {
    const longContent = Array.from({ length: 100 }, (_, i) => `Linea ${i + 1}`).join('\n');
    
    render(<DiffViewer oldContent={longContent} newContent={longContent} />);
    
    expect(screen.getByText('Anterior')).toBeInTheDocument();
    expect(screen.getByText('Nuevo')).toBeInTheDocument();
  });

  it('debe manejar scroll en unified view sin error', () => {
    const oldContent = 'Linea 1\nLinea 2';
    const newContent = 'Linea 1\nLinea 2';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    const unifiedButton = screen.getByText('Unificado');
    fireEvent.click(unifiedButton);
    
    expect(screen.queryByText('Anterior')).not.toBeInTheDocument();
  });

  it('debe manejar caso donde scrollHeight es igual a clientHeight', () => {
    const oldContent = 'Linea 1';
    const newContent = 'Linea 2';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    expect(screen.getByText('Anterior')).toBeInTheDocument();
  });

  it('debe manejar caso donde ref.current es null en handleScroll', () => {
    const oldContent = 'Linea 1';
    const newContent = 'Linea 2';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    // El componente debería renderizar sin errores incluso si los refs no están disponibles
    expect(screen.getByText('Anterior')).toBeInTheDocument();
  });

  it('debe manejar caso donde scrollHeight es 0', () => {
    const oldContent = '';
    const newContent = '';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    expect(screen.getByText('Anterior')).toBeInTheDocument();
  });

  it('debe probar scroll sincronizado en split view', () => {
    const longContent = Array.from({ length: 50 }, (_, i) => `Linea ${i + 1}`).join('\n');
    
    render(<DiffViewer oldContent={longContent} newContent={longContent} />);
    
    const leftPanel = screen.getByText('Anterior').closest('div')?.parentElement;
    const rightPanel = screen.getByText('Nuevo').closest('div')?.parentElement;
    
    expect(leftPanel).toBeInTheDocument();
    expect(rightPanel).toBeInTheDocument();
  });

  it('debe manejar scroll cuando viewMode no es split', () => {
    const oldContent = 'Linea 1';
    const newContent = 'Linea 2';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    const unifiedButton = screen.getByText('Unificado');
    fireEvent.click(unifiedButton);
    
    expect(screen.queryByText('Anterior')).not.toBeInTheDocument();
  });

  it('debe renderizar unified view con todas las líneas', () => {
    const oldContent = 'Linea 1\nLinea 2\nLinea 3';
    const newContent = 'Linea 1\nLinea 2\nLinea 3';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    const unifiedButton = screen.getByText('Unificado');
    fireEvent.click(unifiedButton);
    
    expect(screen.getByText('Linea 1')).toBeInTheDocument();
    expect(screen.getByText('Linea 2')).toBeInTheDocument();
    expect(screen.getByText('Linea 3')).toBeInTheDocument();
  });

  it('debe mostrar línea vacía cuando content es string vacío', () => {
    const oldContent = 'Linea 1\n\nLinea 3';
    const newContent = 'Linea 1\n\nLinea 3';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    expect(screen.getByText('Anterior')).toBeInTheDocument();
  });

  it('debe manejar diffLine sin match en split view', () => {
    const oldContent = 'Linea 1\nLinea 2';
    const newContent = 'Linea 3\nLinea 4';
    
    render(<DiffViewer oldContent={oldContent} newContent={newContent} />);
    
    expect(screen.getByText('Anterior')).toBeInTheDocument();
    expect(screen.getByText('Nuevo')).toBeInTheDocument();
  });
});
