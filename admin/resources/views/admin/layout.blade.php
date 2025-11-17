<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'Airzone Admin')</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .nav-link {
            @apply inline-flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-colors;
        }
        .nav-link.active {
            @apply text-blue-600 bg-blue-50;
        }
        .mobile-menu {
            @apply hidden;
        }
        .mobile-menu.active {
            @apply block;
        }
    </style>
</head>
<body class="bg-gray-100">
    <nav class="bg-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <a href="{{ route('dashboard') }}" class="flex items-center px-2 text-gray-900 font-bold text-xl hover:text-blue-600 transition-colors">
                        <i class="fas fa-plane-departure mr-2"></i>
                        Airzone Admin
                    </a>
                    <button id="mobile-menu-button" class="md:hidden ml-4 p-2 rounded-md text-gray-700 hover:bg-gray-100">
                        <i class="fas fa-bars"></i>
                    </button>
                </div>
                
                <div class="hidden md:flex md:items-center md:space-x-1">
                    <a href="{{ route('dashboard') }}" class="nav-link {{ request()->routeIs('dashboard') ? 'active' : '' }}">
                        <i class="fas fa-home mr-1"></i> ダッシュボード
                    </a>
                    <a href="{{ route('users.index') }}" class="nav-link {{ request()->routeIs('users.*') ? 'active' : '' }}">
                        <i class="fas fa-users mr-1"></i> ユーザー
                    </a>
                    <a href="{{ route('products.index') }}" class="nav-link {{ request()->routeIs('products.*') ? 'active' : '' }}">
                        <i class="fas fa-box mr-1"></i> 商品
                    </a>
                    <a href="{{ route('orders.index') }}" class="nav-link {{ request()->routeIs('orders.*') ? 'active' : '' }}">
                        <i class="fas fa-shopping-cart mr-1"></i> 注文
                    </a>
                    <a href="{{ route('nfts.index') }}" class="nav-link {{ request()->routeIs('nfts.*') ? 'active' : '' }}">
                        <i class="fas fa-image mr-1"></i> NFT
                    </a>
                    <a href="{{ route('referrals.index') }}" class="nav-link {{ request()->routeIs('referrals.*') ? 'active' : '' }}">
                        <i class="fas fa-share-nodes mr-1"></i> 紹介
                    </a>
                    <a href="{{ route('users.importance') }}" class="nav-link {{ request()->routeIs('users.importance') ? 'active' : '' }}">
                        <i class="fas fa-crown mr-1"></i> VIP
                    </a>
                    <a href="{{ route('admin.batch-transfers.index') }}" class="nav-link {{ request()->routeIs('admin.batch-transfers.*') ? 'active' : '' }}">
                        <i class="fas fa-paper-plane mr-1"></i> 一括送金
                    </a>
                </div>
                
                <div class="flex items-center">
                    <form method="POST" action="{{ route('logout') }}">
                        @csrf
                        <button type="submit" class="text-sm text-gray-700 hover:text-red-600 px-3 py-2 rounded-md hover:bg-red-50 transition-colors">
                            <i class="fas fa-sign-out-alt mr-1"></i> ログアウト
                        </button>
                    </form>
                </div>
            </div>
            
            <!-- Mobile Menu -->
            <div id="mobile-menu" class="mobile-menu md:hidden pb-4">
                <div class="flex flex-col space-y-1">
                    <a href="{{ route('dashboard') }}" class="nav-link {{ request()->routeIs('dashboard') ? 'active' : '' }}">
                        <i class="fas fa-home mr-2"></i> ダッシュボード
                    </a>
                    <a href="{{ route('users.index') }}" class="nav-link {{ request()->routeIs('users.*') ? 'active' : '' }}">
                        <i class="fas fa-users mr-2"></i> ユーザー
                    </a>
                    <a href="{{ route('products.index') }}" class="nav-link {{ request()->routeIs('products.*') ? 'active' : '' }}">
                        <i class="fas fa-box mr-2"></i> 商品
                    </a>
                    <a href="{{ route('orders.index') }}" class="nav-link {{ request()->routeIs('orders.*') ? 'active' : '' }}">
                        <i class="fas fa-shopping-cart mr-2"></i> 注文
                    </a>
                    <a href="{{ route('nfts.index') }}" class="nav-link {{ request()->routeIs('nfts.*') ? 'active' : '' }}">
                        <i class="fas fa-image mr-2"></i> NFT
                    </a>
                    <a href="{{ route('referrals.index') }}" class="nav-link {{ request()->routeIs('referrals.*') ? 'active' : '' }}">
                        <i class="fas fa-share-nodes mr-2"></i> 紹介
                    </a>
                    <a href="{{ route('users.importance') }}" class="nav-link {{ request()->routeIs('users.importance') ? 'active' : '' }}">
                        <i class="fas fa-crown mr-2"></i> VIP
                    </a>
                    <a href="{{ route('admin.batch-transfers.index') }}" class="nav-link {{ request()->routeIs('admin.batch-transfers.*') ? 'active' : '' }}">
                        <i class="fas fa-paper-plane mr-2"></i> 一括送金
                    </a>
                </div>
            </div>
        </div>
    </nav>
    
    <script>
        document.getElementById('mobile-menu-button')?.addEventListener('click', function() {
            document.getElementById('mobile-menu')?.classList.toggle('active');
        });
    </script>

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
