@extends('admin.layout')

@section('title', '商品管理')

@section('content')
<div class="flex justify-between items-center mb-6">
    <h1 class="text-3xl font-bold">商品管理</h1>
    <a href="{{ route('products.create') }}" class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">新規作成</a>
</div>

<div class="bg-white rounded-lg shadow overflow-hidden">
    <table class="min-w-full">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">商品名</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">価格</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">在庫</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ステータス</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">作成日</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">操作</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
            @foreach($products as $product)
            <tr>
                <td class="px-6 py-4">{{ $product->name }}</td>
                <td class="px-6 py-4">¥{{ number_format($product->price) }}</td>
                <td class="px-6 py-4">{{ $product->stock_quantity }}</td>
                <td class="px-6 py-4">
                    @if($product->is_active)
                        <span class="px-2 py-1 text-xs rounded bg-green-100 text-green-800">公開中</span>
                    @else
                        <span class="px-2 py-1 text-xs rounded bg-gray-100 text-gray-800">非公開</span>
                    @endif
                </td>
                <td class="px-6 py-4">{{ $product->created_at }}</td>
                <td class="px-6 py-4">
                    <a href="{{ route('products.edit', $product->id) }}" class="text-blue-600 hover:underline mr-3">編集</a>
                    <form method="POST" action="{{ route('products.destroy', $product->id) }}" class="inline" onsubmit="return confirm('本当に削除しますか？')">
                        @csrf
                        @method('DELETE')
                        <button type="submit" class="text-red-600 hover:underline">削除</button>
                    </form>
                </td>
            </tr>
            @endforeach
        </tbody>
    </table>
</div>

<div class="mt-6">
    {{ $products->links() }}
</div>
@endsection
