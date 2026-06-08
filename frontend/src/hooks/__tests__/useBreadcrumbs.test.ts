import React from 'react';
import { describe, it, expect } from 'vitest';
import { renderHook } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { useBreadcrumbs } from '../useBreadcrumbs';

describe('useBreadcrumbs', () => {
  it('debe retornar Dashboard para ruta raíz', () => {
    const { result } = renderHook(() => useBreadcrumbs(), {
      wrapper: ({ children }) => React.createElement(MemoryRouter, { initialEntries: ['/'] }, children),
    });
    
    expect(result.current).toEqual([{ label: 'Dashboard', path: '/' }]);
  });

  it('debe retornar Iniciar sesión para ruta login', () => {
    const { result } = renderHook(() => useBreadcrumbs(), {
      wrapper: ({ children }) => React.createElement(MemoryRouter, { initialEntries: ['/login'] }, children),
    });
    
    expect(result.current).toEqual([{ label: 'Iniciar sesión', path: '/login' }]);
  });

  it('debe construir breadcrumbs para /documents', () => {
    const { result } = renderHook(() => useBreadcrumbs(), {
      wrapper: ({ children }) => React.createElement(MemoryRouter, { initialEntries: ['/documents'] }, children),
    });
    
    expect(result.current).toEqual([
      { label: 'Dashboard', path: '/' },
      { label: 'Documentos', path: '/documents' },
    ]);
  });

  it('debe construir breadcrumbs para /gaps', () => {
    const { result } = renderHook(() => useBreadcrumbs(), {
      wrapper: ({ children }) => React.createElement(MemoryRouter, { initialEntries: ['/gaps'] }, children),
    });
    
    expect(result.current).toEqual([
      { label: 'Dashboard', path: '/' },
      { label: 'Gaps', path: '/gaps' },
    ]);
  });

  it('debe construir breadcrumbs para /proposals', () => {
    const { result } = renderHook(() => useBreadcrumbs(), {
      wrapper: ({ children }) => React.createElement(MemoryRouter, { initialEntries: ['/proposals'] }, children),
    });
    
    expect(result.current).toEqual([
      { label: 'Dashboard', path: '/' },
      { label: 'Propuestas', path: '/proposals' },
    ]);
  });

  it('debe capitalizar segmentos no mapeados', () => {
    const { result } = renderHook(() => useBreadcrumbs(), {
      wrapper: ({ children }) => React.createElement(MemoryRouter, { initialEntries: ['/custom'] }, children),
    });
    
    expect(result.current).toEqual([
      { label: 'Dashboard', path: '/' },
      { label: 'Custom', path: '/custom' },
    ]);
  });

  it('debe manejar rutas anidadas', () => {
    const { result } = renderHook(() => useBreadcrumbs(), {
      wrapper: ({ children }) => React.createElement(MemoryRouter, { initialEntries: ['/documents/123'] }, children),
    });
    
    expect(result.current).toEqual([
      { label: 'Dashboard', path: '/' },
      { label: 'Documentos', path: '/documents' },
      { label: '123', path: '/documents/123' },
    ]);
  });

  it('debe manejar rutas con múltiples segmentos anidados', () => {
    const { result } = renderHook(() => useBreadcrumbs(), {
      wrapper: ({ children }) => React.createElement(MemoryRouter, { initialEntries: ['/documents/123/edit'] }, children),
    });
    
    expect(result.current).toEqual([
      { label: 'Dashboard', path: '/' },
      { label: 'Documentos', path: '/documents' },
      { label: '123', path: '/documents/123' },
      { label: 'Edit', path: '/documents/123/edit' },
    ]);
  });

  it('debe manejar segmentos vacíos en la ruta', () => {
    const { result } = renderHook(() => useBreadcrumbs(), {
      wrapper: ({ children }) => React.createElement(MemoryRouter, { initialEntries: ['//'] }, children),
    });
    
    expect(result.current).toEqual([{ label: 'Dashboard', path: '/' }]);
  });
});
