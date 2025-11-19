# VIP機能（/users/importance）500エラーの修正

## 問題
`https://admin.airz.one/users/importance` にアクセスすると500エラーが発生

## 原因
1. コントローラーが存在しないカラム（`importance_score`, `importance_level`）をusersテーブルから取得しようとしていた
2. 存在しないテーブル（`user_activities`）を参照していた
3. ビューファイルが存在しないデータ（`login_count`）を参照していた

## 修正内容

### 1. UserController.php - importanceメソッド
- `importance_score`と`importance_level`をデータベースから取得するのではなく、動的に計算するように変更
- `user_activities`テーブルへの参照を削除
- スコア計算式を簡略化：
  - 購入数 × 10pt
  - 購入金額 ÷ 100pt
  - 紹介成功数 × 5pt
  - NFT発行数 × 2pt

### 2. importance.blade.php
- `login_count`の表示を`nft_count`に変更
- レベルの閾値を実際の計算式に合わせて調整
- スコア配点の説明を更新

## サーバー上での修正手順

### 1. キャッシュをクリア

```bash
cd /var/www/airzone/admin
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear
composer dump-autoload
```

### 2. パーミッションを確認

```bash
sudo chown -R www-data:www-data /var/www/airzone/admin
sudo chmod -R 775 /var/www/airzone/admin/storage
sudo chmod -R 775 /var/www/airzone/admin/bootstrap/cache
```

### 3. 動作確認

ブラウザで `https://admin.airz.one/users/importance` にアクセス

## スコア計算ロジック

### 計算式
```
importance_score = 
    (購入数 × 10) + 
    (購入金額 ÷ 100) + 
    (紹介成功数 × 5) + 
    (NFT発行数 × 2)
```

### レベル判定
- **Diamond (👑)**: 1,000pt以上
- **Platinum (💎)**: 500-999pt
- **Gold (🥇)**: 200-499pt
- **Silver (🥈)**: 50-199pt
- **Bronze (🥉)**: 0-49pt

### 例
ユーザーが以下の活動をした場合：
- 購入: 5回 → 50pt
- 購入金額: 10,000円 → 100pt
- 紹介成功: 3件 → 15pt
- NFT発行: 2回 → 4pt
- **合計: 169pt (Silver)**

## 必要なデータベーステーブル

このVIP機能は以下のテーブルを使用します：

### users
```sql
-- 基本的なusersテーブル（既存）
SELECT id, name, email, created_at, coins FROM users;
```

### orders
```sql
-- 注文テーブル
SELECT user_id, COUNT(*) as purchase_count, SUM(total_amount) as total_spent
FROM orders
WHERE status = 'completed'
GROUP BY user_id;
```

### referrals
```sql
-- 紹介テーブル
SELECT referrer_id, COUNT(*) as referral_count
FROM referrals
WHERE status = 'completed'
GROUP BY referrer_id;
```

### nft_mints
```sql
-- NFT発行テーブル
SELECT user_id, COUNT(*) as nft_count
FROM nft_mints
WHERE status = 'completed'
GROUP BY user_id;
```

## トラブルシューティング

### エラー: "SQLSTATE[42S02]: Base table or view not found: 'orders'"

ordersテーブルが存在しません。マイグレーションを実行：

```bash
cd /var/www/airzone/backend
python run_migration.py
```

または

```bash
cd /var/www/airzone/admin
php artisan migrate
```

### エラー: "SQLSTATE[42S02]: Base table or view not found: 'referrals'"

referralsテーブルが存在しません。作成：

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
    FOREIGN KEY (referred_id) REFERENCES users(id)
);
```

### エラー: "SQLSTATE[42S02]: Base table or view not found: 'nft_mints'"

nft_mintsテーブルが存在しません。作成：

```sql
CREATE TABLE IF NOT EXISTS nft_mints (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    wallet_address VARCHAR(255) NOT NULL,
    nft_object_id VARCHAR(255),
    transaction_digest VARCHAR(255),
    status ENUM('pending', 'minting', 'completed', 'failed') DEFAULT 'pending',
    metadata JSON,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
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

### ログを確認

```bash
tail -f /var/www/airzone/admin/storage/logs/laravel.log
```

## 完了チェックリスト

- [ ] キャッシュをクリア
- [ ] `https://admin.airz.one/users/importance` にアクセスできる
- [ ] VIPユーザーランキングが表示される
- [ ] スコアが正しく計算されている
- [ ] レベルアイコンが表示されている
- [ ] ユーザー詳細へのリンクが動作する

## 参考

VIP機能は以下の情報を表示します：
- ユーザーの重要度スコア
- 重要度レベル（Diamond, Platinum, Gold, Silver, Bronze）
- 購入数、紹介数、NFT発行数
- ランキング順位

この情報を使って、一括送金機能でVIPユーザーに特別報酬を送ることができます。
