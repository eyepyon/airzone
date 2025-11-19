@extends('admin.layout')

@section('title', '紹介管理')

@section('content')
<div class="mb-6">
    <h1 class="text-3xl font-bold mb-2">紹介管理</h1>
    <p class="text-gray-600">ユーザーの紹介状況を管理</p>
</div>

<!-- 全体統計 -->
<div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
    <div class="bg-white rounded-lg shadow p-4">
        <div class="text-gray-500 text-sm">紹介者数</div>
        <div class="text-2xl font-bold">{{ number_format($overallStats['total_users_with_referrals']) }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-4">
        <div class="text-gray-500 text-sm">総紹介数</div>
        <div class="text-2xl font-bold">{{ number_format($overallStats['total_referrals']) }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-4">
        <div class="text-gray-500 text-sm">完了</div>
        <div class="text-2xl font-bold text-green-600">{{ number_format($overallStats['completed_referrals']) }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-4">
        <div class="text-gray-500 text-sm">保留中</div>
        <div class="text-2xl font-bold text-yellow-600">{{ number_format($overallStats['pending_referrals']) }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-4">
        <div class="text-gray-500 text-sm">付与コイン</div>
        <div class="text-2xl font-bold text-purple-600">{{ number_format($overallStats['total_coins_awarded']) }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-4">
        <div class="text-gray-500 text-sm">被紹介者</div>
        <div class="text-2xl font-bold">{{ number_format($overallStats['total_referred_users']) }}</div>
    </div>
</div>

<!-- アクションボタン -->
<div class="mb-6 flex gap-4">
    <a href="{{ route('referrals.ranking') }}" class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
        🏆 ランキング
    </a>
</div>

<!-- 紹介者一覧 -->
<div class="bg-white rounded-lg shadow overflow-hidden">
    <div class="px-6 py-4 border-b">
        <h2 class="text-xl font-bold">紹介者一覧</h2>
    </div>

    <div class="overflow-x-auto">
        <table class="min-w-full">
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ユーザー</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">紹介コード</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">総紹介数</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">完了</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">保留中</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">獲得コイン</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">現在コイン</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">操作</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
                @forelse($referralStats as $stat)
                <tr class="hover:bg-gray-50">
                    <td class="px-6 py-4">
                        <div class="font-medium">{{ $stat->name }}</div>
                        <div class="text-sm text-gray-500">{{ $stat->email }}</div>
                    </td>
                    <td class="px-6 py-4">
                        <span class="px-2 py-1 text-xs font-mono bg-purple-100 text-purple-800 rounded">
                            {{ $stat->referral_code ?? 'N/A' }}
                        </span>
                    </td>
                    <td class="px-6 py-4">
                        <span class="text-lg font-bold">{{ number_format($stat->total_referrals) }}</span>
                    </td>
                    <td class="px-6 py-4">
                        <span class="px-2 py-1 text-xs bg-green-100 text-green-800 rounded">
                            {{ number_format($stat->completed_referrals) }}
                        </span>
                    </td>
                    <td class="px-6 py-4">
                        <span class="px-2 py-1 text-xs bg-yellow-100 text-yellow-800 rounded">
                            {{ number_format($stat->pending_referrals) }}
                        </span>
                    </td>
                    <td class="px-6 py-4">
                        <span class="text-purple-600 font-semibold">
                            {{ number_format($stat->total_coins_earned) }}
                        </span>
                    </td>
                    <td class="px-6 py-4">
                        <span class="font-semibold">{{ number_format($stat->coins ?? 0) }}</span>
                    </td>
                    <td class="px-6 py-4">
                        <a href="{{ route('referrals.show', $stat->id) }}"
                           class="text-blue-600 hover:text-blue-800">
                            詳細
                        </a>
                    </td>
                </tr>
                @empty
                <tr>
                    <td colspan="8" class="px-6 py-8 text-center text-gray-500">
                        紹介データがありません
                    </td>
                </tr>
                @endforelse
            </tbody>
        </table>
    </div>

    <!-- ページネーション -->
    @if($referralStats->hasPages())
    <div class="px-6 py-4 border-t">
        {{ $referralStats->links() }}
    </div>
    @endif
</div>
@endsection
