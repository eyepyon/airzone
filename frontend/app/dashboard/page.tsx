'use client';

import { useAuthStore } from '@/stores/auth-store';
import { useRouter } from 'next/navigation';
import Layout from '@/components/layout/Layout';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import Loading from '@/components/ui/Loading';
import XamanWalletConnectWorking from '@/components/wallet/XamanWalletConnectWorking';

const XRPL_NETWORK = process.env.NEXT_PUBLIC_XRPL_NETWORK || 'testnet';

const getExplorerUrl = (address: string) => {
  const network = XRPL_NETWORK === 'mainnet' ? 'mainnet' : 'testnet';
  return `https://${network}.xrpl.org/accounts/${address}`;
};

export default function DashboardPage() {
  const { user, wallet, isLoading } = useAuthStore();
  const router = useRouter();

  if (isLoading) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <Loading />
        </div>
      </Layout>
    );
  }

  if (!user) {
    return null; // AuthProvider will redirect to login
  }

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">ダッシュボード</h1>
            <p className="text-gray-600 mt-1">ようこそ、{user.name}さん！</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card>
            <h2 className="text-xl font-semibold mb-4">User Information</h2>
            <div className="space-y-2">
              <div>
                <span className="text-gray-600">Name:</span>
                <span className="ml-2 font-medium">{user.name}</span>
              </div>
              <div>
                <span className="text-gray-600">Email:</span>
                <span className="ml-2 font-medium">{user.email}</span>
              </div>
              <div>
                <span className="text-gray-600">User ID:</span>
                <span className="ml-2 font-mono text-sm">{user.id}</span>
              </div>
            </div>
          </Card>

          {wallet ? (
            <Card className="md:col-span-2">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold">💼 XRPL Wallet</h2>
                <span className="px-3 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded-full flex items-center gap-1">
                  <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                  Active
                </span>
              </div>

              {/* Wallet Type Info */}
              <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-start">
                  <svg className="w-5 h-5 text-blue-600 mt-0.5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                  </svg>
                  <div className="text-sm">
                    <p className="font-semibold text-blue-900">自動生成ウォレット</p>
                    <p className="text-blue-800 mt-1">
                      このウォレットはログイン時に自動的に作成されました。秘密鍵は安全に暗号化されて保存されています。
                    </p>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                {/* Wallet Address */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-gray-700 font-medium text-sm">ウォレットアドレス</span>
                    <span className="text-xs text-gray-500">XRPL {XRPL_NETWORK}</span>
                  </div>
                  <div className="relative">
                    <div className="p-4 bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-200 rounded-lg font-mono text-sm break-all">
                      {wallet.address}
                    </div>
                    <div className="absolute top-2 right-2">
                      <button
                        onClick={() => {
                          navigator.clipboard.writeText(wallet.address);
                          alert('✓ アドレスをコピーしました！');
                        }}
                        className="p-2 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow"
                        title="アドレスをコピー"
                      >
                        <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>

                {/* Quick Actions */}
                <div className="grid grid-cols-2 gap-3">
                  <a
                    href={getExplorerUrl(wallet.address)}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-center gap-2 px-4 py-3 bg-white border-2 border-gray-200 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition-all"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                    <span className="text-sm font-medium text-gray-700">Explorer</span>
                  </a>
                  <button
                    onClick={() => router.push('/nfts')}
                    className="flex items-center justify-center gap-2 px-4 py-3 bg-white border-2 border-gray-200 rounded-lg hover:border-purple-400 hover:bg-purple-50 transition-all"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <span className="text-sm font-medium text-gray-700">My NFTs</span>
                  </button>
                </div>

                {/* Wallet Details */}
                <div className="pt-4 border-t space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">ウォレットID</span>
                    <span className="text-sm font-mono text-gray-900">{wallet.id}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">ネットワーク</span>
                    <span className="text-sm font-semibold text-gray-900">
                      XRPL {XRPL_NETWORK === 'testnet' ? 'Testnet' : 'Mainnet'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">作成日時</span>
                    <span className="text-sm text-gray-900">
                      {new Date(wallet.created_at).toLocaleDateString('ja-JP', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">ウォレットタイプ</span>
                    <span className="text-sm font-semibold text-green-600">自動生成</span>
                  </div>
                </div>

                {/* Security Info */}
                <div className="pt-4 border-t">
                  <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                    <div className="flex items-start">
                      <svg className="w-5 h-5 text-green-600 mt-0.5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                      <div className="text-sm">
                        <p className="font-semibold text-green-900">セキュリティ</p>
                        <p className="text-green-800 mt-1">
                          秘密鍵は AES-256 で暗号化され、安全に保存されています。
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          ) : (
            <Card className="md:col-span-2">
              <div className="text-center py-8">
                <div className="text-4xl mb-4">💼</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  ウォレットを作成中...
                </h3>
                <p className="text-sm text-gray-600">
                  ログイン時に自動的にXRPLウォレットが作成されます
                </p>
              </div>
            </Card>
          )}

          {/* Xaman Wallet統合 - 簡易版 */}
          <Card className="md:col-span-2">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold">🔗 外部ウォレット接続</h2>
              <span className="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full">
                簡易版
              </span>
            </div>
            <div className="space-y-4">
              <p className="text-sm text-gray-600">
                Xaman Wallet（旧Xumm）を接続して、より高度なセキュリティとウォレット管理を利用できます。
              </p>
              
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-blue-900 mb-2">
                  Xaman Walletとは？
                </h3>
                <ul className="text-sm text-blue-800 space-y-1">
                  <li>• XRPLの公式モバイルウォレット</li>
                  <li>• 秘密鍵をあなた自身が管理</li>
                  <li>• 最高レベルのセキュリティ</li>
                  <li>• NFTの直接管理が可能</li>
                </ul>
              </div>

              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-start">
                  <svg className="w-5 h-5 text-green-600 mt-0.5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <div>
                    <h4 className="text-sm font-semibold text-green-900">簡易版が利用可能</h4>
                    <p className="text-sm text-green-800 mt-1">
                      Xaman WalletのXRPLアドレスを入力するだけで接続できます。
                      接続後、NFTはXaman Walletに送信されます。
                    </p>
                  </div>
                </div>
              </div>

              <div className="pt-2">
                <XamanWalletConnectWorking />
              </div>

              <div className="text-xs text-gray-500 text-center">
                詳細: <a 
                  href="https://github.com/yourusername/airzone/blob/main/docs/XAMAN_WALLET_STATUS_JP.md" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 underline"
                >
                  Xaman Wallet統合ステータス
                </a>
              </div>
            </div>
          </Card>
        </div>

        <div className="mt-8">
          <Card>
            <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
              <Button
                onClick={() => router.push('/shop')}
                className="w-full"
              >
                🛍️ Shop
              </Button>
              <Button
                onClick={() => router.push('/staking')}
                className="w-full bg-purple-600 hover:bg-purple-700"
              >
                💎 Staking
              </Button>
              <Button
                onClick={() => router.push('/referral')}
                className="w-full bg-pink-600 hover:bg-pink-700"
              >
                🎁 Referral
              </Button>
              <Button
                onClick={() => router.push('/orders')}
                variant="secondary"
                className="w-full"
              >
                📦 Orders
              </Button>
              <Button
                onClick={() => router.push('/nfts')}
                variant="secondary"
                className="w-full"
              >
                🎨 NFTs
              </Button>
            </div>
          </Card>
        </div>
        </div>
      </div>
    </Layout>
  );
}
