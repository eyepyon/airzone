@extends('admin.layout')

@section('title', '一括送金統計')

@section('content')
<div class="mb-6">
    <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold text-gray-900">📊 一括送金統計</h1>
        <a href="{{ route('admin.batch-transfers.index') }}"
           class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700">
            ← 戻る
        </a>
    </div>
</div>

<!-- 統計カード -->
<div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-8">
    <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-500 text-sm mb-2">総ユーザー数</div>
        <div class="text-3xl font-bold">{{ number_format($stats['total_users']) }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-500 text-sm mb-2">紹介コード保有</div>
        <div class="text-3xl font-bold text-blue-600">{{ number_format($stats['users_with_referral_code']) }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-500 text-sm mb-2">完了紹介数</div>
        <div class="text-3xl font-bold text-green-600">{{ number_format($stats['total_referrals']) }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-500 text-sm mb-2">完了NFT数</div>
        <div class="text-3xl font-bold text-purple-600">{{ number_format($stats['total_nfts']) }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-500 text-sm mb-2">完了注文数</div>
        <div class="text-3xl font-bold text-orange-600">{{ number_format($stats['total_orders']) }}</div>
    </div>
</div>

<!-- 送金対象の推奨 -->
<div class="bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-xl font-bold mb-4">💡 送金対象の推奨</h2>
    <div class="space-y-4">
        <div class="p-4 bg-purple-50 rounded-lg">
            <h3 class="font-bold text-purple-900 mb-2">👑 VIPユーザー</h3>
            <p class="text-sm text-purple-800 mb-2">
                重要度スコアが高いユーザー（購入・紹介・NFT発行が多い）
            </p>
            <a href="{{ route('users.importance') }}"
               class="text-sm text-purple-600 hover:text-purple-800 underline">
                VIPユーザー一覧を見る →
            </a>
        </div>

        <div class="p-4 bg-green-50 rounded-lg">
            <h3 class="font-bold text-green-900 mb-2">🏆 トップ紹介者</h3>
            <p class="text-sm text-green-800 mb-2">
                紹介数が多いユーザー（コミュニティ拡大に貢献）
            </p>
            <a href="{{ route('referrals.ranking') }}"
               class="text-sm text-green-600 hover:text-green-800 underline">
                紹介ランキングを見る →
            </a>
        </div>

        <div class="p-4 bg-blue-50 rounded-lg">
            <h3 class="font-bold text-blue-900 mb-2">👥 全ユーザー</h3>
            <p class="text-sm text-blue-800 mb-2">
                紹介コードを持つ全ユーザー（{{ number_format($stats['users_with_referral_code']) }}人）
            </p>
            <p class="text-xs text-blue-700">
                ※ 大量送金の場合は時間がかかります
            </p>
        </div>
    </div>
</div>

<!-- 送金の流れ -->
<div class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-bold mb-4">📋 一括送金の流れ</h2>
    <div class="space-y-4">
        <div class="flex items-start gap-4">
            <div class="flex-shrink-0 w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold">
                1
            </div>
            <div>
                <h3 class="font-semibold">対象ユーザーを選択</h3>
                <p class="text-sm text-gray-600">VIPユーザー、トップ紹介者、または全ユーザーから選択</p>
            </div>
        </div>

        <div class="flex items-start gap-4">
            <div class="flex-shrink-0 w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold">
                2
            </div>
            <div>
                <h3 class="font-semibold">送金金額と理由を入力</h3>
                <p class="text-sm text-gray-600">XRP金額と送金理由を入力（例: 「キャンペーン報酬」）</p>
            </div>
        </div>

        <div class="flex items-start gap-4">
            <div class="flex-shrink-0 w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold">
                3
            </div>
            <div>
                <h3 class="font-semibold">プレビューで確認</h3>
                <p class="text-sm text-gray-600">送金対象と総額を確認</p>
            </div>
        </div>

        <div class="flex items-start gap-4">
            <div class="flex-shrink-0 w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold">
                4
            </div>
            <div>
                <h3 class="font-semibold">送金実行</h3>
                <p class="text-sm text-gray-600">バックエンドAPIが一括送金を実行</p>
            </div>
        </div>
    </div>
</div>
@endsection
