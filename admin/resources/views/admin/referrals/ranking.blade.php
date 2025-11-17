@extends('admin.layout')

@section('title', '紹介ランキング')

@section('content')
<div class="mb-6">
    <a href="{{ route('referrals.index') }}" class="text-blue-600 hover:text-blue-800 mb-4 inline-block">
        ← 紹介一覧に戻る
    </a>
    <h1 class="text-3xl font-bold mb-2">🏆 紹介ランキング</h1>
    <p class="text-gray-600">紹介数トップ50</p>
</div>

<div class="bg-white rounded-lg shadow overflow-hidden">
    <div class="overflow-x-auto">
        <table class="min-w-full">
            <thead class="bg-gradient-to-r from-purple-500 to-pink-500 text-white">
                <tr>
                    <th class="px-6 py-4 text-left text-sm font-bold">順位</th>
                    <th class="px-6 py-4 text-left text-sm font-bold">ユーザー</th>
                    <th class="px-6 py-4 text-left text-sm font-bold">紹介コード</th>
                    <th class="px-6 py-4 text-left text-sm font-bold">紹介数</th>
                    <th class="px-6 py-4 text-left text-sm font-bold">獲得コイン</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
                @forelse($topReferrers as $index => $referrer)
                <tr class="hover:bg-gray-50 {{ $index < 3 ? 'bg-yellow-50' : '' }}">
                    <td class="px-6 py-4">
                        <div class="flex items-center">
                            @if($index === 0)
                                <span class="text-3xl">🥇</span>
                            @elseif($index === 1)
                                <span class="text-3xl">🥈</span>
                            @elseif($index === 2)
                                <span class="text-3xl">🥉</span>
                            @else
                                <span class="text-xl font-bold text-gray-600">{{ $index + 1 }}</span>
                            @endif
                        </div>
                    </td>
                    <td class="px-6 py-4">
                        <div class="font-medium">{{ $referrer->name }}</div>
                        <div class="text-sm text-gray-500">{{ $referrer->email }}</div>
                    </td>
                    <td class="px-6 py-4">
                        <span class="px-2 py-1 text-xs font-mono bg-purple-100 text-purple-800 rounded">
                            {{ $referrer->referral_code }}
                        </span>
                    </td>
                    <td class="px-6 py-4">
                        <span class="text-2xl font-bold text-purple-600">
                            {{ number_format($referrer->referral_count) }}
                        </span>
                    </td>
                    <td class="px-6 py-4">
                        <span class="text-xl font-bold text-green-600">
                            {{ number_format($referrer->total_coins) }}
                        </span>
                    </td>
                </tr>
                @empty
                <tr>
                    <td colspan="5" class="px-6 py-8 text-center text-gray-500">
                        ランキングデータがありません
                    </td>
                </tr>
                @endforelse
            </tbody>
        </table>
    </div>
</div>
@endsection
