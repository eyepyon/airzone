-- ユーザー重要度スコアシステム

-- ユーザーテーブルに重要度スコアを追加
ALTER TABLE users 
ADD COLUMN importance_score INT DEFAULT 0,
ADD COLUMN importance_level ENUM('bronze', 'silver', 'gold', 'platinum', 'diamond') DEFAULT 'bronze',
ADD COLUMN last_score_updated TIMESTAMP NULL,
ADD INDEX idx_importance_score (importance_score DESC),
ADD INDEX idx_importance_level (importance_level);

-- リファラルクリック追跡テーブル
CREATE TABLE referral_clicks (
    id CHAR(36) PRIMARY KEY,
    referral_code VARCHAR(20) NOT NULL,
    referrer_id CHAR(36) NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    converted BOOLEAN DEFAULT FALSE,
    converted_user_id CHAR(36) NULL,
    FOREIGN KEY (referrer_id) REFERENCES users(id),
    FOREIGN KEY (converted_user_id) REFERENCES users(id),
    INDEX idx_referral_code (referral_code),
    INDEX idx_referrer (referrer_id),
    INDEX idx_clicked_at (clicked_at),
    INDEX idx_converted (converted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- スコア履歴テーブル
CREATE TABLE user_score_history (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    score_before INT NOT NULL,
    score_after INT NOT NULL,
    score_change INT NOT NULL,
    reason VARCHAR(255) NOT NULL,
    details JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user (user_id),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
