import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, Calendar, FileText } from 'lucide-react';
import { ProposalActions } from '@/components/proposals/ProposalActions';
import { proposalsService } from '@/services/proposals';
import type { Proposal } from '@/types/proposal';

export function ProposalDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [proposal, setProposal] = useState<Proposal | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    if (id) {
      loadProposal(id);
    }
  }, [id]);

  const loadProposal = async (proposalId: string) => {
    setLoading(true);
    try {
      const data = await proposalsService.get(proposalId);
      setProposal(data);
    } catch (error) {
      console.error('Error loading proposal:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async () => {
    if (!id) return;
    setActionLoading(true);
    try {
      await proposalsService.update(id, { status: 'accepted' });
      loadProposal(id);
    } catch (error) {
      console.error('Error approving proposal:', error);
    } finally {
      setActionLoading(false);
    }
  };

  const handleReject = async () => {
    if (!id) return;
    setActionLoading(true);
    try {
      await proposalsService.update(id, { status: 'rejected' });
      loadProposal(id);
    } catch (error) {
      console.error('Error rejecting proposal:', error);
    } finally {
      setActionLoading(false);
    }
  };

  const handleApply = async () => {
    if (!id) return;
    setActionLoading(true);
    try {
      await proposalsService.update(id, { status: 'implemented' });
      loadProposal(id);
    } catch (error) {
      console.error('Error applying proposal:', error);
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <p className="text-sm text-muted-foreground">Cargando propuesta...</p>
      </div>
    );
  }

  if (!proposal) {
    return (
      <div className="flex items-center justify-center py-8">
        <p className="text-sm text-muted-foreground">Propuesta no encontrada</p>
      </div>
    );
  }

  const statusColors: Record<string, 'default' | 'success' | 'destructive'> = {
    pending: 'default',
    accepted: 'success',
    rejected: 'destructive',
    implemented: 'success',
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" onClick={() => navigate('/proposals')}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          Volver
        </Button>
        <div className="flex-1">
          <h1 className="text-2xl font-bold">{proposal.name}</h1>
          <p className="text-sm text-muted-foreground">ID: {proposal.id}</p>
        </div>
        <Badge variant={statusColors[proposal.status] || 'default'}>
          {proposal.status.charAt(0).toUpperCase() + proposal.status.slice(1)}
        </Badge>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Descripción</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm whitespace-pre-wrap">{proposal.description}</p>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Acciones</CardTitle>
            </CardHeader>
            <CardContent>
              <ProposalActions
                status={proposal.status}
                onApprove={handleApprove}
                onReject={handleReject}
                onApply={handleApply}
                loading={actionLoading}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Metadatos</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Estado</span>
                <Badge variant={statusColors[proposal.status] || 'default'}>
                  {proposal.status.charAt(0).toUpperCase() + proposal.status.slice(1)}
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Creada</span>
                <div className="flex items-center gap-1 text-sm">
                  <Calendar className="h-3 w-3" />
                  <span>{new Date(proposal.created_at).toLocaleString()}</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Actualizada</span>
                <div className="flex items-center gap-1 text-sm">
                  <Calendar className="h-3 w-3" />
                  <span>{new Date(proposal.updated_at).toLocaleString()}</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {proposal.gaps && proposal.gaps.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  <FileText className="h-4 w-4" />
                  Gaps relacionados ({proposal.gaps.length})
                </CardTitle>
              </CardHeader>
              <CardContent>
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
                      {proposal.gaps.map((gap) => (
                        <tr
                          key={gap.id}
                          className="border-t hover:bg-accent/50 cursor-pointer transition-colors"
                          onClick={() => navigate(`/gaps/${gap.slug}`)}
                        >
                          <td className="px-3 py-2 max-w-[200px] truncate" title={gap.question}>
                            {gap.question}
                          </td>
                          <td className="px-3 py-2">
                            <Badge variant="outline" className="text-xs">
                              {gap.status}
                            </Badge>
                          </td>
                          <td className="px-3 py-2">
                            <Badge variant="outline" className="text-xs">
                              {gap.priority}
                            </Badge>
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
