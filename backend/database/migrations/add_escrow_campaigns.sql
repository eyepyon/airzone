-- Escrowステーキングキャンペーンシステム

-- キャンペーンテーブル
CREATE TABLE escrow_campaigns (
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
CREATE TABLE escrow_stakes (
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
