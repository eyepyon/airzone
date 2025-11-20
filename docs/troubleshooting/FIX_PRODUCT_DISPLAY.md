# 商品詳細ページ表示問題の修正

## 問題

商品詳細ページで以下の問題が発生：
- 「価格未設定」と表示される
- 「Out of stock」と表示される
- 購入ボタンが無効化されている

## 原因

1. データベースの商品データに`price`または`stock_quantity`が正しく設定されていない
2. `api-client.ts`で`API_URL`がハードコードされていた

## 修正内容

### 1. API_URLの修正

**ファイル**: `frontend/lib/api-client.ts`

```typescript
// 修正前
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api.airz.one';

// 修正後
const API_URL = process.env.NEXT_PUBLIC_API_URL || '';
```

これにより、環境変数が空の場合は相対パスを使用します。

### 2. データベースの商品データを確認

```sql
-- 特定の商品を確認
SELECT 
    id,
    name,
    price,
    stock_quantity,
    is_active,
    category,
    delivery_method
FROM products 
WHERE id = '576d325b-c172-4983-b2ac-e76634f3c76b';
```

### 3. 商品データを修正

```sql
-- 価格と在庫を設定
UPDATE products 
SET 
    price = 1000,  -- 価格を設定（円単位）
    stock_quantity = 10,  -- 在庫数を設定
    is_active = 1  -- 有効化
WHERE id = '576d325b-c172-4983-b2ac-e76634f3c76b';

-- 確認
SELECT * FROM products 
WHERE id = '576d325b-c172-4983-b2ac-e76634f3c76b';
```

### 4. すべての商品を確認

```sql
-- すべての商品の状態を確認
SELECT 
    id,
    name,
    price,
    stock_quantity,
    is_active,
    CASE 
        WHEN price IS NULL OR price = 0 THEN '価格未設定'
        WHEN stock_quantity IS NULL OR stock_quantity = 0 THEN '在庫切れ'
        WHEN is_active = 0 THEN '非公開'
        ELSE '正常'
    END as status
FROM products
ORDER BY created_at DESC;
```

### 5. 一括修正（必要に応じて）

```sql
-- すべての商品に適切な値を設定
UPDATE products 
SET 
    price = CASE 
        WHEN price IS NULL OR price = 0 THEN 1000
        ELSE price
    END,
    stock_quantity = CASE 
        WHEN stock_quantity IS NULL OR stock_quantity = 0 THEN 10
        ELSE stock_quantity
    END,
    is_active = 1
WHERE is_active = 1;
```

## フロントエンドの再ビルド

```bash
cd frontend
npm run build
```

## 動作確認

### 1. APIレスポンスを確認

```bash
# 商品詳細を取得
curl -X GET http://localhost:5000/api/v1/products/576d325b-c172-4983-b2ac-e76634f3c76b

# 期待されるレスポンス
{
  "status": "success",
  "data": {
    "id": "576d325b-c172-4983-b2ac-e76634f3c76b",
    "name": "商品名",
    "description": "商品説明",
    "price": 1000,
    "stock_quantity": 10,
    "is_active": true,
    "category": "goods",
    "delivery_method": "venue_pickup",
    ...
  }
}
```

### 2. フロントエンドで確認

1. https://airz.one/shop/576d325b-c172-4983-b2ac-e76634f3c76b にアクセス
2. 以下が正しく表示されることを確認：
   - 価格（例: ¥1,000）
   - 在庫数（例: 10 in stock）
   - 「カートに追加」ボタンが有効

3. F12キーを押して開発者ツールを開く
4. Networkタブで以下を確認：
   - `/api/v1/products/...` のリクエスト
   - ステータスコード（200 OK）
   - レスポンスに`price`と`stock_quantity`が含まれている

## トラブルシューティング

### 価格が0円と表示される場合

```sql
-- priceカラムのデータ型を確認
DESCRIBE products;

-- priceが0の商品を確認
SELECT id, name, price FROM products WHERE price = 0 OR price IS NULL;

-- 修正
UPDATE products SET price = 1000 WHERE price = 0 OR price IS NULL;
```

### 在庫が0と表示される場合

```sql
-- stock_quantityが0の商品を確認
SELECT id, name, stock_quantity FROM products WHERE stock_quantity = 0 OR stock_quantity IS NULL;

-- 修正
UPDATE products SET stock_quantity = 10 WHERE stock_quantity = 0 OR stock_quantity IS NULL;
```

### APIが404エラーを返す場合

1. **バックエンドが起動しているか確認**
   ```bash
   curl http://localhost:5000/health
   ```

2. **環境変数を確認**
   ```bash
   cat frontend/.env
   # NEXT_PUBLIC_API_URL= （空文字列）
   ```

3. **バックエンドを再起動**
   ```bash
   cd backend
   python app.py
   ```

## 商品管理画面での設定

管理画面から商品を編集する場合：

1. http://localhost/admin/products にアクセス
2. 編集したい商品の「編集」をクリック
3. 以下を設定：
   - 価格: 1000（円単位）
   - 在庫数: 10
   - カテゴリー: グッズ/NFT/チケット
   - 受け取り方法: 会場内受取/宅配便配送
   - 公開する: チェック
4. 「更新」をクリック

## 完了

修正後、商品詳細ページで以下が正しく表示されます：
- ✅ 価格が表示される
- ✅ 在庫数が表示される
- ✅ 「カートに追加」ボタンが有効
- ✅ 購入が可能

## 関連ドキュメント

- `admin/PRODUCT_CATEGORY_DELIVERY_UPDATE.md` - 商品カテゴリーと受け取り方法の追加
- `FINAL_API_FIX_SUMMARY.md` - API接続問題の修正
