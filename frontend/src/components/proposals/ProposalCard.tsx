import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Clock, CheckCircle, XCircle, Play } from 'lucide-react';
import type { Proposal } from '@/types/proposal';

interface ProposalCardProps {
  proposal: Proposal;
  onClick: () => void;
}

const statusConfig: Record<string, { icon: typeof Clock; label: string; variant: 'default' | 'success' | 'destructive' }> = {
  pending: { icon: Clock, label: 'Pendiente', variant: 'default' },
  accepted: { icon: CheckCircle, label: 'Aceptada', variant: 'success' },
  rejected: { icon: XCircle, label: 'Rechazada', variant: 'destructive' },
  implemented: { icon: Play, label: 'Implementada', variant: 'success' },
};

export function ProposalCard({ proposal, onClick }: ProposalCardProps) {
  const status = statusConfig[proposal.status] || statusConfig.pending;
  const StatusIcon = status.icon;

  return (
    <Card className="cursor-pointer hover:bg-accent/50 transition-colors" onClick={onClick}>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-2">
          <CardTitle className="text-base flex-1">{proposal.name}</CardTitle>
          <Badge variant={status.variant}>{status.label}</Badge>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground line-clamp-2">{proposal.description}</p>
        <div className="flex items-center gap-2 mt-3 text-xs text-muted-foreground">
          <StatusIcon className="h-3 w-3" />
          <span>Creada: {new Date(proposal.created_at).toLocaleDateString()}</span>
        </div>
      </CardContent>
    </Card>
  );
}
