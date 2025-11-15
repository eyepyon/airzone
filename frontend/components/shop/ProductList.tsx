'use client';

import { useState } from 'react';
import ProductCard from './ProductCard';
import Loading from '../ui/Loading';
import { useCartStore } from '../../stores/cart-store';
import type { Product } from '../../types';

interface ProductListProps {
  products?: Product[];
  loading?: boolean;
  error?: string | null;
  showNFTRequirement?: boolean;
  onProductAdded?: (product: Product) => void;
}

export default function ProductList({
  products = [],
  loading = false,
  error = null,
  showNFTRequirement = true,
  onProductAdded,
}: ProductListProps) {
  const { addItem } = useCartStore();
  const [addedProductId, setAddedProductId] = useState<string | null>(null);

  const handleAddToCart = (product: Product) => {
    addItem(product, 1);
    setAddedProductId(product.id);
    onProductAdded?.(product);

    // Clear the added state after 2 seconds
    setTimeout(() => {
      setAddedProductId(null);
    }, 2000);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <Loading size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-100 mb-4">
          <svg
            className="w-8 h-8 text-red-600"
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
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          エラーが発生しました
        </h3>
        <p className="text-gray-600">{error}</p>
      </div>
    );
  }

  if (products.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 mb-4">
          <svg
            className="w-8 h-8 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
            />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          商品が見つかりません
        </h3>
        <p className="text-gray-600">現在販売中の商品はありません</p>
      </div>
    );
  }

  return (
    <>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {products.map((product) => (
          <div key={product.id} className="relative">
            <ProductCard
              product={product}
              onAddToCart={handleAddToCart}
              showNFTRequirement={showNFTRequirement}
            />
            {addedProductId === product.id && (
              <div className="absolute top-2 right-2 bg-green-500 text-white px-3 py-1 rounded-full text-sm font-medium shadow-lg animate-fade-in">
                カートに追加しました
              </div>
            )}
          </div>
        ))}
      </div>

      <style jsx>{`
        @keyframes fade-in {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fade-in {
          animation: fade-in 0.3s ease-out;
        }
      `}</style>
    </>
  );
}
