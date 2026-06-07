import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Textarea } from '../textarea';

describe('Textarea', () => {
  it('debe renderizar textarea con clases por defecto', () => {
    render(<Textarea />);
    const textarea = screen.getByRole('textbox');
    expect(textarea).toBeInTheDocument();
    expect(textarea).toHaveClass('flex', 'min-h-[80px]', 'w-full');
  });

  it('debe aceptar className personalizado', () => {
    render(<Textarea className="custom-class" />);
    const textarea = screen.getByRole('textbox');
    expect(textarea).toHaveClass('custom-class');
  });

  it('debe pasar props adicionales al textarea', () => {
    render(<Textarea placeholder="Escribe aquí" rows={5} />);
    const textarea = screen.getByRole('textbox');
    expect(textarea).toHaveAttribute('placeholder', 'Escribe aquí');
    expect(textarea).toHaveAttribute('rows', '5');
  });

  it('debe tener displayName correcto', () => {
    expect(Textarea.displayName).toBe('Textarea');
  });
});
