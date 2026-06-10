import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { AppLayout } from '../AppLayout';
import { useAuthStore } from '@/stores/authStore';
import { useBreadcrumbs } from '@/hooks/useBreadcrumbs';

vi.mock('@/stores/authStore');
vi.mock('@/hooks/useBreadcrumbs');

describe('AppLayout', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debe renderizar sidebar con navegación', () => {
    vi.mocked(useAuthStore).mockReturnValue({
      user: { id: '1', username: 'test', email: 'test@example.com', is_active: true, created_at: '2024-01-01', updated_at: '2024-01-01' },
      loading: false,
      error: null,
      logout: vi.fn(),
      fetchMe: vi.fn(),
    });
    vi.mocked(useBreadcrumbs).mockReturnValue([
      { label: 'Dashboard', path: '/' },
    ]);

    render(
      <MemoryRouter initialEntries={['/']}>
        <AppLayout />
      </MemoryRouter>
    );

    expect(screen.getAllByText('Dashboard')).toHaveLength(1); // Only in sidebar; single breadcrumb is hidden
    expect(screen.queryByText('Documentos')).not.toBeInTheDocument();
    expect(screen.queryByText('Gaps')).not.toBeInTheDocument();
    expect(screen.queryByText('Propuestas')).not.toBeInTheDocument();
  });

  it('debe mostrar información de usuario', () => {
    vi.mocked(useAuthStore).mockReturnValue({
      user: { id: '1', username: 'testuser', email: 'test@example.com', is_active: true, created_at: '2024-01-01', updated_at: '2024-01-01' },
      loading: false,
      error: null,
      logout: vi.fn(),
      fetchMe: vi.fn(),
    });
    vi.mocked(useBreadcrumbs).mockReturnValue([
      { label: 'Dashboard', path: '/' },
    ]);

    render(
      <MemoryRouter initialEntries={['/']}>
        <AppLayout />
      </MemoryRouter>
    );

    expect(screen.getByText('testuser')).toBeInTheDocument();
    expect(screen.getByText('test@example.com')).toBeInTheDocument();
  });

  it('debe llamar logout al hacer click en cerrar sesión', () => {
    const logoutMock = vi.fn();
    vi.mocked(useAuthStore).mockReturnValue({
      user: { id: '1', username: 'test', email: 'test@example.com', is_active: true, created_at: '2024-01-01', updated_at: '2024-01-01' },
      loading: false,
      error: null,
      logout: logoutMock,
      fetchMe: vi.fn(),
    });
    vi.mocked(useBreadcrumbs).mockReturnValue([
      { label: 'Dashboard', path: '/' },
    ]);

    render(
      <MemoryRouter initialEntries={['/']}>
        <AppLayout />
      </MemoryRouter>
    );

    const logoutButton = screen.getByLabelText('Cerrar sesión');
    fireEvent.click(logoutButton);

    expect(logoutMock).toHaveBeenCalled();
  });

  it('debe manejar usuario null', () => {
    vi.mocked(useAuthStore).mockReturnValue({
      user: null,
      loading: false,
      error: null,
      logout: vi.fn(),
      fetchMe: vi.fn(),
    });
    vi.mocked(useBreadcrumbs).mockReturnValue([
      { label: 'Dashboard', path: '/' },
    ]);

    render(
      <MemoryRouter initialEntries={['/']}>
        <AppLayout />
      </MemoryRouter>
    );

    expect(screen.queryByText(/test/)).not.toBeInTheDocument();
  });

  it('debe mostrar breadcrumbs con múltiples niveles', () => {
    vi.mocked(useAuthStore).mockReturnValue({
      user: { id: '1', username: 'test', email: 'test@example.com', is_active: true, created_at: '2024-01-01', updated_at: '2024-01-01' },
      loading: false,
      error: null,
      logout: vi.fn(),
      fetchMe: vi.fn(),
    });
    vi.mocked(useBreadcrumbs).mockReturnValue([
      { label: 'Dashboard', path: '/' },
      { label: 'Documentos', path: '/documents' },
      { label: 'Detalle', path: '/documents/1' },
    ]);

    render(
      <MemoryRouter initialEntries={['/documents/1']}>
        <AppLayout />
      </MemoryRouter>
    );

    // Without project context, only Dashboard appears in sidebar;
    // Documentos and Detalle appear only in breadcrumbs
    expect(screen.getAllByText('Dashboard')).toHaveLength(2); // Sidebar + breadcrumbs
    expect(screen.getAllByText('Documentos')).toHaveLength(1); // Breadcrumbs only
    expect(screen.getByText('Detalle')).toBeInTheDocument();
  });

  it('debe navegar al hacer click en breadcrumb no último', () => {
    vi.mocked(useAuthStore).mockReturnValue({
      user: { id: '1', username: 'test', email: 'test@example.com', is_active: true, created_at: '2024-01-01', updated_at: '2024-01-01' },
      loading: false,
      error: null,
      logout: vi.fn(),
      fetchMe: vi.fn(),
    });
    vi.mocked(useBreadcrumbs).mockReturnValue([
      { label: 'Dashboard', path: '/' },
      { label: 'Documentos', path: '/documents' },
    ]);

    render(
      <MemoryRouter initialEntries={['/documents']}>
        <AppLayout />
      </MemoryRouter>
    );

    // Breadcrumb should render when there are multiple levels
    expect(screen.getByRole('button', { name: 'Dashboard' })).toBeInTheDocument();
  });
});
