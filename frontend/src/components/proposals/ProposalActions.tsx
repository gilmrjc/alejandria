import { Button } from '@/components/ui/button';
import { CheckCircle, XCircle, Play } from 'lucide-react';
import type { ProposalStatus } from '@/types/proposal';

interface ProposalActionsProps {
  status: ProposalStatus;
  onApprove: () => void;
  onReject: () => void;
  onApply: () => void;
  loading?: boolean;
}

export function ProposalActions({ status, onApprove, onReject, onApply, loading }: ProposalActionsProps) {
  if (status === 'pending') {
    return (
      <div className="flex gap-2">
        <Button onClick={onApprove} disabled={loading}>
          <CheckCircle className="h-4 w-4 mr-2" />
          Aprobar
        </Button>
        <Button variant="outline" onClick={onReject} disabled={loading}>
          <XCircle className="h-4 w-4 mr-2" />
          Rechazar
        </Button>
      </div>
    );
  }

  if (status === 'accepted') {
    return (
      <Button onClick={onApply} disabled={loading}>
        <Play className="h-4 w-4 mr-2" />
        Aplicar
      </Button>
    );
  }

  return null;
}
