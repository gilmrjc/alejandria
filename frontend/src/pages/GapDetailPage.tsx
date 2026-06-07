import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';
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
        <div>
          <h1 className="text-2xl font-bold">Gap</h1>
          <p className="text-sm text-muted-foreground">Slug: {gap.slug}</p>
        </div>
      </div>

      <GapResolutionPanel gap={gap} onSubmit={handleSubmit} loading={submitting} />
    </div>
  );
}
