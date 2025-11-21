// Wallet API functions

import { apiRequest } from '../api-client';

/**
 * Get wallet balance for an address
 * @param address - XRPL wallet address
 * @returns Wallet balance in XRP
 */
export async function getWalletBalance(address: string): Promise<number> {
  const data = await apiRequest<{ balance_xrp: number }>(
    `/api/v1/wallet/balance?address=${address}`,
    {
      method: 'GET',
    }
  );
  return data.balance_xrp || 0;
}

/**
 * Get user's wallet information
 * @returns Wallet details
 */
export async function getUserWallet(): Promise<{
  address: string;
  balance_xrp: number;
}> {
  return apiRequest<{ address: string; balance_xrp: number }>(
    '/api/v1/wallet',
    {
      method: 'GET',
    }
  );
}
