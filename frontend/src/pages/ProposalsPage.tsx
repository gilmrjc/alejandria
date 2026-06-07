import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ProposalFilters } from '@/components/proposals/ProposalFilters';
import { ProposalList } from '@/components/proposals/ProposalList';
import { useProposalsStore } from '@/stores/proposalsStore';

export function ProposalsPage() {
  const navigate = useNavigate();
  const { proposals, loading, fetchProposals } = useProposalsStore();
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchProposals();
  }, [fetchProposals]);

  const handleSearchChange = (value: string) => {
    setSearch(value);
  };

  const handleClearSearch = () => {
    setSearch('');
  };

  const handleProposalClick = (id: string) => {
    navigate(`/proposals/${id}`);
  };

  const filteredProposals = proposals.filter((proposal) =>
    proposal.name.toLowerCase().includes(search.toLowerCase()) ||
    proposal.description.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Propuestas</h1>
        <p className="text-sm text-muted-foreground">Propuestas de cambios pendientes</p>
      </div>

      <ProposalFilters
        search={search}
        onSearchChange={handleSearchChange}
        onClear={handleClearSearch}
      />

      <ProposalList
        proposals={filteredProposals}
        loading={loading}
        onProposalClick={handleProposalClick}
      />
    </div>
  );
}
