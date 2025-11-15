@extends('admin.layout')

@section('title', '注文管理')

@section('content')
<h1 class="text-3xl font-bold mb-6">注文管理</h1>

<div class="bg-white rounded-lg shadow p-6 mb-6">
    <form method="GET" class="flex gap-4">
        <select name="status" class="px-4 py-2 border rounded-lg">
            <option value="">全てのステータス</option>
            <option value="pending" {{ request('status') == 'pending' ? 'selected' : '' }}>保留中</option>
            <option value="processing" {{ request('status') == 'processing' ? 'selected' : '' }}>処理中</option>
            <option value="completed" {{ request('status') == 'completed' ? 'selected' : '' }}>完了</option>
            <option value="failed" {{ request('status') == 'failed' ? 'selected' : '' }}>失敗</option>
            <option value="cancelled" {{ request('status') == 'cancelled' ? 'selected' : '' }}>キャンセル</option>
        </select>
        <button type="submit" class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">フィルター</button>
        <a href="{{ route('orders.index') }}" class="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">クリア</a>
    </form>
</div>

<div class="bg-white rounded-lg shadow overflow-hidden">
    <table class="min-w-full">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">注文ID</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ユーザー</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">金額</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ステータス</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">注文日時</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">操作</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
            @foreach($orders as $order)
            <tr>
                <td class="px-6 py-4 font-mono text-sm">{{ substr($order->id, 0, 8) }}...</td>
                <td class="px-6 py-4">
                    <div>{{ $order->user_name }}</div>
                    <div class="text-xs text-gray-500">{{ $order->user_email }}</div>
                </td>
                <td class="px-6 py-4 font-bold">¥{{ number_format($order->total_amount) }}</td>
                <td class="px-6 py-4">
                    <span class="px-2 py-1 text-xs rounded 
                        @if($order->status == 'completed') bg-green-100 text-green-800
                        @elseif($order->status == 'processing') bg-blue-100 text-blue-800
                        @elseif($order->status == 'pending') bg-yellow-100 text-yellow-800
                        @else bg-red-100 text-red-800
                        @endif">
                        {{ $order->status }}
                    </span>
                </td>
                <td class="px-6 py-4">{{ $order->created_at }}</td>
                <td class="px-6 py-4">
                    <a href="{{ route('orders.show', $order->id) }}" class="text-blue-600 hover:underline">詳細</a>
                </td>
            </tr>
            @endforeach
        </tbody>
    </table>
</div>

<div class="mt-6">
    {{ $orders->links() }}
</div>
@endsection
