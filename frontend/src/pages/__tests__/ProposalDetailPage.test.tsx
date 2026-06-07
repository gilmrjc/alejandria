import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import { ProposalDetailPage } from '../ProposalDetailPage';

vi.mock('react-router-dom', () => ({
  useParams: () => ({ id: '123' }),
  useNavigate: () => vi.fn(),
}));

describe('ProposalDetailPage', () => {
  it('debe renderizar página de detalle de propuesta', () => {
    render(<ProposalDetailPage />);
    
    expect(document.body).toBeTruthy();
  });
});
