import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft, FileText } from 'lucide-react';
import { GapResolutionPanel } from '@/components/gaps/GapResolutionPanel';
import { gapsService } from '@/services/gaps';
import type { Gap } from '@/types/gap';

export function GapDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const [gap, setGap] = useState<Gap | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (slug) {
      loadGap(slug);
    }
  }, [slug]);

  const loadGap = async (gapSlug: string) => {
    setLoading(true);
    try {
      const data = await gapsService.getBySlug(gapSlug);
      setGap(data);
    } catch (error) {
      console.error('Error loading gap:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (answer: string) => {
    if (!slug) return;
    setSubmitting(true);
    try {
      if (answer) {
        await gapsService.updateBySlug(slug, { answer, status: 'responded' });
      } else {
        await gapsService.updateBySlug(slug, { status: 'rejected' });
      }
      // Reload gap
      loadGap(slug);
    } catch (error) {
      console.error('Error updating gap:', error);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <p className="text-sm text-muted-foreground">Cargando gap...</p>
      </div>
    );
  }

  if (!gap) {
    return (
      <div className="flex items-center justify-center py-8">
        <p className="text-sm text-muted-foreground">Gap no encontrado</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" onClick={() => navigate('/gaps')}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          Volver
        </Button>
        <div className="flex-1">
          <h1 className="text-2xl font-bold">Gap</h1>
          <p className="text-sm text-muted-foreground">Slug: {gap.slug}</p>
          {gap.document_title && (
            <p className="text-sm text-muted-foreground">Documento: {gap.document_title}</p>
          )}
        </div>
        {gap.document_slug && (
          <Button variant="outline" size="sm" onClick={() => navigate(`/documents/${gap.document_slug}`)}>
            Ver documento
          </Button>
        )}
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <GapResolutionPanel gap={gap} onSubmit={handleSubmit} loading={submitting} />
        </div>

        <div className="space-y-6">
          {gap.reference_documents && gap.reference_documents.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  <FileText className="h-4 w-4" />
                  Documentos de referencia ({gap.reference_documents.length})
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="border rounded-lg overflow-hidden">
                  <table className="w-full text-sm">
                    <thead className="bg-muted">
                      <tr>
                        <th className="px-3 py-2 text-left font-medium">Título</th>
                        <th className="px-3 py-2 text-left font-medium">Archivo</th>
                      </tr>
                    </thead>
                    <tbody>
                      {gap.reference_documents.map((doc) => (
                        <tr
                          key={doc.id}
                          className="border-t hover:bg-accent/50 cursor-pointer transition-colors"
                          onClick={() => navigate(`/documents/${doc.slug}`)}
                        >
                          <td className="px-3 py-2 max-w-[200px] truncate" title={doc.title}>
                            {doc.title}
                          </td>
                          <td className="px-3 py-2 max-w-[150px] truncate" title={doc.filename}>
                            {doc.filename}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
