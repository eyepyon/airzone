@extends('admin.layout')

@section('title', 'エスクローキャンペーン管理')

@section('content')
<div class="flex justify-between items-center mb-6">
    <h1 class="text-3xl font-bold">エスクローキャンペーン管理</h1>
    <div class="flex gap-2">
        <a href="{{ route('admin.escrow-campaigns.stats') }}" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            統計
        </a>
        <a href="{{ route('admin.escrow-campaigns.create') }}" class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            新規作成
        </a>
    </div>
</div>

<div class="bg-white rounded-lg shadow overflow-hidden">
    <table class="min-w-full">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">キャンペーン名</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">最小金額</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ロック期間</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">NFT報酬</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">期間</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">参加者数</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ステータス</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">操作</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
            @forelse($campaigns as $campaign)
                <tr>
                    <td class="px-6 py-4">
                        <div class="font-semibold text-gray-900">{{ $campaign->name }}</div>
                        @if($campaign->description)
                            <div class="text-sm text-gray-500">{{ Str::limit($campaign->description, 50) }}</div>
                        @endif
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ number_format($campaign->min_amount_drops / 1000000, 2) }} XRP</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ $campaign->lock_days }}日</td>
                    <td class="px-6 py-4">{{ $campaign->nft_reward_name }}</td>
                    <td class="px-6 py-4 text-sm whitespace-nowrap">
                        {{ \Carbon\Carbon::parse($campaign->start_date)->format('Y/m/d') }}<br>
                        ～ {{ \Carbon\Carbon::parse($campaign->end_date)->format('Y/m/d') }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        {{ $campaign->current_participants }}
                        @if($campaign->max_participants)
                            / {{ $campaign->max_participants }}
                        @endif
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        @if($campaign->is_active)
                            <span class="px-2 py-1 text-xs rounded bg-green-100 text-green-800">有効</span>
                        @else
                            <span class="px-2 py-1 text-xs rounded bg-gray-100 text-gray-800">無効</span>
                        @endif
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <a href="{{ route('admin.escrow-campaigns.show', $campaign->id) }}" class="text-blue-600 hover:underline mr-3" title="詳細">詳細</a>
                        <a href="{{ route('admin.escrow-campaigns.edit', $campaign->id) }}" class="text-blue-600 hover:underline mr-3" title="編集">編集</a>
                        <form action="{{ route('admin.escrow-campaigns.destroy', $campaign->id) }}"
                              method="POST" class="inline"
                              onsubmit="return confirm('本当に削除しますか？');">
                            @csrf
                            @method('DELETE')
                            <button type="submit" class="text-red-600 hover:underline">削除</button>
                        </form>
                    </td>
                </tr>
            @empty
                <tr>
                    <td colspan="8" class="px-6 py-12 text-center text-gray-500">
                        キャンペーンがありません
                    </td>
                </tr>
            @endforelse
        </tbody>
    </table>
</div>

<div class="mt-6">
    {{ $campaigns->links() }}
</div>
@endsection
