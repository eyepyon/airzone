@extends('admin.layout')

@section('title', 'ダッシュボード')

@section('content')
<h1 class="text-3xl font-bold mb-6">ダッシュボード</h1>

<!-- 効果測定指標 -->
<div class="mb-8">
    <h2 class="text-xl font-bold mb-4">効果測定</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-lg shadow p-6">
            <div class="text-blue-100 text-sm mb-1">DAU (本日)</div>
            <div class="text-3xl font-bold">{{ number_format($metrics['dau']) }}</div>
            <div class="text-blue-100 text-xs mt-2">デイリーアクティブユーザー</div>
        </div>
        <div class="bg-gradient-to-br from-purple-500 to-purple-600 text-white rounded-lg shadow p-6">
            <div class="text-purple-100 text-sm mb-1">MAU (今月)</div>
            <div class="text-3xl font-bold">{{ number_format($metrics['mau']) }}</div>
            <div class="text-purple-100 text-xs mt-2">マンスリーアクティブユーザー</div>
        </div>
        <div class="bg-gradient-to-br from-green-500 to-green-600 text-white rounded-lg shadow p-6">
            <div class="text-green-100 text-sm mb-1">DL数 (本日)</div>
            <div class="text-3xl font-bold">{{ number_format($metrics['dailyDownloads']) }}</div>
            <div class="text-green-100 text-xs mt-2">総DL: {{ number_format($metrics['totalDownloads']) }}</div>
        </div>
        <div class="bg-gradient-to-br from-orange-500 to-orange-600 text-white rounded-lg shadow p-6">
            <div class="text-orange-100 text-sm mb-1">エンゲージメント率</div>
            <div class="text-3xl font-bold">{{ $metrics['engagementRate'] }}%</div>
            <div class="text-orange-100 text-xs mt-2">DAU/MAU比率</div>
        </div>
    </div>
</div>

<!-- トレンドグラフ -->
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
    <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-bold mb-4">DAU推移 (過去7日間)</h3>
        <div class="h-64 flex items-end justify-between space-x-2">
            @foreach($metrics['dauTrend'] as $data)
            <div class="flex-1 flex flex-col items-center">
                <div class="w-full bg-blue-500 rounded-t" style="height: {{ $data['count'] > 0 ? max(10, ($data['count'] / max(array_column($metrics['dauTrend'], 'count'))) * 100) : 0 }}%"></div>
                <div class="text-xs mt-2 text-gray-600">{{ $data['date'] }}</div>
                <div class="text-xs font-bold text-gray-800">{{ $data['count'] }}</div>
            </div>
            @endforeach
        </div>
    </div>
    
    <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-bold mb-4">ダウンロード推移 (過去7日間)</h3>
        <div class="h-64 flex items-end justify-between space-x-2">
            @foreach($metrics['downloadTrend'] as $data)
            <div class="flex-1 flex flex-col items-center">
                <div class="w-full bg-green-500 rounded-t" style="height: {{ $data['count'] > 0 ? max(10, ($data['count'] / max(array_column($metrics['downloadTrend'], 'count'))) * 100) : 0 }}%"></div>
                <div class="text-xs mt-2 text-gray-600">{{ $data['date'] }}</div>
                <div class="text-xs font-bold text-gray-800">{{ $data['count'] }}</div>
            </div>
            @endforeach
        </div>
    </div>
</div>

<!-- 基本統計 -->
<div class="mb-8">
    <h2 class="text-xl font-bold mb-4">基本統計</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="bg-white rounded-lg shadow p-6">
            <div class="text-gray-500 text-sm">総ユーザー数</div>
            <div class="text-3xl font-bold">{{ number_format($stats['users']) }}</div>
        </div>
        <div class="bg-white rounded-lg shadow p-6">
            <div class="text-gray-500 text-sm">注文数</div>
            <div class="text-3xl font-bold">{{ number_format($stats['orders']) }}</div>
        </div>
        <div class="bg-white rounded-lg shadow p-6">
            <div class="text-gray-500 text-sm">商品数</div>
            <div class="text-3xl font-bold">{{ number_format($stats['products']) }}</div>
        </div>
        <div class="bg-white rounded-lg shadow p-6">
            <div class="text-gray-500 text-sm">NFT発行数</div>
            <div class="text-3xl font-bold">{{ number_format($stats['nfts']) }}</div>
        </div>
    </div>
</div>

<!-- 最近の注文 -->
<div class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-bold mb-4">最近の注文</h2>
    <div class="overflow-x-auto">
        <table class="min-w-full">
            <thead>
                <tr class="border-b">
                    <th class="text-left py-2">注文ID</th>
                    <th class="text-left py-2">ユーザー</th>
                    <th class="text-left py-2">金額</th>
                    <th class="text-left py-2">ステータス</th>
                    <th class="text-left py-2">日時</th>
                </tr>
            </thead>
            <tbody>
                @foreach($recentOrders as $order)
                <tr class="border-b">
                    <td class="py-2"><a href="{{ route('orders.show', $order->id) }}" class="text-blue-600 hover:underline">{{ substr($order->id, 0, 8) }}...</a></td>
                    <td class="py-2">{{ $order->user_name }}</td>
                    <td class="py-2">¥{{ number_format($order->total_amount) }}</td>
                    <td class="py-2"><span class="px-2 py-1 text-xs rounded bg-gray-200">{{ $order->status }}</span></td>
                    <td class="py-2">{{ $order->created_at }}</td>
                </tr>
                @endforeach
            </tbody>
        </table>
    </div>
</div>
@endsection
