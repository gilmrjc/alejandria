import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { GapFilters } from '../GapFilters';

describe('GapFilters', () => {
  it('debe renderizar input de búsqueda con placeholder correcto', () => {
    render(<GapFilters search="" onSearchChange={vi.fn()} onClear={vi.fn()} />);
    expect(screen.getByPlaceholderText('Buscar gaps...')).toBeInTheDocument();
  });

  it('debe mostrar valor de búsqueda correctamente', () => {
    render(<GapFilters search="test" onSearchChange={vi.fn()} onClear={vi.fn()} />);
    const input = screen.getByPlaceholderText('Buscar gaps...') as HTMLInputElement;
    expect(input.value).toBe('test');
  });

  it('debe llamar onSearchChange cuando input cambia', () => {
    const onSearchChange = vi.fn();
    render(<GapFilters search="" onSearchChange={onSearchChange} onClear={vi.fn()} />);
    
    const input = screen.getByPlaceholderText('Buscar gaps...');
    fireEvent.change(input, { target: { value: 'test' } });
    
    expect(onSearchChange).toHaveBeenCalledWith('test');
  });

  it('debe mostrar botón de limpiar cuando hay búsqueda', () => {
    render(<GapFilters search="test" onSearchChange={vi.fn()} onClear={vi.fn()} />);
    const clearButton = screen.getByRole('button');
    expect(clearButton).toBeInTheDocument();
  });

  it('debe llamar onClear cuando se hace click en botón limpiar', () => {
    const onClear = vi.fn();
    render(<GapFilters search="test" onSearchChange={vi.fn()} onClear={onClear} />);
    
    const clearButton = screen.getByRole('button');
    fireEvent.click(clearButton);
    
    expect(onClear).toHaveBeenCalled();
  });

  it('no debe mostrar botón de limpiar cuando búsqueda está vacía', () => {
    render(<GapFilters search="" onSearchChange={vi.fn()} onClear={vi.fn()} />);
    const clearButton = screen.queryByRole('button');
    expect(clearButton).not.toBeInTheDocument();
  });
});
