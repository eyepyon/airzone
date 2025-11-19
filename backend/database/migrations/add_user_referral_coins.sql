-- ユーザーテーブルに紹介機能とコイン関連のカラムを追加

-- referral_codeカラムを追加（存在しない場合）
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS referral_code VARCHAR(20) UNIQUE;

-- referred_byカラムを追加（存在しない場合）
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS referred_by CHAR(36);

-- coinsカラムを追加（存在しない場合）
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS coins INT DEFAULT 0;

-- インデックスを追加
CREATE INDEX IF NOT EXISTS idx_users_referral_code ON users(referral_code);
CREATE INDEX IF NOT EXISTS idx_users_referred_by ON users(referred_by);

-- 既存データのデフォルト値を設定
UPDATE users SET coins = 0 WHERE coins IS NULL;
