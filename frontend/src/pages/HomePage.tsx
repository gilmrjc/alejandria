import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Building2,
  FolderGit2,
  ChevronRight,
  Plus,
  FileText,
  AlertCircle,
  Star,
  FolderOpen,
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { useOrganizationsStore } from '@/stores/organizationsStore';
import { useProjectsStore } from '@/stores/projectsStore';
import { useProjectContextStore } from '@/stores/projectContextStore';
import type { Project } from '@/types/organization';

function ProjectHealthDot({ percentage }: { percentage: number }) {
  const color =
    percentage >= 80
      ? 'bg-emerald-500'
      : percentage >= 50
        ? 'bg-amber-500'
        : percentage > 0
          ? 'bg-red-500'
          : 'bg-slate-300';
  return (
    <span
      className={`inline-block h-2 w-2 rounded-full ${color}`}
      title={`${percentage}% de documentos saludables`}
    />
  );
}

function ProjectMetricsRow({ project }: { project: Project }) {
  const m = project.metrics;
  if (!m) return null;

  return (
    <div className="mt-3 flex flex-wrap items-center gap-2">
      <Badge variant="outline" className="text-xs gap-1 font-normal">
        <FileText className="h-3 w-3" />
        {m.document_count}
      </Badge>
      {m.gap_count > 0 && (
        <Badge
          variant={m.pending_gap_count > 0 ? 'destructive' : 'outline'}
          className="text-xs gap-1 font-normal"
        >
          <AlertCircle className="h-3 w-3" />
          {m.pending_gap_count > 0 ? `${m.pending_gap_count} gaps` : `${m.gap_count} gaps`}
        </Badge>
      )}
      {m.avg_rating !== null && m.avg_rating !== undefined && (
        <Badge variant="outline" className="text-xs gap-1 font-normal">
          <Star className="h-3 w-3" />
          {m.avg_rating}
        </Badge>
      )}
    </div>
  );
}

export function HomePage() {
  const navigate = useNavigate();
  const { organizations, fetchOrganizations } = useOrganizationsStore();
  const { projects, fetchProjects } = useProjectsStore();
  const { setProjectContext } = useProjectContextStore();

  useEffect(() => {
    fetchOrganizations();
    fetchProjects();
  }, [fetchOrganizations, fetchProjects]);

  const handleSelectProject = (org: (typeof organizations)[0], project: Project) => {
    setProjectContext(org, project);
    navigate(`/${org.slug}/${project.slug}`);
  };

  // Group projects by organization
  const projectsByOrg = organizations.map((org) => ({
    ...org,
    projects: projects.filter((p) => p.organization_id === org.id),
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
        <div className="space-y-8">
          {projectsByOrg.map((org) => (
            <div key={org.id} className="space-y-4">
              {/* Organization header */}
              <div className="flex items-center gap-3 pb-2 border-b">
                <Building2 className="h-5 w-5 text-muted-foreground" />
                <h2
                  className="text-lg font-semibold cursor-pointer hover:text-primary transition-colors"
                  onClick={() => navigate(`/${org.slug}`)}
                >
                  {org.name}
                </h2>
                {org.is_personal && (
                  <Badge variant="secondary" className="text-xs">
                    Personal
                  </Badge>
                )}
                <span className="text-xs text-muted-foreground ml-auto">
                  {org.projects.length} {org.projects.length === 1 ? 'proyecto' : 'proyectos'}
                </span>
              </div>

              {org.projects.length === 0 ? (
                <Card className="border-dashed bg-muted/30">
                  <CardContent className="py-10 text-center">
                    <FolderOpen className="h-10 w-10 text-muted-foreground mx-auto mb-3" />
                    <h3 className="text-base font-medium mb-1">
                      Esta organización no tiene proyectos
                    </h3>
                    <p className="text-sm text-muted-foreground mb-4 max-w-sm mx-auto">
                      Los proyectos agrupan documentos, gaps y propuestas. Crea uno para comenzar a documentar.
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
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {org.projects.map((project) => (
                    <Card
                      key={project.id}
                      className="cursor-pointer hover:border-primary/50 hover:shadow-sm transition-all group"
                      onClick={() => handleSelectProject(org, project)}
                    >
                      <CardHeader className="pb-3">
                        <div className="flex items-start justify-between">
                          <div className="flex items-center gap-2 min-w-0">
                            <ProjectHealthDot
                              percentage={project.metrics?.healthy_percentage ?? 0}
                            />
                            <FolderGit2 className="h-5 w-5 text-primary shrink-0" />
                            <CardTitle className="text-base font-medium group-hover:text-primary transition-colors truncate">
                              {project.name}
                            </CardTitle>
                          </div>
                          <ChevronRight className="h-4 w-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity shrink-0" />
                        </div>
                      </CardHeader>
                      <CardContent>
                        <p className="text-sm text-muted-foreground line-clamp-2">
                          {project.description || 'Sin descripción'}
                        </p>
                        <ProjectMetricsRow project={project} />
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
