/**
 * XRPL Payment Utilities
 * XRPLネットワークとの通信（バックエンド経由）
 */

import { getWalletBalance as apiGetWalletBalance } from './api/wallet';
import { executeXRPLPayment, verifyXRPLTransaction } from './api/payments';

/**
 * XRPLアドレスの検証
 */
export function validateXRPLAddress(address: string): boolean {
  if (!address.startsWith('r')) return false;
  if (address.length < 25 || address.length > 35) return false;
  if (!/^[a-zA-Z0-9]+$/.test(address)) return false;
  return true;
}

/**
 * ウォレットの残高を取得（バックエンド経由）
 */
export async function getWalletBalance(address: string): Promise<number> {
  try {
    return await apiGetWalletBalance(address);
  } catch (error) {
    console.error('Failed to get wallet balance:', error);
    return 0;
  }
}

/**
 * XRP決済を実行（バックエンド経由）
 */
export async function sendXRPPayment(
  orderId: string
): Promise<{
  hash: string;
  validated: boolean;
  ledgerIndex: number;
}> {
  try {
    const data = await executeXRPLPayment(orderId);
    return {
      hash: data.transaction_hash,
      validated: true,
      ledgerIndex: 0,
    };
  } catch (error) {
    console.error('XRPL payment failed:', error);
    throw error;
  }
}

/**
 * トランザクションの詳細を取得（バックエンド経由）
 */
export async function getTransactionDetails(txHash: string): Promise<Record<string, unknown>> {
  try {
    return await verifyXRPLTransaction(txHash);
  } catch (error) {
    console.error('Failed to get transaction details:', error);
    throw error;
  }
}

/**
 * XRP/JPYレートを取得（CoinGecko API使用）
 */
export async function getXRPJPYRate(): Promise<number> {
  try {
    // CoinGecko API（無料、認証不要）
    const response = await fetch(
      'https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=jpy',
      {
        headers: {
          'Accept': 'application/json',
        },
      }
    );

    if (!response.ok) {
      throw new Error('Failed to fetch XRP rate');
    }

    const data = await response.json();
    const rate = data?.ripple?.jpy;

    if (!rate || typeof rate !== 'number') {
      throw new Error('Invalid rate data');
    }

    return rate;
  } catch (error) {
    console.error('Failed to fetch XRP/JPY rate from CoinGecko:', error);
    // フォールバック: 固定レート（エラー時のみ）
    console.warn('Using fallback rate: 150 JPY');
    return 150;
  }
}

/**
 * JPYをXRPに換算
 */
export function convertJPYToXRP(amountJPY: number, rate: number): number {
  return amountJPY / rate;
}

/**
 * XRPをJPYに換算
 */
export function convertXRPToJPY(amountXRP: number, rate: number): number {
  return amountXRP * rate;
}
