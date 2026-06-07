import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';
import { DocumentMetadata } from '@/components/documents/DocumentMetadata';
import { SnapshotHistory } from '@/components/documents/SnapshotHistory';
import { documentsService } from '@/services/documents';
import type { Document, DocumentSnapshot } from '@/types/document';

export function DocumentDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [document, setDocument] = useState<Document | null>(null);
  const [snapshots, setSnapshots] = useState<DocumentSnapshot[]>([]);
  const [loading, setLoading] = useState(true);
  const [snapshotsLoading, setSnapshotsLoading] = useState(false);

  useEffect(() => {
    if (id) {
      loadDocument(id);
      loadSnapshots(id);
    }
  }, [id]);

  const loadDocument = async (docId: string) => {
    setLoading(true);
    try {
      const data = await documentsService.get(docId);
      setDocument(data);
    } catch (error) {
      console.error('Error loading document:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadSnapshots = async (docId: string) => {
    setSnapshotsLoading(true);
    try {
      const data = await documentsService.getSnapshots(docId);
      setSnapshots(data.items);
    } catch (error) {
      console.error('Error loading snapshots:', error);
    } finally {
      setSnapshotsLoading(false);
    }
  };

  const handleRestoreSnapshot = async (snapshotId: string) => {
    if (!id) return;
    try {
      await documentsService.restoreSnapshot(id, snapshotId);
      // Reload document and snapshots
      loadDocument(id);
      loadSnapshots(id);
    } catch (error) {
      console.error('Error restoring snapshot:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <p className="text-sm text-muted-foreground">Cargando documento...</p>
      </div>
    );
  }

  if (!document) {
    return (
      <div className="flex items-center justify-center py-8">
        <p className="text-sm text-muted-foreground">Documento no encontrado</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" onClick={() => navigate('/documents')}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          Volver
        </Button>
        <div>
          <h1 className="text-2xl font-bold">{document.title}</h1>
          <p className="text-sm text-muted-foreground">{document.filename}</p>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-6">
          <div className="border rounded-lg p-6 bg-background">
            <h2 className="text-lg font-semibold mb-4">Contenido</h2>
            <pre className="whitespace-pre-wrap text-sm font-mono bg-muted/50 p-4 rounded overflow-auto max-h-[600px]">
              {document.content}
            </pre>
          </div>
        </div>

        <div className="space-y-6">
          <DocumentMetadata document={document} />
          <SnapshotHistory
            snapshots={snapshots}
            loading={snapshotsLoading}
            onRestore={handleRestoreSnapshot}
          />
        </div>
      </div>
    </div>
  );
}
