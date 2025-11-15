@extends('admin.layout')

@section('title', 'ユーザー管理')

@section('content')
<div class="flex justify-between items-center mb-6">
    <h1 class="text-3xl font-bold">ユーザー管理</h1>
</div>

<div class="bg-white rounded-lg shadow p-6 mb-6">
    <form method="GET" class="flex gap-4">
        <input type="text" name="search" placeholder="メールアドレスまたは名前で検索" value="{{ request('search') }}" class="flex-1 px-4 py-2 border rounded-lg">
        <button type="submit" class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">検索</button>
        <a href="{{ route('users.index') }}" class="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">クリア</a>
    </form>
</div>

<div class="bg-white rounded-lg shadow overflow-hidden">
    <table class="min-w-full">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">名前</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">メール</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ウォレット</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">登録日</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">操作</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
            @foreach($users as $user)
            <tr>
                <td class="px-6 py-4">{{ $user->name }}</td>
                <td class="px-6 py-4">{{ $user->email }}</td>
                <td class="px-6 py-4">
                    @if($user->wallet_address)
                        <span class="font-mono text-xs">{{ substr($user->wallet_address, 0, 10) }}...</span>
                    @else
                        <span class="text-gray-400">なし</span>
                    @endif
                </td>
                <td class="px-6 py-4">{{ $user->created_at }}</td>
                <td class="px-6 py-4">
                    <a href="{{ route('users.show', $user->id) }}" class="text-blue-600 hover:underline mr-3">詳細</a>
                    <form method="POST" action="{{ route('users.destroy', $user->id) }}" class="inline" onsubmit="return confirm('本当に削除しますか？')">
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
    {{ $users->links() }}
</div>
@endsection
