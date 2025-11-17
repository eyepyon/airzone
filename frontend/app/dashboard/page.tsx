'use client';

import { useAuthStore } from '@/stores/auth-store';
import { useRouter } from 'next/navigation';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import Loading from '@/components/ui/Loading';

const XRPL_NETWORK = process.env.NEXT_PUBLIC_XRPL_NETWORK || 'testnet';

const getExplorerUrl = (address: string) => {
  const network = XRPL_NETWORK === 'mainnet' ? 'mainnet' : 'testnet';
  return `https://${network}.xrpl.org/accounts/${address}`;
};

export default function DashboardPage() {
  const { user, wallet, logout, isLoading } = useAuthStore();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loading />
      </div>
    );
  }

  if (!user) {
    return null; // AuthProvider will redirect to login
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-600 mt-1">Welcome back, {user.name}!</p>
          </div>
          <Button onClick={handleLogout} variant="secondary">
            Logout
          </Button>
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

          {wallet && (
            <Card>
              <h2 className="text-xl font-semibold mb-4">💼 Wallet Information</h2>
              <div className="space-y-4">
                <div>
                  <span className="text-gray-600 text-sm">Wallet Address:</span>
                  <div className="mt-1 p-3 bg-gray-100 rounded-lg font-mono text-sm break-all">
                    {wallet.address}
                  </div>
                  <div className="mt-2 flex gap-2">
                    <button
                      onClick={() => {
                        navigator.clipboard.writeText(wallet.address);
                        alert('Address copied to clipboard!');
                      }}
                      className="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                      </svg>
                      Copy Address
                    </button>
                    <a
                      href={getExplorerUrl(wallet.address)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                      View on Explorer ({XRPL_NETWORK})
                    </a>
                  </div>
                </div>
                
                <div className="pt-2 border-t">
                  <span className="text-gray-600 text-sm">Wallet ID:</span>
                  <div className="mt-1 font-mono text-xs text-gray-500 break-all">
                    {wallet.id}
                  </div>
                </div>
                
                <div className="pt-2">
                  <span className="text-gray-600 text-sm">Created:</span>
                  <div className="mt-1 text-sm text-gray-700">
                    {new Date(wallet.created_at).toLocaleString('ja-JP')}
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t">
                  <Button
                    onClick={() => router.push('/nfts')}
                    className="w-full"
                  >
                    View My NFTs
                  </Button>
                </div>
              </div>
            </Card>
          )}
        </div>

        <div className="mt-8">
          <Card>
            <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <Button
                onClick={() => router.push('/shop')}
                className="w-full"
              >
                Browse Shop
              </Button>
              <Button
                onClick={() => router.push('/orders')}
                variant="secondary"
                className="w-full"
              >
                My Orders
              </Button>
              <Button
                onClick={() => router.push('/nfts')}
                variant="secondary"
                className="w-full"
              >
                My NFTs
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
