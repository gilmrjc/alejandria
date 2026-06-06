import api from './api';
import type { AuthTokens, LoginCredentials, User } from '@/types/auth';

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthTokens> {
    const response = await api.post<AuthTokens>('/auth/login', credentials);
    return response.data;
  },

  async me(): Promise<User> {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },

  async register(data: { email: string; username: string; password: string }): Promise<User> {
    const response = await api.post<User>('/auth/register', data);
    return response.data;
  },
};
