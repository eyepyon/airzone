@extends('admin.layout')

@section('title', '紹介詳細')

@section('content')
<div class="mb-6">
    <a href="{{ route('referrals.index') }}" class="text-blue-600 hover:text-blue-800 mb-4 inline-block">
        ← 紹介一覧に戻る
    </a>
    <h1 class="text-3xl font-bold mb-2">紹介詳細</h1>
</div>

<!-- ユーザー情報 -->
<div class="bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-xl font-bold mb-4">ユーザー情報</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
            <div class="text-sm text-gray-500">名前</div>
            <div class="font-medium">{{ $user->name }}</div>
        </div>
        <div>
            <div class="text-sm text-gray-500">メールアドレス</div>
            <div class="font-medium">{{ $user->email }}</div>
        </div>
        <div>
            <div class="text-sm text-gray-500">紹介コード</div>
            <div class="font-mono font-bold text-purple-600">{{ $user->referral_code }}</div>
        </div>
        <div>
            <div class="text-sm text-gray-500">現在のコイン</div>
            <div class="font-bold text-2xl">{{ number_format($user->coins ?? 0) }}</div>
        </div>
    </div>
</div>

<!-- 統計 -->
<div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
    <div class="bg-white rounded-lg shadow p-4">
        <div class="text-gray-500 text-sm">総紹介数</div>
        <div class="text-2xl font-bold">{{ number_format($stats['total_referrals']) }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-4">
        <div class="text-gray-500 text-sm">完了</div>
        <div class="text-2xl font-bold text-green-600">{{ number_format($stats['completed_referrals']) }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-4">
        <div class="text-gray-500 text-sm">保留中</div>
        <div class="text-2xl font-bold text-yellow-600">{{ number_format($stats['pending_referrals']) }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-4">
        <div class="text-gray-500 text-sm">獲得コイン</div>
        <div class="text-2xl font-bold text-purple-600">{{ number_format($stats['total_coins_earned']) }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-4">
        <div class="text-gray-500 text-sm">現在コイン</div>
        <div class="text-2xl font-bold">{{ number_format($stats['current_coins']) }}</div>
    </div>
</div>

<!-- 紹介履歴 -->
<div class="bg-white rounded-lg shadow mb-6">
    <div class="px-6 py-4 border-b">
        <h2 class="text-xl font-bold">紹介履歴</h2>
    </div>
    
    <div class="overflow-x-auto">
        <table class="min-w-full">
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">被紹介者</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ステータス</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">付与コイン</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">登録日時</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">完了日時</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
                @forelse($referrals as $referral)
                <tr>
                    <td class="px-6 py-4">
                        <div class="font-medium">{{ $referral->referred_name }}</div>
                        <div class="text-sm text-gray-500">{{ $referral->referred_email }}</div>
                    </td>
                    <td class="px-6 py-4">
                        @if($referral->status === 'completed')
                            <span class="px-2 py-1 text-xs bg-green-100 text-green-800 rounded">完了</span>
                        @elseif($referral->status === 'pending')
                            <span class="px-2 py-1 text-xs bg-yellow-100 text-yellow-800 rounded">保留中</span>
                        @else
                            <span class="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded">{{ $referral->status }}</span>
                        @endif
                    </td>
                    <td class="px-6 py-4">
                        <span class="font-semibold text-purple-600">{{ number_format($referral->coins_awarded) }}</span>
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500">
                        {{ $referral->created_at }}
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500">
                        {{ $referral->completed_at ?? '-' }}
                    </td>
                </tr>
                @empty
                <tr>
                    <td colspan="5" class="px-6 py-8 text-center text-gray-500">
                        紹介履歴がありません
                    </td>
                </tr>
                @endforelse
            </tbody>
        </table>
    </div>
</div>

<!-- コイン取引履歴 -->
<div class="bg-white rounded-lg shadow">
    <div class="px-6 py-4 border-b">
        <h2 class="text-xl font-bold">コイン取引履歴</h2>
    </div>
    
    <div class="overflow-x-auto">
        <table class="min-w-full">
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">日時</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">種類</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">説明</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">金額</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">残高</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
                @forelse($coinTransactions as $transaction)
                <tr>
                    <td class="px-6 py-4 text-sm text-gray-500">
                        {{ $transaction->created_at }}
                    </td>
                    <td class="px-6 py-4">
                        @if($transaction->transaction_type === 'referral_bonus')
                            <span class="px-2 py-1 text-xs bg-purple-100 text-purple-800 rounded">紹介ボーナス</span>
                        @elseif($transaction->transaction_type === 'purchase')
                            <span class="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">購入</span>
                        @else
                            <span class="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded">{{ $transaction->transaction_type }}</span>
                        @endif
                    </td>
                    <td class="px-6 py-4 text-sm">
                        {{ $transaction->description }}
                    </td>
                    <td class="px-6 py-4">
                        <span class="font-semibold {{ $transaction->amount > 0 ? 'text-green-600' : 'text-red-600' }}">
                            {{ $transaction->amount > 0 ? '+' : '' }}{{ number_format($transaction->amount) }}
                        </span>
                    </td>
                    <td class="px-6 py-4 font-semibold">
                        {{ number_format($transaction->balance_after) }}
                    </td>
                </tr>
                @empty
                <tr>
                    <td colspan="5" class="px-6 py-8 text-center text-gray-500">
                        取引履歴がありません
                    </td>
                </tr>
                @endforelse
            </tbody>
        </table>
    </div>
</div>
@endsection
