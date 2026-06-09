import { useMemo } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import { useProjectContextStore } from '@/stores/projectContextStore';

interface Breadcrumb {
  label: string;
  path: string;
}

const routeLabels: Record<string, string> = {
  '/': 'Inicio',
  '/login': 'Iniciar sesión',
  'documents': 'Documentos',
  'gaps': 'Gaps',
  'proposals': 'Propuestas',
};

export function useBreadcrumbs(): Breadcrumb[] {
  const location = useLocation();
  const { orgSlug, projectSlug } = useParams<{ orgSlug?: string; projectSlug?: string }>();
  const { currentOrganization, currentProject } = useProjectContextStore();

  const breadcrumbs = useMemo(() => {
    const path = location.pathname;

    // Handle root path
    if (path === '/') {
      return [{ label: 'Inicio', path: '/' }];
    }

    // Handle login path
    if (path === '/login') {
      return [{ label: 'Iniciar sesión', path: '/login' }];
    }

    const segments = path.split('/').filter(Boolean);

    if (segments.length === 0) {
      return [{ label: 'Inicio', path: '/' }];
    }

    // Check if this is a project-scoped route
    const isProjectRoute = segments.length >= 2 && !routeLabels[segments[0]];
    // segments[0] is orgSlug, segments[1] is projectSlug (if exists)

    // Build breadcrumbs
    const result: Breadcrumb[] = [{ label: 'Inicio', path: '/' }];

    if (isProjectRoute && orgSlug) {
      // Organization breadcrumb - uses real name from store if available
      const orgName = currentOrganization?.slug === orgSlug
        ? currentOrganization.name
        : orgSlug;
      result.push({
        label: orgName,
        path: `/${orgSlug}`,
      });

      // If we have a project slug, add project breadcrumb
      if (projectSlug && segments.length >= 2) {
        const projName = currentProject?.slug === projectSlug &&
                         currentProject?.organization_id === currentOrganization?.id
          ? currentProject.name
          : projectSlug;
        result.push({
          label: projName,
          path: `/${orgSlug}/${projectSlug}`,
        });

        // Add remaining segments (documents, gaps, etc.)
        for (let i = 2; i < segments.length; i++) {
          const segment = segments[i];
          const segmentPath = `/${orgSlug}/${projectSlug}` + segments.slice(2, i + 1).join('/');
          const label = routeLabels[segment] ||
                       segment.charAt(0).toUpperCase() + segment.slice(1);
          result.push({ label, path: segmentPath });
        }
      }
    } else {
      // Non-project routes - build from segments
      let currentPath = '';
      segments.forEach((segment) => {
        currentPath += `/${segment}`;
        const label = routeLabels[currentPath] ||
                     routeLabels[segment] ||
                     segment.charAt(0).toUpperCase() + segment.slice(1);
        result.push({ label, path: currentPath });
      });
    }

    return result;
  }, [location.pathname, orgSlug, projectSlug, currentOrganization, currentProject]);

  return breadcrumbs;
}
