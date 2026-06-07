import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { GapFilters } from '@/components/gaps/GapFilters';
import { GapList } from '@/components/gaps/GapList';
import { useGapsStore } from '@/stores/gapsStore';

export function GapsPage() {
  const navigate = useNavigate();
  const { gaps, loading, fetchGaps } = useGapsStore();
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchGaps();
  }, [fetchGaps]);

  const handleSearchChange = (value: string) => {
    setSearch(value);
  };

  const handleClearSearch = () => {
    setSearch('');
  };

  const handleGapClick = (slug: string) => {
    navigate(`/gaps/${slug}`);
  };

  const filteredGaps = gaps.filter((gap) =>
    gap.question.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Gaps</h1>
        <p className="text-sm text-muted-foreground">Gaps detectados en documentos</p>
      </div>

      <GapFilters
        search={search}
        onSearchChange={handleSearchChange}
        onClear={handleClearSearch}
      />

      <GapList
        gaps={filteredGaps}
        loading={loading}
        onGapClick={handleGapClick}
      />
    </div>
  );
}
