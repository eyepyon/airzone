'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/stores/auth-store';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import { getXRPJPYRate, getWalletBalance } from '@/lib/xrpl-payment';

interface XRPLPaymentFormProps {
  orderId: string;
  amount: number;
  onSuccess?: (orderId: string) => void;
  onError?: (error: Error) => void;
}

type PaymentStatus = 'idle' | 'creating' | 'waiting' | 'processing' | 'completed' | 'failed';

export default function XRPLPaymentForm({
  orderId,
  amount,
  onSuccess,
  onError,
}: XRPLPaymentFormProps) {
  const router = useRouter();
  const { wallet } = useAuthStore();
  const [status, setStatus] = useState<PaymentStatus>('idle');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [xrpRate, setXrpRate] = useState(150);
  const [walletBalance, setWalletBalance] = useState<number | null>(null);

  const [pollingInterval, setPollingInterval] = useState<NodeJS.Timeout | null>(null);

  const amountXRP = (amount / xrpRate).toFixed(6);
  const SPONSOR_ADDRESS = process.env.NEXT_PUBLIC_XRPL_SPONSOR_ADDRESS || 'rN7n7otQDd6FczFgLdSqtcsAUxDkw6fzRH';

  // XRP/JPYレートとウォレット残高を取得
  useEffect(() => {
    const fetchData = async () => {
      try {
        const rate = await getXRPJPYRate();
        setXrpRate(rate);

        if (wallet?.address) {
          const balance = await getWalletBalance(wallet.address);
          setWalletBalance(balance);
        }
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    fetchData();
  }, [wallet]);

  // 支払いステータスをポーリング
  useEffect(() => {
    if (status === 'waiting' && !pollingInterval) {
      const interval = setInterval(async () => {
        try {
          // バックエンドで支払い確認
          const response = await fetch(`/api/v1/payments/xrpl/check/${orderId}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          });

          if (response.ok) {
            const data = await response.json();
            if (data.data.status === 'completed') {
              clearInterval(interval);
              setPollingInterval(null);
              setStatus('completed');
              if (onSuccess) {
                onSuccess(orderId);
              }
              setTimeout(() => {
                router.push(`/orders/${orderId}?payment=success`);
              }, 2000);
            }
          }
        } catch (error) {
          console.error('Failed to check payment status:', error);
        }
      }, 5000); // 5秒ごとにチェック

      setPollingInterval(interval);
    }

    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval);
      }
    };
  }, [status, pollingInterval, orderId, onSuccess, router]);

  const handleExecutePayment = async () => {
    setStatus('processing');
    setErrorMessage(null);

    try {
      // バックエンドで実際にXRPL決済を実行
      const response = await fetch('/api/v1/payments/xrpl/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          order_id: orderId,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || '決済の実行に失敗しました');
      }

      const data = await response.json();
      setStatus('completed');

      // 成功後の処理
      if (onSuccess) {
        onSuccess(orderId);
      }

      setTimeout(() => {
        router.push(`/orders/${orderId}?payment=success&tx=${data.data.transaction_hash}`);
      }, 2000);

    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : '予期しないエラーが発生しました';
      setErrorMessage(errorMsg);
      setStatus('failed');
      if (onError) {
        onError(err instanceof Error ? err : new Error(errorMsg));
      }
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ja-JP', {
      style: 'currency',
      currency: 'JPY',
    }).format(price);
  };

  if (!wallet) {
    return (
      <Card className="p-6">
        <div className="text-center py-8">
          <svg
            className="w-16 h-16 mx-auto text-gray-400 mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
            />
          </svg>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            ウォレットが見つかりません
          </h3>
          <p className="text-sm text-gray-600">
            XRP決済を利用するには、ウォレットが必要です。
          </p>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Payment Amount */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          支払い金額
        </h3>
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-gray-600">日本円</span>
            <span className="text-2xl font-bold text-gray-900">
              {formatPrice(amount)}
            </span>
          </div>
          <div className="flex justify-between items-center pt-3 border-t">
            <span className="text-gray-600">XRP換算</span>
            <span className="text-2xl font-bold text-purple-600">
              {amountXRP} XRP
            </span>
          </div>
          <p className="text-xs text-gray-500 text-right">
            レート: 1 XRP = ¥{xrpRate}
          </p>
        </div>
      </Card>

      {/* Wallet Info */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          支払い元ウォレット
        </h3>
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <p className="text-xs text-gray-500 mb-1">ウォレットアドレス</p>
              <p className="text-sm font-mono text-gray-900 break-all">
                {wallet.address}
              </p>
              {walletBalance !== null && (
                <p className="text-xs text-gray-600 mt-2">
                  残高: {walletBalance.toFixed(6)} XRP
                </p>
              )}
            </div>
            <div className="ml-4">
              <svg
                className="w-8 h-8 text-purple-600"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z" />
                <path
                  fillRule="evenodd"
                  d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
          </div>
        </div>
      </Card>

      {/* Transaction Details */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          トランザクション詳細
        </h3>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600">ネットワーク</span>
            <span className="font-medium text-gray-900">
              XRPL {process.env.NEXT_PUBLIC_XRPL_NETWORK || 'Testnet'}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">送金先</span>
            <span className="font-medium text-gray-900 font-mono text-xs">
              {SPONSOR_ADDRESS.substring(0, 10)}...{SPONSOR_ADDRESS.substring(SPONSOR_ADDRESS.length - 6)}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">手数料</span>
            <span className="font-medium text-gray-900">~0.00001 XRP</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">処理時間</span>
            <span className="font-medium text-gray-900">約3-5秒</span>
          </div>
        </div>
      </Card>

      {/* Error Message */}
      {errorMessage && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-start">
            <svg
              className="w-5 h-5 text-red-500 mt-0.5 mr-2 flex-shrink-0"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            </svg>
            <div>
              <h3 className="text-sm font-medium text-red-800">決済エラー</h3>
              <p className="text-sm text-red-700 mt-1">{errorMessage}</p>
            </div>
          </div>
        </div>
      )}

      {/* Payment Status & Actions */}
      {status === 'idle' && (
        <Button
          onClick={handleExecutePayment}
          variant="primary"
          size="lg"
          className="w-full bg-purple-600 hover:bg-purple-700"
        >
          {`${amountXRP} XRP で支払う`}
        </Button>
      )}

      {status === 'processing' && (
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mb-4"></div>
          <p className="text-gray-600">XRPLブロックチェーンで決済処理中...</p>
          <p className="text-sm text-gray-500 mt-2">トランザクションを送信しています</p>
        </div>
      )}

      {status === 'completed' && (
        <div className="text-center py-8">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-green-900 mb-2">
            支払い完了！
          </h3>
          <p className="text-sm text-green-700">
            XRPLブロックチェーンで決済が完了しました
          </p>
          <p className="text-xs text-gray-500 mt-2">
            注文詳細ページにリダイレクトしています...
          </p>
        </div>
      )}

      {status === 'failed' && (
        <div className="space-y-4">
          <Button
            onClick={handleExecutePayment}
            variant="primary"
            size="lg"
            className="w-full bg-purple-600 hover:bg-purple-700"
          >
            再試行
          </Button>
        </div>
      )}

      {/* Security Notice */}
      <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
        <div className="flex items-start">
          <svg
            className="w-5 h-5 text-purple-600 mt-0.5 mr-3 flex-shrink-0"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fillRule="evenodd"
              d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
              clipRule="evenodd"
            />
          </svg>
          <div>
            <h4 className="text-sm font-semibold text-purple-900">
              安全な決済
            </h4>
            <p className="text-xs text-purple-700 mt-1">
              トランザクションは実際のXRPLブロックチェーン上で処理され、
              ブロックチェーンに永続的に記録されます。
              支払い完了後、自動的にNFTがミントされます。
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
