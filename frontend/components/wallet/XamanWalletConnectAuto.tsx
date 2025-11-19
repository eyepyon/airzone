'use client';

import { useState, useEffect } from 'react';
import { xamanConnector, WalletConnection } from '@/lib/xaman-wallet-connector';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';

interface XamanWalletConnectAutoProps {
  onConnect?: (address: string) => void;
  onDisconnect?: () => void;
}

export default function XamanWalletConnectAuto({
  onConnect,
  onDisconnect,
}: XamanWalletConnectAutoProps) {
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [connection, setConnection] = useState<WalletConnection | null>(null);

  useEffect(() => {
    // 初期状態を取得
    const currentConnection = xamanConnector.getConnection();
    setConnection(currentConnection);
  }, []);

  const handleConnect = async () => {
    setIsConnecting(true);
    setError(null);

    try {
      const newConnection = await xamanConnector.connect();
      setConnection(newConnection);

      if (onConnect) {
        onConnect(newConnection.address);
      }

      // 成功メッセージ
      alert(
        '✓ Xaman Walletの接続に成功しました！\n\n' +
        `アドレス: ${newConnection.address.slice(0, 10)}...${newConnection.address.slice(-6)}\n\n` +
        'これからNFTはこのウォレットに送信されます。'
      );

      // ページをリロード
      setTimeout(() => window.location.reload(), 1000);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : '接続に失敗しました';
      setError(errorMsg);
      console.error('Connection error:', err);
    } finally {
      setIsConnecting(false);
    }
  };

  const handleDisconnect = async () => {
    if (!confirm('Xaman Walletの接続を解除しますか？\n\n解除後は自動ウォレットに戻ります。')) {
      return;
    }

    try {
      await xamanConnector.disconnect();
      setConnection(null);

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

  if (connection && connection.address) {
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
              {connection.address}
            </p>
            <p className="text-xs text-gray-500 mt-2">
              ネットワーク: {connection.network === 'mainnet' ? 'Mainnet' : 'Testnet'}
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
            ウォレットに接続すると、アドレスが自動的に取得されます
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-start">
              <svg className="w-5 h-5 text-red-500 mt-0.5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <div>
                <h4 className="text-sm font-medium text-red-800">接続エラー</h4>
                <p className="text-sm text-red-700 mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        <Button
          onClick={handleConnect}
          variant="primary"
          size="lg"
          className="w-full"
          disabled={isConnecting}
        >
          {isConnecting ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              接続中...
            </span>
          ) : (
            'Xaman Walletに接続'
          )}
        </Button>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="text-sm font-semibold text-blue-900 mb-2">
            接続方法
          </h4>
          <ul className="text-xs text-blue-700 space-y-1">
            <li>• ブラウザ拡張機能がある場合は自動的に接続</li>
            <li>• モバイルの場合はQRコードをスキャン</li>
            <li>• アドレスは自動的に取得されます</li>
          </ul>
        </div>

        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <p className="text-xs text-gray-600">
            💡 Xaman Walletアプリをお持ちでない場合は、
            <a href="https://xaman.app/" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800 underline font-medium">
              こちら
            </a>
            からダウンロードしてください。
          </p>
        </div>
      </div>
    </Card>
  );
}
