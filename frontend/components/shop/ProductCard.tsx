'use client';

import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import Card, { CardContent, CardFooter } from '../ui/Card';
import Button from '../ui/Button';
import { useNFTStore } from '../../stores/nft-store';
import { useAuthStore } from '../../stores/auth-store';
import type { Product } from '../../types';

interface ProductCardProps {
  product: Product;
  onAddToCart?: (product: Product) => void;
  showNFTRequirement?: boolean;
}

export default function ProductCard({
  product,
  onAddToCart,
  showNFTRequirement = true,
}: ProductCardProps) {
  const [isAdding, setIsAdding] = useState(false);
  const { nfts } = useNFTStore();
  const { user } = useAuthStore();

  // Check if user has required NFT
  const hasRequiredNFT = product.required_nft_id
    ? nfts.some(
        (nft) =>
          nft.id === product.required_nft_id && nft.status === 'completed'
      )
    : true;

  const isOutOfStock = product.stock_quantity <= 0;
  const canPurchase = hasRequiredNFT && !isOutOfStock && product.is_active;

  const handleAddToCart = async () => {
    if (!canPurchase || !onAddToCart) return;

    setIsAdding(true);
    try {
      onAddToCart(product);
    } finally {
      setIsAdding(false);
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ja-JP', {
      style: 'currency',
      currency: 'JPY',
    }).format(price);
  };

  return (
    <Card className="flex flex-col h-full" padding="none" hover>
      <Link href={`/shop/${product.id}`}>
        <div className="relative w-full h-48 bg-gray-200">
          {product.image_url ? (
            <Image
              src={product.image_url}
              alt={product.name}
              fill
              className="object-cover rounded-t-lg"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            />
          ) : (
            <div className="flex items-center justify-center h-full text-gray-400">
              <svg
                className="w-16 h-16"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
            </div>
          )}
          {!product.is_active && (
            <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center rounded-t-lg">
              <span className="text-white font-semibold text-lg">
                販売終了
              </span>
            </div>
          )}
        </div>
      </Link>

      <CardContent className="flex-1 p-4">
        <Link href={`/shop/${product.id}`}>
          <h3 className="text-lg font-semibold text-gray-900 mb-2 hover:text-blue-600 transition-colors">
            {product.name}
          </h3>
        </Link>

        {product.description && (
          <p className="text-sm text-gray-600 mb-3 line-clamp-2">
            {product.description}
          </p>
        )}

        <div className="flex items-center justify-between mb-2">
          <span className="text-2xl font-bold text-gray-900">
            {formatPrice(product.price)}
          </span>
          <span
            className={`text-sm ${
              isOutOfStock ? 'text-red-600' : 'text-gray-600'
            }`}
          >
            {isOutOfStock ? '在庫切れ' : `在庫: ${product.stock_quantity}`}
          </span>
        </div>

        {showNFTRequirement && product.required_nft_id && (
          <div className="mt-2">
            {hasRequiredNFT ? (
              <div className="flex items-center text-sm text-green-600">
                <svg
                  className="w-4 h-4 mr-1"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                NFT保有済み
              </div>
            ) : (
              <div className="flex items-center text-sm text-amber-600">
                <svg
                  className="w-4 h-4 mr-1"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                    clipRule="evenodd"
                  />
                </svg>
                NFTが必要です
              </div>
            )}
          </div>
        )}
      </CardContent>

      <CardFooter className="p-4">
        {user ? (
          <Button
            onClick={handleAddToCart}
            disabled={!canPurchase}
            isLoading={isAdding}
            fullWidth
            variant={canPurchase ? 'primary' : 'outline'}
          >
            {isOutOfStock
              ? '在庫切れ'
              : !hasRequiredNFT
              ? 'NFTが必要'
              : !product.is_active
              ? '販売終了'
              : 'カートに追加'}
          </Button>
        ) : (
          <Link href="/login" className="block w-full">
            <Button fullWidth variant="outline">
              ログインして購入
            </Button>
          </Link>
        )}
      </CardFooter>
    </Card>
  );
}
