import { Outlet, useNavigate, useParams } from 'react-router-dom';
import { DocumentSidebar } from '@/components/documents/DocumentSidebar';

export function DocumentExplorerLayout() {
  const navigate = useNavigate();
  const { slug } = useParams();

  const handleDocumentClick = (docSlug: string) => {
    navigate(`/documents/${docSlug}`);
  };

  return (
    <div className="flex h-full overflow-hidden">
      <aside className="w-64 border-r overflow-hidden flex flex-col">
        <div className="px-4 py-3 border-b">
          <h2 className="font-semibold text-sm">Explorador</h2>
        </div>
        <DocumentSidebar
          onDocumentClick={handleDocumentClick}
          selectedSlug={slug}
        />
      </aside>
      <main className="flex-1 overflow-y-auto">
        <Outlet />
      </main>
    </div>
  );
}
