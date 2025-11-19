/**
 * XRPL Payment Utilities
 * XRPLネットワークで実際にトランザクションを発行
 */

import { Client, Wallet, xrpToDrops, dropsToXrp } from 'xrpl';

const XRPL_NETWORK = process.env.NEXT_PUBLIC_XRPL_NETWORK || 'testnet';
const SPONSOR_ADDRESS = process.env.NEXT_PUBLIC_XRPL_SPONSOR_ADDRESS || '';

// XRPLクライアントのシングルトン
let clientInstance: Client | null = null;

/**
 * XRPLクライアントを取得
 */
async function getClient(): Promise<Client> {
  if (!clientInstance) {
    const wsUrl =
      XRPL_NETWORK === 'mainnet'
        ? 'wss://xrplcluster.com'
        : 'wss://s.altnet.rippletest.net:51233';

    clientInstance = new Client(wsUrl);
    await clientInstance.connect();
  }

  if (!clientInstance.isConnected()) {
    await clientInstance.connect();
  }

  return clientInstance;
}

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
 * ウォレットの残高を取得
 */
export async function getWalletBalance(address: string): Promise<number> {
  try {
    const client = await getClient();
    const response = await client.request({
      command: 'account_info',
      account: address,
      ledger_index: 'validated',
    });

    const balanceDrops = response.result.account_data.Balance;
    return parseFloat(dropsToXrp(String(balanceDrops)));
  } catch (error) {
    console.error('Failed to get wallet balance:', error);
    throw new Error('ウォレット残高の取得に失敗しました');
  }
}

/**
 * XRP決済を実行（ユーザーのウォレットから）
 */
export async function sendXRPPayment(
  fromWalletSeed: string,
  toAddress: string,
  amountXRP: number,
  memo?: string
): Promise<{
  hash: string;
  validated: boolean;
  ledgerIndex: number;
}> {
  try {
    const client = await getClient();

    // ウォレットを作成
    const wallet = Wallet.fromSeed(fromWalletSeed);

    // トランザクションを準備
    const payment: any = {
      TransactionType: 'Payment',
      Account: wallet.address,
      Destination: toAddress,
      Amount: xrpToDrops(String(amountXRP)),
    };

    // メモを追加（オプション）
    if (memo) {
      payment.Memos = [
        {
          Memo: {
            MemoType: Buffer.from('order_id', 'utf8').toString('hex').toUpperCase(),
            MemoData: Buffer.from(memo, 'utf8').toString('hex').toUpperCase(),
          },
        },
      ];
    }

    // トランザクションを準備（自動的にFeeとSequenceを設定）
    const prepared = await client.autofill(payment);

    // トランザクションに署名
    const signed = wallet.sign(prepared);

    // トランザクションを送信
    const result = await client.submitAndWait(signed.tx_blob);

    // 結果を確認
    if (result.result.meta && typeof result.result.meta === 'object') {
      const meta = result.result.meta as any;
      if (meta.TransactionResult !== 'tesSUCCESS') {
        throw new Error(`Transaction failed: ${meta.TransactionResult}`);
      }
    }

    return {
      hash: result.result.hash,
      validated: result.result.validated || false,
      ledgerIndex: result.result.ledger_index || 0,
    };
  } catch (error) {
    console.error('XRPL payment failed:', error);
    throw error;
  }
}

/**
 * スポンサーウォレットへの支払いを実行
 * （バックエンドで秘密鍵を管理する安全な方法）
 */
export async function requestXRPLPayment(
  orderId: string,
  amountXRP: number
): Promise<{
  paymentUrl: string;
  taskId: string;
}> {
  try {
    const response = await fetch('/api/v1/payments/xrpl/request', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
      body: JSON.stringify({
        order_id: orderId,
        amount_xrp: amountXRP,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'XRP決済リクエストに失敗しました');
    }

    return await response.json();
  } catch (error) {
    console.error('Failed to request XRPL payment:', error);
    throw error;
  }
}

/**
 * XRP決済のステータスを確認
 */
export async function checkXRPLPaymentStatus(taskId: string): Promise<{
  status: 'pending' | 'processing' | 'completed' | 'failed';
  transaction_hash?: string;
  error?: string;
}> {
  try {
    const response = await fetch(`/api/v1/payments/xrpl/status/${taskId}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    });

    if (!response.ok) {
      throw new Error('ステータスの取得に失敗しました');
    }

    return await response.json();
  } catch (error) {
    console.error('Failed to check payment status:', error);
    throw error;
  }
}

/**
 * トランザクションの詳細を取得
 */
export async function getTransactionDetails(txHash: string): Promise<any> {
  try {
    const client = await getClient();
    const response = await client.request({
      command: 'tx',
      transaction: txHash,
    });

    return response.result;
  } catch (error) {
    console.error('Failed to get transaction details:', error);
    throw error;
  }
}

/**
 * XRPLクライアントを切断
 */
export async function disconnectClient(): Promise<void> {
  if (clientInstance && clientInstance.isConnected()) {
    await clientInstance.disconnect();
    clientInstance = null;
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
