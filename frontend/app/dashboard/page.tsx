'use client';

import { useAuthStore } from '@/stores/auth-store';
import { useRouter } from 'next/navigation';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import Loading from '@/components/ui/Loading';

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
              <h2 className="text-xl font-semibold mb-4">Wallet Information</h2>
              <div className="space-y-2">
                <div>
                  <span className="text-gray-600">Address:</span>
                  <div className="mt-1 p-2 bg-gray-100 rounded font-mono text-sm break-all">
                    {wallet.address}
                  </div>
                </div>
                <div className="mt-4">
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
