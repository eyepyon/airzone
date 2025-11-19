'use client';

import { useState, useEffect } from 'react';
import { xamanWallet, XamanWalletState } from '@/lib/xaman-wallet';

export default function XamanWalletButton() {
  const [walletState, setWalletState] = useState<XamanWalletState>(
    xamanWallet.getState()
  );
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    // 初期状態を取得
    setWalletState(xamanWallet.getState());
  }, []);

  const handleConnect = () => {
    setShowModal(true);
  };

  const handleManualConnect = async () => {
    setLoading(true);
    try {
      const state = await xamanWallet.connectManual();
      setWalletState(state);
      setShowModal(false);
      
      // ページをリロードして最新の状態を反映
      setTimeout(() => window.location.reload(), 1000);
    } catch (error) {
      console.error('Failed to connect wallet:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDisconnect = async () => {
    if (!confirm('Xaman Walletの接続を解除しますか？')) {
      return;
    }

    try {
      await xamanWallet.disconnect();
      setWalletState(xamanWallet.getState());
      
      // ページをリロードして最新の状態を反映
      setTimeout(() => window.location.reload(), 500);
    } catch (error) {
      console.error('Failed to disconnect wallet:', error);
    }
  };

  if (walletState.connected && walletState.address) {
    return (
      <div className="flex flex-col sm:flex-row items-center gap-4">
        <div className="flex items-center gap-2 px-4 py-2 bg-green-100 rounded-lg">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm font-medium text-green-800 font-mono">
            {walletState.address.slice(0, 8)}...{walletState.address.slice(-6)}
          </span>
        </div>
        <button
          onClick={handleDisconnect}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition"
        >
          切断
        </button>
      </div>
    );
  }

  return (
    <>
      <button
        onClick={handleConnect}
        disabled={loading}
        className="flex items-center gap-2 px-6 py-3 text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition shadow-lg hover:shadow-xl"
      >
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M21 18v1a2 2 0 01-2 2H5a2 2 0 01-2-2v-1a2 2 0 012-2h14a2 2 0 012 2zM5 10h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v1a2 2 0 002 2z"/>
        </svg>
        <span>Xaman Walletを接続</span>
      </button>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                Xaman Walletを接続
              </h3>
              <button
                onClick={() => setShowModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="space-y-4">
              <p className="text-sm text-gray-600">
                Xaman Walletアドレスを入力してください
              </p>

              <button
                onClick={handleManualConnect}
                disabled={loading}
                className="w-full px-4 py-3 text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition"
              >
                {loading ? '接続中...' : 'アドレスを入力'}
              </button>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-xs text-blue-700">
                  💡 Xaman Walletアプリをお持ちでない場合は、
                  <a href="https://xaman.app/" target="_blank" rel="noopener noreferrer" className="underline font-medium">
                    こちら
                  </a>
                  からダウンロードしてください。
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
