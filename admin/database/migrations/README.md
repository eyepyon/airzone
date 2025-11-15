# データベースマイグレーション

## user_activities テーブル

効果測定（DAU、MAU、ダウンロード数など）のためのユーザーアクティビティを記録するテーブルです。

### マイグレーション実行

```bash
# Laravelマイグレーション実行
php artisan migrate
```

### 手動でテーブル作成する場合

```sql
CREATE TABLE user_activities (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    activity_type VARCHAR(255) NOT NULL,
    ip_address VARCHAR(255) NULL,
    user_agent VARCHAR(255) NULL,
    metadata JSON NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_created (user_id, created_at),
    INDEX idx_activity_created (activity_type, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## アクティビティタイプ

- `login`: ユーザーログイン（DAU/MAU計測用）
- `download`: 商品ダウンロード（DL数計測用）
- `purchase`: 商品購入（売上分析用）

## バックエンド連携

バックエンドAPIは以下のタイミングでアクティビティを自動記録します：

1. **ログイン時** (`/api/v1/auth/google`)
   - `activity_type`: `login`
   - DAU/MAU計測に使用

2. **ダウンロード時** (`/api/v1/downloads/product/{product_id}`)
   - `activity_type`: `download`
   - ダウンロード数計測に使用

3. **購入時** (`/api/v1/orders`)
   - `activity_type`: `purchase`
   - 売上分析に使用
