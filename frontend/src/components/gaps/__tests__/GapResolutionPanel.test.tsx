import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { GapResolutionPanel } from '../GapResolutionPanel';

describe('GapResolutionPanel', () => {
  const mockGap = {
    id: '1',
    slug: 'test-gap',
    question: '¿Cuál es el propósito del sistema?',
    context_missing: 'Falta información sobre arquitectura',
    priority: 'high' as const,
    status: 'pending' as const,
    role_affected: 'developer',
    document_id: 'doc-1',
    created_at: '2024-01-01',
    updated_at: '2024-01-01',
    answer: null,
    answered_at: null,
  };

  it('debe renderizar pregunta del gap', () => {
    render(<GapResolutionPanel gap={mockGap} onSubmit={vi.fn()} />);
    
    expect(screen.getByText('¿Cuál es el propósito del sistema?')).toBeInTheDocument();
  });

  it('debe mostrar contexto faltante cuando existe', () => {
    render(<GapResolutionPanel gap={mockGap} onSubmit={vi.fn()} />);
    
    expect(screen.getByText('Contexto faltante:')).toBeInTheDocument();
    expect(screen.getByText('Falta información sobre arquitectura')).toBeInTheDocument();
  });

  it('debe mostrar rol afectado cuando existe', () => {
    render(<GapResolutionPanel gap={mockGap} onSubmit={vi.fn()} />);
    
    expect(screen.getByText(/Rol afectado: developer/)).toBeInTheDocument();
  });

  it('debe mostrar botones de acción cuando status es pending', () => {
    render(<GapResolutionPanel gap={mockGap} onSubmit={vi.fn()} />);
    
    expect(screen.getByText('Responder')).toBeInTheDocument();
    expect(screen.getByText('Rechazar')).toBeInTheDocument();
  });

  it('debe llamar onSubmit con respuesta al hacer click en Responder', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<GapResolutionPanel gap={mockGap} onSubmit={onSubmit} />);
    
    const textarea = screen.getByPlaceholderText('Ingresa tu respuesta...');
    await user.type(textarea, 'Esta es la respuesta');
    
    const respondButton = screen.getByText('Responder');
    await user.click(respondButton);
    
    expect(onSubmit).toHaveBeenCalledWith('Esta es la respuesta');
  });

  it('debe deshabilitar botón Responder cuando respuesta está vacía', () => {
    render(<GapResolutionPanel gap={mockGap} onSubmit={vi.fn()} />);
    
    const respondButton = screen.getByText('Responder');
    expect(respondButton).toBeDisabled();
  });

  it('debe llamar onSubmit con string vacío al rechazar', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<GapResolutionPanel gap={mockGap} onSubmit={onSubmit} />);
    
    const rejectButton = screen.getByText('Rechazar');
    await user.click(rejectButton);
    
    expect(onSubmit).toHaveBeenCalledWith('');
  });

  it('debe mostrar estado respondido cuando status es responded', () => {
    const respondedGap = { ...mockGap, status: 'responded' as const };
    render(<GapResolutionPanel gap={respondedGap} onSubmit={vi.fn()} />);
    
    expect(screen.getByText('Gap respondido')).toBeInTheDocument();
    expect(screen.queryByText('Responder')).not.toBeInTheDocument();
  });

  it('debe mostrar estado rechazado cuando status es rejected', () => {
    const rejectedGap = { ...mockGap, status: 'rejected' as const };
    render(<GapResolutionPanel gap={rejectedGap} onSubmit={vi.fn()} />);
    
    expect(screen.getByText('Gap rechazado')).toBeInTheDocument();
    expect(screen.queryByText('Responder')).not.toBeInTheDocument();
  });

  it('debe deshabilitar textarea cuando status no es pending', () => {
    const respondedGap = { ...mockGap, status: 'responded' as const };
    render(<GapResolutionPanel gap={respondedGap} onSubmit={vi.fn()} />);
    
    const textarea = screen.getByPlaceholderText('Ingresa tu respuesta...');
    expect(textarea).toBeDisabled();
  });

  it('debe deshabilitar botones cuando loading es true', () => {
    render(<GapResolutionPanel gap={mockGap} onSubmit={vi.fn()} loading />);
    
    const respondButton = screen.getByText('Responder');
    const rejectButton = screen.getByText('Rechazar');
    expect(respondButton).toBeDisabled();
    expect(rejectButton).toBeDisabled();
  });

  it('debe inicializar textarea con answer existente', () => {
    const gapWithAnswer = { ...mockGap, answer: 'Respuesta existente' };
    render(<GapResolutionPanel gap={gapWithAnswer} onSubmit={vi.fn()} />);
    
    const textarea = screen.getByPlaceholderText('Ingresa tu respuesta...');
    expect(textarea).toHaveValue('Respuesta existente');
  });
});
