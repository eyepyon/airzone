/**
 * Xaman Wallet SDK統合
 * 最新のXaman API仕様に基づいた実装
 */

export interface XamanWalletState {
  connected: boolean;
  address: string | null;
  publicKey: string | null;
  network: 'mainnet' | 'testnet';
}

export interface XamanPayload {
  uuid: string;
  next: {
    always: string;
    no_push_msg_received?: string;
  };
  refs: {
    qr_png: string;
    qr_matrix: string;
    qr_uri_quality_opts: string[];
    websocket_status: string;
  };
  pushed: boolean;
}

export interface XamanPayloadResponse {
  meta: {
    exists: boolean;
    uuid: string;
    multisign: boolean;
    submit: boolean;
    destination: string;
    resolved_destination: string;
    resolved: boolean;
    signed: boolean;
    cancelled: boolean;
    expired: boolean;
    pushed: boolean;
    app_opened: boolean;
    return_url_app?: string;
    return_url_web?: string;
  };
  application: {
    name: string;
    description: string;
    disabled: number;
    uuidv4: string;
    icon_url: string;
    issued_user_token?: string;
  };
  payload: {
    tx_type: string;
    tx_destination: string;
    tx_destination_tag?: number;
    request_json: Record<string, unknown>;
    created_at: string;
    expires_at: string;
    expires_in_seconds: number;
  };
  response?: {
    hex: string;
    txid: string;
    resolved_at: string;
    dispatched_to: string;
    dispatched_nodetype: string;
    dispatched_result: string;
    multisign_account?: string;
    account: string;
  };
  custom_meta?: {
    identifier?: string;
    blob?: Record<string, unknown>;
    instruction?: string;
  };
}

export class XamanWalletSDK {
  private static instance: XamanWalletSDK;
  private state: XamanWalletState = {
    connected: false,
    address: null,
    publicKey: null,
    network: 'testnet',
  };
  private apiUrl = 'https://xumm.app/api/v1/platform';

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

  static getInstance(): XamanWalletSDK {
    if (!XamanWalletSDK.instance) {
      XamanWalletSDK.instance = new XamanWalletSDK();
    }
    return XamanWalletSDK.instance;
  }

  /**
   * Xaman Walletに接続（サインインペイロード）
   */
  async connect(): Promise<XamanWalletState> {
    try {
      // バックエンドでXamanペイロードを作成
      const response = await fetch('/api/v1/wallet/xaman/signin', {
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
        throw new Error(error.error || 'サインインペイロードの作成に失敗しました');
      }

      const data = await response.json();
      const payload: XamanPayload = data.data;

      // WebSocketでペイロードの結果を待機
      const result = await this.waitForPayload(payload.refs.websocket_status);

      if (result.response && result.response.account) {
        // 接続成功
        this.state = {
          connected: true,
          address: result.response.account,
          publicKey: null,
          network: this.state.network,
        };

        // バックエンドにアドレスを登録
        await this.registerAddress(result.response.account);

        this.saveState();
        return this.state;
      } else {
        throw new Error('署名が完了しませんでした');
      }
    } catch (error) {
      console.error('Failed to connect to Xaman Wallet:', error);
      throw error;
    }
  }

  /**
   * ペイロードの結果を待機
   */
  private async waitForPayload(websocketUrl: string): Promise<XamanPayloadResponse> {
    return new Promise((resolve, reject) => {
      const ws = new WebSocket(websocketUrl);
      let resolved = false;

      ws.onopen = () => {
        console.log('WebSocket connected, waiting for signature...');
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          if (data.signed === true) {
            // 署名完了
            ws.close();
            resolved = true;
            resolve(data as XamanPayloadResponse);
          } else if (data.signed === false || data.expired === true) {
            // 署名拒否または期限切れ
            ws.close();
            resolved = true;
            reject(new Error(data.expired ? 'ペイロードの有効期限が切れました' : 'ユーザーが署名を拒否しました'));
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
   * バックエンドにアドレスを登録
   */
  private async registerAddress(address: string): Promise<void> {
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
  }

  /**
   * Xaman Walletから切断
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
      // バックエンドでXamanペイロードを作成
      const response = await fetch('/api/v1/wallet/xaman/sign', {
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
        throw new Error(error.error || 'サインペイロードの作成に失敗しました');
      }

      const data = await response.json();
      const payload: XamanPayload = data.data;

      // WebSocketでペイロードの結果を待機
      const result = await this.waitForPayload(payload.refs.websocket_status);

      if (result.response && result.response.txid) {
        return result.response.txid;
      } else {
        throw new Error('トランザクションの署名に失敗しました');
      }
    } catch (error) {
      console.error('Failed to sign transaction:', error);
      throw error;
    }
  }
}

export const xamanWalletSDK = XamanWalletSDK.getInstance();
