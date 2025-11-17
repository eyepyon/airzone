# XRPLバッチ送金機能ガイド

## 概要

XRPLの**Batch Transactions**機能を使って、複数のユーザーに効率的にXRPを一括送信できる機能です。

### 特徴

- **高速処理**: Ticketを使った並列トランザクション送信
- **低コスト**: 通常のトランザクションと同じ手数料（約0.00001 XRP/トランザクション）
- **信頼性**: XRPLネイティブ機能による安全な送金
- **柔軟性**: ユーザーID指定、VIPユーザー、トップ紹介者など様々な条件で送信可能

## Batch Transactionsとは？

XRPLのBatch Transactionsは、**Ticket**という仕組みを使って複数のトランザクションを並列に送信できる機能です。

### 通常のトランザクション vs Batch Transactions

| 項目 | 通常のトランザクション | Batch Transactions |
|------|----------------------|-------------------|
| 送信方法 | Sequenceベース（順次） | Ticketベース（並列） |
| 処理速度 | 遅い（1つずつ） | 速い（並列処理） |
| 手数料 | 約0.00001 XRP/tx | 約0.00001 XRP/tx + Ticket作成費 |
| 複雑さ | シンプル | やや複雑 |

### 仕組み

```
1. Ticketを作成（受取人数分）
   ↓
2. 各Ticketを使ってPaymentトランザクションを並列送信
   ↓
3. 全トランザクションが独立して処理される
```

参考: https://xrpl.org/docs/concepts/transactions/batch-transactions

## 使い方

### 1. 特定のユーザーに一括送信

```bash
POST /api/v1/batch-transfer/send
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "user_ids": [1, 2, 3, 4, 5],
  "amount_xrp": 10.0,
  "reason": "Monthly reward"
}
```

**レスポンス例:**
```json
{
  "success": true,
  "summary": {
    "total": 5,
    "successful": 5,
    "failed": 0,
    "total_amount_xrp": 50.0,
    "ticket_sequence_range": "12345 - 12349"
  },
  "transactions": [
    {
      "recipient": "rN7n7otQDd6FczFgLdlqtyMVrn3HMzve5w",
      "amount_xrp": 10.0,
      "transaction_hash": "ABC123...",
      "ticket_sequence": 12345,
      "status": "success"
    }
  ],
  "errors": []
}
```

### 2. VIPユーザーに一括送信

```bash
POST /api/v1/batch-transfer/send-to-vip
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "min_importance_level": "Gold",
  "amount_xrp": 50.0,
  "reason": "VIP monthly reward"
}
```

**対象レベル:**
- `Bronze`: ブロンズ以上
- `Silver`: シルバー以上
- `Gold`: ゴールド以上
- `Platinum`: プラチナ以上
- `Diamond`: ダイヤモンドのみ

### 3. トップ紹介者に一括送信

```bash
POST /api/v1/batch-transfer/send-to-top-referrers
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "top_n": 10,
  "amount_xrp": 100.0,
  "reason": "Top 10 referrer reward"
}
```

### 4. 送信プレビュー

実際に送信する前に、対象ユーザーと金額を確認できます。

```bash
POST /api/v1/batch-transfer/preview
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "user_ids": [1, 2, 3, 4, 5],
  "amount_xrp": 10.0
}
```

**レスポンス例:**
```json
{
  "total_users": 5,
  "valid_users": 4,
  "invalid_users": 1,
  "amount_per_user_xrp": 10.0,
  "total_amount_xrp": 40.0,
  "users": [
    {
      "id": 1,
      "email": "user1@example.com",
      "wallet_address": "rN7n7otQDd6FczFgLdlqtyMVrn3HMzve5w",
      "importance_level": "Gold"
    }
  ],
  "users_without_wallet": [
    {
      "id": 5,
      "email": "user5@example.com"
    }
  ]
}
```

### 5. 送信履歴の確認

```bash
GET /api/v1/batch-transfer/history?limit=100&offset=0
Authorization: Bearer {admin_token}
```

**レスポンス例:**
```json
{
  "transfers": [
    {
      "id": 1,
      "user_id": 1,
      "wallet_address": "rN7n7otQDd6FczFgLdlqtyMVrn3HMzve5w",
      "amount_xrp": 10.0,
      "transaction_hash": "ABC123...",
      "ticket_sequence": 12345,
      "reason": "Monthly reward",
      "status": "success",
      "created_at": "2025-11-17T10:00:00Z",
      "email": "user1@example.com",
      "importance_level": "Gold"
    }
  ],
  "total": 100,
  "limit": 100,
  "offset": 0
}
```

## データベース

### batch_transfers テーブル

```sql
CREATE TABLE batch_transfers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    wallet_address VARCHAR(255) NOT NULL,
    amount_xrp DECIMAL(20, 6) NOT NULL,
    transaction_hash VARCHAR(255) NOT NULL,
    ticket_sequence INT,
    reason VARCHAR(500),
    status ENUM('success', 'failed') DEFAULT 'success',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### マイグレーション実行

```bash
mysql -u airzone_user -p airzone < backend/database/migrations/add_batch_transfers.sql
```

## ユースケース

### 1. 月次報酬配布

```javascript
// 全アクティブユーザーに10 XRPを配布
const response = await fetch('/api/v1/batch-transfer/send', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${adminToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    user_ids: activeUserIds,
    amount_xrp: 10.0,
    reason: 'November 2025 monthly reward'
  })
});
```

### 2. VIPユーザー特典

```javascript
// ゴールド以上のVIPユーザーに50 XRPを配布
const response = await fetch('/api/v1/batch-transfer/send-to-vip', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${adminToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    min_importance_level: 'Gold',
    amount_xrp: 50.0,
    reason: 'VIP exclusive reward'
  })
});
```

### 3. 紹介キャンペーン

```javascript
// トップ10紹介者に100 XRPを配布
const response = await fetch('/api/v1/batch-transfer/send-to-top-referrers', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${adminToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    top_n: 10,
    amount_xrp: 100.0,
    reason: 'Top 10 referrer bonus'
  })
});
```

## セキュリティ

### 管理者権限必須

全てのバッチ送金APIは**管理者権限**が必要です。

```python
@batch_transfer_bp.route('/batch-transfer/send', methods=['POST'])
@require_admin  # 管理者のみアクセス可能
def send_batch_transfer(current_user):
    # ...
```

### 残高確認

送信前に自動的に残高を確認し、不足している場合はエラーを返します。

```python
if sender_balance < (total_amount_drops + estimated_fees):
    raise Exception(
        f"Insufficient balance. Required: {required_xrp} XRP, "
        f"Available: {available_xrp} XRP"
    )
```

### トランザクション記録

全ての送金は`batch_transfers`テーブルに記録され、監査可能です。

## パフォーマンス

### 処理速度

- **Ticket作成**: 約3-5秒
- **各Payment**: 約3-5秒（並列処理）
- **100人への送信**: 約10-15秒

### コスト

- **Ticket作成**: 約0.00001 XRP
- **各Payment**: 約0.00001 XRP
- **100人への送信**: 約0.00101 XRP（手数料のみ）

## トラブルシューティング

### エラー: "Sponsor wallet not configured"

スポンサーウォレットが設定されていません。

```bash
# .envファイルを確認
XRPL_SPONSOR_SEED=sXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### エラー: "Insufficient balance"

スポンサーウォレットの残高が不足しています。

```bash
# テストネットの場合
# https://xrpl.org/xrp-testnet-faucet.html から資金を取得

# 本番環境の場合
# スポンサーウォレットにXRPを送金
```

### エラー: "Ticket creation failed"

ネットワークエラーまたは残高不足の可能性があります。

```bash
# ネットワーク接続を確認
# スポンサーウォレットの残高を確認
```

## ベストプラクティス

### 1. 事前プレビュー

送信前に必ずプレビューAPIで対象ユーザーと金額を確認しましょう。

```javascript
// プレビュー
const preview = await fetch('/api/v1/batch-transfer/preview', {
  method: 'POST',
  body: JSON.stringify({ user_ids, amount_xrp })
});

// 確認後に送信
if (confirm(`${preview.valid_users}人に合計${preview.total_amount_xrp} XRPを送信しますか？`)) {
  await fetch('/api/v1/batch-transfer/send', {
    method: 'POST',
    body: JSON.stringify({ user_ids, amount_xrp, reason })
  });
}
```

### 2. 適切な理由を記録

`reason`フィールドに送信理由を明記しましょう。

```javascript
{
  "reason": "November 2025 monthly active user reward"
}
```

### 3. 送信履歴の定期確認

定期的に送信履歴を確認し、異常がないかチェックしましょう。

```bash
GET /api/v1/batch-transfer/history
```

## まとめ

XRPLのBatch Transactions機能を使うことで：

- ✅ **効率的**: 複数ユーザーへの並列送信
- ✅ **低コスト**: 最小限の手数料
- ✅ **安全**: XRPLネイティブ機能
- ✅ **柔軟**: 様々な条件での送信
- ✅ **追跡可能**: 完全な履歴記録

大規模なユーザーベースへの報酬配布やキャンペーン実施に最適です！
