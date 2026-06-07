import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Send, CheckCircle, XCircle } from 'lucide-react';
import type { Gap } from '@/types/gap';
import { GapPriorityBadge } from './GapPriorityBadge';

interface GapResolutionPanelProps {
  gap: Gap;
  onSubmit: (answer: string) => void;
  loading?: boolean;
}

export function GapResolutionPanel({ gap, onSubmit, loading }: GapResolutionPanelProps) {
  const [answer, setAnswer] = useState(gap.answer || '');

  const handleRespond = () => {
    onSubmit(answer);
  };

  const handleReject = () => {
    onSubmit('');
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between gap-2">
          <CardTitle className="text-base flex-1">{gap.question}</CardTitle>
          <GapPriorityBadge priority={gap.priority} />
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {gap.context_missing && (
          <div className="p-3 bg-muted rounded">
            <p className="text-sm font-medium mb-1">Contexto faltante:</p>
            <p className="text-sm text-muted-foreground">{gap.context_missing}</p>
          </div>
        )}

        {gap.role_affected && (
          <div className="flex items-center gap-2">
            <Badge variant="outline">Rol afectado: {gap.role_affected}</Badge>
          </div>
        )}

        <div className="space-y-2">
          <label className="text-sm font-medium">Respuesta</label>
          <Textarea
            placeholder="Ingresa tu respuesta..."
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            rows={4}
            disabled={gap.status === 'responded' || gap.status === 'rejected'}
          />
        </div>

        {gap.status === 'pending' && (
          <div className="flex gap-2">
            <Button onClick={handleRespond} disabled={!answer.trim() || loading}>
              <Send className="h-4 w-4 mr-2" />
              Responder
            </Button>
            <Button variant="outline" onClick={handleReject} disabled={loading}>
              <XCircle className="h-4 w-4 mr-2" />
              Rechazar
            </Button>
          </div>
        )}

        {gap.status === 'responded' && (
          <div className="flex items-center gap-2 text-sm text-green-600">
            <CheckCircle className="h-4 w-4" />
            <span>Gap respondido</span>
          </div>
        )}

        {gap.status === 'rejected' && (
          <div className="flex items-center gap-2 text-sm text-red-600">
            <XCircle className="h-4 w-4" />
            <span>Gap rechazado</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
