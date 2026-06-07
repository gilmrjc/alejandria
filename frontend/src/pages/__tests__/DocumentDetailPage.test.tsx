import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import { DocumentDetailPage } from '../DocumentDetailPage';

vi.mock('react-router-dom', () => ({
  useParams: () => ({ id: '123' }),
  useNavigate: () => vi.fn(),
}));

describe('DocumentDetailPage', () => {
  it('debe renderizar página de detalle de documento', () => {
    render(<DocumentDetailPage />);
    
    expect(document.body).toBeTruthy();
  });
});
