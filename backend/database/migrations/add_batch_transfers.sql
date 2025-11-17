-- バッチ送金履歴テーブル
CREATE TABLE IF NOT EXISTS batch_transfers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    wallet_address VARCHAR(255) NOT NULL,
    amount_xrp DECIMAL(20, 6) NOT NULL,
    transaction_hash VARCHAR(255) NOT NULL,
    ticket_sequence INT,
    reason VARCHAR(500),
    status ENUM('success', 'failed') DEFAULT 'success',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_status (status),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- バッチ送金統計ビュー
CREATE OR REPLACE VIEW batch_transfer_stats AS
SELECT 
    DATE(created_at) as transfer_date,
    COUNT(*) as total_transfers,
    SUM(amount_xrp) as total_amount_xrp,
    AVG(amount_xrp) as avg_amount_xrp,
    COUNT(DISTINCT user_id) as unique_users
FROM batch_transfers
WHERE status = 'success'
GROUP BY DATE(created_at)
ORDER BY transfer_date DESC;
