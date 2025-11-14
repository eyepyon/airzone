// NFT store using Zustand

import { create } from 'zustand';
import type { NFT } from '../types';
import { getNFTs, mintNFT, getNFTMintStatus } from '../lib/api/nfts';

interface NFTState {
  nfts: NFT[];
  loading: boolean;
  error: string | null;
  mintingTaskId: string | null;

  // Actions
  fetchNFTs: (walletAddress?: string) => Promise<void>;
  refreshNFTs: () => Promise<void>;
  requestMint: (walletAddress: string) => Promise<string>;
  checkMintStatus: (taskId: string) => Promise<void>;
  clearError: () => void;
}

export const useNFTStore = create<NFTState>((set, get) => ({
  nfts: [],
  loading: false,
  error: null,
  mintingTaskId: null,

  fetchNFTs: async (walletAddress?: string) => {
    set({ loading: true, error: null });
    try {
      const response = await getNFTs();
      set({
        nfts: response.nfts,
        loading: false,
      });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch NFTs',
        loading: false,
      });
    }
  },

  refreshNFTs: async () => {
    // Refresh without setting loading state (for background updates)
    try {
      const response = await getNFTs();
      set({ nfts: response.nfts });
    } catch (error) {
      // Silently fail on refresh
      console.error('Failed to refresh NFTs:', error);
    }
  },

  requestMint: async (walletAddress: string) => {
    set({ loading: true, error: null });
    try {
      const response = await mintNFT(walletAddress);
      set({
        mintingTaskId: response.task_id,
        loading: false,
      });
      return response.task_id;
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to request NFT mint',
        loading: false,
      });
      throw error;
    }
  },

  checkMintStatus: async (taskId: string) => {
    try {
      const response = await getNFTMintStatus(taskId);
      
      // If minting is complete, refresh NFT list
      if (response.task.status === 'completed' && response.nft) {
        await get().refreshNFTs();
        set({ mintingTaskId: null });
      } else if (response.task.status === 'failed') {
        set({
          error: response.task.error_message || 'NFT minting failed',
          mintingTaskId: null,
        });
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to check mint status',
      });
    }
  },

  clearError: () => set({ error: null }),
}));
