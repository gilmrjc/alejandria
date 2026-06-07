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

    expect(screen.getAllByText('Dashboard')).toHaveLength(2); // One in sidebar, one in breadcrumbs
    expect(screen.getAllByText('Documentos')).toHaveLength(1); // Only in sidebar
    expect(screen.getAllByText('Gaps')).toHaveLength(1); // Only in sidebar
    expect(screen.getAllByText('Propuestas')).toHaveLength(1); // Only in sidebar
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

    const logoutButton = screen.getByText('Cerrar sesión');
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

    expect(screen.getAllByText('Dashboard')).toHaveLength(2); // Sidebar + breadcrumbs
    expect(screen.getAllByText('Documentos')).toHaveLength(2); // Sidebar + breadcrumbs
    expect(screen.getByText('Detalle')).toBeInTheDocument();
  });
});
