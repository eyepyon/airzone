// Authentication state management with Zustand

import { create } from 'zustand';
import type { User, Wallet } from '@/types';
import {
  getAuthToken,
  setAuthToken,
  removeAuthToken,
  getRefreshToken,
  setRefreshToken,
  removeRefreshToken,
} from '@/lib/api-client';
import {
  authenticateWithGoogle,
  refreshAccessToken,
  getCurrentUser,
} from '@/lib/api/auth';

interface AuthState {
  user: User | null;
  wallet: Wallet | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (idToken: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
  loadUser: () => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  wallet: null,
  token: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  login: async (idToken: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authenticateWithGoogle(idToken);
      setAuthToken(response.access_token);
      setRefreshToken(response.refresh_token);
      set({
        user: response.user,
        wallet: response.wallet,
        token: response.access_token,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Login failed',
        isLoading: false,
      });
      throw error;
    }
  },

  logout: () => {
    removeAuthToken();
    removeRefreshToken();
    set({
      user: null,
      wallet: null,
      token: null,
      isAuthenticated: false,
      error: null,
    });
  },

  refreshToken: async () => {
    const refreshToken = getRefreshToken();
    if (!refreshToken) {
      get().logout();
      return;
    }

    try {
      const response = await refreshAccessToken(refreshToken);
      setAuthToken(response.access_token);
      set({ token: response.access_token });
    } catch (error) {
      get().logout();
      throw error;
    }
  },

  loadUser: async () => {
    const token = getAuthToken();
    if (!token) {
      set({ isAuthenticated: false, isLoading: false });
      return;
    }

    set({ isLoading: true });
    try {
      const user = await getCurrentUser(token);
      set({
        user,
        token,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      // Try to refresh token
      try {
        await get().refreshToken();
        const newToken = getAuthToken();
        if (newToken) {
          const user = await getCurrentUser(newToken);
          set({
            user,
            token: newToken,
            isAuthenticated: true,
            isLoading: false,
          });
        }
      } catch {
        get().logout();
        set({ isLoading: false });
      }
    }
  },

  clearError: () => set({ error: null }),
}));
