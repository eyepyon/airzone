'use client';

import { useState, useEffect } from 'react';
import { xamanWallet, XamanWalletState } from '@/lib/xaman-wallet';

export default function XamanWalletButton() {
  const [walletState, setWalletState] = useState<XamanWalletState>(
    xamanWallet.getState()
  );
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // 初期状態を取得
    setWalletState(xamanWallet.getState());
  }, []);

  const handleConnect = async () => {
    setLoading(true);
    try {
      const state = await xamanWallet.connect();
      setWalletState(state);
      
      // ページをリロードして最新の状態を反映
      setTimeout(() => window.location.reload(), 1000);
    } catch (error) {
      console.error('Failed to connect wallet:', error);
      // エラーはxamanWallet.connect()内で表示される
    } finally {
      setLoading(false);
    }
  };

  const handleDisconnect = () => {
    xamanWallet.disconnect();
    setWalletState({
      connected: false,
      address: null,
      publicKey: null,
    });
    
    // ページをリロードして最新の状態を反映
    setTimeout(() => window.location.reload(), 500);
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
    <button
      onClick={handleConnect}
      disabled={loading}
      className="flex items-center gap-2 px-6 py-3 text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition shadow-lg hover:shadow-xl"
    >
      {loading ? (
        <>
          <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>接続中...</span>
        </>
      ) : (
        <>
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M21 18v1a2 2 0 01-2 2H5a2 2 0 01-2-2v-1a2 2 0 012-2h14a2 2 0 012 2zM5 10h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v1a2 2 0 002 2z"/>
          </svg>
          <span>Xaman Walletを接続</span>
        </>
      )}
    </button>
  );
}
