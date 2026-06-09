import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Building2, FolderGit2, ChevronRight, Plus } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { useOrganizationsStore } from '@/stores/organizationsStore';
import { useProjectsStore } from '@/stores/projectsStore';
import { useProjectContextStore } from '@/stores/projectContextStore';

export function HomePage() {
  const navigate = useNavigate();
  const { organizations, fetchOrganizations } = useOrganizationsStore();
  const { projects, fetchProjects } = useProjectsStore();
  const { setProjectContext } = useProjectContextStore();

  useEffect(() => {
    fetchOrganizations();
    fetchProjects();
  }, [fetchOrganizations, fetchProjects]);

  const handleSelectProject = (org: typeof organizations[0], project: typeof projects[0]) => {
    setProjectContext(org, project);
    // Navigate to project dashboard (not documents)
    navigate(`/${org.slug}/${project.slug}`);
  };

  // Group projects by organization
  const projectsByOrg = organizations.map(org => ({
    ...org,
    projects: projects.filter(p => p.organization_id === org.id),
  }));

  const hasOrganizations = organizations.length > 0;
  const hasProjects = projects.length > 0;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold">Inicio</h1>
        <p className="text-sm text-muted-foreground">
          {hasProjects
            ? 'Selecciona un proyecto para comenzar'
            : 'Crea una organización y un proyecto para comenzar'}
        </p>
      </div>

      {!hasOrganizations ? (
        <Card className="border-dashed">
          <CardContent className="py-12 text-center">
            <Building2 className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-medium mb-2">No tienes organizaciones</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Las organizaciones te permiten agrupar proyectos y colaborar con tu equipo
            </p>
            <Button onClick={() => navigate('/organizations/new')}>
              <Plus className="h-4 w-4 mr-2" />
              Crear organización
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-6">
          {projectsByOrg.map(org => (
            <div key={org.id} className="space-y-3">
              <div
                className="flex items-center gap-2 cursor-pointer hover:text-primary transition-colors"
                onClick={() => navigate(`/${org.slug}`)}
              >
                <Building2 className="h-5 w-5 text-muted-foreground" />
                <h2 className="text-lg font-semibold hover:underline">{org.name}</h2>
                {org.is_personal && (
                  <Badge variant="secondary" className="text-xs">Personal</Badge>
                )}
              </div>

              {org.projects.length === 0 ? (
                <Card className="border-dashed">
                  <CardContent className="py-6 text-center">
                    <p className="text-sm text-muted-foreground mb-3">
                      Esta organización no tiene proyectos
                    </p>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => navigate(`/organizations/${org.slug}/projects/new`)}
                    >
                      <Plus className="h-4 w-4 mr-2" />
                      Crear proyecto
                    </Button>
                  </CardContent>
                </Card>
              ) : (
                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                  {org.projects.map(project => (
                    <Card
                      key={project.id}
                      className="cursor-pointer hover:border-primary/50 transition-colors group"
                      onClick={() => handleSelectProject(org, project)}
                    >
                      <CardHeader className="pb-3">
                        <div className="flex items-start justify-between">
                          <div className="flex items-center gap-2">
                            <FolderGit2 className="h-5 w-5 text-primary" />
                            <CardTitle className="text-base font-medium group-hover:text-primary transition-colors">
                              {project.name}
                            </CardTitle>
                          </div>
                          <ChevronRight className="h-4 w-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                        </div>
                      </CardHeader>
                      <CardContent>
                        <p className="text-sm text-muted-foreground line-clamp-2">
                          {project.description || 'Sin descripción'}
                        </p>
                        <div className="mt-3 flex items-center gap-2 text-xs text-muted-foreground">
                          <span className="px-2 py-1 bg-muted rounded">{org.slug}/{project.slug}</span>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
