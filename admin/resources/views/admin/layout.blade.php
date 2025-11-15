<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'Airzone Admin')</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <nav class="bg-white shadow-lg">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between h-16">
                <div class="flex">
                    <a href="{{ route('dashboard') }}" class="flex items-center px-2 text-gray-900 font-bold text-xl">
                        Airzone Admin
                    </a>
                    <div class="hidden md:flex md:ml-6 md:space-x-4">
                        <a href="{{ route('dashboard') }}" class="inline-flex items-center px-3 py-2 text-sm font-medium">ダッシュボード</a>
                        <a href="{{ route('users.index') }}" class="inline-flex items-center px-3 py-2 text-sm font-medium">ユーザー</a>
                        <a href="{{ route('products.index') }}" class="inline-flex items-center px-3 py-2 text-sm font-medium">商品</a>
                        <a href="{{ route('orders.index') }}" class="inline-flex items-center px-3 py-2 text-sm font-medium">注文</a>
                        <a href="{{ route('nfts.index') }}" class="inline-flex items-center px-3 py-2 text-sm font-medium">NFT</a>
                    </div>
                </div>
                <div class="flex items-center">
                    <form method="POST" action="{{ route('logout') }}">
                        @csrf
                        <button type="submit" class="text-sm text-gray-700 hover:text-gray-900">ログアウト</button>
                    </form>
                </div>
            </div>
        </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        @if(session('success'))
            <div class="mb-4 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
                {{ session('success') }}
            </div>
        @endif

        @if($errors->any())
            <div class="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                <ul>
                    @foreach($errors->all() as $error)
                        <li>{{ $error }}</li>
                    @endforeach
                </ul>
            </div>
        @endif

        @yield('content')
    </main>
</body>
</html>
