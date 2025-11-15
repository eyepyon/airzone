@extends('admin.layout')

@section('title', 'NFT詳細')

@section('content')
<div class="mb-6">
    <a href="{{ route('nfts.index') }}" class="text-blue-600 hover:underline">← NFT一覧に戻る</a>
</div>

<h1 class="text-3xl font-bold mb-6">NFT詳細</h1>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold mb-4">基本情報</h2>
        <dl class="space-y-3">
            <div>
                <dt class="text-sm text-gray-500">NFT ID</dt>
                <dd class="font-mono text-sm break-all">{{ $nft->id }}</dd>
            </div>
            <div>
                <dt class="text-sm text-gray-500">ユーザー</dt>
                <dd>
                    <a href="{{ route('users.show', $nft->user_id) }}" class="text-blue-600 hover:underline">
                        {{ $nft->user_name }} ({{ $nft->user_email }})
                    </a>
                </dd>
            </div>
            <div>
                <dt class="text-sm text-gray-500">ウォレットアドレス</dt>
                <dd class="font-mono text-sm break-all">{{ $nft->wallet_address }}</dd>
                <dd class="mt-1">
                    <a href="https://suiscan.xyz/testnet/account/{{ $nft->wallet_address }}" target="_blank" class="text-blue-600 hover:underline text-sm">
                        エクスプローラーで確認 →
                    </a>
                </dd>
            </div>
            <div>
                <dt class="text-sm text-gray-500">ステータス</dt>
                <dd>
                    <span class="px-2 py-1 text-xs rounded 
                        @if($nft->status == 'completed') bg-green-100 text-green-800
                        @elseif($nft->status == 'minting') bg-blue-100 text-blue-800
                        @elseif($nft->status == 'pending') bg-yellow-100 text-yellow-800
                        @else bg-red-100 text-red-800
                        @endif">
                        {{ $nft->status }}
                    </span>
                </dd>
            </div>
            <div>
                <dt class="text-sm text-gray-500">作成日時</dt>
                <dd>{{ $nft->created_at }}</dd>
            </div>
            <div>
                <dt class="text-sm text-gray-500">更新日時</dt>
                <dd>{{ $nft->updated_at }}</dd>
            </div>
        </dl>
    </div>

    <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold mb-4">ブロックチェーン情報</h2>
        <dl class="space-y-3">
            @if($nft->nft_object_id)
            <div>
                <dt class="text-sm text-gray-500">NFT Object ID</dt>
                <dd class="font-mono text-sm break-all">{{ $nft->nft_object_id }}</dd>
                <dd class="mt-1">
                    <a href="https://suiscan.xyz/testnet/object/{{ $nft->nft_object_id }}" target="_blank" class="text-blue-600 hover:underline text-sm">
                        エクスプローラーで確認 →
                    </a>
                </dd>
            </div>
            @endif

            @if($nft->transaction_digest)
            <div>
                <dt class="text-sm text-gray-500">Transaction Digest</dt>
                <dd class="font-mono text-sm break-all">{{ $nft->transaction_digest }}</dd>
                <dd class="mt-1">
                    <a href="https://suiscan.xyz/testnet/tx/{{ $nft->transaction_digest }}" target="_blank" class="text-blue-600 hover:underline text-sm">
                        トランザクション詳細 →
                    </a>
                </dd>
            </div>
            @endif

            @if($nft->error_message)
            <div>
                <dt class="text-sm text-gray-500">エラーメッセージ</dt>
                <dd class="text-sm text-red-600">{{ $nft->error_message }}</dd>
            </div>
            @endif
        </dl>
    </div>
</div>

@if($nft->nft_metadata)
<div class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-bold mb-4">メタデータ</h2>
    <pre class="bg-gray-100 p-4 rounded-lg overflow-x-auto text-sm">{{ json_encode(json_decode($nft->nft_metadata), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) }}</pre>
</div>
@endif
@endsection
