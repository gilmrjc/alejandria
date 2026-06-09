import { Badge } from '@/components/ui/badge';
import { FileText, Calendar, Star, File, ChevronRight, ChevronDown, Folder } from 'lucide-react';
import type { DocumentListItem } from '@/types/document';
import { useState } from 'react';

interface DocumentListProps {
  documents: DocumentListItem[];
  loading: boolean;
  onDocumentClick: (slug: string) => void;
}

interface FolderNode {
  name: string;
  path: string;
  documents: DocumentListItem[];
  children: Record<string, FolderNode>;
}

export function DocumentList({ documents, loading, onDocumentClick }: DocumentListProps) {
  const [expandedPaths, setExpandedPaths] = useState<Set<string>>(new Set());

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <p className="text-sm text-muted-foreground">Cargando documentos...</p>
      </div>
    );
  }

  if (documents.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 border border-dashed rounded-lg">
        <FileText className="h-12 w-12 text-muted-foreground mb-4" />
        <p className="text-sm text-muted-foreground">No se encontraron documentos</p>
      </div>
    );
  }

  // Build folder tree from documents
  const buildTree = (docs: DocumentListItem[]): FolderNode => {
    const root: FolderNode = { name: 'root', path: '', documents: [], children: {} };

    docs.forEach((doc) => {
      const path = doc.folder_path || '';
      if (!path) {
        root.documents.push(doc);
        return;
      }

      const parts = path.split('/').filter(Boolean);
      let current = root;

      parts.forEach((part, index) => {
        const currentPath = parts.slice(0, index + 1).join('/');
        if (!current.children[part]) {
          current.children[part] = {
            name: part,
            path: currentPath,
            documents: [],
            children: {},
          };
        }
        current = current.children[part];
      });

      current.documents.push(doc);
    });

    return root;
  };

  const tree = buildTree(documents);

  const togglePath = (path: string) => {
    setExpandedPaths((prev) => {
      const next = new Set(prev);
      if (next.has(path)) {
        next.delete(path);
      } else {
        next.add(path);
      }
      return next;
    });
  };

  const renderDocument = (doc: DocumentListItem, level: number) => {
    const indent = level * 16;

    return (
      <div
        key={doc.id}
        className="flex items-center gap-3 px-4 py-2 hover:bg-accent/50 cursor-pointer transition-colors"
        style={{ paddingLeft: `${16 + indent}px` }}
        onClick={() => onDocumentClick(doc.slug)}
      >
        <File className="h-4 w-4 text-muted-foreground flex-shrink-0" />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className="font-medium text-sm hover:underline">{doc.title}</span>
            {doc.rating && doc.rating >= 9 && (
              <Badge variant="success" className="text-xs">Healthy</Badge>
            )}
          </div>
          <div className="flex items-center gap-4 text-xs text-muted-foreground mt-0.5">
            <span className="truncate">{doc.filename}</span>
            <div className="flex items-center gap-1 flex-shrink-0">
              <Calendar className="h-3 w-3" />
              <span>{new Date(doc.updated_at).toLocaleDateString()}</span>
            </div>
            {doc.rating && (
              <div className="flex items-center gap-1 flex-shrink-0">
                <Star className="h-3 w-3" />
                <span>{doc.rating.toFixed(1)}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  const renderFolder = (folder: FolderNode, level: number) => {
    const isExpanded = expandedPaths.has(folder.path);
    const indent = level * 16;
    const hasChildren = Object.keys(folder.children).length > 0;
    const totalDocs = folder.documents.length + Object.values(folder.children).reduce((sum, child) => sum + child.documents.length, 0);

    return (
      <div key={folder.path}>
        <div
          className="flex items-center gap-2 px-4 py-2 hover:bg-accent/50 cursor-pointer transition-colors"
          style={{ paddingLeft: `${16 + indent}px` }}
          onClick={() => togglePath(folder.path)}
        >
          {hasChildren ? (
            isExpanded ? (
              <ChevronDown className="h-4 w-4 text-muted-foreground flex-shrink-0" />
            ) : (
              <ChevronRight className="h-4 w-4 text-muted-foreground flex-shrink-0" />
            )
          ) : (
            <div className="w-4 h-4 flex-shrink-0" />
          )}
          <Folder className="h-4 w-4 text-muted-foreground flex-shrink-0" />
          <span className="font-medium text-sm">{folder.name}</span>
          <span className="text-xs text-muted-foreground">({totalDocs})</span>
        </div>
        {isExpanded && (
          <div className="divide-y">
            {folder.documents.map((doc) => renderDocument(doc, level + 1))}
            {Object.values(folder.children).map((child) => renderFolder(child, level + 1))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="border rounded-md divide-y">
      {tree.documents.map((doc) => renderDocument(doc, 0))}
      {Object.values(tree.children).map((folder) => renderFolder(folder, 0))}
    </div>
  );
}
