@extends('admin.layout')

@section('title', '一括送金履歴')

@section('content')
<div class="mb-6">
    <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold text-gray-900">一括送金履歴</h1>
        <div class="flex space-x-3">
            <a href="{{ route('admin.batch-transfers.stats') }}" class="inline-flex items-center px-4 py-2 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 transition-colors">
                <i class="fas fa-chart-bar mr-2"></i> 統計
            </a>
            <a href="{{ route('admin.batch-transfers.create') }}" class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                <i class="fas fa-paper-plane mr-2"></i> 新規送金
            </a>
        </div>
    </div>
</div>

<div class="bg-white rounded-lg shadow-md overflow-hidden">
    <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ユーザー</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ウォレット</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">金額 (XRP)</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">トランザクション</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">チケット</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">理由</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ステータス</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">日時</th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                @forelse($transfers as $transfer)
                    <tr class="hover:bg-gray-50">
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ $transfer['id'] }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="text-sm font-medium text-gray-900">{{ $transfer['email'] }}</div>
                            @if(isset($transfer['importance_level']))
                                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium 
                                    {{ $transfer['importance_level'] == 'Diamond' ? 'bg-blue-100 text-blue-800' : 
                                       ($transfer['importance_level'] == 'Platinum' ? 'bg-cyan-100 text-cyan-800' : 
                                       ($transfer['importance_level'] == 'Gold' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800')) }}">
                                    {{ $transfer['importance_level'] }}
                                </span>
                            @endif
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-500">
                            {{ substr($transfer['wallet_address'], 0, 10) }}...
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">
                            {{ number_format($transfer['amount_xrp'], 6) }} XRP
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm">
                            <a href="https://testnet.xrpl.org/transactions/{{ $transfer['transaction_hash'] }}" 
                               target="_blank" 
                               class="text-blue-600 hover:text-blue-800 font-mono">
                                {{ substr($transfer['transaction_hash'], 0, 10) }}...
                                <i class="fas fa-external-link-alt ml-1"></i>
                            </a>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {{ $transfer['ticket_sequence'] ?? '-' }}
                        </td>
                        <td class="px-6 py-4 text-sm text-gray-500">
                            {{ $transfer['reason'] }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            @if($transfer['status'] == 'success')
                                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                    成功
                                </span>
                            @else
                                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                    失敗
                                </span>
                            @endif
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {{ date('Y-m-d H:i', strtotime($transfer['created_at'])) }}
                        </td>
                    </tr>
                @empty
                    <tr>
                        <td colspan="9" class="px-6 py-8 text-center text-gray-500">
                            送金履歴がありません
                        </td>
                    </tr>
                @endforelse
            </tbody>
        </table>
    </div>

    @if($total > $limit)
        <div class="bg-white px-6 py-4 flex items-center justify-between border-t border-gray-200">
            <div class="text-sm text-gray-700">
                {{ $offset + 1 }} - {{ min($offset + $limit, $total) }} / {{ $total }} 件
            </div>
            <nav class="flex space-x-2">
                @if($offset > 0)
                    <a href="?offset={{ max(0, $offset - $limit) }}&limit={{ $limit }}" 
                       class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors">
                        前へ
                    </a>
                @endif
                @if($offset + $limit < $total)
                    <a href="?offset={{ $offset + $limit }}&limit={{ $limit }}" 
                       class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                        次へ
                    </a>
                @endif
            </nav>
        </div>
    @endif
</div>
@endsection
