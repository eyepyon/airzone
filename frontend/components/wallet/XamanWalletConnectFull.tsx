'use client';

import { useState, useEffect } from 'react';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';

interface XamanWalletConnectFullProps {
  onConnect?: (address: string) => void;
  onDisconnect?: () => void;
}

export default function XamanWalletConnectFull({
  onConnect,
  onDisconnect,
}: XamanWalletConnectFullProps) {
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [connected, setConnected] = useState(false);
  const [address, setAddress] = useState<string | null>(null);
  const [qrCode, setQrCode] = useState<string | null>(null);
  const [deepLink, setDeepLink] = useState<string | null>(null);
  const [showQR, setShowQR] = useState(false);

  useEffect(() => {
    // LocalStorageから状態を復元
    const savedAddress = localStorage.getItem('xaman_wallet_address');
    if (savedAddress) {
      setConnected(true);
      setAddress(savedAddress);
    }
  }, []);

  const handleConnect = async () => {
    setIsConnecting(true);
    setError(null);
    setShowQR(false);

    try {
      // バックエンドでXamanサインインペイロードを作成
      const response = await fetch('/api/v1/wallet/xaman/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          network: process.env.NEXT_PUBLIC_XRPL_NETWORK || 'testnet',
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'サインインペイロードの作成に失敗しました');
      }

      const data = await response.json();
      const payload = data.data;

      // QRコードとディープリンクを表示
      setQrCode(payload.qr_code);
      setDeepLink(payload.deep_link);
      setShowQR(true);

      // WebSocketで署名を待機
      await waitForSignature(payload.uuid);

    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : '接続に失敗しました';
      setError(errorMsg);
      setShowQR(false);
    } finally {
      setIsConnecting(false);
    }
  };

  const waitForSignature = (uuid: string): Promise<void> => {
    return new Promise((resolve, reject) => {
      let checkCount = 0;
      const maxChecks = 60; // 5分間（5秒 × 60）

      const checkInterval = setInterval(async () => {
        checkCount++;

        try {
          // バックエンドでペイロードステータスを確認
          const response = await fetch(`/api/v1/wallet/xaman/status/${uuid}`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
          });

          if (response.ok) {
            const data = await response.json();
            const status = data.data;

            if (status.signed === true && status.account) {
              // 署名完了 - アドレスを取得
              clearInterval(checkInterval);
              
              // バックエンドにアドレスを登録
              await registerAddress(status.account);

              // 接続成功
              setConnected(true);
              setAddress(status.account);
              setShowQR(false);

              // LocalStorageに保存
              localStorage.setItem('xaman_wallet_address', status.account);

              alert(
                '✓ Xaman Walletの接続に成功しました！\n\n' +
                `アドレス: ${status.account.slice(0, 10)}...${status.account.slice(-6)}\n\n` +
                'これからNFTはこのウォレットに送信されます。'
              );

              if (onConnect) {
                onConnect(status.account);
              }

              // ページをリロード
              setTimeout(() => window.location.reload(), 1000);
              resolve();
            } else if (status.signed === false) {
              // 署名拒否
              clearInterval(checkInterval);
              reject(new Error('ユーザーが署名を拒否しました'));
            }
          }

          // タイムアウトチェック
          if (checkCount >= maxChecks) {
            clearInterval(checkInterval);
            reject(new Error('署名がタイムアウトしました'));
          }
        } catch (error) {
          console.error('Status check error:', error);
        }
      }, 5000); // 5秒ごとにチェック
    });
  };

  const registerAddress = async (walletAddress: string): Promise<void> => {
    try {
      await fetch('/api/v1/wallet/connect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          address: walletAddress,
          wallet_type: 'xaman',
        }),
      });
    } catch (error) {
      console.error('Failed to register address:', error);
    }
  };

  const handleOpenXaman = () => {
    if (deepLink) {
      window.open(deepLink, '_blank');
    }
  };

  const handleDisconnect = async () => {
    if (!confirm('Xaman Walletの接続を解除しますか？\n\n解除後は自動ウォレットに戻ります。')) {
      return;
    }

    try {
      await fetch('/api/v1/wallet/disconnect', {
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

      setTimeout(() => window.location.reload(), 500);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : '切断に失敗しました';
      setError(errorMsg);
      alert('✗ 切断に失敗しました\n\n' + errorMsg);
    }
  };

  if (connected && address) {
    return (
      <Card className="p-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">
              ✓ Xaman Wallet 接続済み
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

          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <p className="text-xs text-green-700">
              ✓ NFTはこのXaman Walletアドレスに送信されます
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

  if (showQR && qrCode) {
    return (
      <Card className="p-6">
        <div className="space-y-4">
          <div className="text-center">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Xamanアプリで署名
            </h3>
            <p className="text-sm text-gray-600">
              QRコードをスキャンするか、ボタンをクリックしてください
            </p>
          </div>

          {/* QR Code */}
          <div className="bg-white border-2 border-gray-200 rounded-lg p-4">
            <img src={qrCode} alt="QR Code" className="w-64 h-64 mx-auto" />
          </div>

          {/* Open Xaman Button */}
          <Button
            onClick={handleOpenXaman}
            variant="primary"
            size="lg"
            className="w-full"
          >
            Xamanアプリで開く
          </Button>

          {/* Waiting Status */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600 mr-3"></div>
              <div>
                <h4 className="text-sm font-semibold text-blue-900">
                  署名を待っています...
                </h4>
                <p className="text-xs text-blue-700 mt-1">
                  Xamanアプリで署名を承認してください
                </p>
              </div>
            </div>
          </div>

          {/* Cancel Button */}
          <Button
            onClick={() => {
              setShowQR(false);
              setIsConnecting(false);
            }}
            variant="secondary"
            size="sm"
            className="w-full"
          >
            キャンセル
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
          {isConnecting ? '接続中...' : 'Xaman Walletに接続'}
        </Button>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="text-sm font-semibold text-blue-900 mb-2">
            接続方法
          </h4>
          <ul className="text-xs text-blue-700 space-y-1">
            <li>• QRコードが表示されます</li>
            <li>• Xamanアプリでスキャン</li>
            <li>• 署名を承認</li>
            <li>• アドレスが自動的に取得されます</li>
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
