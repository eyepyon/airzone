// NFT API functions

import { apiRequest } from '../api-client';
import type {
  NFT,
  NFTListResponse,
  MintNFTRequest,
  MintNFTResponse,
  NFTStatusResponse,
  QueryParams,
} from '../../types';

/**
 * Get list of NFTs for the current user
 * @param params - Query parameters for filtering and pagination
 * @returns List of NFTs
 */
export async function getNFTs(params?: QueryParams): Promise<NFTListResponse> {
  const queryString = params ? `?${new URLSearchParams(params as Record<string, string>).toString()}` : '';
  return apiRequest<NFTListResponse>(`/api/v1/nfts${queryString}`, {
    method: 'GET',
  });
}

/**
 * Get NFT details by ID
 * @param nftId - NFT ID
 * @returns NFT details
 */
export async function getNFTById(nftId: string): Promise<NFT> {
  return apiRequest<NFT>(`/api/v1/nfts/${nftId}`, {
    method: 'GET',
  });
}

/**
 * Request NFT minting
 * @param walletAddress - Wallet address to mint NFT to
 * @returns Mint response with task ID
 */
export async function mintNFT(walletAddress: string): Promise<MintNFTResponse> {
  return apiRequest<MintNFTResponse>('/api/v1/nfts/mint', {
    method: 'POST',
    body: JSON.stringify({ wallet_address: walletAddress } as MintNFTRequest),
  });
}

/**
 * Get NFT minting task status
 * @param taskId - Task ID from mint request
 * @returns Task status and NFT data if completed
 */
export async function getNFTMintStatus(taskId: string): Promise<NFTStatusResponse> {
  return apiRequest<NFTStatusResponse>(`/api/v1/nfts/status/${taskId}`, {
    method: 'GET',
  });
}

/**
 * Check if user owns a specific NFT
 * @param walletAddress - Wallet address
 * @param nftId - NFT ID to check
 * @returns Boolean indicating ownership
 */
export async function verifyNFTOwnership(
  walletAddress: string,
  nftId: string
): Promise<boolean> {
  try {
    const response = await getNFTs({ status: 'completed' });
    return response.nfts.some(
      (nft) => nft.wallet_address === walletAddress && nft.id === nftId
    );
  } catch {
    return false;
  }
}
