# AirZOne受取機能の追加

## 概要

商品の受け取り方法に「AirZOne受取」を追加しました。管理画面では複数の受け取り方法をチェックボックスで選択でき、ユーザーは購入時にその中から1つを選択します。

## 受け取り方法の種類

1. **会場内受取** (`venue_pickup`) - イベント会場で受け取り
2. **宅配便配送** (`home_delivery`) - 自宅への配送
3. **AirZOne受取** (`airzone_pickup`) - AirZOne店舗で受け取り ⭐ NEW

## データベース変更

### マイグレーション

**ファイル**: `backend/database/migrations/add_airzone_pickup_and_delivery_options.sql`

```sql
-- productsテーブル
ALTER TABLE products 
ADD COLUMN delivery_options JSON DEFAULT NULL;

-- ordersテーブル
ALTER TABLE orders 
ADD COLUMN selected_delivery_method VARCHAR(50) DEFAULT NULL;

-- order_itemsテーブル
ALTER TABLE order_items 
ADD COLUMN selected_delivery_method VARCHAR(50) DEFAULT NULL;
```

### 実行方法

```bash
mysql -u airzone_user -p airzone < backend/database/migrations/add_airzone_pickup_and_delivery_options.sql
```

## 管理画面の使い方

### 商品作成・編集

1. 商品管理画面で「新規作成」または「編集」をクリック
2. 「受け取り方法」セクションで、ユーザーに提供したい受け取り方法をチェック
   - ✅ 会場内受取
   - ✅ 宅配便配送
   - ✅ AirZOne受取
3. 複数選択可能（最低1つは必須）
4. 保存

### データ構造

```json
{
  "delivery_options": ["venue_pickup", "home_delivery", "airzone_pickup"]
}
```

## フロントエンドの実装

### 商品詳細ページ

商品の`delivery_options`配列に基づいて、利用可能な受け取り方法が表示されます。

### チェックアウトページ

`DeliveryMethodSelector`コンポーネントを使用して、ユーザーが受け取り方法を選択します。

```typescript
import DeliveryMethodSelector from '@/components/shop/DeliveryMethodSelector';

<DeliveryMethodSelector
  availableMethods={product.delivery_options || []}
  selectedMethod={selectedDeliveryMethod}
  onSelect={setSelectedDeliveryMethod}
/>
```

### 注文データ

選択された受け取り方法は以下に保存されます：

- `orders.selected_delivery_method` - 注文全体の受け取り方法
- `order_items.selected_delivery_method` - 各商品の受け取り方法

## バックエンドAPI

### Product型

```python
class Product(BaseModel):
    # ...
    delivery_options = Column(JSON, nullable=True)  # ['venue_pickup', 'home_delivery', 'airzone_pickup']
```

### APIレスポンス

```json
{
  "id": "uuid",
  "name": "商品名",
  "delivery_options": ["venue_pickup", "airzone_pickup"],
  ...
}
```

## 後方互換性

- 既存の`delivery_method`カラムは保持されています
- `delivery_options`が`null`の場合、`delivery_method`の値が使用されます
- 新規商品では`delivery_options`を使用してください

## 移行手順

### 既存商品の移行

```sql
-- 既存のdelivery_methodをdelivery_optionsに移行
UPDATE products 
SET delivery_options = JSON_ARRAY(delivery_method)
WHERE delivery_method IS NOT NULL AND delivery_options IS NULL;
```

### 確認

```sql
-- 移行結果を確認
SELECT id, name, delivery_method, delivery_options 
FROM products 
LIMIT 10;
```

## トラブルシューティング

### 管理画面でチェックボックスが表示されない

- ブラウザのキャッシュをクリア
- ビューファイルが正しく更新されているか確認

### フロントエンドで受け取り方法が表示されない

1. APIレスポンスを確認
   ```bash
   curl http://localhost:5000/api/v1/products/{id}
   ```

2. `delivery_options`フィールドが含まれているか確認

3. フロントエンドを再ビルド
   ```bash
   cd frontend
   npm run build
   ```

### 注文時にエラーが発生する

- `selected_delivery_method`が正しく送信されているか確認
- バックエンドのバリデーションを確認

## 完了

AirZOne受取機能が追加され、管理画面とフロントエンドの両方で利用可能になりました。
