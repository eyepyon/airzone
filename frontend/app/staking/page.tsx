'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/stores/auth-store';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Loading from '@/components/ui/Loading';

interface Campaign {
  id: string;
  name: string;
  description: string;
  min_amount_drops: number;
  lock_days: number;
  nft_reward_name: string;
  nft_reward_description: string;
  nft_reward_image_url: string;
  max_participants: number;
  current_participants: number;
  start_date: string;
  end_date: string;
  status: string;
}

interface Stake {
  id: string;
  campaign_id: string;
  campaign_name: string;
  amount_drops: number;
  escrow_sequence: number;
  finish_after: string;
  status: string;
  created_at: string;
}

export default function StakingPage() {
  const router = useRouter();
  const { user, isAuthenticated } = useAuthStore();
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [myStakes, setMyStakes] = useState<Stake[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'campaigns' | 'mystakes'>('campaigns');

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login?redirect=/staking');
      return;
    }

    fetchData();
  }, [isAuthenticated, router]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('access_token');
      
      // キャンペーン一覧を取得
      const campaignsRes = await fetch('/api/v1/escrow/campaigns', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (campaignsRes.ok) {
        const campaignsData = await campaignsRes.json();
        setCampaigns(campaignsData.campaigns || []);
      }

      // 自分のステーク一覧を取得
      const stakesRes = await fetch('/api/v1/escrow/my-stakes', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (stakesRes.ok) {
        const stakesData = await stakesRes.json();
        setMyStakes(stakesData.stakes || []);
      }
    } catch (err) {
      console.error('Failed to fetch staking data:', err);
      setError('データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const handleStake = async (campaignId: string, minAmount: number) => {
    const amount = prompt(`ステークするXRP量を入力してください（最小: ${minAmount / 1_000_000} XRP）:`);
    
    if (!amount) return;
    
    const amountXrp = parseFloat(amount);
    if (isNaN(amountXrp) || amountXrp < minAmount / 1_000_000) {
      alert(`最小${minAmount / 1_000_000} XRP以上を入力してください`);
      return;
    }

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/v1/escrow/stake', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          campaign_id: campaignId,
          amount_xrp: amountXrp,
        }),
      });

      if (response.ok) {
        alert('ステーキングが完了しました！期間終了後にNFTを受け取れます。');
        fetchData(); // データを再取得
      } else {
        const error = await response.json();
        alert(`エラー: ${error.error || 'ステーキングに失敗しました'}`);
      }
    } catch (err) {
      console.error('Staking failed:', err);
      alert('ステーキングに失敗しました');
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ja-JP');
  };

  const getStatusBadge = (status: string) => {
    const styles = {
      active: 'bg-green-100 text-green-800',
      completed: 'bg-blue-100 text-blue-800',
      cancelled: 'bg-red-100 text-red-800',
    };
    
    const labels = {
      active: 'アクティブ',
      completed: '完了',
      cancelled: 'キャンセル',
    };

    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${styles[status as keyof typeof styles] || 'bg-gray-100 text-gray-800'}`}>
        {labels[status as keyof typeof labels] || status}
      </span>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loading size="lg" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-6 sm:py-8 lg:py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="mb-6 sm:mb-8">
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 mb-2">
              💎 XRP Escrowステーキング
            </h1>
            <p className="text-sm sm:text-base text-gray-600">
              XRPをロックして限定NFTを獲得しよう
            </p>
          </div>

          {/* Info Banner */}
          <div className="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start">
              <svg className="w-5 h-5 text-blue-500 mt-0.5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
              <div>
                <h3 className="text-sm font-semibold text-blue-900">Escrowステーキングとは？</h3>
                <p className="text-sm text-blue-800 mt-1">
                  XRPLのEscrow機能を使って、XRPを一定期間ロックします。期間終了後、XRPと限定NFTを自動的に受け取れます。
                </p>
              </div>
            </div>
          </div>

          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          {/* Tabs */}
          <div className="mb-6 border-b border-gray-200">
            <nav className="flex space-x-8">
              <button
                onClick={() => setActiveTab('campaigns')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'campaigns'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                キャンペーン一覧
              </button>
              <button
                onClick={() => setActiveTab('mystakes')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'mystakes'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                マイステーク ({myStakes.length})
              </button>
            </nav>
          </div>

          {/* Content */}
          {activeTab === 'campaigns' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {campaigns.length === 0 ? (
                <div className="col-span-2">
                  <Card className="text-center py-12">
                    <div className="text-4xl mb-4">📭</div>
                    <h2 className="text-xl font-semibold text-gray-900 mb-2">
                      現在開催中のキャンペーンはありません
                    </h2>
                    <p className="text-gray-600">
                      新しいキャンペーンをお待ちください
                    </p>
                  </Card>
                </div>
              ) : (
                campaigns.map((campaign) => (
                  <Card key={campaign.id} className="overflow-hidden">
                    {campaign.nft_reward_image_url && (
                      <img
                        src={campaign.nft_reward_image_url}
                        alt={campaign.nft_reward_name}
                        className="w-full h-48 object-cover"
                      />
                    )}
                    <div className="p-6">
                      <div className="flex justify-between items-start mb-4">
                        <h3 className="text-xl font-bold text-gray-900">
                          {campaign.name}
                        </h3>
                        {getStatusBadge(campaign.status)}
                      </div>
                      
                      <p className="text-gray-600 text-sm mb-4">
                        {campaign.description}
                      </p>

                      <div className="space-y-2 mb-4 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-600">最小ロック量:</span>
                          <span className="font-semibold">{campaign.min_amount_drops / 1_000_000} XRP</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">ロック期間:</span>
                          <span className="font-semibold">{campaign.lock_days}日間</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">報酬NFT:</span>
                          <span className="font-semibold">{campaign.nft_reward_name}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">参加者:</span>
                          <span className="font-semibold">
                            {campaign.current_participants} / {campaign.max_participants}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">期間:</span>
                          <span className="font-semibold text-xs">
                            {formatDate(campaign.start_date)} - {formatDate(campaign.end_date)}
                          </span>
                        </div>
                      </div>

                      <Button
                        onClick={() => handleStake(campaign.id, campaign.min_amount_drops)}
                        className="w-full"
                        disabled={campaign.status !== 'active' || campaign.current_participants >= campaign.max_participants}
                      >
                        {campaign.status !== 'active' ? 'キャンペーン終了' :
                         campaign.current_participants >= campaign.max_participants ? '定員に達しました' :
                         'ステーキングする'}
                      </Button>
                    </div>
                  </Card>
                ))
              )}
            </div>
          ) : (
            <div className="space-y-4">
              {myStakes.length === 0 ? (
                <Card className="text-center py-12">
                  <div className="text-4xl mb-4">💼</div>
                  <h2 className="text-xl font-semibold text-gray-900 mb-2">
                    ステーキング履歴がありません
                  </h2>
                  <p className="text-gray-600 mb-6">
                    キャンペーンに参加してXRPをステーキングしましょう
                  </p>
                  <Button onClick={() => setActiveTab('campaigns')}>
                    キャンペーンを見る
                  </Button>
                </Card>
              ) : (
                myStakes.map((stake) => (
                  <Card key={stake.id}>
                    <div className="p-6">
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <h3 className="text-lg font-bold text-gray-900">
                            {stake.campaign_name}
                          </h3>
                          <p className="text-sm text-gray-500">
                            ステーキング日: {formatDate(stake.created_at)}
                          </p>
                        </div>
                        {getStatusBadge(stake.status)}
                      </div>

                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="text-gray-600">ステーク量:</span>
                          <p className="font-semibold text-lg">
                            {stake.amount_drops / 1_000_000} XRP
                          </p>
                        </div>
                        <div>
                          <span className="text-gray-600">解放予定:</span>
                          <p className="font-semibold">
                            {formatDate(stake.finish_after)}
                          </p>
                        </div>
                      </div>

                      {stake.status === 'active' && (
                        <div className="mt-4 bg-yellow-50 border border-yellow-200 rounded p-3">
                          <p className="text-xs text-yellow-800">
                            ⏳ ロック期間中です。期間終了後に自動的にXRPとNFTを受け取れます。
                          </p>
                        </div>
                      )}

                      {stake.status === 'completed' && (
                        <div className="mt-4 bg-green-50 border border-green-200 rounded p-3">
                          <p className="text-xs text-green-800">
                            ✅ 完了しました！XRPとNFTを受け取りました。
                          </p>
                        </div>
                      )}
                    </div>
                  </Card>
                ))
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
