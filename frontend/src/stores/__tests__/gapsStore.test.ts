import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useGapsStore } from '../gapsStore';
import { gapsService } from '@/services/gaps';

vi.mock('@/services/gaps');

describe('gapsStore', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debe tener estado inicial correcto', () => {
    const store = useGapsStore.getState();
    expect(store.gaps).toEqual([]);
    expect(store.total).toBe(0);
    expect(store.page).toBe(1);
    expect(store.loading).toBe(false);
    expect(store.error).toBeNull();
  });

  it('debe llamar gapsService.list en fetchGaps', async () => {
    const mockResponse = {
      items: [{ id: '1', question: 'Test', slug: 'test', priority: 'high' as const, status: 'pending' as const, document_id: '1', created_at: '2024-01-01', updated_at: '2024-01-01', answer: null, answered_at: null, context_missing: null, role_affected: null }],
      pagination: { page: 1, per_page: 10, total: 1, total_pages: 1 },
    } as any;
    
    vi.mocked(gapsService.list).mockResolvedValue(mockResponse);

    const store = useGapsStore.getState();
    await store.fetchGaps();
    const updatedStore = useGapsStore.getState();

    expect(gapsService.list).toHaveBeenCalled();
    expect(updatedStore.gaps).toEqual(mockResponse.items);
    expect(updatedStore.total).toBe(1);
    expect(updatedStore.loading).toBe(false);
  });

  it('debe manejar error en fetchGaps', async () => {
    vi.mocked(gapsService.list).mockRejectedValue(new Error('API Error'));

    const store = useGapsStore.getState();
    await store.fetchGaps();
    const updatedStore = useGapsStore.getState();

    expect(updatedStore.error).toBe('Error al cargar gaps');
    expect(updatedStore.loading).toBe(false);
  });

  it('debe llamar gapsService.updateBySlug en updateGap', async () => {
    const updatedGap = { id: '1', question: 'Test', slug: 'test', priority: 'high' as const, status: 'resolved' as const, document_id: '1', created_at: '2024-01-01', updated_at: '2024-01-01', answer: null, answered_at: null, context_missing: null, role_affected: null } as any;
    
    vi.mocked(gapsService.updateBySlug).mockResolvedValue(updatedGap);

    const store = useGapsStore.getState();
    await store.updateGap('test', { status: 'resolved' });

    expect(gapsService.updateBySlug).toHaveBeenCalledWith('test', { status: 'resolved' });
  });

  it('debe actualizar gap en la lista al updateGap exitoso', async () => {
    const initialGap = { id: '1', question: 'Test', slug: 'test', priority: 'high' as const, status: 'pending' as const, document_id: '1', created_at: '2024-01-01', updated_at: '2024-01-01', answer: null, answered_at: null, context_missing: null, role_affected: null };
    const updatedGap = { id: '1', question: 'Test', slug: 'test', priority: 'high' as const, status: 'resolved' as const, document_id: '1', created_at: '2024-01-01', updated_at: '2024-01-01', answer: null, answered_at: null, context_missing: null, role_affected: null };
    
    useGapsStore.setState({ gaps: [initialGap] });
    vi.mocked(gapsService.updateBySlug).mockResolvedValue(updatedGap as any);

    const store = useGapsStore.getState();
    await store.updateGap('test', { status: 'resolved' });
    const updatedStore = useGapsStore.getState();

    expect(gapsService.updateBySlug).toHaveBeenCalledWith('test', { status: 'resolved' });
    expect(updatedStore.gaps[0].status).toBe('resolved');
  });

  it('debe manejar error en updateGap', async () => {
    vi.mocked(gapsService.updateBySlug).mockRejectedValue(new Error('API Error'));

    const store = useGapsStore.getState();
    await store.updateGap('test', { status: 'resolved' });
    const updatedStore = useGapsStore.getState();

    expect(updatedStore.error).toBe('Error al actualizar gap');
  });

  it('debe manejar gap no encontrado en updateGap', async () => {
    const initialGap = { id: '1', question: 'Test', slug: 'test', priority: 'high' as const, status: 'pending' as const, document_id: '1', created_at: '2024-01-01', updated_at: '2024-01-01', answer: null, answered_at: null, context_missing: null, role_affected: null };
    const updatedGap = { id: '2', question: 'Test2', slug: 'test2', priority: 'high' as const, status: 'resolved' as const, document_id: '1', created_at: '2024-01-01', updated_at: '2024-01-01', answer: null, answered_at: null, context_missing: null, role_affected: null };
    
    useGapsStore.setState({ gaps: [initialGap] });
    vi.mocked(gapsService.updateBySlug).mockResolvedValue(updatedGap as any);

    const store = useGapsStore.getState();
    await store.updateGap('test2', { status: 'resolved' });
    const updatedStore = useGapsStore.getState();

    expect(updatedStore.gaps).toHaveLength(1);
    expect(updatedStore.gaps[0].slug).toBe('test');
  });
});
