'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import ProductList from '../../components/shop/ProductList';
import { useCartStore } from '../../stores/cart-store';
import { useAuthStore } from '../../stores/auth-store';
import { useNFTStore } from '../../stores/nft-store';
import { getActiveProducts } from '../../lib/api/products';
import type { Product } from '../../types';
import Button from '../../components/ui/Button';

import Layout from '@/components/layout/Layout';

export default function ShopPage() {
  const router = useRouter();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { user } = useAuthStore();
  const { fetchNFTs } = useNFTStore();
  const { addItem, getItemCount } = useCartStore();

  useEffect(() => {
    loadProducts();
    if (user) {
      fetchNFTs();
    }
  }, [user]);

  const loadProducts = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getActiveProducts();
      setProducts(response.products);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = (product: Product) => {
    addItem(product, 1);
  };

  const handleViewCart = () => {
    router.push('/checkout');
  };

  const cartItemCount = getItemCount();

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <div className="mb-8">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">ショップ</h1>
                <p className="mt-2 text-gray-600">
                  限定商品をご覧ください
                </p>
              </div>

              {cartItemCount > 0 && (
                <Button onClick={handleViewCart} className="relative">
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
                      d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
                    />
                  </svg>
                  カートを見る
                  <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full h-6 w-6 flex items-center justify-center">
                    {cartItemCount}
                  </span>
                </Button>
              )}
            </div>

            {!user && (
              <div className="mt-4 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <p className="text-yellow-800">
                  ログインして商品を購入し、NFT限定アイテムにアクセスしてください。
                </p>
              </div>
            )}
          </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center">
              <svg
                className="w-5 h-5 text-red-500 mr-2"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
              <p className="text-red-800">{error}</p>
            </div>
            <Button
              onClick={loadProducts}
              variant="secondary"
              size="sm"
              className="mt-2"
            >
              Retry
            </Button>
          </div>
        )}

          {/* Product List */}
          <ProductList
            products={products}
            loading={loading}
            error={error}
            showNFTRequirement={true}
            onProductAdded={handleAddToCart}
          />
        </div>
      </div>
    </Layout>
  );
}
