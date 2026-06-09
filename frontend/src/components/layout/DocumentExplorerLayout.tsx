import { Outlet, useNavigate, useParams } from 'react-router-dom';
import { DocumentSidebar } from '@/components/documents/DocumentSidebar';

export function DocumentExplorerLayout() {
  const navigate = useNavigate();
  const { orgSlug, projectSlug, slug } = useParams<{
    orgSlug: string;
    projectSlug: string;
    slug?: string;
  }>();

  const handleDocumentClick = (docSlug: string) => {
    if (orgSlug && projectSlug) {
      navigate(`/${orgSlug}/${projectSlug}/documents/${docSlug}`);
    }
  };

  // Show message if no project context
  if (!orgSlug || !projectSlug) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="text-center">
          <h2 className="text-lg font-semibold text-muted-foreground">
            Selecciona un proyecto
          </h2>
          <p className="text-sm text-muted-foreground mt-2">
            Usa el selector de proyectos en la barra superior
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-full overflow-hidden">
      <aside className="w-64 border-r overflow-hidden flex flex-col">
        <div className="px-4 py-3 border-b">
          <h2 className="font-semibold text-sm">Explorador</h2>
        </div>
        <DocumentSidebar
          onDocumentClick={handleDocumentClick}
          selectedSlug={slug}
          orgSlug={orgSlug}
          projectSlug={projectSlug}
        />
      </aside>
      <main className="flex-1 overflow-y-auto">
        <Outlet />
      </main>
    </div>
  );
}
