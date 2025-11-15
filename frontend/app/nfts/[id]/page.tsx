'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { useAuthStore } from '@/stores/auth-store';
import { getNFTById } from '@/lib/api/nfts';
import { NFT } from '@/types';
import Card, { CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Loading from '@/components/ui/Loading';

export default function NFTDetailPage() {
  const router = useRouter();
  const params = useParams();
  const nftId = params.id as string;
  
  const { user, isLoading: authLoading } = useAuthStore();
  const [nft, setNft] = useState<NFT | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
      return;
    }

    if (user && nftId) {
      loadNFT();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, authLoading, nftId]);

  const loadNFT = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getNFTById(nftId);
      setNft(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load NFT');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: NFT['status']) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'minting':
        return 'bg-blue-100 text-blue-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: NFT['status']) => {
    switch (status) {
      case 'completed':
        return 'Completed';
      case 'minting':
        return 'Minting...';
      case 'pending':
        return 'Pending';
      case 'failed':
        return 'Failed';
      default:
        return status;
    }
  };

  if (authLoading || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loading size="lg" text="Loading NFT..." />
      </div>
    );
  }

  if (!user) {
    return null;
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="text-center py-8">
            <div className="text-red-600 mb-4">
              <svg
                className="w-16 h-16 mx-auto"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              Error Loading NFT
            </h2>
            <p className="text-gray-600 mb-6">{error}</p>
            <Button onClick={() => router.push('/nfts')} variant="primary">
              Back to NFTs
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!nft) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="text-center py-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              NFT Not Found
            </h2>
            <p className="text-gray-600 mb-6">
              The NFT you're looking for doesn't exist or you don't have access to it.
            </p>
            <Button onClick={() => router.push('/nfts')} variant="primary">
              Back to NFTs
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const imageUrl = nft.metadata?.image_url || nft.metadata?.image || '/placeholder-nft.png';
  const name = nft.metadata?.name || `NFT #${nft.id.slice(0, 8)}`;
  const description = nft.metadata?.description || 'Airzone NFT';

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Back Button */}
        <div className="mb-6">
          <Button
            onClick={() => router.push('/nfts')}
            variant="secondary"
            className="flex items-center gap-2"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 19l-7-7 7-7"
              />
            </svg>
            Back to NFTs
          </Button>
        </div>

        {/* NFT Detail */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Image Section */}
          <Card padding="none" className="overflow-hidden">
            <div className="relative aspect-square bg-gray-100">
              {nft.status === 'completed' ? (
                <img
                  src={imageUrl}
                  alt={name}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.src = '/placeholder-nft.png';
                  }}
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <div className="text-center">
                    <div className="animate-pulse">
                      <div className="w-24 h-24 mx-auto mb-6 bg-gray-300 rounded-full" />
                      <div className="h-6 bg-gray-300 rounded w-32 mx-auto" />
                    </div>
                  </div>
                </div>
              )}
            </div>
          </Card>

          {/* Details Section */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <CardTitle>{name}</CardTitle>
                  <span
                    className={`px-3 py-1 text-sm font-semibold rounded-full ${getStatusColor(
                      nft.status
                    )}`}
                  >
                    {getStatusText(nft.status)}
                  </span>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 mb-6">{description}</p>

                <div className="space-y-4">
                  <div>
                    <h3 className="text-sm font-semibold text-gray-700 mb-1">
                      NFT ID
                    </h3>
                    <p className="text-sm text-gray-900 font-mono break-all">
                      {nft.id}
                    </p>
                  </div>

                  {nft.nft_object_id && (
                    <div>
                      <h3 className="text-sm font-semibold text-gray-700 mb-1">
                        Object ID
                      </h3>
                      <p className="text-sm text-gray-900 font-mono break-all">
                        {nft.nft_object_id}
                      </p>
                    </div>
                  )}

                  <div>
                    <h3 className="text-sm font-semibold text-gray-700 mb-1">
                      Wallet Address
                    </h3>
                    <p className="text-sm text-gray-900 font-mono break-all">
                      {nft.wallet_address}
                    </p>
                  </div>

                  {nft.transaction_digest && (
                    <div>
                      <h3 className="text-sm font-semibold text-gray-700 mb-1">
                        Transaction
                      </h3>
                      <a
                        href={`https://suiexplorer.com/txblock/${nft.transaction_digest}?network=testnet`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-blue-600 hover:text-blue-800 hover:underline font-mono break-all"
                      >
                        {nft.transaction_digest}
                      </a>
                    </div>
                  )}

                  <div>
                    <h3 className="text-sm font-semibold text-gray-700 mb-1">
                      Created At
                    </h3>
                    <p className="text-sm text-gray-900">
                      {new Date(nft.created_at).toLocaleString()}
                    </p>
                  </div>

                  {nft.updated_at !== nft.created_at && (
                    <div>
                      <h3 className="text-sm font-semibold text-gray-700 mb-1">
                        Updated At
                      </h3>
                      <p className="text-sm text-gray-900">
                        {new Date(nft.updated_at).toLocaleString()}
                      </p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Error Message */}
            {nft.status === 'failed' && nft.error_message && (
              <Card className="border-red-200 bg-red-50">
                <CardHeader>
                  <CardTitle className="text-red-800">Error Details</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-red-600">{nft.error_message}</p>
                </CardContent>
              </Card>
            )}

            {/* Metadata */}
            {nft.metadata && Object.keys(nft.metadata).length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Metadata</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {Object.entries(nft.metadata).map(([key, value]) => (
                      <div key={key} className="flex justify-between py-2 border-b border-gray-100 last:border-0">
                        <span className="text-sm font-medium text-gray-700 capitalize">
                          {key.replace(/_/g, ' ')}
                        </span>
                        <span className="text-sm text-gray-900 text-right max-w-xs truncate">
                          {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                        </span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Actions */}
            {nft.transaction_digest && (
              <Card>
                <CardContent>
                  <Button
                    onClick={() =>
                      window.open(
                        `https://suiexplorer.com/txblock/${nft.transaction_digest}?network=testnet`,
                        '_blank'
                      )
                    }
                    variant="primary"
                    className="w-full"
                  >
                    View on Sui Explorer
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
