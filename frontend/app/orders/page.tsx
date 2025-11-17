'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Layout from '@/components/layout/Layout';
import { Card, Loading } from '@/components/ui';
import { useAuthStore } from '@/stores';
import { getOrders } from '@/lib/api';
import type { Order } from '@/types';

export default function OrdersPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const fetchOrders = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getOrders();
        setOrders(data.orders || []);
      } catch (err) {
        console.error('Failed to fetch orders:', err);
        const errorMessage = err instanceof Error ? err.message : '注文の取得に失敗しました';
        setError(errorMessage);
        setOrders([]);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-600 bg-green-50';
      case 'processing':
        return 'text-blue-600 bg-blue-50';
      case 'pending':
        return 'text-yellow-600 bg-yellow-50';
      case 'failed':
      case 'cancelled':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
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

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50 py-6 sm:py-8 lg:py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="mb-6 sm:mb-8">
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 mb-2">
              注文履歴
            </h1>
            <p className="text-sm sm:text-base text-gray-600">
              過去の注文を確認できます
            </p>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="flex items-center justify-center py-12">
              <Loading size="lg" />
            </div>
          )}

          {/* Error Message */}
          {error && !loading && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <div className="flex items-start">
                <svg
                  className="w-5 h-5 text-red-500 mt-0.5 mr-3 flex-shrink-0"
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
                  <h3 className="text-sm font-medium text-red-800">エラーが発生しました</h3>
                  <p className="text-sm text-red-700 mt-1">{error}</p>
                  <button
                    onClick={() => window.location.reload()}
                    className="mt-3 text-sm text-red-600 hover:text-red-800 underline"
                  >
                    ページを再読み込み
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Orders List */}
          {!loading && orders.length === 0 && !error ? (
            <Card className="text-center py-12 sm:py-16">
              <div className="text-4xl sm:text-5xl mb-4">📦</div>
              <h2 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2">
                注文履歴がありません
              </h2>
              <p className="text-sm sm:text-base text-gray-600 mb-6">
                まだ注文がありません。ショップで商品を探してみましょう。
              </p>
              <Link href="/shop">
                <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm sm:text-base">
                  ショップを見る
                </button>
              </Link>
            </Card>
          ) : !loading && !error ? (
            <div className="space-y-4 sm:space-y-6">
              {orders.map((order) => (
                <Link key={order.id} href={`/orders/${order.id}`}>
                  <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                    <div className="p-4 sm:p-6">
                      {/* Order Header */}
                      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 sm:gap-4 mb-4">
                        <div>
                          <p className="text-xs sm:text-sm text-gray-500 mb-1">
                            注文番号
                          </p>
                          <p className="text-sm sm:text-base font-mono text-gray-900 break-all">
                            {order.id}
                          </p>
                        </div>
                        <span
                          className={`px-3 py-1 rounded-full text-xs sm:text-sm font-medium self-start sm:self-auto ${getStatusColor(
                            order.status
                          )}`}
                        >
                          {getStatusText(order.status)}
                        </span>
                      </div>

                      {/* Order Details */}
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 mb-4">
                        <div>
                          <p className="text-xs sm:text-sm text-gray-500 mb-1">
                            注文日時
                          </p>
                          <p className="text-sm sm:text-base text-gray-900">
                            {new Date(order.created_at).toLocaleString('ja-JP')}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs sm:text-sm text-gray-500 mb-1">
                            合計金額
                          </p>
                          <p className="text-lg sm:text-xl font-bold text-gray-900">
                            ¥{order.total_amount.toLocaleString()}
                          </p>
                        </div>
                      </div>

                      {/* Order Items */}
                      {order.items && order.items.length > 0 && (
                        <div className="border-t pt-4">
                          <p className="text-xs sm:text-sm text-gray-500 mb-2">
                            商品 ({order.items.length}点)
                          </p>
                          <div className="space-y-2">
                            {order.items.slice(0, 2).map((item) => (
                              <div
                                key={item.id}
                                className="flex justify-between items-center text-sm"
                              >
                                <span className="text-gray-700 truncate mr-2">
                                  {item.product?.name || '商品'}
                                </span>
                                <span className="text-gray-900 whitespace-nowrap">
                                  ¥{item.unit_price.toLocaleString()} × {item.quantity}
                                </span>
                              </div>
                            ))}
                            {order.items.length > 2 && (
                              <p className="text-xs sm:text-sm text-gray-500">
                                他 {order.items.length - 2} 点
                              </p>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </Card>
                </Link>
              ))}
            </div>
          ) : null}
          </div>
        </div>
      </div>
    </Layout>
  );
}
