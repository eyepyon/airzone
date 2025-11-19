# クイック修正サマリー

## 問題

商品データに新しいフィールド（`product_type`, `purchase_restriction`, `delivery_method`など）を追加したことで、既存のデータと互換性がなくなり、以下のエラーが発生：

```
TypeError: can't access property "toLocaleString", product.price is undefined
```

## 原因

1. 既存の商品データに新しいフィールドが存在しない
2. `product.price`が`undefined`の場合の処理がない
3. 新しいフィールドが必須になっていた

## 解決方法

### 1. 型定義の修正

新しいフィールドをオプショナルに変更：

```typescript
// frontend/types/index.ts
export interface Product {
  id: string;
  name: string;
  description: string | null;
  price: number;
  stock_quantity: number;
  image_url: string | null;
  product_type?: ProductType;              // ← オプショナル
  delivery_method?: DeliveryMethod | null; // ← オプショナル
  purchase_restriction?: PurchaseRestriction; // ← オプショナル
  required_nft_id?: string | null;
  is_active: boolean;
  event_date?: string | null;
  venue?: string | null;
  created_at: string;
  updated_at: string;
}
```

### 2. デフォルト値の設定

```typescript
// frontend/components/shop/ProductCard.tsx
const productWithDefaults = {
  ...product,
  product_type: product.product_type || 'goods',
  purchase_restriction: product.purchase_restriction || 'public',
  delivery_method: product.delivery_method || null,
};
```

### 3. 価格の安全な表示

```typescript
// ProductCard.tsx
const formatPrice = (price: number | undefined) => {
  if (price === undefined || price === null) {
    return '価格未設定';
  }
  return new Intl.NumberFormat('ja-JP', {
    style: 'currency',
    currency: 'JPY',
  }).format(price);
};

// 商品詳細ページ
{product.price !== undefined && product.price !== null
  ? `¥${product.price.toLocaleString()}`
  : '価格未設定'}
```

### 4. 条件付きバッジ表示

```typescript
// 新しいフィールドが存在する場合のみバッジを表示
{(product.product_type || product.purchase_restriction) && (
  <div className="flex flex-wrap gap-2 mb-3">
    {/* バッジ */}
  </div>
)}
```

## 修正したファイル

1. ✅ `frontend/types/index.ts` - 型定義をオプショナルに
2. ✅ `frontend/components/shop/ProductCard.tsx` - デフォルト値と安全な価格表示
3. ✅ `frontend/app/shop/[id]/page.tsx` - 商品詳細ページの価格表示
4. ✅ `frontend/lib/purchase-restrictions.ts` - デフォルト値の処理

## 動作確認

### ✅ 既存の商品データ
- 新しいフィールドがなくても正常に表示される
- 価格が`undefined`でもエラーにならない
- デフォルト値（`goods`, `public`）が使用される

### ✅ 新しい商品データ
- 商品タイプのバッジが表示される
- 購入制限のバッジが表示される
- 配送方法が表示される（グッズの場合）

## 今後の対応

### データベース移行（推奨）

新しいフィールドをデータベースに追加：

```bash
cd admin
php artisan make:migration add_new_fields_to_products_table
php artisan migrate
```

詳細は `MIGRATION_GUIDE.md` を参照。

### 既存データの更新

```php
// 既存商品を一括更新
Product::whereNull('product_type')->update([
    'product_type' => 'goods',
    'purchase_restriction' => 'public',
]);
```

## テスト項目

- [x] 商品一覧ページが表示される
- [x] 商品詳細ページが表示される
- [x] 価格が正しく表示される
- [x] カートに追加できる
- [x] 新しいフィールドがある商品でバッジが表示される
- [x] 新しいフィールドがない商品でもエラーが出ない

## まとめ

すべてのエラーが修正され、既存データとの後方互換性が確保されました。

新しい機能を使用する場合は、データベース移行を実行してください。
