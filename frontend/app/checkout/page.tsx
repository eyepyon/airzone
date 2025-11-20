'use client';

import Image from 'next/image';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Layout from '@/components/layout/Layout';
import { useCartStore } from '@/stores/cart-store';
import { useAuthStore } from '@/stores/auth-store';
import CheckoutForm from '@/components/shop/CheckoutForm';
import XRPLPaymentForm from '@/components/shop/XRPLPaymentForm';
import PaymentMethodSelector, { PaymentMethod } from '@/components/shop/PaymentMethodSelector';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Loading from '@/components/ui/Loading';
import { createOrder } from '@/lib/api/orders';
import type { Order } from '@/types';

export default function CheckoutPage() {
  const router = useRouter();
  const { items, total, clearCart } = useCartStore();
  const { user, isAuthenticated } = useAuthStore();

  const [order, setOrder] = useState<Order | null>(null);
  const [isCreatingOrder, setIsCreatingOrder] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [nftCheckPassed, setNftCheckPassed] = useState(false);
  const [isCheckingNFTs, setIsCheckingNFTs] = useState(true);
  const [paymentMethod, setPaymentMethod] = useState<PaymentMethod>('stripe');

  // Redirect if not authenticated
  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login?redirect=/checkout');
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated]);

  // Redirect if cart is empty
  useEffect(() => {
    if (items.length === 0 && !order) {
      router.push('/shop');
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [items, order]);

  // Check NFT requirements
  useEffect(() => {
    const checkNFTRequirements = async () => {
      if (!user) return;

      setIsCheckingNFTs(true);
      setError(null);
      
      try {
        // まず、商品にNFT要件があるかチェック
        const productsWithNFTRequirement = items.filter(
          (item) => item.product.required_nft_id
        );

        if (productsWithNFTRequirement.length === 0) {
          // NFT要件がない商品のみの場合
          setNftCheckPassed(true);
          setIsCheckingNFTs(false);
          return;
        }

        // バックエンドAPIでNFT保有を確認
        const token = localStorage.getItem('access_token');
        if (!token) {
          setError('認証トークンがありません。再度ログインしてください。');
          setNftCheckPassed(false);
          setIsCheckingNFTs(false);
          return;
        }

        // 商品IDのリストを作成
        const productIds = items.map((item) => item.product.id);

        // バックエンドAPIを呼び出してNFT保有を確認
        const response = await fetch('/api/v1/orders/validate-nft-requirements', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({
            product_ids: productIds,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'NFT確認に失敗しました');
        }

        const data = await response.json();
        
        if (data.data.valid) {
          setNftCheckPassed(true);
        } else {
          setError(
            data.data.message || 
            'カート内の一部の商品に必要なNFTを保有していません。NFTを取得してから再度お試しください。'
          );
          setNftCheckPassed(false);
        }
      } catch (err) {
        console.error('NFT check failed:', err);
        setError(
          err instanceof Error 
            ? err.message 
            : 'NFTの確認中にエラーが発生しました'
        );
        setNftCheckPassed(false);
      } finally {
        setIsCheckingNFTs(false);
      }
    };

    if (user && items.length > 0) {
      checkNFTRequirements();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, items.length]);

  // Create order
  const handleCreateOrder = async () => {
    if (!nftCheckPassed) return;

    setIsCreatingOrder(true);
    setError(null);

    try {
      const orderData = {
        items: items.map((item) => ({
          product_id: item.product.id,
          quantity: item.quantity,
        })),
      };

      const createdOrder = await createOrder(orderData);
      setOrder(createdOrder);
    } catch (err) {
      const errorMsg =
        err instanceof Error ? err.message : '注文の作成に失敗しました';
      setError(errorMsg);
    } finally {
      setIsCreatingOrder(false);
    }
  };

  const handlePaymentSuccess = (orderId: string) => {
    // Clear cart after successful payment
    clearCart();
    // Redirect to order confirmation page
    router.push(`/orders/${orderId}?payment=success`);
  };

  const handlePaymentError = (error: Error) => {
    setError(error.message);
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ja-JP', {
      style: 'currency',
      currency: 'JPY',
    }).format(price);
  };

  if (!isAuthenticated || items.length === 0) {
    return (
      <Layout>
        <div className="flex justify-center items-center min-h-screen">
          <Loading size="lg" />
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <h1 className="text-3xl font-bold mb-8">チェックアウト</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Order Summary */}
        <div className="lg:col-span-1">
          <Card className="p-6 sticky top-4">
            <h2 className="text-xl font-semibold mb-4">注文内容</h2>

            <div className="space-y-4 mb-6">
              {items.map((item) => (
                <div key={item.product.id} className="flex gap-3">
                  <div className="flex-shrink-0 relative w-16 h-16">
                    {item.product.image_url ? (
                      <Image
                        src={item.product.image_url}
                        alt={item.product.name}
                        fill
                        className="object-cover rounded"
                      />
                    ) : (
                      <div className="w-16 h-16 bg-gray-200 rounded flex items-center justify-center">
                        <svg
                          className="w-8 h-8 text-gray-400"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                          />
                        </svg>
                      </div>
                    )}
                  </div>
                  <div className="flex-grow">
                    <p className="font-medium text-sm">{item.product.name}</p>
                    <p className="text-xs text-gray-500">
                      数量: {item.quantity}
                    </p>
                    <p className="text-sm font-semibold text-blue-600">
                      {formatPrice(item.product.price * item.quantity)}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            <div className="border-t pt-4 space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">小計</span>
                <span className="font-medium">{formatPrice(total)}</span>
              </div>
              <div className="flex justify-between text-lg font-bold">
                <span>合計</span>
                <span className="text-blue-600">{formatPrice(total)}</span>
              </div>
            </div>
          </Card>
        </div>

        {/* Payment Form */}
        <div className="lg:col-span-2">
          <Card className="p-6">
            {isCheckingNFTs ? (
              <div className="flex flex-col items-center justify-center py-12">
                <Loading size="lg" />
                <p className="mt-4 text-gray-600">NFT保有状況を確認中...</p>
              </div>
            ) : error && !order ? (
              <div className="space-y-6">
                <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                  <div className="flex items-start">
                    <svg
                      className="w-6 h-6 text-red-500 mt-0.5 mr-3 flex-shrink-0"
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
                      <h3 className="text-lg font-medium text-red-800">
                        エラー
                      </h3>
                      <p className="text-sm text-red-700 mt-2">{error}</p>
                    </div>
                  </div>
                </div>
                <div className="flex gap-4">
                  <Button
                    onClick={() => router.push('/nfts')}
                    variant="primary"
                  >
                    NFTを確認
                  </Button>
                  <Button
                    onClick={() => router.push('/shop')}
                    variant="secondary"
                  >
                    ショップに戻る
                  </Button>
                </div>
              </div>
            ) : !order ? (
              <div className="space-y-6">
                <div>
                  <h2 className="text-xl font-semibold mb-2">
                    注文を確定してください
                  </h2>
                  <p className="text-gray-600 text-sm">
                    注文を確定すると、決済画面に進みます。
                  </p>
                </div>

                {nftCheckPassed && (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div className="flex items-center">
                      <svg
                        className="w-5 h-5 text-green-500 mr-2"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                          clipRule="evenodd"
                        />
                      </svg>
                      <span className="text-sm text-green-800 font-medium">
                        購入可能
                      </span>
                    </div>
                  </div>
                )}

                <Button
                  onClick={handleCreateOrder}
                  variant="primary"
                  size="lg"
                  className="w-full"
                  disabled={isCreatingOrder || !nftCheckPassed}
                >
                  {isCreatingOrder ? (
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
                      注文を作成中...
                    </span>
                  ) : (
                    '注文を確定する'
                  )}
                </Button>

                <Button
                  onClick={() => router.push('/shop')}
                  variant="secondary"
                  size="lg"
                  className="w-full"
                >
                  キャンセル
                </Button>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Payment Method Selector */}
                <PaymentMethodSelector
                  onSelect={setPaymentMethod}
                  selectedMethod={paymentMethod}
                />

                {/* Payment Form */}
                {paymentMethod === 'stripe' ? (
                  <CheckoutForm
                    orderId={order.id}
                    amount={order.total_amount}
                    onSuccess={handlePaymentSuccess}
                    onError={handlePaymentError}
                  />
                ) : (
                  <XRPLPaymentForm
                    orderId={order.id}
                    amount={order.total_amount}
                    onSuccess={handlePaymentSuccess}
                    onError={handlePaymentError}
                  />
                )}
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
    </Layout>
  );
}
