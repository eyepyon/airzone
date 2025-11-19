'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/stores/auth-store';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';

interface XRPLPaymentFormProps {
  orderId: string;
  amount: number;
  onSuccess?: (orderId: string) => void;
  onError?: (error: Error) => void;
}

export default function XRPLPaymentForm({
  orderId,
  amount,
  onSuccess,
  onError,
}: XRPLPaymentFormProps) {
  const router = useRouter();
  const { wallet } = useAuthStore();
  const [isProcessing, setIsProcessing] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // XRP/JPY レート（実際にはAPIから取得すべき）
  const XRP_JPY_RATE = 150; // 1 XRP = 150 JPY（仮）
  const amountXRP = (amount / XRP_JPY_RATE).toFixed(6);

  const handlePayment = async () => {
    if (!wallet) {
      setErrorMessage('ウォレットが見つかりません');
      return;
    }

    setIsProcessing(true);
    setErrorMessage(null);

    try {
      // XRPLでの支払い処理
      const response = await fetch('/api/v1/payments/xrpl', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          order_id: orderId,
          wallet_address: wallet.address,
          amount_xrp: parseFloat(amountXRP),
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || '支払い処理に失敗しました');
      }

      const data = await response.json();

      // 支払い成功
      if (onSuccess) {
        onSuccess(orderId);
      }
      router.push(`/orders/${orderId}?payment=success`);
    } catch (err) {
      const errorMsg =
        err instanceof Error ? err.message : '予期しないエラーが発生しました';
      setErrorMessage(errorMsg);
      if (onError) {
        onError(err instanceof Error ? err : new Error(errorMsg));
      }
    } finally {
      setIsProcessing(false);
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
            レート: 1 XRP = ¥{XRP_JPY_RATE}
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

      {/* Payment Button */}
      <Button
        onClick={handlePayment}
        variant="primary"
        size="lg"
        className="w-full bg-purple-600 hover:bg-purple-700"
        disabled={isProcessing}
      >
        {isProcessing ? (
          <span className="flex items-center justify-center">
            <svg
              className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            処理中...
          </span>
        ) : (
          `${amountXRP} XRP で支払う`
        )}
      </Button>

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
              トランザクションはXRPL上で処理され、ブロックチェーンに記録されます。
              支払い完了後、自動的にNFTがミントされます。
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
