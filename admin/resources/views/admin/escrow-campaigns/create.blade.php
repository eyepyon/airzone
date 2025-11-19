@extends('admin.layout')

@section('title', 'エスクローキャンペーン作成')

@section('content')
<div class="mb-6">
    <a href="{{ route('admin.escrow-campaigns.index') }}" class="text-blue-600 hover:underline">← キャンペーン一覧に戻る</a>
</div>

<h1 class="text-3xl font-bold mb-6">エスクローキャンペーン作成</h1>

<div class="bg-white rounded-lg shadow p-6">
    <form action="{{ route('admin.escrow-campaigns.store') }}" method="POST">
        @csrf

        <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
                <label class="block text-gray-700 font-bold mb-2">キャンペーン名 <span class="text-red-500">*</span></label>
                <input type="text" name="name" value="{{ old('name') }}" required
                       class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500 @error('name') border-red-500 @enderror">
                @error('name')
                    <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
                @enderror
            </div>

            <div>
                <label class="flex items-center mt-8">
                    <input type="checkbox" name="is_active" value="1" {{ old('is_active', true) ? 'checked' : '' }} class="mr-2">
                    <span class="text-gray-700">有効</span>
                </label>
            </div>
        </div>

        <div class="mb-4">
            <label class="block text-gray-700 font-bold mb-2">説明</label>
            <textarea name="description" rows="3"
                      class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500">{{ old('description') }}</textarea>
        </div>

        <div class="grid grid-cols-3 gap-4 mb-4">
            <div>
                <label class="block text-gray-700 font-bold mb-2">最小金額 (XRP) <span class="text-red-500">*</span></label>
                <input type="number" id="min_amount_xrp" step="0.01" min="0" value="{{ old('min_amount_xrp', 100) }}" required
                       class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
                       onchange="document.getElementById('min_amount_drops').value = Math.floor(this.value * 1000000)">
                <input type="hidden" id="min_amount_drops" name="min_amount_drops" value="{{ old('min_amount_drops', 100000000) }}">
            </div>

            <div>
                <label class="block text-gray-700 font-bold mb-2">ロック期間 (日) <span class="text-red-500">*</span></label>
                <input type="number" name="lock_days" value="{{ old('lock_days', 30) }}" min="1" required
                       class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
            </div>

            <div>
                <label class="block text-gray-700 font-bold mb-2">最大参加者数</label>
                <input type="number" name="max_participants" value="{{ old('max_participants') }}" min="1"
                       class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
                <small class="text-gray-500">空欄の場合は無制限</small>
            </div>
        </div>

        <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
                <label class="block text-gray-700 font-bold mb-2">開始日時 <span class="text-red-500">*</span></label>
                <input type="datetime-local" name="start_date" value="{{ old('start_date') }}" required
                       class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
            </div>

            <div>
                <label class="block text-gray-700 font-bold mb-2">終了日時 <span class="text-red-500">*</span></label>
                <input type="datetime-local" name="end_date" value="{{ old('end_date') }}" required
                       class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
            </div>
        </div>

        <hr class="my-6">
        <h3 class="text-xl font-bold mb-4">NFT報酬設定</h3>

        <div class="mb-4">
            <label class="block text-gray-700 font-bold mb-2">NFT名 <span class="text-red-500">*</span></label>
            <input type="text" name="nft_reward_name" value="{{ old('nft_reward_name') }}" required
                   class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
        </div>

        <div class="mb-4">
            <label class="block text-gray-700 font-bold mb-2">NFT説明</label>
            <textarea name="nft_reward_description" rows="3"
                      class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500">{{ old('nft_reward_description') }}</textarea>
        </div>

        <div class="mb-6">
            <label class="block text-gray-700 font-bold mb-2">NFT画像URL</label>
            <input type="url" name="nft_reward_image_url" value="{{ old('nft_reward_image_url') }}"
                   class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
        </div>

        <div class="flex gap-4">
            <button type="submit" class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">作成</button>
            <a href="{{ route('admin.escrow-campaigns.index') }}" class="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">キャンセル</a>
        </div>
    </form>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const xrpInput = document.getElementById('min_amount_xrp');
    const dropsInput = document.getElementById('min_amount_drops');
    dropsInput.value = Math.floor(xrpInput.value * 1000000);
});
</script>
@endsection
