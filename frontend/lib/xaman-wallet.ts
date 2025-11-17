/**
 * Xaman Wallet (旧Xumm) 統合
 * XRPLウォレット接続とトランザクション署名
 * 
 * 注意: この実装は簡易版です。本番環境では以下が必要です：
 * 1. Xaman SDK (xumm-sdk) のインストール
 * 2. Xaman API Key の取得
 * 3. WebSocket接続の実装
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export interface XamanWalletState {
  connected: boolean;
  address: string | null;
  publicKey: string | null;
}

export class XamanWalletClient {
  private static instance: XamanWalletClient;
  private state: XamanWalletState = {
    connected: false,
    address: null,
    publicKey: null,
  };

  private constructor() {
    // ローカルストレージから状態を復元
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('xaman_wallet_state');
      if (saved) {
        try {
          this.state = JSON.parse(saved);
        } catch (e) {
          console.error('Failed to restore wallet state:', e);
        }
      }
    }
  }

  static getInstance(): XamanWalletClient {
    if (!XamanWalletClient.instance) {
      XamanWalletClient.instance = new XamanWalletClient();
    }
    return XamanWalletClient.instance;
  }

  /**
   * Xaman Walletに接続
   * 
   * 実装方法:
   * 1. バックエンドでXaman APIを呼び出してペイロードを作成
   * 2. QRコードまたはディープリンクを表示
   * 3. ユーザーがXamanアプリで承認
   * 4. WebSocketまたはポーリングで結果を取得
   */
  async connect(): Promise<XamanWalletState> {
    try {
      console.log('Connecting to Xaman Wallet...');
      
      // バックエンドにXaman接続リクエストを送信
      const response = await fetch(`${API_BASE_URL}/api/v1/wallet/xaman/connect`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to initiate Xaman connection');
      }

      const data = await response.json();
      
      // QRコードまたはディープリンクを表示
      if (data.qr_url) {
        // QRコードを表示するモーダルを開く
        this.showQRModal(data.qr_url, data.deeplink);
        
        // ポーリングで結果を待つ
        const result = await this.pollForResult(data.uuid);
        
        if (result.success) {
          this.state = {
            connected: true,
            address: result.address,
            publicKey: result.publicKey,
          };
          
          // ローカルストレージに保存
          this.saveState();
          
          return this.state;
        } else {
          throw new Error('User rejected connection');
        }
      } else {
        throw new Error('No QR code received from server');
      }
    } catch (error) {
      console.error('Failed to connect to Xaman Wallet:', error);
      throw error;
    }
  }

  /**
   * QRコードモーダルを表示
   */
  private showQRModal(qrUrl: string, deeplink: string): void {
    // 実装: QRコードを表示するモーダル
    // または、コンポーネント側で処理
    console.log('QR URL:', qrUrl);
    console.log('Deeplink:', deeplink);
    
    // モバイルの場合はディープリンクを開く
    if (/iPhone|iPad|iPod|Android/i.test(navigator.userAgent)) {
      window.location.href = deeplink;
    }
  }

  /**
   * 接続結果をポーリング
   */
  private async pollForResult(uuid: string, maxAttempts: number = 60): Promise<any> {
    for (let i = 0; i < maxAttempts; i++) {
      await new Promise(resolve => setTimeout(resolve, 2000)); // 2秒待機
      
      try {
        const response = await fetch(`${API_BASE_URL}/api/v1/wallet/xaman/status/${uuid}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        
        if (response.ok) {
          const data = await response.json();
          
          if (data.status === 'signed') {
            return {
              success: true,
              address: data.address,
              publicKey: data.publicKey,
            };
          } else if (data.status === 'rejected') {
            return { success: false };
          }
          // 'pending' の場合は続行
        }
      } catch (error) {
        console.error('Polling error:', error);
      }
    }
    
    throw new Error('Connection timeout');
  }

  /**
   * Xaman Walletから切断
   */
  disconnect(): void {
    this.state = {
      connected: false,
      address: null,
      publicKey: null,
    };
    
    if (typeof window !== 'undefined') {
      localStorage.removeItem('xaman_wallet_state');
    }
  }

  /**
   * 現在の接続状態を取得
   */
  getState(): XamanWalletState {
    return { ...this.state };
  }

  /**
   * 状態をローカルストレージに保存
   */
  private saveState(): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('xaman_wallet_state', JSON.stringify(this.state));
    }
  }

  /**
   * トランザクションに署名
   */
  async signTransaction(transaction: any): Promise<string> {
    if (!this.state.connected) {
      throw new Error('Wallet not connected');
    }

    try {
      console.log('Signing transaction with Xaman Wallet...');
      
      // バックエンドにトランザクション署名リクエストを送信
      const response = await fetch(`${API_BASE_URL}/api/v1/wallet/xaman/sign`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          transaction,
          address: this.state.address,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to initiate transaction signing');
      }

      const data = await response.json();
      
      // QRコードを表示してユーザーの署名を待つ
      this.showQRModal(data.qr_url, data.deeplink);
      const result = await this.pollForResult(data.uuid);
      
      if (result.success) {
        return result.signedTransaction;
      } else {
        throw new Error('User rejected transaction');
      }
    } catch (error) {
      console.error('Failed to sign transaction:', error);
      throw error;
    }
  }
}

export const xamanWallet = XamanWalletClient.getInstance();
