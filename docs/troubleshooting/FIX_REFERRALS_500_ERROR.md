# Referrals 500エラーの修正

## 問題
`https://admin.airz.one/referrals` にアクセスすると500エラーが発生

## 原因
1. コントローラーが存在しないカラム（`importance_score`, `importance_level`）を参照
2. 存在しないテーブル（`referral_clicks`）を参照
3. ビューファイルが存在しないデータを参照

## 修正内容

### 1. ReferralController.php
- `importance_score`, `importance_level`カラムの参照を削除
- `referral_clicks`テーブルのJOINを削除
- GROUP BYを簡略化

### 2. index.blade.php
- `importance_level`の表示を削除
- `click_count`の表示を削除

## サーバー上での修正手順

### 1. キャッシュをクリア

```bash
cd /var/www/airzone/admin
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear
```

### 2. Composerのオートロードを再生成

```bash
composer dump-autoload
```

### 3. パーミッションを確認

```bash
sudo chown -R www-data:www-data /var/www/airzone/admin
sudo chmod -R 775 /var/www/airzone/admin/storage
sudo chmod -R 775 /var/www/airzone/admin/bootstrap/cache
```

### 4. ログを確認

エラーが続く場合は、ログを確認：

```bash
tail -f /var/www/airzone/admin/storage/logs/laravel.log
```

### 5. データベーステーブルを確認

必要なテーブルが存在するか確認：

```bash
mysql -u kanri -p airdb
```

```sql
-- テーブル一覧を確認
SHOW TABLES;

-- referralsテーブルの構造を確認
DESCRIBE referrals;

-- usersテーブルの構造を確認
DESCRIBE users;

-- coin_transactionsテーブルの構造を確認
DESCRIBE coin_transactions;

-- データを確認
SELECT COUNT(*) FROM referrals;
SELECT COUNT(*) FROM users WHERE referral_code IS NOT NULL;

exit;
```

## 必要なテーブル構造

### referralsテーブル

```sql
CREATE TABLE IF NOT EXISTS referrals (
    id VARCHAR(36) PRIMARY KEY,
    referrer_id VARCHAR(36) NOT NULL,
    referred_id VARCHAR(36) NOT NULL,
    status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
    coins_awarded INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (referrer_id) REFERENCES users(id),
    FOREIGN KEY (referred_id) REFERENCES users(id),
    INDEX idx_referrer (referrer_id),
    INDEX idx_referred (referred_id),
    INDEX idx_status (status)
);
```

### usersテーブルに必要なカラム

```sql
-- referral_code, referred_by, coinsカラムが存在するか確認
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS referral_code VARCHAR(20) UNIQUE,
ADD COLUMN IF NOT EXISTS referred_by VARCHAR(36),
ADD COLUMN IF NOT EXISTS coins INT DEFAULT 0;

-- インデックスを追加
CREATE INDEX IF NOT EXISTS idx_referral_code ON users(referral_code);
CREATE INDEX IF NOT EXISTS idx_referred_by ON users(referred_by);
```

### coin_transactionsテーブル

```sql
CREATE TABLE IF NOT EXISTS coin_transactions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    amount INT NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    description VARCHAR(500),
    balance_after INT NOT NULL,
    related_id VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user (user_id),
    INDEX idx_type (transaction_type),
    INDEX idx_created (created_at)
);
```

## マイグレーションの実行

必要なマイグレーションファイルが存在する場合：

```bash
cd /var/www/airzone/admin
php artisan migrate
```

または、バックエンドのマイグレーションを実行：

```bash
cd /var/www/airzone/backend
python run_migration.py
```

## 動作確認

1. ブラウザで `https://admin.airz.one/referrals` にアクセス
2. エラーなく紹介一覧ページが表示されることを確認
3. 統計情報が正しく表示されることを確認

## トラブルシューティング

### エラー: "SQLSTATE[42S22]: Column not found"

カラムが存在しません。上記のALTER TABLE文を実行してください。

### エラー: "SQLSTATE[42S02]: Base table or view not found"

テーブルが存在しません。上記のCREATE TABLE文を実行してください。

### エラー: "Class 'App\Models\Referral' not found"

モデルファイルが必要な場合は作成：

```bash
php artisan make:model Referral
```

### 500エラーが続く場合

デバッグモードを有効にして詳細なエラーを確認：

```bash
nano /var/www/airzone/admin/.env
```

```env
APP_DEBUG=true
```

ブラウザでページをリロードして、詳細なエラーメッセージを確認してください。

問題解決後は必ずデバッグモードを無効に：

```env
APP_DEBUG=false
```

## 完了

修正が完了したら、以下を確認：

- ✅ `/referrals` - 紹介一覧が表示される
- ✅ `/referrals/ranking` - ランキングが表示される
- ✅ `/referrals/{id}` - 個別の紹介詳細が表示される
