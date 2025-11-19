# デバッグ チートシート 🐛

## 🚀 クイックスタート

### フロントエンド開発サーバー起動
```bash
cd frontend
npm run dev
# http://localhost:3000 でアクセス
```

### バックエンド開発サーバー起動
```bash
cd admin
php artisan serve
# http://localhost:8000 でアクセス
```

---

## 📝 よく使うコマンド

### フロントエンド（Next.js）

```bash
# ビルドエラーをチェック
npm run build

# 型エラーをチェック
npx tsc --noEmit

# ESLint でコードチェック
npm run lint

# キャッシュをクリア
rm -rf .next
npm run dev
```

### バックエンド（Laravel）

```bash
# ログをリアルタイム監視
tail -f storage/logs/laravel.log

# キャッシュクリア
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear

# データベースリセット
php artisan migrate:fresh --seed

# Tinker で対話的にテスト
php artisan tinker
```

---

## 🔍 デバッグコードスニペット

### JavaScript/TypeScript

```typescript
// 1. 基本的なログ
console.log('変数:', variable);

// 2. オブジェクトを見やすく表示
console.log('ユーザー:', JSON.stringify(user, null, 2));

// 3. テーブル形式で表示
console.table(products);

// 4. 実行時間を測定
console.time('処理時間');
// ... 処理 ...
console.timeEnd('処理時間');

// 5. スタックトレース
console.trace('ここに到達しました');

// 6. 条件付きログ
console.assert(user !== null, 'ユーザーがnullです');

// 7. グループ化
console.group('購入処理');
console.log('商品:', product);
console.log('数量:', quantity);
console.groupEnd();

// 8. デバッガーで停止
debugger;

// 9. エラーの詳細をログ
try {
  // 処理
} catch (error) {
  console.error('エラー:', {
    message: error.message,
    stack: error.stack,
    name: error.name,
  });
}

// 10. パフォーマンスマーク
performance.mark('start');
// ... 処理 ...
performance.mark('end');
performance.measure('処理時間', 'start', 'end');
console.log(performance.getEntriesByType('measure'));
```

### PHP/Laravel

```php
// 1. 基本的なログ
Log::info('メッセージ', ['data' => $data]);

// 2. dd() - Dump and Die
dd($user);
dd($user, $products, $orders);

// 3. dump() - 実行を継続
dump($user);
dump('ここまで実行されました');

// 4. クエリログ
DB::enableQueryLog();
$users = User::all();
dd(DB::getQueryLog());

// 5. SQLを表示
$sql = User::where('active', true)->toSql();
dd($sql);

// 6. レスポンスをログ
Log::info('API Response', [
    'status' => $response->status(),
    'data' => $response->json(),
]);

// 7. 例外をログ
try {
    // 処理
} catch (\Exception $e) {
    Log::error('エラー発生', [
        'message' => $e->getMessage(),
        'file' => $e->getFile(),
        'line' => $e->getLine(),
        'trace' => $e->getTraceAsString(),
    ]);
}

// 8. 実行時間を測定
$start = microtime(true);
// ... 処理 ...
$time = microtime(true) - $start;
Log::info('処理時間', ['time' => $time]);

// 9. メモリ使用量
Log::info('メモリ使用量', [
    'memory' => memory_get_usage(true) / 1024 / 1024 . ' MB'
]);

// 10. バックトレース
Log::info('バックトレース', [
    'trace' => debug_backtrace()
]);
```

---

## 🌐 ネットワークデバッグ

### cURL コマンド

```bash
# GET リクエスト
curl http://localhost:8000/api/v1/products

# POST リクエスト
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"items":[{"product_id":"123","quantity":1}]}'

# レスポンスヘッダーを表示
curl -i http://localhost:8000/api/v1/products

# 詳細情報を表示
curl -v http://localhost:8000/api/v1/products

# レスポンスをファイルに保存
curl http://localhost:8000/api/v1/products > response.json

# タイムアウトを設定
curl --max-time 10 http://localhost:8000/api/v1/products
```

### ブラウザコンソールでのテスト

```javascript
// Fetch API でテスト
fetch('http://localhost:8000/api/v1/products')
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));

// POST リクエスト
fetch('http://localhost:8000/api/v1/orders', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
  },
  body: JSON.stringify({
    items: [{ product_id: '123', quantity: 1 }]
  })
})
  .then(res => res.json())
  .then(data => console.log(data));

// LocalStorage の確認
console.log('Token:', localStorage.getItem('access_token'));
console.log('All items:', Object.keys(localStorage));

// Cookie の確認
console.log('Cookies:', document.cookie);
```

---

## 🗄️ データベースデバッグ

### MySQL コマンド

```bash
# MySQL に接続
mysql -u root -p airzone

# データベース一覧
SHOW DATABASES;

# テーブル一覧
SHOW TABLES;

# テーブル構造を確認
DESCRIBE products;

# データを確認
SELECT * FROM products LIMIT 10;

# 特定の条件で検索
SELECT * FROM users WHERE email = 'test@example.com';

# レコード数を確認
SELECT COUNT(*) FROM orders;

# 最新のレコードを確認
SELECT * FROM orders ORDER BY created_at DESC LIMIT 5;

# クエリの実行計画を確認
EXPLAIN SELECT * FROM products WHERE price > 1000;
```

### Laravel Tinker

```bash
php artisan tinker

# モデルを取得
>>> $user = App\Models\User::find(1);
>>> $user->name;

# 全レコードを取得
>>> $users = App\Models\User::all();
>>> $users->count();

# 条件で検索
>>> $products = App\Models\Product::where('price', '>', 1000)->get();

# リレーションを確認
>>> $order = App\Models\Order::with('items')->first();
>>> $order->items;

# レコードを作成
>>> $product = App\Models\Product::create([
...     'name' => 'テスト商品',
...     'price' => 1000,
...     'stock_quantity' => 10,
... ]);

# レコードを更新
>>> $product->update(['price' => 1500]);

# レコードを削除
>>> $product->delete();

# 関数をテスト
>>> $result = someFunction($param);
```

---

## 🔧 トラブルシューティング

### エラー別対処法

#### 1. "Cannot find module" エラー
```bash
# node_modules を再インストール
rm -rf node_modules package-lock.json
npm install
```

#### 2. "Port 3000 is already in use" エラー
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9

# または別のポートを使用
PORT=3001 npm run dev
```

#### 3. CORS エラー
```typescript
// フロントエンドで確認
console.log('API URL:', process.env.NEXT_PUBLIC_API_URL);

// バックエンドで確認（admin/config/cors.php）
'allowed_origins' => ['http://localhost:3000'],
```

#### 4. 認証エラー
```javascript
// トークンを確認
const token = localStorage.getItem('access_token');
console.log('Token:', token);

// トークンをデコード（JWT）
if (token) {
  const parts = token.split('.');
  const payload = JSON.parse(atob(parts[1]));
  console.log('Payload:', payload);
  console.log('Expires:', new Date(payload.exp * 1000));
}
```

#### 5. データベース接続エラー
```bash
# 接続情報を確認
cat admin/.env | grep DB_

# MySQL が起動しているか確認
# Windows
sc query MySQL80

# Linux/Mac
sudo systemctl status mysql
```

---

## 📊 パフォーマンスデバッグ

### フロントエンド

```typescript
// React のレンダリング回数を確認
useEffect(() => {
  console.log('Component rendered');
});

// レンダリング時間を測定
const start = performance.now();
// ... レンダリング処理 ...
const end = performance.now();
console.log(`Render time: ${end - start}ms`);

// メモリ使用量を確認
console.log('Memory:', performance.memory);
```

### バックエンド

```php
// クエリ数を確認
DB::enableQueryLog();
// ... 処理 ...
$queries = DB::getQueryLog();
Log::info('Query count', ['count' => count($queries)]);

// 実行時間を測定
$start = microtime(true);
// ... 処理 ...
$time = microtime(true) - $start;
Log::info('Execution time', ['time' => $time]);

// N+1 問題をチェック
// ❌ 悪い例
$orders = Order::all();
foreach ($orders as $order) {
    echo $order->user->name; // N+1 問題
}

// ✅ 良い例
$orders = Order::with('user')->get();
foreach ($orders as $order) {
    echo $order->user->name;
}
```

---

## 💡 デバッグのヒント

### 1. 問題を再現する
- 同じ手順で何度も再現できるか確認
- 再現手順をメモする

### 2. エラーメッセージを読む
- エラーメッセージの全文を確認
- ファイル名と行番号をチェック
- スタックトレースを確認

### 3. 段階的にデバッグ
```typescript
// ❌ 一度に全部やらない
const result = await complexFunction(data);

// ✅ 段階的に確認
console.log('1. Input:', data);
const step1 = validateData(data);
console.log('2. Validated:', step1);
const step2 = processData(step1);
console.log('3. Processed:', step2);
const result = await saveData(step2);
console.log('4. Result:', result);
```

### 4. 最小限の再現コードを作成
- 問題を最小限のコードで再現
- 不要な部分を削除

### 5. ドキュメントを確認
- 公式ドキュメントを読む
- エラーメッセージでGoogle検索

---

## 🆘 困ったときは

1. **エラーメッセージをコピー**してGoogle検索
2. **Stack Overflow**で類似の問題を検索
3. **GitHub Issues**で同じ問題がないか確認
4. **公式ドキュメント**を読む
5. **チームメンバー**に相談

---

## 📚 参考リンク

- [Next.js Debugging](https://nextjs.org/docs/advanced-features/debugging)
- [React DevTools](https://react.dev/learn/react-developer-tools)
- [Laravel Debugging](https://laravel.com/docs/10.x/logging)
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/)
- [VS Code Debugging](https://code.visualstudio.com/docs/editor/debugging)
