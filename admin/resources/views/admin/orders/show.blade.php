@extends('admin.layout')

@section('title', '注文詳細')

@section('content')
<div class="mb-6">
    <a href="{{ route('orders.index') }}" class="text-blue-600 hover:underline">← 注文一覧に戻る</a>
</div>

<h1 class="text-3xl font-bold mb-6">注文詳細</h1>

<div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
    <div class="lg:col-span-2 bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold mb-4">注文情報</h2>
        <dl class="space-y-3">
            <div>
                <dt class="text-sm text-gray-500">注文ID</dt>
                <dd class="font-mono text-sm">{{ $order->id }}</dd>
            </div>
            <div>
                <dt class="text-sm text-gray-500">ユーザー</dt>
                <dd>
                    <a href="{{ route('users.show', $order->user_id) }}" class="text-blue-600 hover:underline">
                        {{ $order->user_name }} ({{ $order->user_email }})
                    </a>
                </dd>
            </div>
            <div>
                <dt class="text-sm text-gray-500">合計金額</dt>
                <dd class="text-2xl font-bold">¥{{ number_format($order->total_amount) }}</dd>
            </div>
            <div>
                <dt class="text-sm text-gray-500">注文日時</dt>
                <dd>{{ $order->created_at }}</dd>
            </div>
            <div>
                <dt class="text-sm text-gray-500">更新日時</dt>
                <dd>{{ $order->updated_at }}</dd>
            </div>
        </dl>
    </div>

    <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold mb-4">ステータス変更</h2>
        <form method="POST" action="{{ route('orders.update', $order->id) }}">
            @csrf
            @method('PUT')
            <select name="status" class="w-full px-4 py-2 border rounded-lg mb-4">
                <option value="pending" {{ $order->status == 'pending' ? 'selected' : '' }}>保留中</option>
                <option value="processing" {{ $order->status == 'processing' ? 'selected' : '' }}>処理中</option>
                <option value="completed" {{ $order->status == 'completed' ? 'selected' : '' }}>完了</option>
                <option value="failed" {{ $order->status == 'failed' ? 'selected' : '' }}>失敗</option>
                <option value="cancelled" {{ $order->status == 'cancelled' ? 'selected' : '' }}>キャンセル</option>
            </select>
            <button type="submit" class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">更新</button>
        </form>
    </div>
</div>

<div class="bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-xl font-bold mb-4">注文商品</h2>
    <table class="min-w-full">
        <thead class="border-b">
            <tr>
                <th class="text-left py-2">商品名</th>
                <th class="text-left py-2">単価</th>
                <th class="text-left py-2">数量</th>
                <th class="text-left py-2">小計</th>
            </tr>
        </thead>
        <tbody class="divide-y">
            @foreach($items as $item)
            <tr>
                <td class="py-2">{{ $item->product_name }}</td>
                <td class="py-2">¥{{ number_format($item->unit_price) }}</td>
                <td class="py-2">{{ $item->quantity }}</td>
                <td class="py-2 font-bold">¥{{ number_format($item->subtotal) }}</td>
            </tr>
            @endforeach
        </tbody>
        <tfoot class="border-t">
            <tr>
                <td colspan="3" class="py-2 text-right font-bold">合計</td>
                <td class="py-2 text-xl font-bold">¥{{ number_format($order->total_amount) }}</td>
            </tr>
        </tfoot>
    </table>
</div>

@if($payment)
<div class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-bold mb-4">決済情報</h2>
    <dl class="space-y-3">
        <div>
            <dt class="text-sm text-gray-500">決済ID</dt>
            <dd class="font-mono text-sm">{{ $payment->id }}</dd>
        </div>
        <div>
            <dt class="text-sm text-gray-500">Stripe Payment Intent ID</dt>
            <dd class="font-mono text-sm">{{ $payment->stripe_payment_intent_id }}</dd>
        </div>
        <div>
            <dt class="text-sm text-gray-500">金額</dt>
            <dd>¥{{ number_format($payment->amount) }}</dd>
        </div>
        <div>
            <dt class="text-sm text-gray-500">ステータス</dt>
            <dd><span class="px-2 py-1 text-xs rounded bg-gray-200">{{ $payment->status }}</span></dd>
        </div>
        <div>
            <dt class="text-sm text-gray-500">作成日時</dt>
            <dd>{{ $payment->created_at }}</dd>
        </div>
    </dl>
</div>
@endif
@endsection
