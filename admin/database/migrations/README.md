# Database Migrations

このディレクトリには、Airzone アプリケーションのデータベーススキーマを作成するためのLaravel migrationファイルが含まれています。

## マイグレーションファイル一覧

1. `2024_01_01_000001_create_users_table.php` - ユーザーテーブル
2. `2024_01_01_000002_create_wallets_table.php` - XRPLウォレットテーブル
3. `2024_01_01_000003_create_products_table.php` - 商品テーブル
4. `2024_01_01_000004_create_orders_table.php` - 注文テーブル
5. `2024_01_01_000005_create_order_items_table.php` - 注文明細テーブル
6. `2024_01_01_000006_create_payments_table.php` - 決済テーブル
7. `2024_01_01_000007_create_nft_mints_table.php` - NFTミントテーブル
8. `2024_01_01_000008_create_referrals_table.php` - 紹介テーブル
9. `2024_01_01_000009_create_coin_transactions_table.php` - コイン取引テーブル

## 使用方法

### Laravel管理画面から実行

```bash
cd admin
php artisan migrate
```

### マイグレーションのロールバック

```bash
php artisan migrate:rollback
```

### すべてのマイグレーションをリセット

```bash
php artisan migrate:reset
```

### マイグレーションをリセットして再実行

```bash
php artisan migrate:refresh
```

## テーブル構造

### users
- Google OAuth認証を使用するユーザー情報
- 各ユーザーは1つのXRPLウォレットを持つ

### wallets
- XRPLブロックチェーンウォレット情報
- 秘密鍵は暗号化されて保存される

### products
- EC ショップの商品情報
- NFT所有要件をオプションで設定可能

### orders
- 顧客の注文情報
- ステータス: pending, processing, completed, failed, cancelled

### order_items
- 注文の明細情報
- 商品、数量、価格を記録

### payments
- Stripe決済情報
- ステータス: pending, processing, succeeded, failed, cancelled

### nft_mints
- NFTミント操作の追跡
- ステータス: pending, minting, completed, failed

### referrals
- ユーザー紹介システム
- 紹介者と被紹介者の関係を記録

### coin_transactions
- コイン取引履歴
- ユーザーのコイン残高変動を追跡

## 注意事項

1. **実行順序**: マイグレーションファイルは番号順に実行されます。外部キー制約があるため、順序を変更しないでください。

2. **データベース設定**: `.env`ファイルでデータベース接続情報を設定してください：
   ```
   DB_CONNECTION=mysql
   DB_HOST=localhost
   DB_PORT=3306
   DB_DATABASE=airdb
   DB_USERNAME=kanri
   DB_PASSWORD=your_password
   ```

3. **UUID**: すべてのテーブルで主キーとしてUUID（36文字の文字列）を使用しています。

4. **タイムスタンプ**: すべてのテーブルに`created_at`と`updated_at`カラムがあります（一部例外あり）。

5. **外部キー制約**: 関連テーブルが削除された場合、カスケード削除が設定されています。

## Python バックエンドとの互換性

これらのマイグレーションは、Pythonバックエンド（Flask + SQLAlchemy）のモデル定義と完全に互換性があります：

- `backend/models/user.py`
- `backend/models/wallet.py`
- `backend/models/product.py`
- `backend/models/order.py`
- `backend/models/payment.py`
- `backend/models/nft_mint.py`
- `backend/models/referral.py`

## トラブルシューティング

### マイグレーションエラーが発生した場合

1. データベース接続を確認
   ```bash
   php artisan db:show
   ```

2. マイグレーションステータスを確認
   ```bash
   php artisan migrate:status
   ```

3. 特定のマイグレーションのみ実行
   ```bash
   php artisan migrate --path=/database/migrations/2024_01_01_000001_create_users_table.php
   ```

### 外部キー制約エラー

外部キー制約エラーが発生した場合は、参照先のテーブルが先に作成されているか確認してください。

## 開発環境

- Laravel 10.x
- MySQL 8.0+
- PHP 8.1+

## 本番環境への適用

本番環境では、以下の手順でマイグレーションを実行してください：

```bash
# バックアップを取得
mysqldump -u username -p airdb > backup_$(date +%Y%m%d_%H%M%S).sql

# マイグレーション実行
php artisan migrate --force
```

`--force`フラグは本番環境で必要です。
