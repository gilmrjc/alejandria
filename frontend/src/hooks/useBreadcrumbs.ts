import { useMemo } from 'react';
import { useLocation } from 'react-router-dom';

interface Breadcrumb {
  label: string;
  path: string;
}

const routeLabels: Record<string, string> = {
  '/': 'Dashboard',
  '/login': 'Iniciar sesión',
  '/documents': 'Documentos',
  '/gaps': 'Gaps',
  '/proposals': 'Propuestas',
};

export function useBreadcrumbs(): Breadcrumb[] {
  const location = useLocation();

  const breadcrumbs = useMemo(() => {
    const path = location.pathname;
    
    // Handle root path
    if (path === '/') {
      return [{ label: 'Dashboard', path: '/' }];
    }

    // Handle login path
    if (path === '/login') {
      return [{ label: 'Iniciar sesión', path: '/login' }];
    }

    // Handle dynamic routes (future expansion)
    // Example: /documents/:id -> [{ label: 'Dashboard', path: '/' }, { label: 'Documento', path: '/documents/:id' }]
    const segments = path.split('/').filter(Boolean);
    
    if (segments.length === 0) {
      return [{ label: 'Dashboard', path: '/' }];
    }

    // Build breadcrumbs from segments
    const result: Breadcrumb[] = [{ label: 'Dashboard', path: '/' }];
    
    let currentPath = '';
    segments.forEach((segment) => {
      currentPath += `/${segment}`;
      
      // Try to get label from routeLabels, otherwise capitalize segment
      const label = routeLabels[currentPath] || 
                   segment.charAt(0).toUpperCase() + segment.slice(1);
      
      result.push({ label, path: currentPath });
    });

    return result;
  }, [location.pathname]);

  return breadcrumbs;
}
