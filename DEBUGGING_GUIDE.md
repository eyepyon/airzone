# デバッグガイド

## 目次
1. [フロントエンド（Next.js/React）のデバッグ](#フロントエンド-nextjsreact-のデバッグ)
2. [バックエンド（Laravel/PHP）のデバッグ](#バックエンド-laravelphp-のデバッグ)
3. [ネットワークリクエストのデバッグ](#ネットワークリクエストのデバッグ)
4. [データベースのデバッグ](#データベースのデバッグ)
5. [よくある問題と解決方法](#よくある問題と解決方法)

---

## フロントエンド (Next.js/React) のデバッグ

### 1. ブラウザの開発者ツール

#### コンソールログ
```typescript
// 基本的なログ
console.log('変数の値:', variable);

// オブジェクトの詳細表示
console.log('ユーザー情報:', JSON.stringify(user, null, 2));

// エラーログ
console.error('エラーが発生しました:', error);

// 警告ログ
console.warn('警告:', message);

// テーブル形式で表示
console.table(arrayOfObjects);

// グループ化
console.group('購入処理');
console.log('商品:', product);
console.log('数量:', quantity);
console.groupEnd();
```

#### デバッガーの使用
```typescript
// コードの実行を一時停止
debugger;

// 条件付きデバッガー
if (user.id === 'specific-id') {
  debugger;
}
```

### 2. React Developer Tools

#### インストール
- Chrome: [React Developer Tools](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi)
- Firefox: [React Developer Tools](https://addons.mozilla.org/en-US/firefox/addon/react-devtools/)

#### 使い方
1. ブラウザの開発者ツールを開く（F12）
2. "Components" タブでReactコンポーネントツリーを確認
3. "Profiler" タブでパフォーマンスを測定

### 3. Next.js のデバッグ

#### 開発サーバーのログ
```bash
# 詳細なログを表示
npm run dev

# ターミナルに表示される情報:
# - コンパイルエラー
# - APIルートのリクエスト
# - ページのレンダリング情報
```

#### VS Code でのデバッグ設定

`.vscode/launch.json` を作成:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js: debug server-side",
      "type": "node-terminal",
      "request": "launch",
      "command": "npm run dev"
    },
    {
      "name": "Next.js: debug client-side",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:3000"
    }
  ]
}
```

### 4. カスタムデバッグフック

`frontend/lib/debug.ts` を作成:
```typescript
// デバッグモードの判定
export const isDebugMode = process.env.NODE_ENV === 'development';

// デバッグログ
export function debugLog(category: string, ...args: any[]) {
  if (isDebugMode) {
    console.log(`[${category}]`, ...args);
  }
}

// パフォーマンス測定
export function measurePerformance(label: string, fn: () => void) {
  if (isDebugMode) {
    console.time(label);
    fn();
    console.timeEnd(label);
  } else {
    fn();
  }
}

// エラートラッキング
export function trackError(error: Error, context?: any) {
  console.error('Error:', error);
  if (context) {
    console.error('Context:', context);
  }
  
  // 本番環境ではエラートラッキングサービスに送信
  // if (!isDebugMode) {
  //   sendToErrorTracking(error, context);
  // }
}
```

使用例:
```typescript
import { debugLog, measurePerformance, trackError } from '@/lib/debug';

export default function ProductPage() {
  useEffect(() => {
    debugLog('ProductPage', 'コンポーネントがマウントされました');
    
    measurePerformance('商品データ取得', async () => {
      try {
        const products = await getProducts();
        debugLog('ProductPage', '商品取得成功:', products.length);
      } catch (error) {
        trackError(error as Error, { page: 'ProductPage' });
      }
    });
  }, []);
}
```

### 5. ネットワークリクエストのデバッグ

```typescript
// APIクライアントにログを追加
export async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  console.log('🌐 API Request:', {
    endpoint,
    method: options?.method || 'GET',
    headers: options?.headers,
    body: options?.body,
  });

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    const data = await response.json();
    
    console.log('✅ API Response:', {
      endpoint,
      status: response.status,
      data,
    });

    if (!response.ok) {
      throw new Error(data.error || 'API request failed');
    }

    return data;
  } catch (error) {
    console.error('❌ API Error:', {
      endpoint,
      error,
    });
    throw error;
  }
}
```

---

## バックエンド (Laravel/PHP) のデバッグ

### 1. Laravel のログ

#### ログの出力
```php
// storage/logs/laravel.log に出力される

// 基本的なログ
Log::info('ユーザーがログインしました', ['user_id' => $user->id]);

// デバッグログ
Log::debug('変数の値', ['variable' => $variable]);

// エラーログ
Log::error('エラーが発生しました', [
    'error' => $exception->getMessage(),
    'trace' => $exception->getTraceAsString()
]);

// 警告ログ
Log::warning('在庫が少なくなっています', ['product_id' => $product->id]);
```

#### ログの確認
```bash
# リアルタイムでログを監視
tail -f admin/storage/logs/laravel.log

# 最新の50行を表示
tail -n 50 admin/storage/logs/laravel.log

# エラーのみを表示
grep "ERROR" admin/storage/logs/laravel.log
```

### 2. dd() と dump() の使用

```php
// dd() - Dump and Die（実行を停止して変数を表示）
dd($user);
dd($user, $products, $orders);

// dump() - 実行を継続しながら変数を表示
dump($user);
dump('ここまで実行されました');

// ddd() - 複数の変数をダンプして停止
ddd($user, $products);
```

### 3. Laravel Debugbar のインストール

```bash
cd admin
composer require barryvdh/laravel-debugbar --dev
```

`admin/config/app.php` に追加:
```php
'providers' => [
    // ...
    Barryvdh\Debugbar\ServiceProvider::class,
],

'aliases' => [
    // ...
    'Debugbar' => Barryvdh\Debugbar\Facades\Debugbar::class,
],
```

使用例:
```php
use Debugbar;

Debugbar::info('情報メッセージ');
Debugbar::error('エラーメッセージ');
Debugbar::warning('警告メッセージ');
Debugbar::addMessage('カスタムメッセージ', 'custom');

// タイムライン
Debugbar::startMeasure('render', '商品一覧のレンダリング');
// ... 処理 ...
Debugbar::stopMeasure('render');
```

### 4. Tinker でのデバッグ

```bash
# Tinker を起動
cd admin
php artisan tinker

# データベースのクエリを試す
>>> $users = App\Models\User::all();
>>> $user = App\Models\User::find(1);
>>> $user->name;

# 関数をテスト
>>> $result = someFunction($param);

# モデルの作成をテスト
>>> $product = App\Models\Product::create([
...     'name' => 'テスト商品',
...     'price' => 1000,
... ]);
```

### 5. クエリログの有効化

```php
// クエリログを有効化
DB::enableQueryLog();

// クエリを実行
$users = User::where('active', true)->get();

// 実行されたクエリを表示
dd(DB::getQueryLog());
```

または、`AppServiceProvider.php` に追加:
```php
public function boot()
{
    if (config('app.debug')) {
        DB::listen(function ($query) {
            Log::info('SQL Query', [
                'sql' => $query->sql,
                'bindings' => $query->bindings,
                'time' => $query->time,
            ]);
        });
    }
}
```

### 6. エラーハンドリング

`admin/app/Exceptions/Handler.php`:
```php
public function report(Throwable $exception)
{
    // カスタムエラーログ
    Log::error('Exception occurred', [
        'message' => $exception->getMessage(),
        'file' => $exception->getFile(),
        'line' => $exception->getLine(),
        'trace' => $exception->getTraceAsString(),
        'url' => request()->fullUrl(),
        'user_id' => auth()->id(),
    ]);

    parent::report($exception);
}
```

---

## ネットワークリクエストのデバッグ

### 1. ブラウザの Network タブ

1. 開発者ツールを開く（F12）
2. "Network" タブを選択
3. ページをリロード
4. リクエストをクリックして詳細を確認:
   - Headers: リクエストヘッダーとレスポンスヘッダー
   - Preview: レスポンスのプレビュー
   - Response: 生のレスポンスデータ
   - Timing: リクエストのタイミング

### 2. cURL でのテスト

```bash
# GET リクエスト
curl -X GET http://localhost:8000/api/v1/products

# POST リクエスト（JSON）
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"items":[{"product_id":"123","quantity":1}]}'

# レスポンスヘッダーも表示
curl -i http://localhost:8000/api/v1/products

# 詳細なデバッグ情報
curl -v http://localhost:8000/api/v1/products
```

### 3. Postman / Insomnia の使用

APIテストツールを使用すると、より簡単にリクエストをテストできます:
- [Postman](https://www.postman.com/)
- [Insomnia](https://insomnia.rest/)

---

## データベースのデバッグ

### 1. データベースクライアント

#### MySQL Workbench
```bash
# インストール（Windows）
# https://dev.mysql.com/downloads/workbench/

# 接続情報
Host: localhost
Port: 3306
User: root
Password: your_password
Database: airzone
```

#### DBeaver（無料・オープンソース）
- [DBeaver](https://dbeaver.io/)
- MySQL, PostgreSQL, SQLite など対応

### 2. Laravel のマイグレーションデバッグ

```bash
# マイグレーションの状態を確認
php artisan migrate:status

# マイグレーションをロールバック
php artisan migrate:rollback

# マイグレーションを再実行
php artisan migrate:fresh

# シーダーも実行
php artisan migrate:fresh --seed
```

### 3. クエリビルダーのデバッグ

```php
// SQLを表示（実行しない）
$sql = User::where('active', true)->toSql();
dd($sql);

// バインディングも含めて表示
$query = User::where('active', true);
dd($query->toSql(), $query->getBindings());
```

---

## よくある問題と解決方法

### 1. CORS エラー

**症状**: ブラウザのコンソールに "CORS policy" エラー

**解決方法**:
```php
// admin/config/cors.php
return [
    'paths' => ['api/*'],
    'allowed_methods' => ['*'],
    'allowed_origins' => ['http://localhost:3000'],
    'allowed_headers' => ['*'],
    'exposed_headers' => [],
    'max_age' => 0,
    'supports_credentials' => true,
];
```

### 2. 認証エラー

**デバッグ方法**:
```typescript
// トークンの確認
const token = localStorage.getItem('access_token');
console.log('Token:', token);

// トークンのデコード（JWT の場合）
const payload = JSON.parse(atob(token.split('.')[1]));
console.log('Token payload:', payload);
console.log('Expires:', new Date(payload.exp * 1000));
```

### 3. 環境変数が読み込まれない

**確認方法**:
```bash
# フロントエンド
cat frontend/.env.local

# バックエンド
cat admin/.env

# キャッシュをクリア（Laravel）
cd admin
php artisan config:clear
php artisan cache:clear
```

### 4. ポートが使用中

**解決方法**:
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9
```

### 5. npm/composer の依存関係エラー

```bash
# フロントエンド
cd frontend
rm -rf node_modules package-lock.json
npm install

# バックエンド
cd admin
rm -rf vendor composer.lock
composer install
```

---

## デバッグのベストプラクティス

### 1. 段階的なデバッグ
```typescript
// ❌ 悪い例
const result = await complexFunction(data);

// ✅ 良い例
console.log('1. データ確認:', data);
const validated = validateData(data);
console.log('2. バリデーション結果:', validated);
const processed = processData(validated);
console.log('3. 処理結果:', processed);
const result = await saveData(processed);
console.log('4. 保存結果:', result);
```

### 2. エラーの詳細をログに記録
```typescript
try {
  await someAsyncFunction();
} catch (error) {
  console.error('エラー詳細:', {
    message: error.message,
    stack: error.stack,
    context: {
      userId: user?.id,
      productId: product?.id,
      timestamp: new Date().toISOString(),
    },
  });
}
```

### 3. 条件付きログ
```typescript
const DEBUG = process.env.NODE_ENV === 'development';

if (DEBUG) {
  console.log('デバッグ情報:', data);
}
```

---

## 便利なツールとコマンド

### フロントエンド
```bash
# TypeScript の型チェック
npm run type-check

# ESLint でコードチェック
npm run lint

# Prettier でフォーマット
npm run format
```

### バックエンド
```bash
# コードスタイルチェック
./vendor/bin/phpcs

# 自動修正
./vendor/bin/phpcbf

# テスト実行
php artisan test

# 特定のテストのみ実行
php artisan test --filter=ProductTest
```

---

## まとめ

デバッグの基本は:
1. **問題を再現する**
2. **ログを確認する**
3. **段階的に原因を特定する**
4. **修正して検証する**

困ったときは、このガイドを参照してください！
