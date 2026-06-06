import { create } from 'zustand';
import type { User } from '@/types/auth';
import { authService } from '@/services/auth';

interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  fetchMe: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  loading: false,
  error: null,

  login: async (email, password) => {
    set({ loading: true, error: null });
    try {
      const tokens = await authService.login({ email, password });
      localStorage.setItem('access_token', tokens.access_token);
      const user = await authService.me();
      set({ user, loading: false });
    } catch {
      set({ error: 'Credenciales incorrectas', loading: false });
      throw new Error('Login failed');
    }
  },

  logout: () => {
    localStorage.removeItem('access_token');
    set({ user: null });
  },

  fetchMe: async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    set({ loading: true });
    try {
      const user = await authService.me();
      set({ user, loading: false });
    } catch {
      localStorage.removeItem('access_token');
      set({ user: null, loading: false });
    }
  },
}));
