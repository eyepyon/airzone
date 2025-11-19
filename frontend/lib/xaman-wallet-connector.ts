/**
 * Xaman Wallet Connector
 * ブラウザ拡張機能やモバイルアプリと連携してアドレスを自動取得
 */

export interface WalletConnection {
  address: string;
  publicKey?: string;
  network: 'mainnet' | 'testnet';
}

export class XamanWalletConnector {
  private static instance: XamanWalletConnector;
  private connection: WalletConnection | null = null;

  private constructor() {
    // LocalStorageから状態を復元
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('xaman_wallet_connection');
      if (saved) {
        try {
          this.connection = JSON.parse(saved);
        } catch (e) {
          console.error('Failed to restore connection:', e);
        }
      }
    }
  }

  static getInstance(): XamanWalletConnector {
    if (!XamanWalletConnector.instance) {
      XamanWalletConnector.instance = new XamanWalletConnector();
    }
    return XamanWalletConnector.instance;
  }

  /**
   * Xaman Walletに接続（自動アドレス取得）
   */
  async connect(): Promise<WalletConnection> {
    try {
      // 方法1: Xaman Browser Extension (存在する場合)
      if (this.hasXamanExtension()) {
        return await this.connectViaExtension();
      }

      // 方法2: WalletConnect経由
      return await this.connectViaWalletConnect();
    } catch (error) {
      console.error('Failed to connect to Xaman Wallet:', error);
      throw error;
    }
  }

  /**
   * Xaman Browser Extensionが利用可能か確認
   */
  private hasXamanExtension(): boolean {
    return typeof window !== 'undefined' && !!(window as unknown as Record<string, unknown>).xaman;
  }

  /**
   * Xaman Browser Extension経由で接続
   */
  private async connectViaExtension(): Promise<WalletConnection> {
    try {
      const xaman = (window as unknown as Record<string, unknown>).xaman as {
        request: (params: { method: string }) => Promise<string[] | string>;
      };
      
      // アカウント接続をリクエスト
      const accounts = await xaman.request({
        method: 'xrpl_requestAccounts',
      });

      if (!accounts || (Array.isArray(accounts) && accounts.length === 0)) {
        throw new Error('アカウントが見つかりませんでした');
      }

      const address = Array.isArray(accounts) ? accounts[0] : accounts;
      
      // ネットワーク情報を取得
      const networkResult = await xaman.request({
        method: 'xrpl_getNetwork',
      });
      
      const network = Array.isArray(networkResult) ? networkResult[0] : networkResult;

      this.connection = {
        address,
        network: network === 'mainnet' ? 'mainnet' : 'testnet',
      };

      await this.saveConnection();
      await this.registerAddress(address);

      return this.connection;
    } catch (error) {
      console.error('Extension connection failed:', error);
      throw new Error('Xaman拡張機能との接続に失敗しました');
    }
  }

  /**
   * WalletConnect経由で接続
   */
  private async connectViaWalletConnect(): Promise<WalletConnection> {
    try {
      // バックエンドでWalletConnectセッションを作成
      const response = await fetch('/api/v1/wallet/walletconnect/session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      if (!response.ok) {
        throw new Error('WalletConnectセッションの作成に失敗しました');
      }

      const data = await response.json();
      const { uri, qrCode } = data.data;

      // QRコードを表示してユーザーにスキャンを促す
      return await this.showWalletConnectQR(uri, qrCode);
    } catch (error) {
      console.error('WalletConnect connection failed:', error);
      throw new Error('WalletConnectとの接続に失敗しました');
    }
  }

  /**
   * WalletConnect QRコードを表示
   */
  private async showWalletConnectQR(uri: string, qrCode: string): Promise<WalletConnection> {
    return new Promise((resolve, reject) => {
      // モーダルを作成
      const modal = document.createElement('div');
      modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
      `;

      const content = document.createElement('div');
      content.style.cssText = `
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        max-width: 400px;
        text-align: center;
      `;

      content.innerHTML = `
        <h2 style="margin-bottom: 1rem; font-size: 1.5rem; font-weight: bold;">
          Xaman Walletで接続
        </h2>
        <p style="margin-bottom: 1rem; color: #666;">
          XamanアプリでこのQRコードをスキャンしてください
        </p>
        <img src="${qrCode}" alt="QR Code" style="width: 250px; height: 250px; margin: 0 auto;" />
        <p style="margin-top: 1rem; font-size: 0.875rem; color: #999;">
          接続を待っています...
        </p>
        <button id="cancel-btn" style="
          margin-top: 1rem;
          padding: 0.5rem 1rem;
          background: #e5e7eb;
          border: none;
          border-radius: 0.5rem;
          cursor: pointer;
        ">
          キャンセル
        </button>
      `;

      modal.appendChild(content);
      document.body.appendChild(modal);

      // キャンセルボタン
      const cancelBtn = content.querySelector('#cancel-btn');
      cancelBtn?.addEventListener('click', () => {
        document.body.removeChild(modal);
        reject(new Error('ユーザーがキャンセルしました'));
      });

      // WebSocketで接続を待機
      this.waitForWalletConnectConnection(uri)
        .then((connection) => {
          document.body.removeChild(modal);
          resolve(connection);
        })
        .catch((error) => {
          document.body.removeChild(modal);
          reject(error);
        });
    });
  }

  /**
   * WalletConnect接続を待機
   */
  private async waitForWalletConnectConnection(_uri: string): Promise<WalletConnection> {
    // WebSocketまたはポーリングで接続を待機
    return new Promise((resolve, reject) => {
      const checkInterval = setInterval(async () => {
        try {
          const response = await fetch('/api/v1/wallet/walletconnect/status', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
          });

          if (response.ok) {
            const data = await response.json();
            if (data.data.connected && data.data.address) {
              clearInterval(checkInterval);
              
              this.connection = {
                address: data.data.address,
                network: data.data.network || 'testnet',
              };

              await this.saveConnection();
              await this.registerAddress(data.data.address);

              resolve(this.connection);
            }
          }
        } catch (error) {
          console.error('Status check failed:', error);
        }
      }, 2000); // 2秒ごとにチェック

      // タイムアウト（5分）
      setTimeout(() => {
        clearInterval(checkInterval);
        reject(new Error('接続がタイムアウトしました'));
      }, 5 * 60 * 1000);
    });
  }

  /**
   * バックエンドにアドレスを登録
   */
  private async registerAddress(address: string): Promise<void> {
    try {
      await fetch('/api/v1/wallet/connect', {
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
    } catch (error) {
      console.error('Failed to register address:', error);
    }
  }

  /**
   * 接続を保存
   */
  private async saveConnection(): Promise<void> {
    if (typeof window !== 'undefined' && this.connection) {
      localStorage.setItem('xaman_wallet_connection', JSON.stringify(this.connection));
    }
  }

  /**
   * 切断
   */
  async disconnect(): Promise<void> {
    try {
      await fetch('/api/v1/wallet/disconnect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      this.connection = null;
      if (typeof window !== 'undefined') {
        localStorage.removeItem('xaman_wallet_connection');
      }
    } catch (error) {
      console.error('Failed to disconnect:', error);
      throw error;
    }
  }

  /**
   * 現在の接続を取得
   */
  getConnection(): WalletConnection | null {
    return this.connection;
  }

  /**
   * 接続されているか確認
   */
  isConnected(): boolean {
    return this.connection !== null && this.connection.address !== '';
  }

  /**
   * アドレスを取得
   */
  getAddress(): string | null {
    return this.connection?.address || null;
  }
}

export const xamanConnector = XamanWalletConnector.getInstance();
