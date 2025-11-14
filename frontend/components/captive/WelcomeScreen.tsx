'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Card, { CardContent, CardHeader, CardTitle } from '../ui/Card';
import Button from '../ui/Button';
import { LoadingDots } from '../ui/Loading';
import { useNFTStore } from '@/stores/nft-store';
import { useAuthStore } from '@/stores/auth-store';

interface WelcomeScreenProps {
  onContinue?: () => void;
}

export default function WelcomeScreen({ onContinue }: WelcomeScreenProps) {
  const router = useRouter();
  const { user, wallet } = useAuthStore();
  const { nfts, mintingTaskId, fetchNFTs, requestMint, checkMintStatus } = useNFTStore();
  const [mintStatus, setMintStatus] = useState<'idle' | 'requesting' | 'minting' | 'completed' | 'failed'>('idle');
  const [error, setError] = useState<string | null>(null);

  // Fetch user's NFTs on mount
  useEffect(() => {
    if (wallet?.address) {
      fetchNFTs(wallet.address);
    }
  }, [wallet?.address, fetchNFTs]);

  // Auto-request NFT mint if user doesn't have any NFTs
  useEffect(() => {
    const autoMintNFT = async () => {
      if (wallet?.address && nfts.length === 0 && mintStatus === 'idle') {
        try {
          setMintStatus('requesting');
          await requestMint(wallet.address);
          setMintStatus('minting');
        } catch (err) {
          setError(err instanceof Error ? err.message : 'NFT発行リクエストに失敗しました');
          setMintStatus('failed');
        }
      }
    };

    autoMintNFT();
  }, [wallet?.address, nfts.length, mintStatus, requestMint]);

  // Poll mint status
  useEffect(() => {
    if (!mintingTaskId || mintStatus !== 'minting') return;

    const pollInterval = setInterval(async () => {
      try {
        await checkMintStatus(mintingTaskId);
        
        // Check if minting completed by refreshing NFT list
        await fetchNFTs(wallet?.address);
        if (nfts.length > 0) {
          setMintStatus('completed');
          clearInterval(pollInterval);
        }
      } catch (err) {
        console.error('Failed to check mint status:', err);
      }
    }, 3000); // Poll every 3 seconds

    // Cleanup
    return () => clearInterval(pollInterval);
  }, [mintingTaskId, mintStatus, checkMintStatus, wallet?.address, fetchNFTs, nfts.length]);

  const handleContinueToShop = () => {
    if (onContinue) {
      onContinue();
    } else {
      router.push('/shop');
    }
  };

  const handleViewDashboard = () => {
    router.push('/dashboard');
  };

  const renderMintStatus = () => {
    switch (mintStatus) {
      case 'requesting':
        return (
          <div className="text-center py-6">
            <LoadingDots className="justify-center mb-4" />
            <p className="text-gray-600">NFTを発行しています...</p>
          </div>
        );
      
      case 'minting':
        return (
          <div className="text-center py-6">
            <LoadingDots className="justify-center mb-4" />
            <p className="text-gray-600">ブロックチェーン上でNFTを作成中...</p>
            <p className="text-sm text-gray-500 mt-2">これには数秒かかる場合があります</p>
          </div>
        );
      
      case 'completed':
        return (
          <div className="text-center py-6">
            <div className="mb-4">
              <svg
                className="w-16 h-16 text-green-500 mx-auto"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              NFTの発行が完了しました！
            </h3>
            <p className="text-gray-600">
              おめでとうございます！あなたのウォレットにNFTが追加されました。
            </p>
          </div>
        );
      
      case 'failed':
        return (
          <div className="text-center py-6">
            <div className="mb-4">
              <svg
                className="w-16 h-16 text-red-500 mx-auto"
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
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              NFTの発行に失敗しました
            </h3>
            <p className="text-gray-600 mb-4">
              {error || '後ほど再度お試しください'}
            </p>
            <Button
              onClick={() => {
                setMintStatus('idle');
                setError(null);
              }}
              variant="outline"
            >
              再試行
            </Button>
          </div>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full space-y-6">
        {/* Welcome Card */}
        <Card className="text-center">
          <CardHeader>
            <CardTitle className="text-3xl">
              Airzoneへようこそ！
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600 mb-6">
              WiFi接続が完了しました。{user?.name}さん、ご利用ありがとうございます。
            </p>
            
            {/* Wallet Info */}
            {wallet && (
              <div className="bg-gray-50 rounded-lg p-4 mb-6">
                <p className="text-sm text-gray-500 mb-1">あなたのウォレットアドレス</p>
                <p className="font-mono text-sm text-gray-900 break-all">
                  {wallet.address}
                </p>
              </div>
            )}

            {/* NFT Status */}
            {nfts.length > 0 ? (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
                <div className="flex items-center justify-center mb-2">
                  <svg
                    className="w-6 h-6 text-green-600 mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  <p className="font-semibold text-green-900">
                    NFTを{nfts.length}個保有しています
                  </p>
                </div>
                <p className="text-sm text-green-700">
                  ECショップで特別な商品を購入できます
                </p>
              </div>
            ) : (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                {renderMintStatus()}
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <Button
                onClick={handleContinueToShop}
                size="lg"
                disabled={mintStatus === 'requesting' || mintStatus === 'minting'}
              >
                ショップを見る
              </Button>
              <Button
                onClick={handleViewDashboard}
                variant="outline"
                size="lg"
                disabled={mintStatus === 'requesting' || mintStatus === 'minting'}
              >
                ダッシュボード
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Info Card */}
        <Card>
          <CardContent className="text-sm text-gray-600">
            <h4 className="font-semibold text-gray-900 mb-2">ご利用について</h4>
            <ul className="space-y-2">
              <li className="flex items-start">
                <span className="text-blue-600 mr-2">•</span>
                <span>WiFi接続中は無料でインターネットをご利用いただけます</span>
              </li>
              <li className="flex items-start">
                <span className="text-blue-600 mr-2">•</span>
                <span>NFTは自動的にあなたのウォレットに発行されます</span>
              </li>
              <li className="flex items-start">
                <span className="text-blue-600 mr-2">•</span>
                <span>NFTを使用してECショップで特別な商品を購入できます</span>
              </li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
