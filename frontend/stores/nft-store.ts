// NFT state management with Zustand

import { create } from 'zustand';
import type { NFT } from '@/types';
import { getUserNFTs } from '@/lib/api/nfts';

interface NFTState {
  nfts: NFT[];
  loading: boolean;
  error: string | null;
  fetchNFTs: (token: string) => Promise<void>;
  refreshNFTs: (token: string) => Promise<void>;
  clearNFTs: () => void;
  clearError: () => void;
}

export const useNFTStore = create<NFTState>((set, get) => ({
  nfts: [],
  loading: false,
  error: null,

  fetchNFTs: async (token: string) => {
    set({ loading: true, error: null });
    try {
      const nfts = await getUserNFTs(token);
      set({ nfts, loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch NFTs',
        loading: false,
      });
      throw error;
    }
  },

  refreshNFTs: async (token: string) => {
    try {
      const nfts = await getUserNFTs(token);
      set({ nfts });
    } catch (error) {
      set({
        error:
          error instanceof Error ? error.message : 'Failed to refresh NFTs',
      });
      throw error;
    }
  },

  clearNFTs: () => {
    set({ nfts: [], error: null });
  },

  clearError: () => set({ error: null }),
}));
