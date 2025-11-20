# エスクローキャンペーン管理画面 500エラー修正

## 問題

エスクローキャンペーン管理画面にアクセスすると500エラーが発生します。

## 原因

`escrow_campaigns` と `escrow_stakes` テーブルがデータベースに存在しないため、クエリが失敗しています。

## 解決方法

### 1. マイグレーションファイルの実行

以下のSQLファイルを実行してテーブルを作成します：

**ファイル**: `backend/database/migrations/add_escrow_campaigns.sql`

### 2. マイグレーション実行手順

#### 方法1: MySQLコマンドラインから実行

```powershell
# PowerShellから実行
mysql -u airzone_user -p airzone < backend/database/migrations/add_escrow_campaigns.sql
```

パスワード入力: `airzone123`（環境に応じて変更）

#### 方法2: MySQLクライアントで直接実行

```sql
-- MySQLにログイン
mysql -u airzone_user -p airzone

-- マイグレーションファイルの内容を実行
source backend/database/migrations/add_escrow_campaigns.sql;

-- または、ファイルの内容をコピー＆ペーストして実行
```

#### 方法3: 手動でテーブル作成

MySQLクライアントで以下のSQLを実行：

```sql
USE airzone;

-- キャンペーンテーブル
CREATE TABLE IF NOT EXISTS escrow_campaigns (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    min_amount_drops BIGINT NOT NULL,
    lock_days INT NOT NULL,
    nft_reward_name VARCHAR(255) NOT NULL,
    nft_reward_description TEXT,
    nft_reward_image_url VARCHAR(500),
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    max_participants INT DEFAULT NULL,
    current_participants INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_active (is_active),
    INDEX idx_dates (start_date, end_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Escrowステークテーブル
CREATE TABLE IF NOT EXISTS escrow_stakes (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    campaign_id CHAR(36) NOT NULL,
    wallet_address VARCHAR(255) NOT NULL,
    amount_drops BIGINT NOT NULL,
    lock_days INT NOT NULL,
    finish_after TIMESTAMP NOT NULL,
    escrow_sequence INT NOT NULL,
    transaction_hash VARCHAR(255) NOT NULL,
    status ENUM('active', 'completed', 'cancelled') DEFAULT 'active',
    nft_awarded BOOLEAN DEFAULT FALSE,
    nft_mint_id CHAR(36) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (campaign_id) REFERENCES escrow_campaigns(id),
    INDEX idx_user (user_id),
    INDEX idx_campaign (campaign_id),
    INDEX idx_status (status),
    INDEX idx_finish (finish_after)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- サンプルキャンペーンを挿入
INSERT INTO escrow_campaigns 
(id, name, description, min_amount_drops, lock_days, 
 nft_reward_name, nft_reward_description, nft_reward_image_url,
 start_date, end_date, max_participants, is_active)
VALUES 
(UUID(), 
 'XRPステーキングキャンペーン', 
 '100 XRPを30日間ロックすると限定NFTがもらえる！',
 100000000,
 30,
 'Airzone Staker NFT',
 'XRPステーキングキャンペーン参加記念NFT',
 'https://example.com/nft/staker.png',
 NOW(),
 DATE_ADD(NOW(), INTERVAL 90 DAY),
 1000,
 TRUE);
```

### 3. テーブル作成の確認

```sql
-- テーブルが作成されたか確認
SHOW TABLES LIKE 'escrow%';

-- テーブル構造を確認
DESCRIBE escrow_campaigns;
DESCRIBE escrow_stakes;

-- サンプルデータを確認
SELECT * FROM escrow_campaigns;
```

### 4. 管理画面で確認

マイグレーション実行後、以下のURLにアクセスして確認：

- エスクローキャンペーン一覧: `http://localhost/admin/escrow-campaigns`
- 統計ページ: `http://localhost/admin/escrow-campaigns/stats`

## トラブルシューティング

### エラー: "Table 'airzone.escrow_campaigns' doesn't exist"

→ マイグレーションが実行されていません。上記の手順でテーブルを作成してください。

### エラー: "Cannot add foreign key constraint"

→ `users` テーブルが存在しない可能性があります。先に基本的なテーブルを作成してください。

```sql
-- usersテーブルの存在確認
SHOW TABLES LIKE 'users';
```

### エラー: "Access denied for user"

→ データベースユーザーの権限を確認してください。

```sql
-- 権限を確認
SHOW GRANTS FOR 'airzone_user'@'localhost';

-- 必要に応じて権限を付与
GRANT ALL PRIVILEGES ON airzone.* TO 'airzone_user'@'localhost';
FLUSH PRIVILEGES;
```

## 完了

マイグレーション実行後、エスクローキャンペーン管理画面が正常に動作するようになります。
