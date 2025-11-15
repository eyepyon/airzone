<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Admin\AuthController;
use App\Http\Controllers\Admin\DashboardController;
use App\Http\Controllers\Admin\UserController;
use App\Http\Controllers\Admin\ProductController;
use App\Http\Controllers\Admin\OrderController;
use App\Http\Controllers\Admin\NFTController;

// 認証
Route::get('/login', [AuthController::class, 'showLogin'])->name('login');
Route::post('/login', [AuthController::class, 'login']);
Route::post('/logout', [AuthController::class, 'logout'])->name('logout');

// 管理画面（認証必須）
Route::middleware('auth:admin')->group(function () {
    Route::get('/', [DashboardController::class, 'index'])->name('dashboard');
    
    // ユーザー管理
    Route::resource('users', UserController::class);
    
    // 商品管理
    Route::resource('products', ProductController::class);
    
    // 注文管理
    Route::resource('orders', OrderController::class)->only(['index', 'show', 'update']);
    
    // NFT管理
    Route::resource('nfts', NFTController::class)->only(['index', 'show']);
});
