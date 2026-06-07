import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Calendar, Star } from 'lucide-react';
import type { Document } from '@/types/document';

interface DocumentMetadataProps {
  document: Document;
}

export function DocumentMetadata({ document }: DocumentMetadataProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Metadatos</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Título</span>
          <span className="text-sm font-medium">{document.title}</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Archivo</span>
          <span className="text-sm font-medium">{document.filename}</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Calificación</span>
          <div className="flex items-center gap-2">
            {document.rating ? (
              <>
                <Star className="h-4 w-4 text-yellow-500" />
                <span className="text-sm font-medium">{document.rating.toFixed(1)}</span>
                {document.rating >= 9 && <Badge variant="success">Healthy</Badge>}
              </>
            ) : (
              <span className="text-sm text-muted-foreground">Sin calificar</span>
            )}
          </div>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Creado</span>
          <div className="flex items-center gap-1 text-sm">
            <Calendar className="h-3 w-3" />
            <span>{new Date(document.created_at).toLocaleString()}</span>
          </div>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Actualizado</span>
          <div className="flex items-center gap-1 text-sm">
            <Calendar className="h-3 w-3" />
            <span>{new Date(document.updated_at).toLocaleString()}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
