'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Layout from '@/components/layout/Layout';
import { useAuthStore } from '../../stores/auth-store';
import { useNFTStore } from '../../stores/nft-store';
import NFTGallery from '../../components/nft/NFTGallery';
import Button from '../../components/ui/Button';
import Loading from '../../components/ui/Loading';

export default function NFTsPage() {
  const router = useRouter();
  const { user, wallet, isLoading: authLoading } = useAuthStore();
  const { nfts, loading: nftsLoading, fetchNFTs, requestMint, mintingTaskId } = useNFTStore();

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

  const handleMintNFT = async () => {
    if (!wallet) return;
    
    try {
      await requestMint(wallet.address);
    } catch (error) {
      console.error('Failed to request NFT mint:', error);
    }
  };

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
              
              <Button
                onClick={handleMintNFT}
                disabled={!!mintingTaskId || nftsLoading}
                variant="primary"
              >
                {mintingTaskId ? 'ミント中...' : '新しいNFTをミント'}
              </Button>
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
