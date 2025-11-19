@extends('admin.layout')

@section('title', 'エスクローキャンペーン統計')

@section('content')
<div class="flex justify-between items-center mb-6">
    <h1 class="text-3xl font-bold">エスクローキャンペーン統計</h1>
    <a href="{{ route('admin.escrow-campaigns.index') }}" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">
        戻る
    </a>
</div>

<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
    <div class="bg-white rounded-lg shadow p-6 text-center">
        <div class="text-sm text-gray-600 mb-2">総キャンペーン数</div>
        <div class="text-3xl font-bold text-gray-900">{{ $totalCampaigns }}</div>
        <div class="text-sm text-green-600 mt-1">有効: {{ $activeCampaigns }}</div>
    </div>

    <div class="bg-white rounded-lg shadow p-6 text-center">
        <div class="text-sm text-gray-600 mb-2">総ステーク数</div>
        <div class="text-3xl font-bold text-gray-900">{{ $totalStakes }}</div>
        <div class="text-sm text-blue-600 mt-1">アクティブ: {{ $activeStakes }}</div>
    </div>

    <div class="bg-white rounded-lg shadow p-6 text-center">
        <div class="text-sm text-gray-600 mb-2">完了ステーク数</div>
        <div class="text-3xl font-bold text-gray-900">{{ $completedStakes }}</div>
        <div class="text-sm text-green-600 mt-1">
            {{ $totalStakes > 0 ? number_format(($completedStakes / $totalStakes) * 100, 1) : 0 }}%
        </div>
    </div>

    <div class="bg-white rounded-lg shadow p-6 text-center">
        <div class="text-sm text-gray-600 mb-2">総ロック額</div>
        <div class="text-3xl font-bold text-gray-900">{{ number_format($totalLockedXRP, 2) }}</div>
        <div class="text-sm text-blue-600 mt-1">XRP</div>
    </div>
</div>

<div class="bg-white rounded-lg shadow">
    <div class="px-6 py-4 border-b">
        <h2 class="text-xl font-bold">キャンペーン別統計</h2>
    </div>
    <div class="overflow-x-auto">
        <table class="min-w-full">
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">キャンペーン名</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ステータス</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">総ステーク数</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">アクティブ</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">完了</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ロック中XRP</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">完了率</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
                @forelse($campaignStats as $stat)
                    <tr>
                        <td class="px-6 py-4">{{ $stat->name }}</td>
                        <td class="px-6 py-4">
                            @if($stat->is_active)
                                <span class="px-2 py-1 text-xs rounded bg-green-100 text-green-800">有効</span>
                            @else
                                <span class="px-2 py-1 text-xs rounded bg-gray-100 text-gray-800">無効</span>
                            @endif
                        </td>
                        <td class="px-6 py-4">{{ $stat->total_stakes }}</td>
                        <td class="px-6 py-4">
                            <span class="px-2 py-1 text-xs rounded bg-blue-100 text-blue-800">{{ $stat->active_stakes }}</span>
                        </td>
                        <td class="px-6 py-4">
                            <span class="px-2 py-1 text-xs rounded bg-green-100 text-green-800">{{ $stat->completed_stakes }}</span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ number_format($stat->locked_drops / 1000000, 2) }} XRP</td>
                        <td class="px-6 py-4">
                            @if($stat->total_stakes > 0)
                                <div class="flex items-center">
                                    <div class="w-full bg-gray-200 rounded-full h-5 mr-2">
                                        <div class="bg-green-500 h-5 rounded-full text-xs text-white flex items-center justify-center"
                                             style="width: {{ ($stat->completed_stakes / $stat->total_stakes) * 100 }}%">
                                            {{ number_format(($stat->completed_stakes / $stat->total_stakes) * 100, 1) }}%
                                        </div>
                                    </div>
                                </div>
                            @else
                                <span class="text-gray-400">-</span>
                            @endif
                        </td>
                    </tr>
                @empty
                    <tr>
                        <td colspan="7" class="px-6 py-12 text-center text-gray-500">
                            データがありません
                        </td>
                    </tr>
                @endforelse
            </tbody>
        </table>
    </div>
</div>
@endsection
