# Laravel 10 互換性修正

## 問題
`composer update`実行時に以下のエラーが発生:
```
PHP Fatal error: Uncaught BadMethodCallException: Method Illuminate\Foundation\Application::configure does not exist.
```

## 原因
- `bootstrap/app.php`がLaravel 11の構文を使用していた
- インストールされているLaravelのバージョンはLaravel 10
- `Application::configure()`メソッドはLaravel 11で導入されたため、Laravel 10では使用できない

## 修正内容

### 1. bootstrap/app.php
Laravel 10の標準的な構文に書き直しました:
- Laravel 11の`Application::configure()`構文を削除
- Laravel 10の従来の構文に変更
- Kernel、Console Kernel、Exception Handlerのバインディングを追加

### 2. app/Http/Kernel.php
`auth.admin`ミドルウェアエイリアスを追加:
```php
'auth.admin' => \App\Http\Middleware\AdminAuthenticate::class,
```

## 確認方法
```bash
cd admin
composer update
```

エラーなく完了すれば修正成功です。

## Laravel 10 vs Laravel 11の主な違い

### Laravel 10 (現在のバージョン)
```php
// bootstrap/app.php
$app = new Illuminate\Foundation\Application(
    $_ENV['APP_BASE_PATH'] ?? dirname(__DIR__)
);

$app->singleton(
    Illuminate\Contracts\Http\Kernel::class,
    App\Http\Kernel::class
);
```

### Laravel 11 (新しい構文)
```php
// bootstrap/app.php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(...)
    ->withMiddleware(...)
    ->withExceptions(...)
    ->create();
```

## 今後の対応
Laravel 11にアップグレードする場合は、以下の手順が必要です:
1. `composer.json`でLaravelバージョンを`^11.0`に変更
2. `composer update`を実行
3. `bootstrap/app.php`をLaravel 11の構文に戻す
4. その他の互換性のない変更を修正

詳細: https://laravel.com/docs/11.x/upgrade
