@extends('admin.layout')

@section('title', '重要ユーザー')

@section('content')
<div class="mb-6">
    <h1 class="text-3xl font-bold mb-2">👑 重要ユーザー</h1>
    <p class="text-gray-600">ユーザー重要度スコアランキング</p>
</div>

<!-- レベル説明 -->
<div class="bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-xl font-bold mb-4">重要度レベル</h2>
    <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div class="text-center p-4 bg-amber-50 rounded-lg">
            <div class="text-4xl mb-2">🥉</div>
            <div class="font-bold">Bronze</div>
            <div class="text-sm text-gray-600">0-49pt</div>
        </div>
        <div class="text-center p-4 bg-gray-50 rounded-lg">
            <div class="text-4xl mb-2">🥈</div>
            <div class="font-bold">Silver</div>
            <div class="text-sm text-gray-600">50-199pt</div>
        </div>
        <div class="text-center p-4 bg-yellow-50 rounded-lg">
            <div class="text-4xl mb-2">🥇</div>
            <div class="font-bold">Gold</div>
            <div class="text-sm text-gray-600">200-499pt</div>
        </div>
        <div class="text-center p-4 bg-blue-50 rounded-lg">
            <div class="text-4xl mb-2">💎</div>
            <div class="font-bold">Platinum</div>
            <div class="text-sm text-gray-600">500-999pt</div>
        </div>
        <div class="text-center p-4 bg-purple-50 rounded-lg">
            <div class="text-4xl mb-2">👑</div>
            <div class="font-bold">Diamond</div>
            <div class="text-sm text-gray-600">1,000pt~</div>
        </div>
    </div>
</div>

<!-- スコア配点 -->
<div class="bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-xl font-bold mb-4">スコア配点</h2>
    <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
        <div class="p-3 bg-gray-50 rounded">
            <div class="text-sm text-gray-600">購入</div>
            <div class="font-bold">10pt / 回</div>
        </div>
        <div class="p-3 bg-gray-50 rounded">
            <div class="text-sm text-gray-600">紹介成功</div>
            <div class="font-bold">5pt / 件</div>
        </div>
        <div class="p-3 bg-gray-50 rounded">
            <div class="text-sm text-gray-600">NFT発行</div>
            <div class="font-bold">2pt / 回</div>
        </div>
        <div class="p-3 bg-gray-50 rounded">
            <div class="text-sm text-gray-600">購入金額</div>
            <div class="font-bold">0.01pt / 円</div>
        </div>
    </div>
</div>

<!-- ランキング -->
<div class="bg-white rounded-lg shadow overflow-hidden">
    <div class="px-6 py-4 border-b">
        <h2 class="text-xl font-bold">重要度ランキング</h2>
    </div>

    <div class="overflow-x-auto">
        <table class="min-w-full">
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">順位</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ユーザー</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">レベル</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">スコア</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">購入数</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">紹介数</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">NFT数</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">操作</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
                @forelse($topUsers as $index => $user)
                <tr class="hover:bg-gray-50">
                    <td class="px-6 py-4">
                        @if($index < 3)
                            <span class="text-2xl">
                                @if($index === 0) 🥇
                                @elseif($index === 1) 🥈
                                @else 🥉
                                @endif
                            </span>
                        @else
                            <span class="font-bold text-gray-600">{{ $index + 1 }}</span>
                        @endif
                    </td>
                    <td class="px-6 py-4">
                        <div class="font-medium">{{ $user->name }}</div>
                        <div class="text-sm text-gray-500">{{ $user->email }}</div>
                    </td>
                    <td class="px-6 py-4">
                        <div class="flex items-center gap-2">
                            <span class="text-2xl">
                                @if($user->importance_level === 'diamond') 👑
                                @elseif($user->importance_level === 'platinum') 💎
                                @elseif($user->importance_level === 'gold') 🥇
                                @elseif($user->importance_level === 'silver') 🥈
                                @else 🥉
                                @endif
                            </span>
                            <span class="font-semibold capitalize">{{ $user->importance_level }}</span>
                        </div>
                    </td>
                    <td class="px-6 py-4">
                        <span class="text-2xl font-bold text-purple-600">
                            {{ number_format($user->importance_score) }}
                        </span>
                    </td>
                    <td class="px-6 py-4">{{ number_format($user->purchase_count) }}</td>
                    <td class="px-6 py-4">{{ number_format($user->referral_count) }}</td>
                    <td class="px-6 py-4">{{ number_format($user->nft_count) }}</td>
                    <td class="px-6 py-4">
                        <a href="{{ route('users.show', $user->id) }}"
                           class="text-blue-600 hover:text-blue-800">
                            詳細
                        </a>
                    </td>
                </tr>
                @empty
                <tr>
                    <td colspan="8" class="px-6 py-8 text-center text-gray-500">
                        データがありません
                    </td>
                </tr>
                @endforelse
            </tbody>
        </table>
    </div>
</div>
@endsection
