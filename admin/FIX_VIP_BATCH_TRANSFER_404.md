# VIP機能・一括送金機能の404エラー修正

## 問題
- `https://admin.airz.one/users/importance` - 404エラー
- `https://admin.airz.one/batch-transfers` - 404エラー

## 原因
Laravelのルート定義の順序が間違っていました。

`Route::resource('users', UserController::class)` が先に定義されていたため、
`/users/importance` が `/users/{id}` として解釈され、`importance`がユーザーIDとして扱われていました。

## 修正内容

### routes/web.php
ルートの定義順序を変更：

**修正前:**
```php
Route::resource('users', UserController::class);
Route::get('/users/importance', [UserController::class, 'importance']);
```

**修正後:**
```php
// 具体的なルートを先に定義
Route::get('/users/importance', [UserController::class, 'importance']);
// resourceルートは後に定義
Route::resource('users', UserController::class);
```

## サーバー上での修正手順

### 1. ルートキャッシュをクリア

```bash
cd /var/www/airzone/admin
php artisan route:clear
php artisan cache:clear
php artisan config:clear
```

### 2. ルート一覧を確認

```bash
php artisan route:list | grep users
php artisan route:list | grep batch-transfers
```

以下のようなルートが表示されるはずです：

```
GET|HEAD  users/importance ............... users.importance › Admin\UserController@importance
POST      users/{id}/update-score ........ users.updateScore › Admin\UserController@updateScore
GET|HEAD  users .......................... users.index › Admin\UserController@index
POST      users .......................... users.store › Admin\UserController@store
GET|HEAD  users/{user} ................... users.show › Admin\UserController@show
PUT|PATCH users/{user} ................... users.update › Admin\UserController@update
DELETE    users/{user} ................... users.destroy › Admin\UserController@destroy

GET|HEAD  batch-transfers ................ admin.batch-transfers.index › Admin\BatchTransferController@index
GET|HEAD  batch-transfers/create ......... admin.batch-transfers.create › Admin\BatchTransferController@create
GET|HEAD  batch-transfers/stats .......... admin.batch-transfers.stats › Admin\BatchTransferController@stats
POST      batch-transfers/send ........... admin.batch-transfers.send › Admin\BatchTransferController@send
POST      batch-transfers/send-all ....... admin.batch-transfers.send-all › Admin\BatchTransferController@sendToAll
POST      batch-transfers/send-to-vip .... admin.batch-transfers.send-to-vip › Admin\BatchTransferController@sendToVip
POST      batch-transfers/send-to-top-referrers ... admin.batch-transfers.send-to-top-referrers › Admin\BatchTransferController@sendToTopReferrers
```

### 3. Composerのオートロードを再生成

```bash
composer dump-autoload
```

### 4. Apacheを再起動（必要に応じて）

```bash
sudo systemctl restart apache2
```

### 5. 動作確認

ブラウザで以下のURLにアクセスして確認：

1. **VIP機能**: `https://admin.airz.one/users/importance`
2. **一括送金**: `https://admin.airz.one/batch-transfers`

## Laravelルート定義の重要なルール

### ルールの優先順位

Laravelは上から順にルートをマッチングします。そのため：

1. **具体的なルートを先に定義**
   ```php
   Route::get('/users/importance', ...);
   Route::get('/users/special', ...);
   ```

2. **動的パラメータを含むルートは後に定義**
   ```php
   Route::get('/users/{id}', ...);
   ```

3. **resourceルートは最後に定義**
   ```php
   Route::resource('users', UserController::class);
   ```

### 正しい順序の例

```php
// ✅ 正しい順序
Route::get('/users/importance', [UserController::class, 'importance']);
Route::get('/users/export', [UserController::class, 'export']);
Route::resource('users', UserController::class);

// ❌ 間違った順序
Route::resource('users', UserController::class);
Route::get('/users/importance', [UserController::class, 'importance']); // これは動作しない！
```

## トラブルシューティング

### 問題: まだ404エラーが出る

```bash
# ルートキャッシュを完全にクリア
cd /var/www/airzone/admin
php artisan route:clear
php artisan optimize:clear

# Apacheを再起動
sudo systemctl restart apache2
```

### 問題: 500エラーが出る

コントローラーメソッドが存在するか確認：

```bash
# UserControllerを確認
grep -n "function importance" app/Http/Controllers/Admin/UserController.php

# BatchTransferControllerを確認
ls -la app/Http/Controllers/Admin/BatchTransferController.php
```

### 問題: "Class not found"エラー

```bash
composer dump-autoload
php artisan clear-compiled
```

## 確認コマンド

```bash
# 全ルートを確認
php artisan route:list

# 特定のルートを検索
php artisan route:list | grep importance
php artisan route:list | grep batch-transfers

# ルートキャッシュの状態を確認
ls -la bootstrap/cache/routes-*.php
```

## 完了チェックリスト

- [ ] `php artisan route:clear` を実行
- [ ] `php artisan route:list` でルートを確認
- [ ] `https://admin.airz.one/users/importance` にアクセスできる
- [ ] `https://admin.airz.one/batch-transfers` にアクセスできる
- [ ] VIP機能が正常に動作する
- [ ] 一括送金機能が正常に動作する

## 参考

- [Laravel Routing Documentation](https://laravel.com/docs/10.x/routing)
- [Route Model Binding](https://laravel.com/docs/10.x/routing#route-model-binding)
