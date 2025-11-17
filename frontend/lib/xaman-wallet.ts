/**
 * Xaman Wallet (旧Xumm) 統合 - 簡易実装版
 * XRPLウォレット接続（ディープリンク方式）
 * 
 * この実装は、Xaman Walletアプリへのディープリンクを使用した
 * シンプルな接続方式です。完全なSDK統合よりも実装が簡単です。
 */

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
   * Xaman Walletに接続（簡易版）
   * 
   * ユーザーにウォレットアドレスの入力を求める方式
   * 完全なSDK統合よりもシンプルで実装が容易
   */
  async connect(): Promise<XamanWalletState> {
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
      const response = await fetch('/api/v1/wallet/connect', {
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
        publicKey: null, // 簡易版では公開鍵は不要
      };

      // ローカルストレージに保存
      this.saveState();

      alert(
        '✓ Xaman Walletの接続に成功しました！\n\n' +
        `アドレス: ${address.slice(0, 10)}...${address.slice(-6)}\n\n` +
        'これからNFTはこのウォレットに送信されます。'
      );

      return this.state;
    } catch (error) {
      console.error('Failed to connect to Xaman Wallet:', error);
      alert(
        '✗ Xaman Walletの接続に失敗しました\n\n' +
        (error instanceof Error ? error.message : '不明なエラー')
      );
      throw error;
    }
  }

  /**
   * XRPLアドレスの形式を検証
   */
  private validateXRPLAddress(address: string): boolean {
    // XRPLアドレスは"r"で始まり、25-35文字
    if (!address.startsWith('r')) {
      return false;
    }
    if (address.length < 25 || address.length > 35) {
      return false;
    }
    // 英数字のみ
    if (!/^[a-zA-Z0-9]+$/.test(address)) {
      return false;
    }
    return true;
  }

  /**
   * Xaman Walletから切断
   */
  disconnect(): void {
    if (confirm('Xaman Walletの接続を解除しますか？\n\n解除後は自動ウォレットに戻ります。')) {
      this.state = {
        connected: false,
        address: null,
        publicKey: null,
      };

      if (typeof window !== 'undefined') {
        localStorage.removeItem('xaman_wallet_state');
      }

      alert('✓ Xaman Walletの接続を解除しました');
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
   * トランザクションに署名（簡易版では未実装）
   */
  async signTransaction(transaction: any): Promise<string> {
    throw new Error(
      'トランザクション署名は現在サポートされていません。\n' +
      'NFTの受け取りは自動的に行われます。'
    );
  }
}

export const xamanWallet = XamanWalletClient.getInstance();
