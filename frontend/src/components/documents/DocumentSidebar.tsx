import { File, ChevronRight, ChevronDown, Folder } from 'lucide-react';
import type { FolderTreeItem } from '@/types/document';
import { useState, useEffect } from 'react';
import { cn } from '@/utils';
import { documentsService } from '@/services/documents';

interface DocumentSidebarProps {
  onDocumentClick: (slug: string) => void;
  selectedSlug?: string;
}

export function DocumentSidebar({ onDocumentClick, selectedSlug }: DocumentSidebarProps) {
  const [tree, setTree] = useState<FolderTreeItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedPaths, setExpandedPaths] = useState<Set<string>>(new Set());

  useEffect(() => {
    loadTree();
  }, []);

  const loadTree = async () => {
    try {
      setLoading(true);
      const data = await documentsService.getTree();
      setTree(data);
    } catch (error) {
      console.error('Error loading tree:', error);
    } finally {
      setLoading(false);
    }
  };

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

  const renderItem = (item: FolderTreeItem, level: number = 0) => {
    const indent = level * 16;
    const isExpanded = expandedPaths.has(item.path);
    const hasChildren = item.children.length > 0;

    if (item.type === 'folder') {
      return (
        <div key={item.id}>
          <div
            className="flex items-center gap-1 px-3 py-1.5 hover:bg-accent/50 cursor-pointer transition-colors text-sm"
            style={{ paddingLeft: `${12 + indent}px` }}
            onClick={() => togglePath(item.path)}
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
            <Folder className="h-4 w-4 text-muted-foreground flex-shrink-0 ml-1" />
            <span className="truncate font-medium">{item.name}</span>
          </div>
          {isExpanded && (
            <div>
              {item.children.map((child) => renderItem(child, level + 1))}
            </div>
          )}
        </div>
      );
    }

    // Document
    const isSelected = selectedSlug === item.slug;
    return (
      <div
        key={item.id}
        className={cn(
          'flex items-center gap-1 px-3 py-1.5 cursor-pointer transition-colors text-sm',
          isSelected ? 'bg-accent text-accent-foreground' : 'hover:bg-accent/50'
        )}
        style={{ paddingLeft: `${12 + indent}px` }}
        onClick={() => item.slug && onDocumentClick(item.slug)}
      >
        <div className="w-4 h-4 flex-shrink-0" />
        <File className="h-4 w-4 text-muted-foreground flex-shrink-0 ml-1" />
        <span className="truncate">{item.name}</span>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <p className="text-sm text-muted-foreground">Cargando...</p>
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto">
      {tree.map((item) => renderItem(item))}
    </div>
  );
}
