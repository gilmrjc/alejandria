import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { AlertCircle, Clock, CheckCircle, XCircle, FileText } from 'lucide-react';
import type { Gap } from '@/types/gap';
import { GapPriorityBadge } from './GapPriorityBadge';

interface GapCardProps {
  gap: Gap;
  onClick: () => void;
  onDocumentClick?: (documentSlug: string) => void;
}

const statusConfig: Record<string, { icon: typeof AlertCircle; label: string; variant: 'default' | 'success' | 'destructive' }> = {
  pending: { icon: Clock, label: 'Pendiente', variant: 'default' },
  responded: { icon: CheckCircle, label: 'Respondido', variant: 'success' },
  rejected: { icon: XCircle, label: 'Rechazado', variant: 'destructive' },
};

export function GapCard({ gap, onClick, onDocumentClick }: GapCardProps) {
  const status = statusConfig[gap.status] || statusConfig.pending;
  const StatusIcon = status.icon;

  const handleDocumentClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (onDocumentClick && gap.document_slug) {
      onDocumentClick(gap.document_slug);
    }
  };

  return (
    <Card className="cursor-pointer hover:bg-accent/50 transition-colors" onClick={onClick}>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-2">
          <CardTitle className="text-base flex-1">{gap.question}</CardTitle>
          <GapPriorityBadge priority={gap.priority} />
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <StatusIcon className="h-4 w-4" />
            <span>{status.label}</span>
          </div>
          {gap.answered_at && (
            <span className="text-xs text-muted-foreground">
              Respondido: {new Date(gap.answered_at).toLocaleDateString()}
            </span>
          )}
        </div>
        {gap.document_title && onDocumentClick && (
          <div className="flex items-center gap-2 mt-2 text-sm text-muted-foreground">
            <FileText className="h-4 w-4" />
            <button
              onClick={handleDocumentClick}
              className="hover:text-foreground transition-colors underline"
            >
              {gap.document_title}
            </button>
          </div>
        )}
        {gap.context_missing && (
          <p className="text-sm text-muted-foreground mt-2 line-clamp-2">
            Contexto faltante: {gap.context_missing}
          </p>
        )}
      </CardContent>
    </Card>
  );
}
