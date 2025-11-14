// Authentication store using Zustand

import { create } from 'zustand';
import type { User, Wallet } from '../types';
import {
  authenticateWithGoogle,
  getCurrentUser,
  logout as apiLogout,
  refreshToken as apiRefreshToken,
} from '../lib/api/auth';
import {
  getAuthToken,
  getRefreshToken,
  removeAuthToken,
  removeRefreshToken,
} from '../lib/api-client';

interface AuthState {
  user: User | null;
  wallet: Wallet | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
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
    apiLogout();
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
      await apiRefreshToken(refreshToken);
      const token = getAuthToken();
      set({ token });
    } catch (error) {
      get().logout();
      throw error;
    }
  },

  loadUser: async () => {
    const token = getAuthToken();
    if (!token) {
      set({ isAuthenticated: false });
      return;
    }

    set({ isLoading: true, error: null });
    try {
      const user = await getCurrentUser();
      set({
        user,
        token,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      removeAuthToken();
      removeRefreshToken();
      set({
        user: null,
        wallet: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to load user',
      });
    }
  },

  clearError: () => set({ error: null }),
}));
