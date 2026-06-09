import { useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Building2, FolderGit2, ChevronRight, ArrowLeft, Plus } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { useOrganizationsStore } from '@/stores/organizationsStore';
import { useProjectsStore } from '@/stores/projectsStore';
import { useProjectContextStore } from '@/stores/projectContextStore';

export function OrganizationPage() {
  const navigate = useNavigate();
  const { orgSlug } = useParams<{ orgSlug: string }>();
  const { organizations } = useOrganizationsStore();
  const { projects, fetchProjects } = useProjectsStore();
  const { setProjectContext } = useProjectContextStore();

  // Find the organization by slug
  const organization = organizations.find((o) => o.slug === orgSlug);

  // Filter projects for this organization
  const orgProjects = projects.filter((p) => p.organization_id === organization?.id);

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  const handleSelectProject = (project: typeof projects[0]) => {
    if (organization) {
      setProjectContext(organization, project);
      navigate(`/${organization.slug}/${project.slug}`);
    }
  };

  if (!organization) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-muted-foreground">Organización no encontrada</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Back button and breadcrumb */}
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => navigate('/')}
          className="gap-2"
        >
          <ArrowLeft className="h-4 w-4" />
          Volver al inicio
        </Button>
      </div>

      {/* Organization header */}
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <Building2 className="h-8 w-8 text-primary" />
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold">{organization.name}</h1>
              {organization.is_personal && (
                <Badge variant="secondary">Personal</Badge>
              )}
            </div>
            <p className="text-sm text-muted-foreground">@{organization.slug}</p>
          </div>
        </div>
        <Button
          variant="outline"
          onClick={() => navigate(`/organizations/${orgSlug}/projects/new`)}
        >
          <Plus className="h-4 w-4 mr-2" />
          Nuevo proyecto
        </Button>
      </div>

      {/* Projects grid */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <FolderGit2 className="h-5 w-5 text-muted-foreground" />
          Proyectos
          <Badge variant="secondary">{orgProjects.length}</Badge>
        </h2>

        {orgProjects.length === 0 ? (
          <Card className="border-dashed">
            <CardContent className="py-12 text-center">
              <FolderGit2 className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-medium mb-2">No hay proyectos</h3>
              <p className="text-sm text-muted-foreground mb-4">
                Esta organización aún no tiene proyectos. Crea uno para comenzar.
              </p>
              <Button onClick={() => navigate(`/organizations/${orgSlug}/projects/new`)}>
                <Plus className="h-4 w-4 mr-2" />
                Crear proyecto
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {orgProjects.map((project) => (
              <Card
                key={project.id}
                className="cursor-pointer hover:border-primary/50 transition-colors group"
                onClick={() => handleSelectProject(project)}
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
                  <div className="mt-3 text-xs text-muted-foreground">
                    <span className="px-2 py-1 bg-muted rounded">
                      {organization.slug}/{project.slug}
                    </span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
