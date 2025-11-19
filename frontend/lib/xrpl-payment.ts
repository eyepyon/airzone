/**
 * XRPL Payment Utilities
 * XRPLネットワークとの通信（バックエンド経由）
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api.airz.one';

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
    const response = await fetch(`${API_URL}/api/v1/wallet/balance?address=${address}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
    });

    if (!response.ok) {
      throw new Error('残高の取得に失敗しました');
    }

    const data = await response.json();
    return data.data.balance_xrp || 0;
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
    const response = await fetch(`${API_URL}/api/v1/payments/xrpl/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
      body: JSON.stringify({
        order_id: orderId,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'XRP決済に失敗しました');
    }

    const data = await response.json();
    return {
      hash: data.data.transaction_hash,
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
    const response = await fetch(`${API_URL}/api/v1/payments/xrpl/verify/${txHash}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
    });

    if (!response.ok) {
      throw new Error('トランザクション詳細の取得に失敗しました');
    }

    const data = await response.json();
    return data.data;
  } catch (error) {
    console.error('Failed to get transaction details:', error);
    throw error;
  }
}

/**
 * XRP/JPYレートを取得（仮実装）
 * 実際にはAPIから取得すべき
 */
export async function getXRPJPYRate(): Promise<number> {
  // TODO: 実際の為替レートAPIから取得
  // 例: CoinGecko API, Binance API など
  return 150; // 1 XRP = 150 JPY（仮）
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
