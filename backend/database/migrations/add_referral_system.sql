-- 紹介リンクシステム用テーブル

-- ユーザーテーブルに紹介コードとコイン残高を追加
ALTER TABLE users 
ADD COLUMN referral_code VARCHAR(20) UNIQUE,
ADD COLUMN coins INT DEFAULT 0,
ADD COLUMN referred_by CHAR(36) NULL,
ADD INDEX idx_referral_code (referral_code),
ADD INDEX idx_referred_by (referred_by);

-- 紹介履歴テーブル
CREATE TABLE referrals (
    id CHAR(36) PRIMARY KEY,
    referrer_id CHAR(36) NOT NULL,
    referred_id CHAR(36) NOT NULL,
    status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
    coins_awarded INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (referrer_id) REFERENCES users(id),
    FOREIGN KEY (referred_id) REFERENCES users(id),
    INDEX idx_referrer (referrer_id),
    INDEX idx_referred (referred_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- コイン取引履歴テーブル
CREATE TABLE coin_transactions (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    amount INT NOT NULL,
    transaction_type ENUM('referral_bonus', 'purchase', 'admin_adjustment') NOT NULL,
    description TEXT,
    balance_after INT NOT NULL,
    related_id CHAR(36) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user (user_id),
    INDEX idx_type (transaction_type),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 商品テーブルに紹介限定フラグを追加
ALTER TABLE products
ADD COLUMN is_referral_only BOOLEAN DEFAULT FALSE,
ADD INDEX idx_referral_only (is_referral_only);
