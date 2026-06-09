import { Card, CardContent } from '@/components/ui/card';
import { AlertCircle, Clock, CheckCircle, XCircle } from 'lucide-react';
import type { Gap } from '@/types/gap';
import { GapCard } from './GapCard';
import { GapPriorityBadge } from './GapPriorityBadge';

interface GapListProps {
  gaps: Gap[];
  loading: boolean;
  onGapClick: (slug: string) => void;
  onDocumentClick?: (documentSlug: string) => void;
  compact?: boolean;
}

export function GapList({ gaps, loading, onGapClick, onDocumentClick, compact = false }: GapListProps) {
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

  if (compact) {
    const statusConfig: Record<string, { icon: typeof Clock; label: string }> = {
      pending: { icon: Clock, label: 'Pendiente' },
      responded: { icon: CheckCircle, label: 'Respondido' },
      rejected: { icon: XCircle, label: 'Rechazado' },
    };

    return (
      <div className="border rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-muted">
            <tr>
              <th className="px-3 py-2 text-left font-medium">Pregunta</th>
              <th className="px-3 py-2 text-left font-medium">Estado</th>
              <th className="px-3 py-2 text-left font-medium">Prioridad</th>
            </tr>
          </thead>
          <tbody>
            {gaps.map((gap) => {
              const status = statusConfig[gap.status] || statusConfig.pending;
              const StatusIcon = status.icon;
              return (
                <tr
                  key={gap.id}
                  className="border-t hover:bg-accent/50 cursor-pointer transition-colors"
                  onClick={() => onGapClick(gap.slug)}
                >
                  <td className="px-3 py-2 max-w-[200px] truncate" title={gap.question}>
                    {gap.question}
                  </td>
                  <td className="px-3 py-2">
                    <div className="flex items-center gap-1.5">
                      <StatusIcon className="h-3.5 w-3.5" />
                      <span className="text-xs">{status.label}</span>
                    </div>
                  </td>
                  <td className="px-3 py-2">
                    <GapPriorityBadge priority={gap.priority} />
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {gaps.map((gap) => (
        <GapCard
          key={gap.id}
          gap={gap}
          onClick={() => onGapClick(gap.slug)}
          onDocumentClick={onDocumentClick}
        />
      ))}
    </div>
  );
}
