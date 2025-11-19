@extends('admin.layout')

@section('title', 'エスクローキャンペーン詳細')

@section('content')
<div class="flex justify-between items-center mb-6">
    <h1 class="text-3xl font-bold">エスクローキャンペーン詳細</h1>
    <div class="flex gap-2">
        <a href="{{ route('admin.escrow-campaigns.edit', $campaign->id) }}" class="px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600">
            編集
        </a>
        <a href="{{ route('admin.escrow-campaigns.index') }}" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">
            戻る
        </a>
    </div>
</div>

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
    <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold mb-4">キャンペーン情報</h2>
        <table class="w-full">
            <tr class="border-b">
                <th class="py-2 text-left text-gray-600 w-1/3">キャンペーン名:</th>
                <td class="py-2">{{ $campaign->name }}</td>
            </tr>
            <tr class="border-b">
                <th class="py-2 text-left text-gray-600">説明:</th>
                <td class="py-2">{{ $campaign->description ?? '-' }}</td>
            </tr>
            <tr class="border-b">
                <th class="py-2 text-left text-gray-600">最小金額:</th>
                <td class="py-2">{{ number_format($campaign->min_amount_drops / 1000000, 2) }} XRP</td>
            </tr>
            <tr class="border-b">
                <th class="py-2 text-left text-gray-600">ロック期間:</th>
                <td class="py-2">{{ $campaign->lock_days }}日</td>
            </tr>
            <tr class="border-b">
                <th class="py-2 text-left text-gray-600">開始日時:</th>
                <td class="py-2">{{ \Carbon\Carbon::parse($campaign->start_date)->format('Y/m/d H:i') }}</td>
            </tr>
            <tr class="border-b">
                <th class="py-2 text-left text-gray-600">終了日時:</th>
                <td class="py-2">{{ \Carbon\Carbon::parse($campaign->end_date)->format('Y/m/d H:i') }}</td>
            </tr>
            <tr class="border-b">
                <th class="py-2 text-left text-gray-600">参加者数:</th>
                <td class="py-2">
                    {{ $campaign->current_participants }}
                    @if($campaign->max_participants)
                        / {{ $campaign->max_participants }}
                    @endif
                </td>
            </tr>
            <tr>
                <th class="py-2 text-left text-gray-600">ステータス:</th>
                <td class="py-2">
                    @if($campaign->is_active)
                        <span class="px-2 py-1 text-xs rounded bg-green-100 text-green-800">有効</span>
                    @else
                        <span class="px-2 py-1 text-xs rounded bg-gray-100 text-gray-800">無効</span>
                    @endif
                </td>
            </tr>
        </table>
    </div>

    <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold mb-4">NFT報酬</h2>
        @if($campaign->nft_reward_image_url)
            <div class="mb-4 text-center">
                <img src="{{ $campaign->nft_reward_image_url }}"
                     alt="{{ $campaign->nft_reward_name }}"
                     class="max-h-48 mx-auto rounded">
            </div>
        @endif
        <table class="w-full">
            <tr class="border-b">
                <th class="py-2 text-left text-gray-600 w-1/3">NFT名:</th>
                <td class="py-2">{{ $campaign->nft_reward_name }}</td>
            </tr>
            <tr class="border-b">
                <th class="py-2 text-left text-gray-600">NFT説明:</th>
                <td class="py-2">{{ $campaign->nft_reward_description ?? '-' }}</td>
            </tr>
            <tr>
                <th class="py-2 text-left text-gray-600">画像URL:</th>
                <td class="py-2">
                    @if($campaign->nft_reward_image_url)
                        <a href="{{ $campaign->nft_reward_image_url }}" target="_blank" class="text-blue-600 hover:underline text-sm">
                            {{ Str::limit($campaign->nft_reward_image_url, 50) }}
                        </a>
                    @else
                        -
                    @endif
                </td>
            </tr>
        </table>
    </div>
</div>

<div class="bg-white rounded-lg shadow">
    <div class="px-6 py-4 border-b">
        <h2 class="text-xl font-bold">参加者一覧</h2>
    </div>
    <div class="overflow-x-auto">
        <table class="min-w-full">
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ユーザー</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ウォレットアドレス</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ステーク金額</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ロック期間</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">完了予定</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ステータス</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">参加日時</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
                @forelse($stakes as $stake)
                    <tr>
                        <td class="px-6 py-4">
                            <div class="font-semibold">{{ $stake->username }}</div>
                            <div class="text-sm text-gray-500">{{ $stake->email }}</div>
                        </td>
                        <td class="px-6 py-4 text-sm">{{ Str::limit($stake->wallet_address, 20) }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ number_format($stake->amount_drops / 1000000, 2) }} XRP</td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ $stake->lock_days }}日</td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ \Carbon\Carbon::parse($stake->finish_after)->format('Y/m/d H:i') }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            @if($stake->status === 'active')
                                <span class="px-2 py-1 text-xs rounded bg-blue-100 text-blue-800">アクティブ</span>
                            @elseif($stake->status === 'completed')
                                <span class="px-2 py-1 text-xs rounded bg-green-100 text-green-800">完了</span>
                            @else
                                <span class="px-2 py-1 text-xs rounded bg-gray-100 text-gray-800">{{ $stake->status }}</span>
                            @endif
                            @if($stake->nft_awarded)
                                <span class="px-2 py-1 text-xs rounded bg-purple-100 text-purple-800 ml-1">NFT付与済</span>
                            @endif
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ \Carbon\Carbon::parse($stake->created_at)->format('Y/m/d H:i') }}</td>
                    </tr>
                @empty
                    <tr>
                        <td colspan="7" class="px-6 py-12 text-center text-gray-500">
                            参加者がいません
                        </td>
                    </tr>
                @endforelse
            </tbody>
        </table>
    </div>
    <div class="px-6 py-4">
        {{ $stakes->links() }}
    </div>
</div>
@endsection
