'use client';

import { useEffect } from 'react';
import { Button } from '@/components/ui';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error('Application error:', error);
  }, [error]);

  return (
    <div className="min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 text-center">
        <div>
          <h1 className="text-6xl sm:text-7xl md:text-8xl font-bold text-red-600">
            エラー
          </h1>
          <h2 className="mt-6 text-2xl sm:text-3xl font-bold text-gray-900">
            問題が発生しました
          </h2>
          <p className="mt-4 text-base sm:text-lg text-gray-600">
            申し訳ございません。予期しないエラーが発生しました。
          </p>
          {error.message && (
            <div className="mt-4 p-4 bg-red-50 rounded-lg">
              <p className="text-sm text-red-800 break-words">
                {error.message}
              </p>
            </div>
          )}
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button
            onClick={reset}
            variant="primary"
            className="w-full sm:w-auto"
          >
            もう一度試す
          </Button>
          <Button
            onClick={() => (window.location.href = '/')}
            variant="secondary"
            className="w-full sm:w-auto"
          >
            ホームに戻る
          </Button>
        </div>

        {error.digest && (
          <p className="text-xs text-gray-400 mt-4">
            エラーID: {error.digest}
          </p>
        )}
      </div>
    </div>
  );
}
