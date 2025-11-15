@extends('admin.layout')

@section('title', 'ユーザー詳細')

@section('content')
<div class="mb-6">
    <a href="{{ route('users.index') }}" class="text-blue-600 hover:underline">← ユーザー一覧に戻る</a>
</div>

<h1 class="text-3xl font-bold mb-6">ユーザー詳細</h1>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
    <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold mb-4">基本情報</h2>
        <dl class="space-y-3">
            <div>
                <dt class="text-sm text-gray-500">ユーザーID</dt>
                <dd class="font-mono text-sm">{{ $user->id }}</dd>
            </div>
            <div>
                <dt class="text-sm text-gray-500">名前</dt>
                <dd>{{ $user->name }}</dd>
            </div>
            <div>
                <dt class="text-sm text-gray-500">メールアドレス</dt>
                <dd>{{ $user->email }}</dd>
            </div>
            <div>
                <dt class="text-sm text-gray-500">Google ID</dt>
                <dd class="font-mono text-sm">{{ $user->google_id }}</dd>
            </div>
            <div>
                <dt class="text-sm text-gray-500">登録日時</dt>
                <dd>{{ $user->created_at }}</dd>
            </div>
        </dl>
    </div>

    @if($wallet)
    <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold mb-4">ウォレット情報</h2>
        <dl class="space-y-3">
            <div>
                <dt class="text-sm text-gray-500">ウォレットアドレス</dt>
                <dd class="font-mono text-sm break-all">{{ $wallet->address }}</dd>
            </div>
            <div>
                <dt class="text-sm text-gray-500">作成日時</dt>
                <dd>{{ $wallet->created_at }}</dd>
            </div>
            <div>
                <a href="https://suiscan.xyz/testnet/account/{{ $wallet->address }}" target="_blank" class="text-blue-600 hover:underline text-sm">
                    ブロックエクスプローラーで確認 →
                </a>
            </div>
        </dl>
    </div>
    @endif
</div>

<div class="bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-xl font-bold mb-4">注文履歴 ({{ count($orders) }}件)</h2>
    @if(count($orders) > 0)
    <table class="min-w-full">
        <thead class="border-b">
            <tr>
                <th class="text-left py-2">注文ID</th>
                <th class="text-left py-2">金額</th>
                <th class="text-left py-2">ステータス</th>
                <th class="text-left py-2">日時</th>
            </tr>
        </thead>
        <tbody class="divide-y">
            @foreach($orders as $order)
            <tr>
                <td class="py-2"><a href="{{ route('orders.show', $order->id) }}" class="text-blue-600 hover:underline">{{ substr($order->id, 0, 8) }}...</a></td>
                <td class="py-2">¥{{ number_format($order->total_amount) }}</td>
                <td class="py-2"><span class="px-2 py-1 text-xs rounded bg-gray-200">{{ $order->status }}</span></td>
                <td class="py-2">{{ $order->created_at }}</td>
            </tr>
            @endforeach
        </tbody>
    </table>
    @else
    <p class="text-gray-500">注文履歴がありません</p>
    @endif
</div>

<div class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-bold mb-4">NFT ({{ count($nfts) }}件)</h2>
    @if(count($nfts) > 0)
    <table class="min-w-full">
        <thead class="border-b">
            <tr>
                <th class="text-left py-2">NFT ID</th>
                <th class="text-left py-2">ステータス</th>
                <th class="text-left py-2">トランザクション</th>
                <th class="text-left py-2">日時</th>
            </tr>
        </thead>
        <tbody class="divide-y">
            @foreach($nfts as $nft)
            <tr>
                <td class="py-2"><a href="{{ route('nfts.show', $nft->id) }}" class="text-blue-600 hover:underline">{{ substr($nft->id, 0, 8) }}...</a></td>
                <td class="py-2"><span class="px-2 py-1 text-xs rounded bg-gray-200">{{ $nft->status }}</span></td>
                <td class="py-2">
                    @if($nft->transaction_digest)
                        <span class="font-mono text-xs">{{ substr($nft->transaction_digest, 0, 10) }}...</span>
                    @else
                        <span class="text-gray-400">-</span>
                    @endif
                </td>
                <td class="py-2">{{ $nft->created_at }}</td>
            </tr>
            @endforeach
        </tbody>
    </table>
    @else
    <p class="text-gray-500">NFTがありません</p>
    @endif
</div>
@endsection
