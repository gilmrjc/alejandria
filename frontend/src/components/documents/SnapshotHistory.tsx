import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { History, RotateCcw } from 'lucide-react';
import type { DocumentSnapshot } from '@/types/document';

interface SnapshotHistoryProps {
  snapshots: DocumentSnapshot[];
  loading: boolean;
  onRestore: (snapshotId: string) => void;
}

export function SnapshotHistory({ snapshots, loading, onRestore }: SnapshotHistoryProps) {
  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <History className="h-4 w-4" />
            Historial de Snapshots
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">Cargando historial...</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base flex items-center gap-2">
          <History className="h-4 w-4" />
          Historial de Snapshots
        </CardTitle>
      </CardHeader>
      <CardContent>
        {snapshots.length === 0 ? (
          <p className="text-sm text-muted-foreground">No hay snapshots disponibles</p>
        ) : (
          <div className="space-y-2">
            {snapshots.map((snapshot) => (
              <div
                key={snapshot.id}
                className="flex items-center justify-between p-2 rounded border bg-muted/50"
              >
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">
                    {new Date(snapshot.created_at).toLocaleString()}
                  </p>
                  {snapshot.created_by && (
                    <p className="text-xs text-muted-foreground">
                      Creado por: {snapshot.created_by}
                    </p>
                  )}
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onRestore(snapshot.id)}
                  className="ml-2"
                >
                  <RotateCcw className="h-4 w-4" />
                </Button>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
