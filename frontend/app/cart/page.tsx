'use client';

import Layout from '@/components/layout/Layout';
import ShoppingCart from '@/components/shop/ShoppingCart';

export default function CartPage() {
  return (
    <Layout>
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">ショッピングカート</h1>
        <ShoppingCart />
      </div>
    </Layout>
  );
}
