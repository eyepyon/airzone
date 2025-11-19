# 商品管理機能の拡張 - カテゴリーと受け取り方法

## 概要

商品管理機能に以下の項目を追加しました：
- **カテゴリー**: グッズ、NFT、チケット
- **受け取り方法**: 会場内受取、宅配便配送

## データベースマイグレーション

### 1. マイグレーションファイル

**ファイル**: `backend/database/migrations/add_product_category_delivery.sql`

以下のカラムを追加：
- `category`: ENUM('goods', 'nft', 'ticket') - 商品カテゴリー
- `delivery_method`: ENUM('venue_pickup', 'home_delivery') - 受け取り方法

### 2. マイグレーション実行

```bash
# Windowsの場合（PowerShell）
Get-Content backend/database/migrations/add_product_category_delivery.sql | mysql -u airzone_user -p airzone

# または直接MySQLクライアントで
mysql -u airzone_user -p airzone < backend/database/migrations/add_product_category_delivery.sql
```

パスワード: `airzone123`（環境に応じて変更）

### 3. マイグレーション確認

```sql
-- テーブル構造を確認
DESCRIBE products;

-- 既存データを確認
SELECT id, name, category, delivery_method FROM products;
```

## 実装内容

### 1. 管理画面の更新

#### コントローラー (`ProductController.php`)
- `store()`: カテゴリーと受け取り方法のバリデーション追加
- `update()`: カテゴリーと受け取り方法のバリデーション追加

#### ビューファイル

**商品一覧** (`index.blade.php`)
- カテゴリーと受け取り方法の列を追加
- カラーバッジで視覚的に表示

**商品作成** (`create.blade.php`)
- カテゴリー選択ドロップダウン（必須）
  - グッズ
  - NFT
  - チケット
- 受け取り方法選択ドロップダウン（必須）
  - 会場内受取
  - 宅配便配送

**商品編集** (`edit.blade.php`)
- 作成フォームと同じ項目を編集可能

### 2. バックエンドAPIの更新

#### モデル (`backend/models/product.py`)
```python
category = Column(String(20), nullable=True, default='goods')
delivery_method = Column(String(20), nullable=True, default='venue_pickup')
```

#### APIレスポンス
商品情報に以下のフィールドが追加されます：
```json
{
  "id": "uuid",
  "name": "商品名",
  "category": "goods",
  "delivery_method": "venue_pickup",
  "price": 1000,
  ...
}
```

## カテゴリーと受け取り方法の値

### カテゴリー (category)

| 値 | 表示名 | 説明 |
|---|---|---|
| `goods` | グッズ | 物理的な商品 |
| `nft` | NFT | デジタルNFT |
| `ticket` | チケット | イベントチケット |

### 受け取り方法 (delivery_method)

| 値 | 表示名 | 説明 |
|---|---|---|
| `venue_pickup` | 会場内受取 | イベント会場で受け取り |
| `home_delivery` | 宅配便配送 | 自宅への配送 |

## 使用方法

### 商品作成

1. 管理画面にログイン
2. 「商品」メニューをクリック
3. 「新規作成」ボタンをクリック
4. 以下の情報を入力：
   - 商品名（必須）
   - 説明
   - **カテゴリー（必須）**: グッズ/NFT/チケットから選択
   - **受け取り方法（必須）**: 会場内受取/宅配便配送から選択
   - 価格（必須）
   - 在庫数（必須）
   - 画像URL
   - 公開ステータス
5. 「作成」ボタンをクリック

### 商品編集

1. 商品一覧から編集したい商品の「編集」をクリック
2. カテゴリーと受け取り方法を変更可能
3. 「更新」ボタンをクリック

### 商品一覧での表示

商品一覧では、カテゴリーと受け取り方法がカラーバッジで表示されます：

**カテゴリー**:
- グッズ: 青色バッジ
- NFT: 紫色バッジ
- チケット: 黄色バッジ

**受け取り方法**:
- 会場内受取: 緑色バッジ
- 宅配便配送: オレンジ色バッジ

## 既存データの扱い

マイグレーション実行時、既存の商品データには以下のデフォルト値が設定されます：
- `category`: `goods`（グッズ）
- `delivery_method`: `venue_pickup`（会場内受取）

必要に応じて、管理画面から個別に変更してください。

## 注意事項

1. **必須項目**: カテゴリーと受け取り方法は必須項目です
2. **既存データ**: マイグレーション後、既存商品のカテゴリーと受け取り方法を確認・更新してください
3. **バックエンド連携**: フロントエンドでこれらの情報を表示する場合は、APIレスポンスに含まれます

## 完了

商品管理機能にカテゴリーと受け取り方法の項目が追加されました。マイグレーションを実行してから使用してください。
