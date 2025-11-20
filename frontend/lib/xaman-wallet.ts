/**
 * Xaman Wallet (旧XUMM) 統合
 * XRPLウォレット接続とトランザクション署名
 * 
 * Xaman Wallet連携方法：
 * 1. QRコード方式 - モバイルアプリでスキャン
 * 2. ディープリンク方式 - モバイルブラウザから直接起動
 * 3. WebSocket方式 - リアルタイム通信
 */

export interface XamanWalletState {
  connected: boolean;
  address: string | null;
  publicKey: string | null;
  network: 'mainnet' | 'testnet';
}

export interface XamanSignRequest {
  uuid: string;
  qrUrl: string;
  deepLink: string;
  websocket: string;
}

export class XamanWalletClient {
  private static instance: XamanWalletClient;
  private state: XamanWalletState = {
    connected: false,
    address: null,
    publicKey: null,
    network: 'testnet',
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
   * バックエンドでサインリクエストを作成し、ユーザーがXamanアプリで承認
   */
  async connect(): Promise<XamanWalletState> {
    try {
      // バックエンドにサインリクエストを作成
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
      const response = await fetch(`${apiUrl}/api/v1/wallet/xaman/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          network: this.state.network,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'サインリクエストの作成に失敗しました');
      }

      const data = await response.json();
      const signRequest: XamanSignRequest = data.data;

      // QRコードとディープリンクを表示
      return await this.waitForSignature(signRequest);
    } catch (error) {
      console.error('Failed to connect to Xaman Wallet:', error);
      throw error;
    }
  }

  /**
   * 手動でウォレットアドレスを接続（簡易版）
   */
  async connectManual(): Promise<XamanWalletState> {
    try {
      // ユーザーにウォレットアドレスの入力を求める
      const address = prompt(
        'Xaman WalletのXRPLアドレスを入力してください\n' +
        '（rから始まる25-35文字のアドレス）\n\n' +
        'アドレスの確認方法：\n' +
        '1. Xaman Walletアプリを開く\n' +
        '2. アカウント名をタップ\n' +
        '3. "r..."で始まるアドレスをコピー'
      );

      if (!address) {
        throw new Error('アドレスが入力されませんでした');
      }

      // XRPLアドレスの形式を検証
      if (!this.validateXRPLAddress(address)) {
        throw new Error(
          '無効なXRPLアドレスです。\n' +
          'アドレスは"r"で始まり、25-35文字である必要があります。'
        );
      }

      // バックエンドにアドレスを登録
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
      const response = await fetch(`${apiUrl}/api/v1/wallet/connect`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          address: address,
          wallet_type: 'xaman',
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'ウォレット接続に失敗しました');
      }

      // 接続成功
      this.state = {
        connected: true,
        address: address,
        publicKey: null,
        network: this.state.network,
      };

      // ローカルストレージに保存
      this.saveState();

      return this.state;
    } catch (error) {
      console.error('Failed to connect to Xaman Wallet:', error);
      throw error;
    }
  }

  /**
   * 署名を待機
   */
  private async waitForSignature(signRequest: XamanSignRequest): Promise<XamanWalletState> {
    return new Promise((resolve, reject) => {
      // WebSocketで署名結果を待機
      const ws = new WebSocket(signRequest.websocket);
      let resolved = false;

      ws.onopen = () => {
        console.log('WebSocket connected, waiting for signature...');
      };

      ws.onmessage = async (event) => {
        try {
          const data = JSON.parse(event.data);
          
          if (data.signed === true) {
            // 署名成功 - アドレスを取得
            const address = data.account;
            const publicKey = data.account_info?.publicKey || null;

            // バックエンドにアドレスを登録
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
            await fetch(`${apiUrl}/api/v1/wallet/connect`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
              },
              body: JSON.stringify({
                address: address,
                wallet_type: 'xaman',
              }),
            });

            this.state = {
              connected: true,
              address: address,
              publicKey: publicKey,
              network: this.state.network,
            };

            this.saveState();
            ws.close();
            resolved = true;
            resolve(this.state);
          } else if (data.signed === false) {
            // 署名拒否
            ws.close();
            resolved = true;
            reject(new Error('ユーザーが署名を拒否しました'));
          }
        } catch (error) {
          console.error('Error processing WebSocket message:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        if (!resolved) {
          resolved = true;
          reject(new Error('WebSocket接続エラー'));
        }
      };

      ws.onclose = () => {
        if (!resolved) {
          resolved = true;
          reject(new Error('WebSocket接続が閉じられました'));
        }
      };

      // タイムアウト（5分）
      setTimeout(() => {
        if (!resolved) {
          ws.close();
          resolved = true;
          reject(new Error('署名のタイムアウト'));
        }
      }, 5 * 60 * 1000);
    });
  }

  /**
   * XRPLアドレスの形式を検証
   */
  private validateXRPLAddress(address: string): boolean {
    if (!address.startsWith('r')) {
      return false;
    }
    if (address.length < 25 || address.length > 35) {
      return false;
    }
    if (!/^[a-zA-Z0-9]+$/.test(address)) {
      return false;
    }
    return true;
  }

  /**
   * Xaman Walletから切断
   */
  async disconnect(): Promise<void> {
    try {
      // バックエンドに切断を通知
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
      await fetch(`${apiUrl}/api/v1/wallet/disconnect`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      this.state = {
        connected: false,
        address: null,
        publicKey: null,
        network: this.state.network,
      };

      if (typeof window !== 'undefined') {
        localStorage.removeItem('xaman_wallet_state');
      }
    } catch (error) {
      console.error('Failed to disconnect:', error);
      throw error;
    }
  }

  /**
   * 現在の接続状態を取得
   */
  getState(): XamanWalletState {
    return { ...this.state };
  }

  /**
   * 接続されているか確認
   */
  isConnected(): boolean {
    return this.state.connected && this.state.address !== null;
  }

  /**
   * ウォレットアドレスを取得
   */
  getAddress(): string | null {
    return this.state.address;
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
   * ネットワークを設定
   */
  setNetwork(network: 'mainnet' | 'testnet'): void {
    this.state.network = network;
    this.saveState();
  }

  /**
   * トランザクションに署名
   */
  async signTransaction(transaction: Record<string, unknown>): Promise<string> {
    if (!this.isConnected()) {
      throw new Error('ウォレットが接続されていません');
    }

    try {
      // バックエンドでサインリクエストを作成
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
      const response = await fetch(`${apiUrl}/api/v1/wallet/xaman/sign`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          transaction: transaction,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'サインリクエストの作成に失敗しました');
      }

      const data = await response.json();
      const signRequest: XamanSignRequest = data.data;

      // 署名を待機
      return await this.waitForTransactionSignature(signRequest);
    } catch (error) {
      console.error('Failed to sign transaction:', error);
      throw error;
    }
  }

  /**
   * トランザクション署名を待機
   */
  private async waitForTransactionSignature(signRequest: XamanSignRequest): Promise<string> {
    return new Promise((resolve, reject) => {
      const ws = new WebSocket(signRequest.websocket);
      let resolved = false;

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          if (data.signed === true) {
            const txHash = data.txid;
            ws.close();
            resolved = true;
            resolve(txHash);
          } else if (data.signed === false) {
            ws.close();
            resolved = true;
            reject(new Error('ユーザーが署名を拒否しました'));
          }
        } catch (error) {
          console.error('Error processing WebSocket message:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        if (!resolved) {
          resolved = true;
          reject(new Error('WebSocket接続エラー'));
        }
      };

      ws.onclose = () => {
        if (!resolved) {
          resolved = true;
          reject(new Error('WebSocket接続が閉じられました'));
        }
      };

      // タイムアウト（5分）
      setTimeout(() => {
        if (!resolved) {
          ws.close();
          resolved = true;
          reject(new Error('署名のタイムアウト'));
        }
      }, 5 * 60 * 1000);
    });
  }
}

export const xamanWallet = XamanWalletClient.getInstance();
