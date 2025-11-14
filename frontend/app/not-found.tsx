import Link from 'next/link';
import { Button } from '@/components/ui';

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="max-w-md w-full space-y-8 text-center">
        <div>
          <h1 className="text-8xl sm:text-9xl md:text-[12rem] font-bold text-gray-300">
            404
          </h1>
          <h2 className="mt-4 text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900">
            ページが見つかりません
          </h2>
          <p className="mt-4 text-base sm:text-lg text-gray-600 px-4">
            お探しのページは存在しないか、移動または削除された可能性があります。
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
          <Link href="/" className="w-full sm:w-auto">
            <Button variant="primary" className="w-full">
              ホームに戻る
            </Button>
          </Link>
          <Link href="/dashboard" className="w-full sm:w-auto">
            <Button variant="secondary" className="w-full">
              ダッシュボード
            </Button>
          </Link>
        </div>

        <div className="pt-8">
          <p className="text-sm text-gray-500">
            お困りの場合は、
            <Link href="/login" className="text-blue-600 hover:text-blue-800 underline ml-1">
              ログイン
            </Link>
            してお試しください。
          </p>
        </div>
      </div>
    </div>
  );
}
