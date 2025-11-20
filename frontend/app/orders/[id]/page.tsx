'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import Layout from '@/components/layout/Layout';
import { Card, Loading, Button } from '@/components/ui';
import { useAuthStore } from '@/stores';
import { getOrderById } from '@/lib/api';
import { mintNFTForOrder } from '@/lib/api/nfts';
import type { Order } from '@/types';

export default function OrderDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { isAuthenticated, wallet } = useAuthStore();
  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [nftMinting, setNftMinting] = useState(false);
  const [nftMinted, setNftMinted] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const fetchOrder = async () => {
      try {
        setLoading(true);
        const data = await getOrderById(params.id);
        setOrder(data);
      } catch (err) {
        console.error('Failed to fetch order:', err);
        
        // 401エラーの場合はログインページにリダイレクト
        if (err instanceof Error && err.message.includes('401')) {
          router.push(`/login?redirect=/orders/${params.id}`);
          return;
        }
        
        setError(err instanceof Error ? err.message : '注文の取得に失敗しました');
      } finally {
        setLoading(false);
      }
    };

    fetchOrder();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params.id, isAuthenticated]);

  // Auto-mint NFT after successful payment - NFTカテゴリの商品のみ
  useEffect(() => {
    const paymentSuccess = searchParams.get('payment') === 'success';
    
    // 注文にNFTカテゴリの商品が含まれているかチェック
    const hasNFTProduct = order?.items?.some(
      item => item.product?.category === 'nft' || item.product?.product_type === 'nft'
    );
    
    if (paymentSuccess && order && order.status === 'completed' && wallet && hasNFTProduct && !nftMinting && !nftMinted) {
      const autoMintNFT = async () => {
        try {
          setNftMinting(true);
          await mintNFTForOrder(order.id);
          setNftMinted(true);
        } catch (err) {
          console.error('NFT auto-mint failed:', err);
          // エラーは表示しない（バックグラウンドで処理）
        } finally {
          setNftMinting(false);
        }
      };

      autoMintNFT();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [order, wallet, searchParams]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'processing':
        return 'text-blue-600 bg-blue-50 border-blue-200';
      case 'pending':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'failed':
      case 'cancelled':
        return 'text-red-600 bg-red-50 border-red-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed':
        return '完了';
      case 'processing':
        return '処理中';
      case 'pending':
        return '保留中';
      case 'failed':
        return '失敗';
      case 'cancelled':
        return 'キャンセル';
      default:
        return status;
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <Loading size="lg" />
        </div>
      </Layout>
    );
  }

  if (error || !order) {
    return (
      <Layout>
        <div className="min-h-screen bg-gray-50 py-6 sm:py-8 lg:py-12">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-2xl mx-auto">
              <Card className="text-center py-12 sm:py-16">
                <div className="text-4xl sm:text-5xl mb-4">❌</div>
                <h2 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2">
                  注文が見つかりません
                </h2>
                <p className="text-sm sm:text-base text-gray-600 mb-6">
                  {error || '指定された注文が見つかりませんでした。'}
                </p>
                <Link href="/orders">
                  <Button variant="primary">注文履歴に戻る</Button>
                </Link>
              </Card>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50 py-6 sm:py-8 lg:py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto">
          {/* Back Button */}
          <div className="mb-4 sm:mb-6">
            <Link href="/orders">
              <Button variant="secondary" className="text-sm sm:text-base">
                ← 注文履歴に戻る
              </Button>
            </Link>
          </div>

          {/* Header */}
          <div className="mb-6 sm:mb-8">
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 mb-2">
              注文詳細
            </h1>
            <p className="text-sm sm:text-base text-gray-600">
              注文番号: {order.id}
            </p>
          </div>

          {/* Status Card */}
          <Card className={`mb-6 border-2 ${getStatusColor(order.status)}`}>
            <div className="p-4 sm:p-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                <div>
                  <p className="text-xs sm:text-sm font-medium mb-1">
                    注文ステータス
                  </p>
                  <p className="text-xl sm:text-2xl font-bold">
                    {getStatusText(order.status)}
                  </p>
                </div>
                <div className="text-left sm:text-right">
                  <p className="text-xs sm:text-sm font-medium mb-1">注文日時</p>
                  <p className="text-sm sm:text-base">
                    {new Date(order.created_at).toLocaleString('ja-JP')}
                  </p>
                </div>
              </div>
            </div>
          </Card>

          {/* NFT Minting Status */}
          {order.status === 'completed' && (
            <>
              {nftMinting && (
                <Card className="mb-6 border-2 border-blue-200 bg-blue-50">
                  <div className="p-4 sm:p-6">
                    <div className="flex items-center">
                      <svg className="animate-spin h-5 w-5 text-blue-600 mr-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      <div>
                        <p className="text-sm font-semibold text-blue-900">NFTをミント中...</p>
                        <p className="text-xs text-blue-700 mt-1">XRPL上でNFTを作成し、あなたのウォレットに送信しています。</p>
                      </div>
                    </div>
                  </div>
                </Card>
              )}
              
              {nftMinted && (
                <Card className="mb-6 border-2 border-green-200 bg-green-50">
                  <div className="p-4 sm:p-6">
                    <div className="flex items-start">
                      <svg className="w-5 h-5 text-green-600 mt-0.5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                      <div>
                        <p className="text-sm font-semibold text-green-900">🎉 NFTミント完了！</p>
                        <p className="text-xs text-green-700 mt-1">
                          NFTがXRPL上で正常にミントされ、あなたのウォレットに送信されました。
                        </p>
                        <Link href="/nfts" className="inline-block mt-2">
                          <button className="text-xs text-green-800 hover:text-green-900 underline font-medium">
                            マイNFTを確認 →
                          </button>
                        </Link>
                      </div>
                    </div>
                  </div>
                </Card>
              )}
            </>
          )}

          {/* Order Items */}
          <Card className="mb-6">
            <div className="p-4 sm:p-6">
              <h2 className="text-lg sm:text-xl font-bold text-gray-900 mb-4">
                注文商品
              </h2>
              <div className="space-y-4">
                {order.items?.map((item) => (
                  <div
                    key={item.id}
                    className="flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-4 pb-4 border-b last:border-b-0 last:pb-0"
                  >
                    <div className="flex-1">
                      <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-1">
                        {item.product?.name || '商品'}
                      </h3>
                      {item.product?.description && (
                        <p className="text-xs sm:text-sm text-gray-600 line-clamp-2">
                          {item.product.description}
                        </p>
                      )}
                    </div>
                    <div className="flex items-center justify-between sm:justify-end gap-4 sm:gap-6">
                      <div className="text-left sm:text-right">
                        <p className="text-xs sm:text-sm text-gray-500">単価</p>
                        <p className="text-sm sm:text-base font-medium text-gray-900">
                          ¥{item.unit_price.toLocaleString()}
                        </p>
                      </div>
                      <div className="text-left sm:text-right">
                        <p className="text-xs sm:text-sm text-gray-500">数量</p>
                        <p className="text-sm sm:text-base font-medium text-gray-900">
                          {item.quantity}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-xs sm:text-sm text-gray-500">小計</p>
                        <p className="text-base sm:text-lg font-bold text-gray-900">
                          ¥{item.subtotal.toLocaleString()}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Total */}
              <div className="mt-6 pt-6 border-t">
                <div className="flex justify-between items-center">
                  <span className="text-lg sm:text-xl font-bold text-gray-900">
                    合計金額
                  </span>
                  <span className="text-2xl sm:text-3xl font-bold text-blue-600">
                    ¥{order.total_amount.toLocaleString()}
                  </span>
                </div>
              </div>
            </div>
          </Card>

          {/* Payment Information */}
          {order.payment && (
            <Card className="mb-6">
              <div className="p-4 sm:p-6">
                <h2 className="text-lg sm:text-xl font-bold text-gray-900 mb-4">
                  決済情報
                </h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs sm:text-sm text-gray-500 mb-1">
                      決済ステータス
                    </p>
                    <p className="text-sm sm:text-base font-medium text-gray-900">
                      {order.payment.status === 'succeeded'
                        ? '決済完了'
                        : order.payment.status === 'processing'
                        ? '処理中'
                        : order.payment.status === 'pending'
                        ? '保留中'
                        : '失敗'}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs sm:text-sm text-gray-500 mb-1">
                      決済金額
                    </p>
                    <p className="text-sm sm:text-base font-medium text-gray-900">
                      ¥{order.payment.amount.toLocaleString()}
                    </p>
                  </div>
                </div>
              </div>
            </Card>
          )}

          {/* Actions */}
          <div className="flex flex-col sm:flex-row gap-4">
            <Link href="/shop" className="flex-1">
              <Button variant="primary" className="w-full">
                ショップに戻る
              </Button>
            </Link>
            <Link href="/orders" className="flex-1">
              <Button variant="secondary" className="w-full">
                注文履歴を見る
              </Button>
            </Link>
          </div>
        </div>
      </div>
      </div>
    </Layout>
  );
}
