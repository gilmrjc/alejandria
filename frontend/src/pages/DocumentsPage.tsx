import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { DocumentFilters } from '@/components/documents/DocumentFilters';
import { DocumentList } from '@/components/documents/DocumentList';
import { useDocumentsStore } from '@/stores/documentsStore';

export function DocumentsPage() {
  const navigate = useNavigate();
  const { documents, loading, fetchDocuments } = useDocumentsStore();
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  const handleSearchChange = (value: string) => {
    setSearch(value);
  };

  const handleClearSearch = () => {
    setSearch('');
  };

  const handleDocumentClick = (slug: string) => {
    navigate(`/documents/${slug}`);
  };

  const filteredDocuments = documents.filter((doc) =>
    doc.title.toLowerCase().includes(search.toLowerCase()) ||
    doc.filename.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Documentos</h1>
        <p className="text-sm text-muted-foreground">Gestión de documentos del proyecto</p>
      </div>

      <DocumentFilters
        search={search}
        onSearchChange={handleSearchChange}
        onClear={handleClearSearch}
      />

      <DocumentList
        documents={filteredDocuments}
        loading={loading}
        onDocumentClick={handleDocumentClick}
      />
    </div>
  );
}
