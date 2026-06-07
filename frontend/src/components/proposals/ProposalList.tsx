import { Card, CardContent } from '@/components/ui/card';
import { Lightbulb } from 'lucide-react';
import type { Proposal } from '@/types/proposal';
import { ProposalCard } from './ProposalCard';

interface ProposalListProps {
  proposals: Proposal[];
  loading: boolean;
  onProposalClick: (id: string) => void;
}

export function ProposalList({ proposals, loading, onProposalClick }: ProposalListProps) {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <p className="text-sm text-muted-foreground">Cargando propuestas...</p>
      </div>
    );
  }

  if (proposals.length === 0) {
    return (
      <Card>
        <CardContent className="flex flex-col items-center justify-center py-12">
          <Lightbulb className="h-12 w-12 text-muted-foreground mb-4" />
          <p className="text-sm text-muted-foreground">No se encontraron propuestas</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-2">
      {proposals.map((proposal) => (
        <ProposalCard key={proposal.id} proposal={proposal} onClick={() => onProposalClick(proposal.id)} />
      ))}
    </div>
  );
}
