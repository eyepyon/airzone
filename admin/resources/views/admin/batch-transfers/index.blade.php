@extends('admin.layout')

@section('title', '一括送金管理')

@section('content')
<div class="mb-6">
    <h1 class="text-3xl font-bold mb-2">💸 一括送金管理</h1>
    <p class="text-gray-600">ユーザーへのXRP一括送金機能</p>
</div>

<!-- 統計情報 -->
<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
    <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-500 text-sm">総ユーザー数</div>
        <div class="text-3xl font-bold">{{ number_format($stats['total_users']) }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-500 text-sm">紹介コード保有</div>
        <div class="text-3xl font-bold text-blue-600">{{ number_format($stats['users_with_referral_code']) }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-500 text-sm">完了紹介数</div>
        <div class="text-3xl font-bold text-green-600">{{ number_format($stats['total_referrals']) }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-500 text-sm">完了NFT数</div>
        <div class="text-3xl font-bold text-purple-600">{{ number_format($stats['total_nfts']) }}</div>
    </div>
</div>

<!-- 送金オプション -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <!-- VIPユーザーへの送金 -->
    <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold mb-4">👑 VIPユーザーへの送金</h2>
        <p class="text-gray-600 mb-4">重要度スコアが高いユーザーに一括送金</p>
        <a href="{{ route('users.importance') }}"
           class="inline-block px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
            VIPユーザーを確認
        </a>
    </div>

    <!-- トップ紹介者への送金 -->
    <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold mb-4">🏆 トップ紹介者への送金</h2>
        <p class="text-gray-600 mb-4">紹介数が多いユーザーに一括送金</p>
        <a href="{{ route('referrals.ranking') }}"
           class="inline-block px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700">
            紹介ランキングを確認
        </a>
    </div>

    <!-- 全ユーザーへの送金 -->
    <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold mb-4">📢 全ユーザーへの送金</h2>
        <p class="text-gray-600 mb-4">紹介コードを持つ全ユーザーに一括送金</p>
        <button onclick="alert('この機能は現在開発中です')"
                class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            全ユーザーに送金
        </button>
    </div>

    <!-- カスタム送金 -->
    <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold mb-4">⚙️ カスタム送金</h2>
        <p class="text-gray-600 mb-4">特定のユーザーを選択して送金</p>
        <a href="{{ route('admin.batch-transfers.create') }}"
           class="inline-block px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700">
            カスタム送金
        </a>
    </div>
</div>

<!-- 注意事項 -->
<div class="mt-8 bg-yellow-50 border border-yellow-200 rounded-lg p-6">
    <h3 class="text-lg font-bold text-yellow-900 mb-2">⚠️ 注意事項</h3>
    <ul class="text-sm text-yellow-800 space-y-1">
        <li>• 一括送金は取り消しできません</li>
        <li>• 送金前に必ず対象ユーザーと金額を確認してください</li>
        <li>• XRPLネットワークの手数料が別途かかります</li>
        <li>• 大量送金の場合は時間がかかる場合があります</li>
    </ul>
</div>

<!-- バックエンドAPI連携について -->
<div class="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-6">
    <h3 class="text-lg font-bold text-blue-900 mb-2">📡 バックエンドAPI連携</h3>
    <p class="text-sm text-blue-800">
        実際の送金処理はバックエンドAPI（Flask）で実行されます。<br>
        バックエンドAPIエンドポイント: <code class="bg-blue-100 px-2 py-1 rounded">/api/v1/batch-transfer/*</code>
    </p>
</div>
@endsection
