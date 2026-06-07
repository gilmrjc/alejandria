import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { DashboardPage } from '../DashboardPage';

describe('DashboardPage', () => {
  it('debe renderizar título Dashboard', () => {
    render(<DashboardPage />);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
  });

  it('debe renderizar subtítulo', () => {
    render(<DashboardPage />);
    expect(screen.getByText('Estado general del sistema')).toBeInTheDocument();
  });

  it('debe renderizar tarjetas de estadísticas', () => {
    render(<DashboardPage />);
    expect(screen.getByText('Total documentos')).toBeInTheDocument();
    expect(screen.getByText('Calificación promedio')).toBeInTheDocument();
    expect(screen.getByText('Gaps pendientes')).toBeInTheDocument();
  });

  it('debe renderizar estado de infraestructura', () => {
    render(<DashboardPage />);
    expect(screen.getByText('Estado de infraestructura')).toBeInTheDocument();
  });

  it('debe mostrar items de infraestructura', () => {
    render(<DashboardPage />);
    expect(screen.getByText('Vite + React + TypeScript')).toBeInTheDocument();
    expect(screen.getByText('TailwindCSS + shadcn/ui')).toBeInTheDocument();
    expect(screen.getByText('React Router')).toBeInTheDocument();
    expect(screen.getByText('Axios + JWT interceptors')).toBeInTheDocument();
    expect(screen.getByText('Zustand stores')).toBeInTheDocument();
  });
});
