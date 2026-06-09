import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { FileText, Calendar, Star } from 'lucide-react';
import type { DocumentListItem } from '@/types/document';

interface DocumentListProps {
  documents: DocumentListItem[];
  loading: boolean;
  onDocumentClick: (slug: string) => void;
}

export function DocumentList({ documents, loading, onDocumentClick }: DocumentListProps) {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <p className="text-sm text-muted-foreground">Cargando documentos...</p>
      </div>
    );
  }

  if (documents.length === 0) {
    return (
      <Card>
        <CardContent className="flex flex-col items-center justify-center py-12">
          <FileText className="h-12 w-12 text-muted-foreground mb-4" />
          <p className="text-sm text-muted-foreground">No se encontraron documentos</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-2">
      {documents.map((doc) => (
        <Card
          key={doc.id}
          className="cursor-pointer hover:bg-accent/50 transition-colors"
          onClick={() => onDocumentClick(doc.slug)}
        >
          <CardContent className="p-4">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <h3 className="font-medium truncate">{doc.title}</h3>
                <p className="text-sm text-muted-foreground truncate">{doc.filename}</p>
                <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Calendar className="h-3 w-3" />
                    <span>{new Date(doc.updated_at).toLocaleDateString()}</span>
                  </div>
                  {doc.rating && (
                    <div className="flex items-center gap-1">
                      <Star className="h-3 w-3" />
                      <span>{doc.rating.toFixed(1)}</span>
                    </div>
                  )}
                </div>
              </div>
              {doc.rating && doc.rating >= 9 && (
                <Badge variant="success">Healthy</Badge>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
