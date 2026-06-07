import { Card, CardContent } from '@/components/ui/card';
import { AlertCircle } from 'lucide-react';
import type { Gap } from '@/types/gap';
import { GapCard } from './GapCard';

interface GapListProps {
  gaps: Gap[];
  loading: boolean;
  onGapClick: (slug: string) => void;
}

export function GapList({ gaps, loading, onGapClick }: GapListProps) {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <p className="text-sm text-muted-foreground">Cargando gaps...</p>
      </div>
    );
  }

  if (gaps.length === 0) {
    return (
      <Card>
        <CardContent className="flex flex-col items-center justify-center py-12">
          <AlertCircle className="h-12 w-12 text-muted-foreground mb-4" />
          <p className="text-sm text-muted-foreground">No se encontraron gaps</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-2">
      {gaps.map((gap) => (
        <GapCard key={gap.id} gap={gap} onClick={() => onGapClick(gap.slug)} />
      ))}
    </div>
  );
}
