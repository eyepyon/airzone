'use client';

import { NFT } from '../../types';
import Card, { CardContent, CardFooter } from '../ui/Card';

interface NFTCardProps {
  nft: NFT;
  onClick?: (nft: NFT) => void;
}

export default function NFTCard({ nft, onClick }: NFTCardProps) {
  const handleClick = () => {
    if (onClick) {
      onClick(nft);
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

  const imageUrl = nft.metadata?.image_url || nft.metadata?.image || '/placeholder-nft.png';
  const name = nft.metadata?.name || `NFT #${nft.id.slice(0, 8)}`;
  const description = nft.metadata?.description || 'Airzone NFT';

  return (
    <Card
      hover={!!onClick}
      padding="none"
      className="overflow-hidden"
      onClick={handleClick}
    >
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
                <div className="w-16 h-16 mx-auto mb-4 bg-gray-300 rounded-full" />
                <div className="h-4 bg-gray-300 rounded w-24 mx-auto" />
              </div>
            </div>
          </div>
        )}
        
        {/* Status Badge */}
        <div className="absolute top-2 right-2">
          <span
            className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(
              nft.status
            )}`}
          >
            {getStatusText(nft.status)}
          </span>
        </div>
      </div>

      <CardContent className="p-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-1 truncate">
          {name}
        </h3>
        <p className="text-sm text-gray-600 line-clamp-2 mb-2">
          {description}
        </p>
        
        {nft.nft_object_id && (
          <p className="text-xs text-gray-500 font-mono truncate">
            ID: {nft.nft_object_id}
          </p>
        )}
      </CardContent>

      {nft.status === 'failed' && nft.error_message && (
        <CardFooter className="bg-red-50 p-3">
          <p className="text-xs text-red-600">
            Error: {nft.error_message}
          </p>
        </CardFooter>
      )}

      {nft.transaction_digest && (
        <CardFooter className="p-3">
          <a
            href={`https://suiexplorer.com/txblock/${nft.transaction_digest}?network=testnet`}
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-blue-600 hover:text-blue-800 hover:underline"
            onClick={(e) => e.stopPropagation()}
          >
            View on Explorer →
          </a>
        </CardFooter>
      )}
    </Card>
  );
}
