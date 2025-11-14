import Link from 'next/link';
import { Button } from '@/components/ui';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Hero Section */}
      <section className="container mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-24">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-4 sm:mb-6">
            Airzone
          </h1>
          <p className="text-lg sm:text-xl md:text-2xl text-gray-600 mb-6 sm:mb-8 px-4">
            WiFi接続でNFTを受け取り、限定商品にアクセス
          </p>
          <p className="text-base sm:text-lg text-gray-500 mb-8 sm:mb-12 px-4 max-w-2xl mx-auto">
            店舗のWiFiに接続するだけで、Sui ブロックチェーン上のNFTが自動配布されます。
            NFTを使って特別な商品を購入できます。
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center px-4">
            <Link href="/login" className="w-full sm:w-auto">
              <Button variant="primary" className="w-full sm:w-auto text-base sm:text-lg px-6 sm:px-8 py-3">
                ログイン
              </Button>
            </Link>
            <Link href="/shop" className="w-full sm:w-auto">
              <Button variant="secondary" className="w-full sm:w-auto text-base sm:text-lg px-6 sm:px-8 py-3">
                ショップを見る
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8 lg:gap-12">
          {/* Feature 1 */}
          <div className="bg-white p-6 sm:p-8 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div className="text-4xl sm:text-5xl mb-4">📶</div>
            <h3 className="text-xl sm:text-2xl font-bold mb-3 sm:mb-4 text-gray-900">
              WiFi接続
            </h3>
            <p className="text-sm sm:text-base text-gray-600">
              店舗のWiFiに接続するだけで、自動的にキャプティブポータルが表示されます。
            </p>
          </div>

          {/* Feature 2 */}
          <div className="bg-white p-6 sm:p-8 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div className="text-4xl sm:text-5xl mb-4">🎨</div>
            <h3 className="text-xl sm:text-2xl font-bold mb-3 sm:mb-4 text-gray-900">
              NFT配布
            </h3>
            <p className="text-sm sm:text-base text-gray-600">
              認証後、Sui ブロックチェーン上のNFTが自動的にあなたのウォレットに配布されます。
            </p>
          </div>

          {/* Feature 3 */}
          <div className="bg-white p-6 sm:p-8 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div className="text-4xl sm:text-5xl mb-4">🛍️</div>
            <h3 className="text-xl sm:text-2xl font-bold mb-3 sm:mb-4 text-gray-900">
              限定ショップ
            </h3>
            <p className="text-sm sm:text-base text-gray-600">
              NFTを使って、限定商品を購入できます。Stripe決済で安全にお買い物。
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-20">
        <div className="bg-blue-600 rounded-2xl p-8 sm:p-12 lg:p-16 text-center text-white">
          <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-4 sm:mb-6">
            今すぐ始めましょう
          </h2>
          <p className="text-base sm:text-lg md:text-xl mb-6 sm:mb-8 max-w-2xl mx-auto px-4">
            Googleアカウントでログインして、あなた専用のウォレットを作成しましょう。
          </p>
          <Link href="/login">
            <Button 
              variant="secondary" 
              className="bg-white text-blue-600 hover:bg-gray-100 text-base sm:text-lg px-6 sm:px-8 py-3"
            >
              無料で始める
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 py-8 sm:py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <p className="text-sm sm:text-base text-gray-600 text-center sm:text-left">
              © 2024 Airzone. All rights reserved.
            </p>
            <div className="flex gap-4 sm:gap-6 flex-wrap justify-center">
              <Link href="/dashboard" className="text-sm sm:text-base text-gray-600 hover:text-gray-900">
                ダッシュボード
              </Link>
              <Link href="/nfts" className="text-sm sm:text-base text-gray-600 hover:text-gray-900">
                NFT
              </Link>
              <Link href="/shop" className="text-sm sm:text-base text-gray-600 hover:text-gray-900">
                ショップ
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
