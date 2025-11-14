'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/stores/auth-store';
import { createWiFiSession } from '@/lib/api/wifi';
import Card, { CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import LoginButton from '@/components/auth/LoginButton';
import WelcomeScreen from '@/components/captive/WelcomeScreen';
import Loading from '@/components/ui/Loading';

export default function CaptivePortalPage() {
  const router = useRouter();
  const { isAuthenticated, user, isLoading: authLoading } = useAuthStore();
  const [agreedToTerms, setAgreedToTerms] = useState(false);
  const [isCreatingSession, setIsCreatingSession] = useState(false);
  const [sessionCreated, setSessionCreated] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Check if user is already authenticated
  useEffect(() => {
    if (isAuthenticated && user && !sessionCreated && !isCreatingSession) {
      handleCreateSession();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated, user, sessionCreated]);

  const handleCreateSession = async () => {
    if (isCreatingSession || sessionCreated) return;

    setIsCreatingSession(true);
    setError(null);

    try {
      // Create WiFi session
      await createWiFiSession();
      setSessionCreated(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'WiFiセッションの作成に失敗しました');
      setIsCreatingSession(false);
    }
  };

  const handleLoginSuccess = () => {
    // Session will be created automatically via useEffect
  };

  const handleLoginError = (error: Error) => {
    setError(error.message);
  };

  // Show loading while checking auth status
  if (authLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <Loading size="lg" text="読み込み中..." />
      </div>
    );
  }

  // Show welcome screen if authenticated and session created
  if (isAuthenticated && sessionCreated) {
    return <WelcomeScreen />;
  }

  // Show login/terms screen
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <Card>
          <CardHeader>
            <div className="text-center mb-4">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-full mb-4">
                <svg
                  className="w-8 h-8 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"
                  />
                </svg>
              </div>
              <CardTitle className="text-2xl">
                Airzone WiFiへようこそ
              </CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600 text-center mb-6">
              無料WiFiをご利用いただくには、Googleアカウントでログインしてください。
              ログイン後、自動的にNFTが発行されます。
            </p>

            {/* Terms and Conditions */}
            <div className="bg-gray-50 rounded-lg p-4 mb-6 max-h-48 overflow-y-auto">
              <h3 className="font-semibold text-gray-900 mb-2">利用規約</h3>
              <div className="text-sm text-gray-600 space-y-2">
                <p>
                  本WiFiサービスをご利用いただくにあたり、以下の利用規約に同意いただく必要があります。
                </p>
                <ul className="list-disc list-inside space-y-1 ml-2">
                  <li>本サービスは無料でご利用いただけます</li>
                  <li>違法なコンテンツへのアクセスは禁止されています</li>
                  <li>他の利用者に迷惑をかける行為は禁止されています</li>
                  <li>接続情報は統計目的で記録される場合があります</li>
                  <li>ログイン時にSuiブロックチェーン上のウォレットが自動作成されます</li>
                  <li>WiFi接続時にNFTが自動的に発行されます</li>
                  <li>発行されたNFTはECショップでの商品購入に使用できます</li>
                </ul>
                <p className="mt-3">
                  本サービスの利用により、上記の利用規約に同意したものとみなされます。
                </p>
              </div>
            </div>

            {/* Terms Checkbox */}
            <div className="mb-6">
              <label className="flex items-start cursor-pointer">
                <input
                  type="checkbox"
                  checked={agreedToTerms}
                  onChange={(e) => setAgreedToTerms(e.target.checked)}
                  className="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span className="ml-2 text-sm text-gray-700">
                  利用規約に同意します
                </span>
              </label>
            </div>

            {/* Error Message */}
            {error && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}

            {/* Login Button */}
            {!isAuthenticated && (
              <div className={!agreedToTerms ? 'opacity-50 pointer-events-none' : ''}>
                <LoginButton
                  onSuccess={handleLoginSuccess}
                  onError={handleLoginError}
                  className="w-full"
                >
                  {agreedToTerms ? 'Googleでログイン' : '利用規約に同意してください'}
                </LoginButton>
              </div>
            )}

            {/* Creating Session State */}
            {isAuthenticated && isCreatingSession && (
              <div className="text-center py-4">
                <Loading size="md" text="WiFiセッションを作成中..." />
              </div>
            )}

            {/* Info */}
            <div className="mt-6 pt-6 border-t border-gray-200">
              <div className="flex items-start text-sm text-gray-600">
                <svg
                  className="w-5 h-5 text-blue-600 mr-2 flex-shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <div>
                  <p className="font-semibold text-gray-900 mb-1">
                    NFTについて
                  </p>
                  <p>
                    ログイン後、Suiブロックチェーン上にウォレットが自動作成され、
                    記念NFTが発行されます。このNFTを使用して、
                    ECショップで特別な商品を購入することができます。
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="mt-6 text-center text-sm text-gray-600">
          <p>© 2024 Airzone. All rights reserved.</p>
        </div>
      </div>
    </div>
  );
}
