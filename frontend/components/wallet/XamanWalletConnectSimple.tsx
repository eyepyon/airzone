'use client';

import { useState } from 'react';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';

interface XamanWalletConnectSimpleProps {
  onConnect?: (address: string) => void;
  onDisconnect?: () => void;
}

export default function XamanWalletConnectSimple({
  onConnect,
  onDisconnect,
}: XamanWalletConnectSimpleProps) {
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [connected, setConnected] = useState(false);
  const [address, setAddress] = useState<string | null>(null);

  const handleConnect = async () => {
    setIsConnecting(true);
    setError(null);

    try {
      // ユーザーにウォレットアドレスの入力を求める
      const userAddress = prompt(
        'Xaman WalletのXRPLアドレスを入力してください\n\n' +
        'アドレスの確認方法：\n' +
        '1. Xaman Walletアプリを開く\n' +
        '2. アカウント名をタップ\n' +
        '3. "r"で始まるアドレスをコピー\n' +
        '4. ここにペースト'
      );

      if (!userAddress) {
        throw new Error('アドレスが入力されませんでした');
      }

      // XRPLアドレスの形式を検証
      if (!validateXRPLAddress(userAddress)) {
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
          address: userAddress,
          wallet_type: 'xaman',
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'ウォレット接続に失敗しました');
      }

      // 接続成功
      setConnected(true);
      setAddress(userAddress);

      // LocalStorageに保存
      localStorage.setItem('xaman_wallet_address', userAddress);

      alert(
        '✓ Xaman Walletの接続に成功しました！\n\n' +
        `アドレス: ${userAddress.slice(0, 10)}...${userAddress.slice(-6)}\n\n` +
        'これからNFTはこのウォレットに送信されます。'
      );

      if (onConnect) {
        onConnect(userAddress);
      }

      // ページをリロード
      setTimeout(() => window.location.reload(), 1000);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : '接続に失敗しました';
      setError(errorMsg);
      alert('✗ Xaman Walletの接続に失敗しました\n\n' + errorMsg);
    } finally {
      setIsConnecting(false);
    }
  };

  const handleDisconnect = async () => {
    if (!confirm('Xaman Walletの接続を解除しますか？\n\n解除後は自動ウォレットに戻ります。')) {
      return;
    }

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

      setConnected(false);
      setAddress(null);
      localStorage.removeItem('xaman_wallet_address');

      alert('✓ Xaman Walletの接続を解除しました');

      if (onDisconnect) {
        onDisconnect();
      }

      // ページをリロード
      setTimeout(() => window.location.reload(), 500);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : '切断に失敗しました';
      setError(errorMsg);
      alert('✗ 切断に失敗しました\n\n' + errorMsg);
    }
  };

  const validateXRPLAddress = (addr: string): boolean => {
    if (!addr.startsWith('r')) return false;
    if (addr.length < 25 || addr.length > 35) return false;
    if (!/^[a-zA-Z0-9]+$/.test(addr)) return false;
    return true;
  };

  // LocalStorageから状態を復元
  if (!connected && !address) {
    const savedAddress = localStorage.getItem('xaman_wallet_address');
    if (savedAddress) {
      setConnected(true);
      setAddress(savedAddress);
    }
  }

  if (connected && address) {
    return (
      <Card className="p-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">
              Xaman Wallet 接続済み
            </h3>
            <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-xs text-gray-500 mb-1">ウォレットアドレス</p>
            <p className="text-sm font-mono text-gray-900 break-all">
              {address}
            </p>
          </div>

          <Button
            onClick={handleDisconnect}
            variant="secondary"
            size="sm"
            className="w-full"
          >
            接続を解除
          </Button>
        </div>
      </Card>
    );
  }

  return (
    <Card className="p-6">
      <div className="space-y-4">
        <div className="text-center">
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Xaman Walletを接続
          </h3>
          <p className="text-sm text-gray-600">
            XRPLウォレットを接続して、NFTを受け取りましょう
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        <Button
          onClick={handleConnect}
          variant="primary"
          size="lg"
          className="w-full"
          disabled={isConnecting}
        >
          {isConnecting ? '接続中...' : 'Xaman Walletを接続'}
        </Button>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-xs text-blue-700">
            💡 Xaman Walletアプリをお持ちでない場合は、
            <a href="https://xaman.app/" target="_blank" rel="noopener noreferrer" className="underline font-medium">
              こちら
            </a>
            からダウンロードしてください。
          </p>
        </div>

        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <p className="text-xs text-gray-600">
            <strong>接続方法：</strong><br />
            1. Xaman Walletアプリを開く<br />
            2. アカウント名をタップ<br />
            3. &quot;r&quot;で始まるアドレスをコピー<br />
            4. 上のボタンをクリックして入力
          </p>
        </div>
      </div>
    </Card>
  );
}
