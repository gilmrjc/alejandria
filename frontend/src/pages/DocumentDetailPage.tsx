import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ArrowLeft, X, FileText, Code } from 'lucide-react';
import { DocumentMetadata } from '@/components/documents/DocumentMetadata';
import { SnapshotHistory } from '@/components/documents/SnapshotHistory';
import { GapList } from '@/components/gaps/GapList';
import { DiffViewer } from '@/components/diff/DiffViewer';
import { MarkdownRenderer } from '@/components/MarkdownRenderer';
import { documentsService } from '@/services/documents';
import { gapsService } from '@/services/gaps';
import type { Document, DocumentSnapshot } from '@/types/document';
import type { Gap } from '@/types/gap';

export function DocumentDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const [document, setDocument] = useState<Document | null>(null);
  const [snapshots, setSnapshots] = useState<DocumentSnapshot[]>([]);
  const [gaps, setGaps] = useState<Gap[]>([]);
  const [loading, setLoading] = useState(true);
  const [snapshotsLoading, setSnapshotsLoading] = useState(false);
  const [gapsLoading, setGapsLoading] = useState(false);
  const [comparingSnapshot, setComparingSnapshot] = useState<DocumentSnapshot | null>(null);
  const [showRaw, setShowRaw] = useState(false);

  useEffect(() => {
    if (slug) {
      loadDocument(slug);
      loadSnapshots(slug);
      loadGaps(slug);
    }
  }, [slug]);

  const loadDocument = async (docSlug: string) => {
    setLoading(true);
    try {
      const data = await documentsService.getBySlug(docSlug);
      setDocument(data);
    } catch (error) {
      console.error('Error loading document:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadSnapshots = async (docSlug: string) => {
    setSnapshotsLoading(true);
    try {
      const data = await documentsService.getSnapshotsBySlug(docSlug);
      setSnapshots(data.items);
    } catch (error) {
      console.error('Error loading snapshots:', error);
    } finally {
      setSnapshotsLoading(false);
    }
  };

  const loadGaps = async (docSlug: string) => {
    setGapsLoading(true);
    try {
      // Get document ID first to filter gaps by document_id
      const doc = await documentsService.getBySlug(docSlug);
      const data = await gapsService.list({ document_id: doc.id });
      setGaps(data.items);
    } catch (error) {
      console.error('Error loading gaps:', error);
    } finally {
      setGapsLoading(false);
    }
  };

  const handleRestoreSnapshot = async (snapshotId: string) => {
    if (!slug) return;
    try {
      await documentsService.restoreSnapshotBySlug(slug, snapshotId);
      // Reload document, snapshots, and gaps
      loadDocument(slug);
      loadSnapshots(slug);
      loadGaps(slug);
    } catch (error) {
      console.error('Error restoring snapshot:', error);
    }
  };

  const handleGapClick = (gapSlug: string) => {
    navigate(`/gaps/${gapSlug}`);
  };

  const handleCompareSnapshot = (snapshotId: string) => {
    const snapshot = snapshots.find(s => s.id === snapshotId);
    if (snapshot && snapshot.old_content) {
      setComparingSnapshot(snapshot);
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

      {comparingSnapshot && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">Comparando con snapshot del {new Date(comparingSnapshot.created_at).toLocaleString()}</h2>
            <Button variant="ghost" size="sm" onClick={() => setComparingSnapshot(null)}>
              <X className="h-4 w-4 mr-2" />
              Cerrar comparación
            </Button>
          </div>
          <DiffViewer
            oldContent={comparingSnapshot.old_content}
            newContent={comparingSnapshot.new_content}
            filename={document.filename}
          />
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-6">
          <div className="border rounded-lg p-6 bg-background">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Contenido</h2>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowRaw(!showRaw)}
              >
                {showRaw ? (
                  <>
                    <FileText className="h-4 w-4 mr-2" />
                    Ver renderizado
                  </>
                ) : (
                  <>
                    <Code className="h-4 w-4 mr-2" />
                    Ver código
                  </>
                )}
              </Button>
            </div>
            {showRaw ? (
              <pre className="whitespace-pre-wrap text-sm font-mono bg-muted/50 p-4 rounded overflow-auto max-h-[600px]">
                {document.content}
              </pre>
            ) : (
              <div className="max-w-none">
                <MarkdownRenderer content={document.content} />
              </div>
            )}
          </div>
        </div>

        <div className="space-y-6">
          <DocumentMetadata document={document} />
          <SnapshotHistory
            snapshots={snapshots}
            loading={snapshotsLoading}
            onRestore={handleRestoreSnapshot}
            onCompare={handleCompareSnapshot}
          />
          <div className="border rounded-lg p-6 bg-background">
            <h2 className="text-lg font-semibold mb-4">Gaps</h2>
            <GapList gaps={gaps} loading={gapsLoading} onGapClick={handleGapClick} compact />
          </div>
        </div>
      </div>
    </div>
  );
}
