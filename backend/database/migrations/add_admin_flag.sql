-- 管理者フラグをusersテーブルに追加
ALTER TABLE users 
ADD COLUMN is_admin BOOLEAN DEFAULT FALSE AFTER importance_level;

-- インデックスを追加
CREATE INDEX idx_users_is_admin ON users(is_admin);

-- 既存のユーザーで最初のユーザーを管理者に設定（オプション）
-- UPDATE users SET is_admin = TRUE WHERE id = 1;
