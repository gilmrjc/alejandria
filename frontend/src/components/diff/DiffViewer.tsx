import { useState, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Plus, Minus, FileText } from 'lucide-react';

export interface DiffViewerProps {
  oldContent: string | null;
  newContent: string;
  filename?: string;
  language?: string;
}

interface DiffLine {
  type: 'addition' | 'deletion' | 'unchanged';
  content: string;
  lineNumber: number;
  originalLineNumber?: number;
  modifiedLineNumber?: number;
}

function computeDiff(oldContent: string | null, newContent: string): DiffLine[] {
  const oldLines = oldContent ? oldContent.split('\n') : [];
  const newLines = newContent.split('\n');
  
  const diff: DiffLine[] = [];
  let oldIndex = 0;
  let newIndex = 0;
  
  while (oldIndex < oldLines.length || newIndex < newLines.length) {
    const oldLine = oldLines[oldIndex];
    const newLine = newLines[newIndex];
    
    if (oldLine === newLine) {
      diff.push({
        type: 'unchanged',
        content: oldLine || '',
        lineNumber: newIndex + 1,
        originalLineNumber: oldIndex + 1,
        modifiedLineNumber: newIndex + 1,
      });
      oldIndex++;
      newIndex++;
    } else if (oldLine !== undefined && newLine !== undefined) {
      // Modification
      diff.push({
        type: 'deletion',
        content: oldLine,
        lineNumber: oldIndex + 1,
        originalLineNumber: oldIndex + 1,
      });
      diff.push({
        type: 'addition',
        content: newLine,
        lineNumber: newIndex + 1,
        modifiedLineNumber: newIndex + 1,
      });
      oldIndex++;
      newIndex++;
    } else if (oldLine !== undefined) {
      // Deletion
      diff.push({
        type: 'deletion',
        content: oldLine,
        lineNumber: oldIndex + 1,
        originalLineNumber: oldIndex + 1,
      });
      oldIndex++;
    } else if (newLine !== undefined) {
      // Addition
      diff.push({
        type: 'addition',
        content: newLine,
        lineNumber: newIndex + 1,
        modifiedLineNumber: newIndex + 1,
      });
      newIndex++;
    }
  }
  
  return diff;
}

export function DiffViewer({ oldContent, newContent, filename, language }: DiffViewerProps) {
  const [viewMode, setViewMode] = useState<'split' | 'unified'>('split');
  const diff = computeDiff(oldContent, newContent);
  const leftPanelRef = useRef<HTMLDivElement>(null);
  const rightPanelRef = useRef<HTMLDivElement>(null);
  
  const additions = diff.filter(d => d.type === 'addition').length;
  const deletions = diff.filter(d => d.type === 'deletion').length;
  
  const handleScroll = (source: 'left' | 'right') => {
    if (viewMode !== 'split') return;
    
    const sourceRef = source === 'left' ? leftPanelRef : rightPanelRef;
    const targetRef = source === 'left' ? rightPanelRef : leftPanelRef;
    
    if (sourceRef.current && targetRef.current) {
      const scrollRatio = sourceRef.current.scrollTop / (sourceRef.current.scrollHeight - sourceRef.current.clientHeight);
      targetRef.current.scrollTop = scrollRatio * (targetRef.current.scrollHeight - targetRef.current.clientHeight);
    }
  };
  
  const getLineClassName = (line: DiffLine) => {
    switch (line.type) {
      case 'addition':
        return 'bg-emerald-500/10 border-l-2 border-emerald-500';
      case 'deletion':
        return 'bg-red-500/10 border-l-2 border-red-500';
      default:
        return 'border-l-2 border-transparent';
    }
  };
  
  const getIcon = (type: DiffLine['type']) => {
    switch (type) {
      case 'addition':
        return <Plus className="h-3 w-3 text-emerald-500 shrink-0" />;
      case 'deletion':
        return <Minus className="h-3 w-3 text-red-500 shrink-0" />;
      default:
        return null;
    }
  };
  
  const renderUnifiedView = () => (
    <div ref={leftPanelRef} className="font-mono text-sm overflow-auto max-h-[600px]">
      {diff.map((line, index) => (
        <div
          key={index}
          className={`flex items-start gap-2 px-3 py-1 ${getLineClassName(line)}`}
        >
          <span className="text-xs text-muted-foreground w-8 shrink-0">
            {line.lineNumber}
          </span>
          {getIcon(line.type)}
          <span className="flex-1 whitespace-pre-wrap break-words">{line.content || ' '}</span>
        </div>
      ))}
    </div>
  );
  
  const renderSplitView = () => {
    const oldLines = oldContent ? oldContent.split('\n') : [];
    const newLines = newContent.split('\n');
    
    return (
      <div className="grid grid-cols-2 gap-4">
        <div
          ref={leftPanelRef}
          onScroll={() => handleScroll('left')}
          className="font-mono text-sm overflow-auto max-h-[600px]"
        >
          <div className="text-xs text-muted-foreground mb-2">Anterior</div>
          {oldLines.map((line, index) => {
            const diffLine = diff.find(d => d.originalLineNumber === index + 1);
            return (
              <div
                key={index}
                className={`flex items-start gap-2 px-3 py-1 ${diffLine ? getLineClassName(diffLine) : 'border-l-2 border-transparent'}`}
              >
                <span className="text-xs text-muted-foreground w-8 shrink-0">{index + 1}</span>
                {diffLine && getIcon(diffLine.type)}
                <span className="flex-1 whitespace-pre-wrap break-words">{line || ' '}</span>
              </div>
            );
          })}
        </div>
        <div
          ref={rightPanelRef}
          onScroll={() => handleScroll('right')}
          className="font-mono text-sm overflow-auto max-h-[600px]"
        >
          <div className="text-xs text-muted-foreground mb-2">Nuevo</div>
          {newLines.map((line, index) => {
            const diffLine = diff.find(d => d.modifiedLineNumber === index + 1);
            return (
              <div
                key={index}
                className={`flex items-start gap-2 px-3 py-1 ${diffLine ? getLineClassName(diffLine) : 'border-l-2 border-transparent'}`}
              >
                <span className="text-xs text-muted-foreground w-8 shrink-0">{index + 1}</span>
                {diffLine && getIcon(diffLine.type)}
                <span className="flex-1 whitespace-pre-wrap break-words">{line || ' '}</span>
              </div>
            );
          })}
        </div>
      </div>
    );
  };
  
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <CardTitle className="text-base flex items-center gap-2">
              <FileText className="h-4 w-4" />
              Diff de Cambios
            </CardTitle>
            {filename && (
              <Badge variant="outline" className="text-xs">
                {filename}
              </Badge>
            )}
            {language && (
              <Badge variant="secondary" className="text-xs">
                {language}
              </Badge>
            )}
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant={viewMode === 'split' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setViewMode('split')}
            >
              Lado a lado
            </Button>
            <Button
              variant={viewMode === 'unified' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setViewMode('unified')}
            >
              Unificado
            </Button>
          </div>
        </div>
        <div className="flex items-center gap-4 text-xs text-muted-foreground">
          <div className="flex items-center gap-1">
            <Plus className="h-3 w-3 text-emerald-500" />
            <span>{additions} adiciones</span>
          </div>
          <div className="flex items-center gap-1">
            <Minus className="h-3 w-3 text-red-500" />
            <span>{deletions} eliminaciones</span>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {viewMode === 'split' ? renderSplitView() : renderUnifiedView()}
      </CardContent>
    </Card>
  );
}
