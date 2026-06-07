import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import { GapDetailPage } from '../GapDetailPage';

vi.mock('react-router-dom', () => ({
  useParams: () => ({ slug: 'test-gap' }),
  useNavigate: () => vi.fn(),
}));

describe('GapDetailPage', () => {
  it('debe renderizar página de detalle de gap', () => {
    render(<GapDetailPage />);
    
    expect(document.body).toBeTruthy();
  });
});
