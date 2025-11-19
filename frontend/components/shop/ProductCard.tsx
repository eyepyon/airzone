'use client';

import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import Card, { CardContent, CardFooter } from '../ui/Card';
import Button from '../ui/Button';
import { useNFTStore } from '../../stores/nft-store';
import { useAuthStore } from '../../stores/auth-store';
import { canPurchaseProduct, getRestrictionBadge, getProductTypeBadge, getDeliveryMethodLabel } from '@/lib/purchase-restrictions';
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

  // Set default values for backward compatibility
  const productWithDefaults = {
    ...product,
    product_type: product.product_type || 'goods',
    purchase_restriction: product.purchase_restriction || 'public',
    delivery_method: product.delivery_method || null,
  };

  // Check purchase eligibility
  const purchaseCheck = canPurchaseProduct(productWithDefaults as Product, nfts, !!user);
  const isOutOfStock = product.stock_quantity <= 0;
  const canPurchase = purchaseCheck.canPurchase && !isOutOfStock;
  
  const restrictionBadge = getRestrictionBadge(productWithDefaults.purchase_restriction);
  const productTypeBadge = getProductTypeBadge(productWithDefaults.product_type);

  const handleAddToCart = async () => {
    if (!canPurchase || !onAddToCart) return;

    setIsAdding(true);
    try {
      onAddToCart(product);
    } finally {
      setIsAdding(false);
    }
  };

  const formatPrice = (price: number | undefined) => {
    if (price === undefined || price === null) {
      return '価格未設定';
    }
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
        {/* Badges - Only show if new fields exist */}
        {(product.product_type || product.purchase_restriction) && (
          <div className="flex flex-wrap gap-2 mb-3">
            {product.product_type && (
              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${productTypeBadge.color}`}>
                {productTypeBadge.icon} {productTypeBadge.label}
              </span>
            )}
            {product.purchase_restriction && (
              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${restrictionBadge.color}`}>
                {restrictionBadge.icon} {restrictionBadge.label}
              </span>
            )}
            {product.delivery_method && product.product_type === 'goods' && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
                {product.delivery_method === 'pickup' ? '📍' : '🚚'} {getDeliveryMethodLabel(product.delivery_method)}
              </span>
            )}
          </div>
        )}

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
        
        {/* Event Info for Tickets */}
        {product.product_type === 'event_ticket' && (product.event_date || product.venue) && (
          <div className="text-xs text-gray-600 mb-2 space-y-1">
            {product.event_date && (
              <div className="flex items-center">
                <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
                </svg>
                {new Date(product.event_date).toLocaleDateString('ja-JP')}
              </div>
            )}
            {product.venue && (
              <div className="flex items-center">
                <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                </svg>
                {product.venue}
              </div>
            )}
          </div>
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

        {/* Purchase Status */}
        {!purchaseCheck.canPurchase && purchaseCheck.reason && (
          <div className="mt-2">
            <div className="flex items-center text-xs text-amber-600">
              <svg
                className="w-4 h-4 mr-1 flex-shrink-0"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                  clipRule="evenodd"
                />
              </svg>
              {purchaseCheck.reason}
            </div>
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
              : !product.is_active
              ? '販売終了'
              : !purchaseCheck.canPurchase
              ? '購入不可'
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
