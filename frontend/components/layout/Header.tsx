'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { useAuthStore } from '@/stores/auth-store';
import { useCartStore } from '@/stores/cart-store';

export default function Header() {
  const pathname = usePathname();
  const { user, logout } = useAuthStore();
  const { items } = useCartStore();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const cartItemCount = items.reduce((sum, item) => sum + item.quantity, 0);

  const isActive = (path: string) => {
    if (path === '/') return pathname === '/';
    return pathname.startsWith(path);
  };

  const navLinkClass = (path: string) =>
    `px-3 py-2 rounded-md text-sm font-medium transition-colors ${
      isActive(path)
        ? 'bg-blue-100 text-blue-700'
        : 'text-gray-700 hover:bg-gray-100 hover:text-blue-600'
    }`;

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <span className="text-2xl">✈️</span>
              <span className="text-2xl font-bold text-blue-600">Airzone</span>
            </Link>
          </div>

          {/* Desktop Navigation Links */}
          <div className="hidden md:flex items-center space-x-1">
            <Link href="/" className={navLinkClass('/')}>
              🏠 ホーム
            </Link>
            <Link href="/shop" className={navLinkClass('/shop')}>
              🛍️ ショップ
            </Link>
            {user && (
              <>
                <Link href="/dashboard" className={navLinkClass('/dashboard')}>
                  📊 ダッシュボード
                </Link>
                <Link href="/nfts" className={navLinkClass('/nfts')}>
                  🎨 NFT
                </Link>
                <Link href="/orders" className={navLinkClass('/orders')}>
                  📦 注文履歴
                </Link>
                <Link href="/referral" className={navLinkClass('/referral')}>
                  🎁 紹介
                </Link>
                <Link href="/staking" className={navLinkClass('/staking')}>
                  💎 ステーキング
                </Link>
              </>
            )}
          </div>

          {/* Right Side Actions */}
          <div className="flex items-center space-x-4">
            {/* Cart */}
            <Link
              href="/cart"
              className="relative p-2 text-gray-700 hover:text-blue-600 hover:bg-gray-100 rounded-md transition-colors"
            >
              <svg
                className="w-6 h-6"
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
              {cartItemCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                  {cartItemCount}
                </span>
              )}
            </Link>

            {/* User Menu - Desktop */}
            {user ? (
              <div className="hidden md:flex items-center space-x-3">
                <span className="text-sm text-gray-700 font-medium">
                  {user.name}
                </span>
                <button
                  onClick={() => {
                    logout();
                  }}
                  className="text-sm px-4 py-2 text-gray-700 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors"
                >
                  ログアウト
                </button>
              </div>
            ) : (
              <Link
                href="/login"
                className="hidden md:inline-flex text-sm text-white bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-md transition-colors font-medium"
              >
                ログイン
              </Link>
            )}

            {/* Mobile menu button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-md text-gray-700 hover:bg-gray-100"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                {mobileMenuOpen ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-200">
            <div className="flex flex-col space-y-2">
              <Link
                href="/"
                className={navLinkClass('/')}
                onClick={() => setMobileMenuOpen(false)}
              >
                🏠 ホーム
              </Link>
              <Link
                href="/shop"
                className={navLinkClass('/shop')}
                onClick={() => setMobileMenuOpen(false)}
              >
                🛍️ ショップ
              </Link>
              {user && (
                <>
                  <Link
                    href="/dashboard"
                    className={navLinkClass('/dashboard')}
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    📊 ダッシュボード
                  </Link>
                  <Link
                    href="/nfts"
                    className={navLinkClass('/nfts')}
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    🎨 NFT
                  </Link>
                  <Link
                    href="/orders"
                    className={navLinkClass('/orders')}
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    📦 注文履歴
                  </Link>
                  <Link
                    href="/referral"
                    className={navLinkClass('/referral')}
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    🎁 紹介
                  </Link>
                  <Link
                    href="/staking"
                    className={navLinkClass('/staking')}
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    💎 ステーキング
                  </Link>
                  <div className="pt-4 border-t border-gray-200">
                    <div className="px-3 py-2 text-sm text-gray-700 font-medium">
                      {user.name}
                    </div>
                    <button
                      onClick={() => {
                        logout();
                        setMobileMenuOpen(false);
                      }}
                      className="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-md transition-colors"
                    >
                      ログアウト
                    </button>
                  </div>
                </>
              )}
              {!user && (
                <Link
                  href="/login"
                  className="text-center text-sm text-white bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-md transition-colors font-medium"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  ログイン
                </Link>
              )}
            </div>
          </div>
        )}
      </nav>
    </header>
  );
}
