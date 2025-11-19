'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Layout from '@/components/layout/Layout';
import { useAuthStore } from '../../stores/auth-store';
import { useNFTStore } from '../../stores/nft-store';
import NFTGallery from '../../components/nft/NFTGallery';
import Loading from '../../components/ui/Loading';

export default function NFTsPage() {
  const router = useRouter();
  const { user, wallet, isLoading: authLoading } = useAuthStore();
  const { nfts, loading: nftsLoading, fetchNFTs } = useNFTStore();

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
      return;
    }

    if (user && wallet) {
      fetchNFTs();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, wallet, authLoading]);

  const handleNFTClick = (nft: { id: string }) => {
    router.push(`/nfts/${nft.id}`);
  };

  if (authLoading) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <Loading size="lg" text="読み込み中..." />
        </div>
      </Layout>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <div className="mb-8">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">マイNFT</h1>
                <p className="text-gray-600">
                  あなたのAirzone NFTコレクションを表示・管理
                </p>
                {wallet && (
                  <p className="text-sm text-gray-500 mt-2 font-mono">
                    ウォレット: {wallet.address.slice(0, 8)}...{wallet.address.slice(-6)}
                  </p>
                )}
              </div>
            </div>
            
            {/* Info Banner */}
            <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-start">
                <svg className="w-5 h-5 text-blue-500 mt-0.5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
                <div>
                  <h3 className="text-sm font-semibold text-blue-900">NFTの取得方法</h3>
                  <p className="text-sm text-blue-800 mt-1">
                    NFTは商品を購入すると自動的にXRPL上でミントされ、あなたのウォレットに送信されます。
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* NFT Gallery */}
          <NFTGallery
            nfts={nfts}
            loading={nftsLoading}
            onNFTClick={handleNFTClick}
            emptyMessage="まだNFTを持っていません"
          />
        </div>
      </div>
    </Layout>
  );
}
