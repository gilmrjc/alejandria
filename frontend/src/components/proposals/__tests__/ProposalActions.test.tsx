import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ProposalActions } from '../ProposalActions';

describe('ProposalActions', () => {
  it('debe mostrar botones Aprobar y Rechazar cuando status es pending', () => {
    const onApprove = vi.fn();
    const onReject = vi.fn();
    const onApply = vi.fn();
    
    render(
      <ProposalActions 
        status="pending" 
        onApprove={onApprove} 
        onReject={onReject} 
        onApply={onApply} 
      />
    );
    
    expect(screen.getByText('Aprobar')).toBeInTheDocument();
    expect(screen.getByText('Rechazar')).toBeInTheDocument();
  });

  it('debe llamar onApprove al hacer click en Aprobar', async () => {
    const user = userEvent.setup();
    const onApprove = vi.fn();
    const onReject = vi.fn();
    const onApply = vi.fn();
    
    render(
      <ProposalActions 
        status="pending" 
        onApprove={onApprove} 
        onReject={onReject} 
        onApply={onApply} 
      />
    );
    
    const approveButton = screen.getByText('Aprobar');
    await user.click(approveButton);
    
    expect(onApprove).toHaveBeenCalled();
  });

  it('debe llamar onReject al hacer click en Rechazar', async () => {
    const user = userEvent.setup();
    const onApprove = vi.fn();
    const onReject = vi.fn();
    const onApply = vi.fn();
    
    render(
      <ProposalActions 
        status="pending" 
        onApprove={onApprove} 
        onReject={onReject} 
        onApply={onApply} 
      />
    );
    
    const rejectButton = screen.getByText('Rechazar');
    await user.click(rejectButton);
    
    expect(onReject).toHaveBeenCalled();
  });

  it('debe mostrar botón Aplicar cuando status es accepted', () => {
    const onApprove = vi.fn();
    const onReject = vi.fn();
    const onApply = vi.fn();
    
    render(
      <ProposalActions 
        status="accepted" 
        onApprove={onApprove} 
        onReject={onReject} 
        onApply={onApply} 
      />
    );
    
    expect(screen.getByText('Aplicar')).toBeInTheDocument();
    expect(screen.queryByText('Aprobar')).not.toBeInTheDocument();
    expect(screen.queryByText('Rechazar')).not.toBeInTheDocument();
  });

  it('debe llamar onApply al hacer click en Aplicar', async () => {
    const user = userEvent.setup();
    const onApprove = vi.fn();
    const onReject = vi.fn();
    const onApply = vi.fn();
    
    render(
      <ProposalActions 
        status="accepted" 
        onApprove={onApprove} 
        onReject={onReject} 
        onApply={onApply} 
      />
    );
    
    const applyButton = screen.getByText('Aplicar');
    await user.click(applyButton);
    
    expect(onApply).toHaveBeenCalled();
  });

  it('debe no renderizar nada cuando status es rejected', () => {
    const onApprove = vi.fn();
    const onReject = vi.fn();
    const onApply = vi.fn();
    
    const { container } = render(
      <ProposalActions 
        status='rejected'
        onApprove={onApprove} 
        onReject={onReject} 
        onApply={onApply} 
      />
    );
    
    expect(container.firstChild).toBeNull();
  });

  it('debe no renderizar nada cuando status es implemented', () => {
    const onApprove = vi.fn();
    const onReject = vi.fn();
    const onApply = vi.fn();
    
    const { container } = render(
      <ProposalActions 
        status='implemented'
        onApprove={onApprove} 
        onReject={onReject} 
        onApply={onApply} 
      />
    );
    
    expect(container.firstChild).toBeNull();
  });

  it('debe deshabilitar botones cuando loading es true', () => {
    const onApprove = vi.fn();
    const onReject = vi.fn();
    const onApply = vi.fn();
    
    render(
      <ProposalActions 
        status="pending" 
        onApprove={onApprove} 
        onReject={onReject} 
        onApply={onApply} 
        loading 
      />
    );
    
    const approveButton = screen.getByText('Aprobar');
    const rejectButton = screen.getByText('Rechazar');
    expect(approveButton).toBeDisabled();
    expect(rejectButton).toBeDisabled();
  });
});
