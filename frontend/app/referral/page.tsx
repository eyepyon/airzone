'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Layout from '@/components/layout/Layout';
import { useAuthStore } from '@/stores/auth-store';
import ReferralCard from '@/components/referral/ReferralCard';
import Card from '@/components/ui/Card';
import Loading from '@/components/ui/Loading';

interface ReferralStats {
  total_referrals: number;
  completed_referrals: number;
  pending_referrals: number;
  total_coins_earned: number;
  current_coins: number;
}

interface ReferralHistory {
  referrals: Array<{
    id: string;
    referred_user_id: string;
    referred_email?: string;
    status: string;
    coins_awarded: number;
    created_at: string;
  }>;
  coin_transactions: Array<{
    id: string;
    amount: number;
    transaction_type: string;
    description: string;
    created_at: string;
  }>;
}

export default function ReferralPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const [stats, setStats] = useState<ReferralStats | null>(null);
  const [history, setHistory] = useState<ReferralHistory | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login?redirect=/referral');
      return;
    }

    fetchStats();
  }, [isAuthenticated, router]);

  const fetchStats = async () => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('access_token');
      if (!token) {
        throw new Error('認証トークンがありません');
      }

      // 統計を取得
      const statsResponse = await fetch('/api/v1/referral/stats', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!statsResponse.ok) {
        const errorData = await statsResponse.json();
        throw new Error(errorData.error || '統計の取得に失敗しました');
      }

      const statsData = await statsResponse.json();
      setStats(statsData.data);

      // 履歴を取得
      const historyResponse = await fetch('/api/v1/referral/history', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (historyResponse.ok) {
        const historyData = await historyResponse.json();
        setHistory(historyData.data);
      }
    } catch (err) {
      console.error('Failed to fetch referral stats:', err);
      setError(err instanceof Error ? err.message : '統計の取得に失敗しました');
    } finally {
      setLoading(false);
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

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50 py-6 sm:py-8 lg:py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="mb-6 sm:mb-8">
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 mb-2">
              🎁 友達紹介プログラム
            </h1>
            <p className="text-sm sm:text-base text-gray-600">
              友達を招待してコインを獲得しよう
            </p>
          </div>

          {/* Info Banner */}
          <div className="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start">
              <svg className="w-5 h-5 text-blue-500 mt-0.5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
              <div>
                <h3 className="text-sm font-semibold text-blue-900">紹介プログラムの特典</h3>
                <ul className="text-sm text-blue-800 mt-1 space-y-1">
                  <li>• 友達が登録すると <strong>100コイン</strong> 獲得</li>
                  <li>• 紹介された友達は <strong>限定商品</strong> が購入可能</li>
                  <li>• SNSで簡単にシェアできます</li>
                </ul>
              </div>
            </div>
          </div>

          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          {/* Referral Card */}
          <div className="mb-8">
            <ReferralCard />
          </div>

          {/* Stats */}
          {stats && (
            <>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                <Card className="p-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-purple-600">
                      {stats.total_referrals}
                    </div>
                    <div className="text-sm text-gray-600 mt-1">総紹介数</div>
                  </div>
                </Card>
                <Card className="p-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-600">
                      {stats.completed_referrals}
                    </div>
                    <div className="text-sm text-gray-600 mt-1">完了</div>
                  </div>
                </Card>
                <Card className="p-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-blue-600">
                      {stats.pending_referrals}
                    </div>
                    <div className="text-sm text-gray-600 mt-1">保留中</div>
                  </div>
                </Card>
                <Card className="p-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-yellow-600">
                      {stats.current_coins}
                    </div>
                    <div className="text-sm text-gray-600 mt-1">現在のコイン</div>
                  </div>
                </Card>
              </div>

              {/* Recent Referrals */}
              <Card className="p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">
                  最近の紹介
                </h2>
                {history && history.referrals && history.referrals.length > 0 ? (
                  <div className="space-y-3">
                    {history.referrals.slice(0, 10).map((referral) => (
                      <div
                        key={referral.id}
                        className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                      >
                        <div className="flex-1">
                          <div className="font-medium text-gray-900">
                            {referral.referred_email || `ユーザー ${referral.referred_user_id.substring(0, 8)}...`}
                          </div>
                          <div className="text-sm text-gray-500">
                            {new Date(referral.created_at).toLocaleDateString('ja-JP')}
                          </div>
                        </div>
                        <div className="flex items-center gap-3">
                          <span
                            className={`px-3 py-1 rounded-full text-xs font-medium ${
                              referral.status === 'completed'
                                ? 'bg-green-100 text-green-800'
                                : 'bg-yellow-100 text-yellow-800'
                            }`}
                          >
                            {referral.status === 'completed' ? '完了' : '保留中'}
                          </span>
                          {referral.coins_awarded > 0 && (
                            <div className="text-yellow-600 font-semibold">
                              +{referral.coins_awarded} コイン
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    <div className="text-4xl mb-2">👥</div>
                    <p>まだ紹介がありません</p>
                    <p className="text-sm mt-1">
                      上の紹介リンクをシェアして友達を招待しましょう
                    </p>
                  </div>
                )}
              </Card>
            </>
          )}

          {/* How it works */}
          <Card className="p-6 mt-8">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              使い方
            </h2>
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center font-bold">
                  1
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">紹介コードをコピー</h3>
                  <p className="text-sm text-gray-600">
                    上のカードから紹介コードまたはリンクをコピーします
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center font-bold">
                  2
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">友達にシェア</h3>
                  <p className="text-sm text-gray-600">
                    SNSボタンを使って簡単にシェアできます
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center font-bold">
                  3
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">コインを獲得</h3>
                  <p className="text-sm text-gray-600">
                    友達が登録すると自動的に100コインが付与されます
                  </p>
                </div>
              </div>
            </div>
          </Card>
          </div>
        </div>
      </div>
    </Layout>
  );
}
