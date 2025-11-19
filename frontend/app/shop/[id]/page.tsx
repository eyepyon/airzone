'use client';

import React, { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Image from 'next/image';
import { getProductById } from '../../../lib/api/products';
import { useCartStore } from '../../../stores/cart-store';
import { useAuthStore } from '../../../stores/auth-store';
import { useNFTStore } from '../../../stores/nft-store';
import type { Product } from '../../../types';
import Button from '../../../components/ui/Button';
import Card from '../../../components/ui/Card';
import Loading from '../../../components/ui/Loading';

export default function ProductDetailPage() {
  const router = useRouter();
  const params = useParams();
  const productId = params.id as string;

  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [quantity, setQuantity] = useState(1);

  const { user } = useAuthStore();
  const { nfts, fetchNFTs } = useNFTStore();
  const { addItem } = useCartStore();

  useEffect(() => {
    loadProduct();
    if (user) {
      fetchNFTs();
    }
  }, [productId, user]);

  const loadProduct = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getProductById(productId);
      setProduct(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load product');
    } finally {
      setLoading(false);
    }
  };

  const hasRequiredNFT = (): boolean => {
    if (!product?.required_nft_id) {
      return true;
    }
    return nfts.some((nft) => nft.status === 'completed');
  };

  const handleAddToCart = () => {
    if (product && canPurchase) {
      addItem(product, quantity);
      router.push('/checkout');
    }
  };

  const handleQuantityChange = (newQuantity: number) => {
    if (product && newQuantity >= 1 && newQuantity <= product.stock_quantity) {
      setQuantity(newQuantity);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Loading size="lg" />
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md w-full p-8 text-center">
          <svg
            className="w-16 h-16 mx-auto text-red-500 mb-4"
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
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Product Not Found
          </h2>
          <p className="text-gray-600 mb-4">
            {error || 'The product you are looking for does not exist.'}
          </p>
          <Button onClick={() => router.push('/shop')}>Back to Shop</Button>
        </Card>
      </div>
    );
  }

  const isOutOfStock = product.stock_quantity <= 0;
  const isLocked = product.required_nft_id && !hasRequiredNFT();
  const canPurchase = !isOutOfStock && !isLocked && product.is_active;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Back Button */}
        <Button
          onClick={() => router.push('/shop')}
          variant="secondary"
          className="mb-6"
        >
          <svg
            className="w-5 h-5 mr-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M10 19l-7-7m0 0l7-7m-7 7h18"
            />
          </svg>
          Back to Shop
        </Button>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Product Image */}
          <div className="relative">
            <Card className="overflow-hidden">
              <div className="relative w-full h-96 lg:h-[600px] bg-gray-200">
                {product.image_url ? (
                  <Image
                    src={product.image_url}
                    alt={product.name}
                    fill
                    className="object-cover"
                  />
                ) : (
                  <div className="flex items-center justify-center h-full text-gray-400">
                    <div className="text-center">
                      <svg
                        className="w-24 h-24 mx-auto mb-4"
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
                      <p>No Image Available</p>
                    </div>
                  </div>
                )}
                {isLocked && (
                  <div className="absolute inset-0 bg-black bg-opacity-60 flex items-center justify-center">
                    <div className="text-white text-center">
                      <svg
                        className="w-20 h-20 mx-auto mb-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                        />
                      </svg>
                      <p className="text-lg font-semibold">NFT Required</p>
                      <p className="text-sm mt-2">
                        Connect to WiFi to receive your NFT
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </Card>
          </div>

          {/* Product Details */}
          <div>
            <Card className="p-6">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                {product.name}
              </h1>

              <div className="flex items-center gap-4 mb-6">
                <span className="text-4xl font-bold text-gray-900">
                  {product.price !== undefined && product.price !== null
                    ? `¥${product.price.toLocaleString()}`
                    : '価格未設定'}
                </span>
                {isOutOfStock && (
                  <span className="bg-red-500 text-white px-3 py-1 rounded text-sm font-semibold">
                    在庫切れ
                  </span>
                )}
              </div>

              {product.description && (
                <div className="mb-6">
                  <h2 className="text-lg font-semibold text-gray-900 mb-2">
                    Description
                  </h2>
                  <p className="text-gray-600 whitespace-pre-line">
                    {product.description}
                  </p>
                </div>
              )}

              <div className="mb-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-2">
                  Availability
                </h2>
                <p className="text-gray-600">
                  {product.stock_quantity > 0
                    ? `${product.stock_quantity} in stock`
                    : 'Out of stock'}
                </p>
              </div>

              {product.required_nft_id && (
                <div className="mb-6">
                  <div
                    className={`p-4 rounded-lg ${
                      hasRequiredNFT()
                        ? 'bg-green-50 border border-green-200'
                        : 'bg-yellow-50 border border-yellow-200'
                    }`}
                  >
                    <div className="flex items-start">
                      <svg
                        className={`w-6 h-6 mr-3 flex-shrink-0 ${
                          hasRequiredNFT() ? 'text-green-600' : 'text-yellow-600'
                        }`}
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
                      </svg>
                      <div>
                        <h3
                          className={`font-semibold ${
                            hasRequiredNFT()
                              ? 'text-green-900'
                              : 'text-yellow-900'
                          }`}
                        >
                          {hasRequiredNFT()
                            ? 'NFT Verified'
                            : 'NFT Required'}
                        </h3>
                        <p
                          className={`text-sm mt-1 ${
                            hasRequiredNFT()
                              ? 'text-green-700'
                              : 'text-yellow-700'
                          }`}
                        >
                          {hasRequiredNFT()
                            ? 'You have the required NFT to purchase this product.'
                            : 'Connect to our WiFi network to receive an NFT and unlock this product.'}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {canPurchase && (
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Quantity
                  </label>
                  <div className="flex items-center gap-3">
                    <Button
                      onClick={() => handleQuantityChange(quantity - 1)}
                      disabled={quantity <= 1}
                      variant="secondary"
                      size="sm"
                    >
                      -
                    </Button>
                    <span className="text-lg font-semibold w-12 text-center">
                      {quantity}
                    </span>
                    <Button
                      onClick={() => handleQuantityChange(quantity + 1)}
                      disabled={quantity >= product.stock_quantity}
                      variant="secondary"
                      size="sm"
                    >
                      +
                    </Button>
                  </div>
                </div>
              )}

              <Button
                onClick={handleAddToCart}
                disabled={!canPurchase}
                fullWidth
                size="lg"
              >
                {isLocked
                  ? 'NFT必須'
                  : isOutOfStock
                  ? '在庫切れ'
                  : product.price !== undefined && product.price !== null
                  ? `カートに追加 - ¥${(product.price * quantity).toLocaleString()}`
                  : 'カートに追加'}
              </Button>

              {!user && (
                <p className="text-sm text-gray-600 text-center mt-4">
                  Please log in to purchase this product
                </p>
              )}

              {/* NFT Auto-Mint Info */}
              {canPurchase && user && (
                <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-start">
                    <svg className="w-5 h-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                    </svg>
                    <div>
                      <h3 className="text-sm font-semibold text-blue-900">🎁 購入特典</h3>
                      <p className="text-xs text-blue-700 mt-1">
                        この商品を購入すると、XRPL上でNFTが自動的にミントされ、あなたのウォレットに送信されます。
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
