@extends('admin.layout')

@section('title', '商品編集')

@section('content')
<div class="mb-6">
    <a href="{{ route('products.index') }}" class="text-blue-600 hover:underline">← 商品一覧に戻る</a>
</div>

<h1 class="text-3xl font-bold mb-6">商品編集</h1>

<div class="bg-white rounded-lg shadow p-6">
    <form method="POST" action="{{ route('products.update', $product->id) }}">
        @csrf
        @method('PUT')

        <div class="mb-4">
            <label class="block text-gray-700 font-bold mb-2">商品名 <span class="text-red-500">*</span></label>
            <input type="text" name="name" value="{{ old('name', $product->name) }}" required class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
        </div>

        <div class="mb-4">
            <label class="block text-gray-700 font-bold mb-2">説明</label>
            <textarea name="description" rows="4" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500">{{ old('description', $product->description) }}</textarea>
        </div>

        <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
                <label class="block text-gray-700 font-bold mb-2">カテゴリー <span class="text-red-500">*</span></label>
                <select name="category" required class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
                    <option value="">選択してください</option>
                    <option value="goods" {{ old('category', $product->category ?? '') == 'goods' ? 'selected' : '' }}>グッズ</option>
                    <option value="nft" {{ old('category', $product->category ?? '') == 'nft' ? 'selected' : '' }}>NFT</option>
                    <option value="ticket" {{ old('category', $product->category ?? '') == 'ticket' ? 'selected' : '' }}>チケット</option>
                </select>
            </div>

            <div>
                <label class="block text-gray-700 font-bold mb-2">受け取り方法 <span class="text-red-500">*</span></label>
                <select name="delivery_method" required class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
                    <option value="">選択してください</option>
                    <option value="venue_pickup" {{ old('delivery_method', $product->delivery_method ?? '') == 'venue_pickup' ? 'selected' : '' }}>会場内受取</option>
                    <option value="home_delivery" {{ old('delivery_method', $product->delivery_method ?? '') == 'home_delivery' ? 'selected' : '' }}>宅配便配送</option>
                </select>
            </div>
        </div>

        <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
                <label class="block text-gray-700 font-bold mb-2">価格 (円) <span class="text-red-500">*</span></label>
                <input type="number" name="price" value="{{ old('price', $product->price) }}" required min="0" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
            </div>

            <div>
                <label class="block text-gray-700 font-bold mb-2">在庫数 <span class="text-red-500">*</span></label>
                <input type="number" name="stock_quantity" value="{{ old('stock_quantity', $product->stock_quantity) }}" required min="0" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
            </div>
        </div>

        <div class="mb-4">
            <label class="block text-gray-700 font-bold mb-2">画像URL</label>
            <input type="url" name="image_url" value="{{ old('image_url', $product->image_url) }}" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
        </div>

        <div class="mb-6">
            <label class="flex items-center">
                <input type="checkbox" name="is_active" value="1" {{ old('is_active', $product->is_active) ? 'checked' : '' }} class="mr-2">
                <span class="text-gray-700">公開する</span>
            </label>
        </div>

        <div class="flex gap-4">
            <button type="submit" class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">更新</button>
            <a href="{{ route('products.index') }}" class="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">キャンセル</a>
        </div>
    </form>
</div>
@endsection
