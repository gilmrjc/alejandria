import { useEffect, useState, useRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ChevronDown, FolderGit2, Building2 } from 'lucide-react';
import { cn } from '@/utils';
import { Button } from '@/components/ui/button';
import { useOrganizationsStore } from '@/stores/organizationsStore';
import { useProjectsStore } from '@/stores/projectsStore';
import { useProjectContextStore } from '@/stores/projectContextStore';
import type { Organization, Project } from '@/types/organization';

export function ProjectSelector() {
  const navigate = useNavigate();
  const { orgSlug, projectSlug } = useParams<{ orgSlug?: string; projectSlug?: string }>();

  const { organizations, fetchOrganizations } = useOrganizationsStore();
  const { projects, fetchProjects } = useProjectsStore();
  const { currentOrganization, currentProject, setProjectContext } = useProjectContextStore();

  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Fetch organizations on mount
  useEffect(() => {
    fetchOrganizations();
  }, [fetchOrganizations]);

  // Fetch projects when organization changes
  useEffect(() => {
    if (currentOrganization) {
      fetchProjects();
    }
  }, [currentOrganization, fetchProjects]);

  // Sync URL params with store context
  useEffect(() => {
    if (orgSlug && projectSlug) {
      // Find organization by slug
      const org = organizations.find((o) => o.slug === orgSlug);
      // Find project by slug within the organization
      const project = projects.find(
        (p) => p.slug === projectSlug && p.organization_id === org?.id
      );

      if (org && project) {
        setProjectContext(org, project);
      }
    }
  }, [orgSlug, projectSlug, organizations, projects, setProjectContext]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelectProject = (org: Organization, project: Project) => {
    setProjectContext(org, project);
    setIsOpen(false);
    // Navigate to the project's dashboard (not documents)
    navigate(`/${org.slug}/${project.slug}`);
  };

  const handleSelectOrganization = (org: Organization) => {
    // Filter projects for this organization
    const orgProjectsList = projects.filter((p) => p.organization_id === org.id);

    if (orgProjectsList.length > 0) {
      // Select the first project of this organization
      handleSelectProject(org, orgProjectsList[0]);
    } else {
      setProjectContext(org, null);
      setIsOpen(false);
    }
  };

  // If we have URL params, show the current project
  const displayOrg = currentOrganization;
  const displayProject = currentProject;

  // Show placeholder if no context
  if (!displayOrg || !displayProject) {
    return (
      <div className="relative" ref={dropdownRef}>
        <Button
          variant="ghost"
          size="sm"
          className="h-8 gap-2 px-2 text-muted-foreground"
          onClick={() => setIsOpen(!isOpen)}
        >
          <FolderGit2 className="h-4 w-4" />
          <span className="max-w-[150px] truncate">Seleccionar proyecto</span>
          <ChevronDown className={cn('h-3 w-3 transition-transform', isOpen && 'rotate-180')} />
        </Button>

        {isOpen && (
          <div className="absolute top-full left-0 mt-1 w-72 bg-popover border rounded-md shadow-md z-50 py-2">
            <div className="px-3 py-2 text-xs font-semibold text-muted-foreground uppercase">
              Organizaciones
            </div>
            {organizations.length === 0 ? (
              <div className="px-3 py-2 text-sm text-muted-foreground">
                No hay organizaciones
              </div>
            ) : (
              organizations.map((org) => (
                <button
                  key={org.id}
                  onClick={() => handleSelectOrganization(org)}
                  className="w-full px-3 py-2 text-sm hover:bg-accent flex items-center gap-2 text-left"
                >
                  <Building2 className="h-4 w-4" />
                  <span>{org.name}</span>
                </button>
              ))
            )}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <Button
        variant="ghost"
        size="sm"
        className={cn('h-8 gap-2 px-2', isOpen && 'bg-accent')}
        onClick={() => setIsOpen(!isOpen)}
      >
        <FolderGit2 className="h-4 w-4 text-primary" />
        <span className="max-w-[150px] truncate">
          {displayOrg.slug}/{displayProject.slug}
        </span>
        <ChevronDown className={cn('h-3 w-3 transition-transform', isOpen && 'rotate-180')} />
      </Button>

      {isOpen && (
        <div className="absolute top-full left-0 mt-1 w-80 bg-popover border rounded-md shadow-md z-50 py-2 max-h-[400px] overflow-y-auto">
          {/* Current selection indicator */}
          <div className="px-3 py-2 bg-muted/50 mb-2">
            <p className="text-xs text-muted-foreground">Proyecto actual</p>
            <p className="font-medium text-sm">
              {displayOrg.name} / {displayProject.name}
            </p>
          </div>

          {/* Organizations and their projects */}
          {organizations.map((org) => {
            const orgProjectsList = projects.filter(
              (p) => p.organization_id === org.id
            );

            return (
              <div key={org.id} className="mb-2">
                <div className="px-3 py-1.5 text-xs font-semibold text-muted-foreground uppercase flex items-center gap-2">
                  <Building2 className="h-3 w-3" />
                  {org.name}
                </div>
                {orgProjectsList.length === 0 ? (
                  <div className="px-3 py-1 text-xs text-muted-foreground pl-6">
                    Sin proyectos
                  </div>
                ) : (
                  orgProjectsList.map((project) => (
                    <button
                      key={project.id}
                      onClick={() => handleSelectProject(org, project)}
                      className={cn(
                        'w-full px-3 py-1.5 text-sm hover:bg-accent flex items-center gap-2 text-left pl-6',
                        project.id === displayProject?.id && 'bg-accent'
                      )}
                    >
                      <FolderGit2 className="h-4 w-4" />
                      <span>{project.name}</span>
                    </button>
                  ))
                )}
              </div>
            );
          })}

          <div className="border-t mt-2 pt-2">
            <button
              onClick={() => {
                setIsOpen(false);
                navigate('/');
              }}
              className="w-full px-3 py-2 text-sm hover:bg-accent flex items-center gap-2 text-left"
            >
              <Building2 className="h-4 w-4" />
              <span>Ir al Dashboard</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
