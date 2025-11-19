# データ移行ガイド

## 概要

新しい購入システムの実装により、`Product`モデルに以下のフィールドが追加されました：
- `product_type`: 商品タイプ（NFT/グッズ/チケット）
- `purchase_restriction`: 購入制限
- `delivery_method`: 配送方法
- `event_date`: イベント日時（チケットの場合）
- `venue`: 会場（チケットの場合）

## 後方互換性

既存のデータとの互換性を保つため、これらのフィールドは**オプショナル**になっています。

### デフォルト値

新しいフィールドが存在しない場合、以下のデフォルト値が使用されます：

```typescript
{
  product_type: 'goods',           // グッズとして扱う
  purchase_restriction: 'public',  // 誰でも購入可能
  delivery_method: null,           // 配送方法未設定
  event_date: null,
  venue: null
}
```

## データベース移行

### 1. マイグレーションファイルの作成

```bash
cd admin
php artisan make:migration add_new_fields_to_products_table
```

### 2. マイグレーション内容

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::table('products', function (Blueprint $table) {
            // 商品タイプ（デフォルト: goods）
            $table->string('product_type', 50)
                  ->default('goods')
                  ->after('image_url');
            
            // 配送方法（NULL許可）
            $table->string('delivery_method', 50)
                  ->nullable()
                  ->after('product_type');
            
            // 購入制限（デフォルト: public）
            $table->string('purchase_restriction', 50)
                  ->default('public')
                  ->after('delivery_method');
            
            // イベント日時（チケット用、NULL許可）
            $table->timestamp('event_date')
                  ->nullable()
                  ->after('purchase_restriction');
            
            // 会場（チケット用、NULL許可）
            $table->text('venue')
                  ->nullable()
                  ->after('event_date');
        });
    }

    public function down()
    {
        Schema::table('products', function (Blueprint $table) {
            $table->dropColumn([
                'product_type',
                'delivery_method',
                'purchase_restriction',
                'event_date',
                'venue'
            ]);
        });
    }
};
```

### 3. マイグレーション実行

```bash
php artisan migrate
```

## 既存データの更新

### オプション1: 全商品を一括更新

```php
// database/seeders/UpdateExistingProductsSeeder.php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Product;

class UpdateExistingProductsSeeder extends Seeder
{
    public function run()
    {
        // 既存の全商品をグッズとして設定
        Product::whereNull('product_type')->update([
            'product_type' => 'goods',
            'purchase_restriction' => 'public',
        ]);
        
        echo "既存商品を更新しました\n";
    }
}
```

実行:
```bash
php artisan db:seed --class=UpdateExistingProductsSeeder
```

### オプション2: 管理画面から個別に更新

1. 管理画面の商品一覧にアクセス
2. 各商品を編集
3. 商品タイプと購入制限を設定
4. 保存

## フロントエンドの対応

### 既存データの表示

新しいフィールドが存在しない商品でも、エラーなく表示されます：

```typescript
// 商品カードコンポーネント
const productWithDefaults = {
  ...product,
  product_type: product.product_type || 'goods',
  purchase_restriction: product.purchase_restriction || 'public',
  delivery_method: product.delivery_method || null,
};
```

### バッジの表示

新しいフィールドが存在する場合のみ、バッジが表示されます：

```typescript
{(product.product_type || product.purchase_restriction) && (
  <div className="flex flex-wrap gap-2 mb-3">
    {/* バッジ表示 */}
  </div>
)}
```

## テストデータの作成

### NFT商品の例

```php
Product::create([
    'name' => 'Airzone限定NFT',
    'description' => 'イベント参加者限定のNFT',
    'price' => 0,
    'stock_quantity' => 1000,
    'product_type' => 'nft',
    'purchase_restriction' => 'onsite_only',
    'delivery_method' => 'digital',
    'is_active' => true,
]);
```

### グッズ（現地受け取り）の例

```php
Product::create([
    'name' => 'イベントTシャツ',
    'description' => '会場で受け取れる限定Tシャツ',
    'price' => 3000,
    'stock_quantity' => 50,
    'product_type' => 'goods',
    'purchase_restriction' => 'onsite_only',
    'delivery_method' => 'pickup',
    'is_active' => true,
]);
```

### グッズ（配送）の例

```php
Product::create([
    'name' => 'オフィシャルグッズセット',
    'description' => '自宅に配送されるグッズセット',
    'price' => 5000,
    'stock_quantity' => 100,
    'product_type' => 'goods',
    'purchase_restriction' => 'public',
    'delivery_method' => 'shipping',
    'is_active' => true,
]);
```

### イベントチケットの例

```php
Product::create([
    'name' => 'ライブチケット（抽選）',
    'description' => 'NFTチケット形式のライブ参加権',
    'price' => 10000,
    'stock_quantity' => 200,
    'product_type' => 'event_ticket',
    'purchase_restriction' => 'nft_holders',
    'delivery_method' => 'digital',
    'event_date' => '2024-12-31 19:00:00',
    'venue' => '東京ドーム',
    'required_nft_id' => 'some-nft-id',
    'is_active' => true,
]);
```

## トラブルシューティング

### エラー: "product.price is undefined"

**原因**: 商品データに`price`フィールドが存在しない

**解決方法**:
```typescript
// formatPrice関数で undefined をチェック
const formatPrice = (price: number | undefined) => {
  if (price === undefined || price === null) {
    return '価格未設定';
  }
  return new Intl.NumberFormat('ja-JP', {
    style: 'currency',
    currency: 'JPY',
  }).format(price);
};
```

### エラー: "Cannot read property 'product_type' of undefined"

**原因**: 商品データ自体が`undefined`

**解決方法**:
```typescript
// コンポーネントで商品データの存在をチェック
if (!product) {
  return <div>商品が見つかりません</div>;
}
```

### バッジが表示されない

**原因**: 新しいフィールドが設定されていない

**解決方法**:
1. データベースを確認
2. マイグレーションが実行されているか確認
3. 既存データを更新

```bash
# マイグレーション状態を確認
php artisan migrate:status

# 未実行のマイグレーションを実行
php artisan migrate
```

## チェックリスト

移行作業のチェックリスト：

- [ ] マイグレーションファイルを作成
- [ ] マイグレーションを実行
- [ ] 既存データを更新（Seederまたは手動）
- [ ] テストデータを作成
- [ ] フロントエンドで表示確認
- [ ] 購入フローをテスト
- [ ] エラーログを確認

## まとめ

この移行ガイドに従うことで、既存のシステムを壊すことなく、新しい購入システムを導入できます。

新しいフィールドはすべてオプショナルなので、段階的に移行することが可能です。
