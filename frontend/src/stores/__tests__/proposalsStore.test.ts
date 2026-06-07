import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useProposalsStore } from '../proposalsStore';
import { proposalsService } from '@/services/proposals';
import type { Proposal } from '@/types/proposal';

vi.mock('@/services/proposals');

describe('proposalsStore', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debe tener estado inicial correcto', () => {
    const store = useProposalsStore.getState();
    expect(store.proposals).toEqual([]);
    expect(store.total).toBe(0);
    expect(store.page).toBe(1);
    expect(store.loading).toBe(false);
    expect(store.error).toBeNull();
  });

  it('debe actualizar proposals y total al fetch exitoso', async () => {
    const mockResponse = {
      items: [{ id: '1', slug: 'test', name: 'Test', description: 'Test description', status: 'pending', created_at: '2024-01-01', updated_at: '2024-01-01' } as Proposal],
      total: 1,
      page: 1,
      per_page: 10,
      total_pages: 1,
    };
    
    vi.mocked(proposalsService.list).mockResolvedValue(mockResponse);

    const store = useProposalsStore.getState();
    await store.fetchProposals();
    const updatedStore = useProposalsStore.getState();

    expect(proposalsService.list).toHaveBeenCalled();
    expect(updatedStore.proposals).toEqual(mockResponse.items);
    expect(updatedStore.total).toBe(1);
    expect(updatedStore.loading).toBe(false);
  });

  it('debe actualizar error al fetch fallido', async () => {
    vi.mocked(proposalsService.list).mockRejectedValue(new Error('API Error'));

    const store = useProposalsStore.getState();
    await store.fetchProposals();
    const updatedStore = useProposalsStore.getState();

    expect(updatedStore.error).not.toBeNull();
    expect(updatedStore.loading).toBe(false);
  });

  it('debe llamar updateProposal con parámetros correctos', async () => {
    const updatedProposal: Proposal = { id: '1', slug: 'test', name: 'Test', description: 'Test description', status: 'accepted', created_at: '2024-01-01', updated_at: '2024-01-01' };
    
    vi.mocked(proposalsService.update).mockResolvedValue(updatedProposal);

    const store = useProposalsStore.getState();
    await store.updateProposal('1', { status: 'accepted' });

    expect(proposalsService.update).toHaveBeenCalledWith('1', { status: 'accepted' });
  });

  it('debe manejar error en updateProposal', async () => {
    vi.mocked(proposalsService.update).mockRejectedValue(new Error('API Error'));

    const store = useProposalsStore.getState();
    await store.updateProposal('1', { status: 'accepted' });
    const updatedStore = useProposalsStore.getState();

    expect(updatedStore.error).not.toBeNull();
  });

  it('debe manejar proposal no encontrado en updateProposal', async () => {
    const initialProposal: Proposal = { id: '1', slug: 'test', name: 'Test', description: 'Test description', status: 'pending', created_at: '2024-01-01', updated_at: '2024-01-01' };
    const updatedProposal: Proposal = { id: '2', slug: 'test2', name: 'Test2', description: 'Test description', status: 'accepted', created_at: '2024-01-01', updated_at: '2024-01-01' };
    
    useProposalsStore.setState({ proposals: [initialProposal] });
    vi.mocked(proposalsService.update).mockResolvedValue(updatedProposal);

    const store = useProposalsStore.getState();
    await store.updateProposal('2', { status: 'accepted' });
    const updatedStore = useProposalsStore.getState();

    expect(updatedStore.proposals).toHaveLength(1);
    expect(updatedStore.proposals[0].id).toBe('1');
  });
});
