'use client';

import Image from 'next/image';
import { useState } from 'react';
import { xamanWallet } from '@/lib/xaman-wallet';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';

interface XamanWalletConnectProps {
  onConnect?: (address: string) => void;
  onDisconnect?: () => void;
}

export default function XamanWalletConnect({
  onConnect,
  onDisconnect,
}: XamanWalletConnectProps) {
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [walletState, setWalletState] = useState(xamanWallet.getState());
  const [showQR, setShowQR] = useState(false);
  const [qrUrl, setQrUrl] = useState<string | null>(null);
  const [deepLink, setDeepLink] = useState<string | null>(null);

  const handleConnect = async () => {
    setIsConnecting(true);
    setError(null);

    try {
      // バックエンドでサインリクエストを作成
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
        throw new Error(errorData.error || 'サインリクエストの作成に失敗しました');
      }

      const data = await response.json();
      const signRequest = data.data;

      // QRコードとディープリンクを表示
      setQrUrl(signRequest.qr_code);
      setDeepLink(signRequest.deep_link);
      setShowQR(true);

      // WebSocketで署名を待機
      await waitForSignature(signRequest.websocket);

      // 接続成功
      const newState = xamanWallet.getState();
      setWalletState(newState);
      setShowQR(false);

      if (onConnect && newState.address) {
        onConnect(newState.address);
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : '接続に失敗しました';
      setError(errorMsg);
      setShowQR(false);
    } finally {
      setIsConnecting(false);
    }
  };

  const handleManualConnect = async () => {
    setIsConnecting(true);
    setError(null);

    try {
      const state = await xamanWallet.connectManual();
      setWalletState(state);

      if (onConnect && state.address) {
        onConnect(state.address);
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : '接続に失敗しました';
      setError(errorMsg);
    } finally {
      setIsConnecting(false);
    }
  };

  const handleDisconnect = async () => {
    if (!confirm('Xaman Walletの接続を解除しますか？')) {
      return;
    }

    try {
      await xamanWallet.disconnect();
      setWalletState(xamanWallet.getState());

      if (onDisconnect) {
        onDisconnect();
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : '切断に失敗しました';
      setError(errorMsg);
    }
  };

  const waitForSignature = (websocketUrl: string): Promise<void> => {
    return new Promise((resolve, reject) => {
      const ws = new WebSocket(websocketUrl);
      let resolved = false;

      ws.onopen = () => {
        console.log('WebSocket connected, waiting for signature...');
      };

      ws.onmessage = async (event) => {
        try {
          const data = JSON.parse(event.data);
          
          if (data.signed === true) {
            // 署名成功
            const address = data.account;

            // バックエンドにアドレスを登録
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

            ws.close();
            resolved = true;
            resolve();
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
  };

  const handleOpenXaman = () => {
    if (deepLink) {
      window.open(deepLink, '_blank');
    }
  };

  if (walletState.connected && walletState.address) {
    return (
      <Card className="p-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">
              Xaman Wallet 接続済み
            </h3>
            <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-xs text-gray-500 mb-1">ウォレットアドレス</p>
            <p className="text-sm font-mono text-gray-900 break-all">
              {walletState.address}
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

        {showQR && qrUrl && (
          <div className="space-y-4">
            <div className="bg-white border-2 border-gray-200 rounded-lg p-4">
              <p className="text-sm text-gray-700 mb-3 text-center">
                Xamanアプリでスキャン
              </p>
              <div className="relative w-48 h-48 mx-auto">
                <Image src={qrUrl} alt="QR Code" fill className="object-contain" />
              </div>
            </div>

            <Button
              onClick={handleOpenXaman}
              variant="primary"
              size="lg"
              className="w-full"
            >
              Xamanアプリで開く
            </Button>

            <p className="text-xs text-gray-500 text-center">
              署名を待っています...
            </p>
          </div>
        )}

        {!showQR && (
          <div className="space-y-3">
            <Button
              onClick={handleConnect}
              variant="primary"
              size="lg"
              className="w-full"
              disabled={isConnecting}
            >
              {isConnecting ? '接続中...' : 'Xaman Walletで接続'}
            </Button>

            <Button
              onClick={handleManualConnect}
              variant="secondary"
              size="lg"
              className="w-full"
              disabled={isConnecting}
            >
              アドレスを手動入力
            </Button>
          </div>
        )}

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-xs text-blue-700">
            💡 Xaman Walletアプリをお持ちでない場合は、
            <a href="https://xaman.app/" target="_blank" rel="noopener noreferrer" className="underline font-medium">
              こちら
            </a>
            からダウンロードしてください。
          </p>
        </div>
      </div>
    </Card>
  );
}
