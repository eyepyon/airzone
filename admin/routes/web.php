<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Admin\AuthController;
use App\Http\Controllers\Admin\DashboardController;
use App\Http\Controllers\Admin\UserController;
use App\Http\Controllers\Admin\ProductController;
use App\Http\Controllers\Admin\OrderController;
use App\Http\Controllers\Admin\NFTController;
use App\Http\Controllers\Admin\BatchTransferController;

// 認証
Route::get('/login', [AuthController::class, 'showLogin'])->name('login');
Route::post('/login', [AuthController::class, 'login']);
Route::post('/logout', [AuthController::class, 'logout'])->name('logout');

// 管理画面（認証必須）
Route::middleware('auth:admin')->group(function () {
    Route::get('/', [DashboardController::class, 'index'])->name('dashboard');

    // 重要ユーザー管理（resourceルートより前に定義）
    Route::get('/users/importance', [UserController::class, 'importance'])->name('users.importance');
    Route::post('/users/{id}/update-score', [UserController::class, 'updateScore'])->name('users.updateScore');

    // ユーザー管理
    Route::resource('users', UserController::class);

    // 商品管理
    Route::resource('products', ProductController::class);

    // 注文管理
    Route::resource('orders', OrderController::class)->only(['index', 'show', 'update']);

    // NFT管理
    Route::resource('nfts', NFTController::class)->only(['index', 'show']);

    // 紹介管理（resourceルートより前に定義）
    Route::get('/referrals/ranking', [App\Http\Controllers\Admin\ReferralController::class, 'ranking'])->name('referrals.ranking');
    Route::get('/referrals/{id}', [App\Http\Controllers\Admin\ReferralController::class, 'show'])->name('referrals.show');
    Route::get('/referrals', [App\Http\Controllers\Admin\ReferralController::class, 'index'])->name('referrals.index');

    // 一括送金管理
    Route::prefix('batch-transfers')->name('admin.batch-transfers.')->group(function () {
        Route::get('/', [BatchTransferController::class, 'index'])->name('index');
        Route::get('/create', [BatchTransferController::class, 'create'])->name('create');
        Route::get('/stats', [BatchTransferController::class, 'stats'])->name('stats');
        Route::post('/send', [BatchTransferController::class, 'send'])->name('send');
        Route::post('/send-all', [BatchTransferController::class, 'sendToAll'])->name('send-all');
        Route::post('/send-to-vip', [BatchTransferController::class, 'sendToVip'])->name('send-to-vip');
        Route::post('/send-to-top-referrers', [BatchTransferController::class, 'sendToTopReferrers'])->name('send-to-top-referrers');
    });
});
