import { FileText } from 'lucide-react';

export function DocumentsPage() {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center">
      <FileText className="h-16 w-16 text-muted-foreground mb-4" />
      <h2 className="text-xl font-semibold mb-2">Selecciona un documento</h2>
      <p className="text-sm text-muted-foreground max-w-md">
        Usa el explorador de archivos a la izquierda para navegar y seleccionar un documento para ver su contenido.
      </p>
    </div>
  );
}
