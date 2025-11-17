# XRP Escrowステーキングキャンペーン

## 概要

XRPLのEscrow機能を使用して、一定期間XRPをロックすることで限定NFTを獲得できるキャンペーンシステムです。

## 仕組み

### Escrowとは

XRPLのEscrow機能は、XRPを一定期間ロックする仕組みです：

1. **ロック**: XRPを指定期間ロック
2. **保管**: ブロックチェーン上で安全に保管
3. **解放**: 期間終了後に自動的に受け取り可能

### キャンペーンフロー

```
ユーザー
  ↓ 1. キャンペーンを選択
  ↓ 2. ロックするXRP量を指定
フロントエンド
  ↓ 3. POST /api/v1/escrow/stake
バックエンド
  ├─ 4. キャンペーン条件を確認
  ├─ 5. Escrowトランザクション作成
  └─ 6. XRPLネットワークに送信
  ↓
XRPL Network
  ├─ 7. XRPをロック
  └─ 8. Escrowシーケンス番号を返却
  ↓
バックエンド
  ├─ 9. データベースに記録
  └─ 10. 参加者数を更新
  ↓
[ロック期間中]
  ↓
[期間終了]
  ↓
バックエンド（定期チェック）
  ├─ 11. 完了可能なEscrowを検出
  ├─ 12. Escrow完了トランザクション実行
  ├─ 13. XRPをユーザーに返却
  └─ 14. 限定NFTを発行
  ↓
ユーザー（XRP返却 + NFT獲得）
```

## キャンペーン設定

### 必須パラメータ

- **名前**: キャンペーン名
- **説明**: キャンペーンの説明
- **最小ロック量**: 最低何XRPが必要か
- **ロック期間**: 何日間ロックするか
- **NFT報酬**: 獲得できるNFTの情報
- **開始日時**: キャンペーン開始
- **終了日時**: キャンペーン終了
- **最大参加者数**: 上限（オプション）

### 設定例

```sql
INSERT INTO escrow_campaigns 
(id, name, description, min_amount_drops, lock_days, 
 nft_reward_name, nft_reward_description, nft_reward_image_url,
 start_date, end_date, max_participants, is_active)
VALUES 
(UUID(), 
 'XRPステーキングキャンペーン', 
 '100 XRPを30日間ロックすると限定NFTがもらえる！',
 100000000,  -- 100 XRP
 30,         -- 30日間
 'Airzone Staker NFT',
 'XRPステーキングキャンペーン参加記念NFT',
 'https://example.com/nft/staker.png',
 NOW(),
 DATE_ADD(NOW(), INTERVAL 90 DAY),
 1000,       -- 最大1000人
 TRUE);
```

## API エンドポイント

### キャンペーン一覧取得

```bash
GET /api/v1/escrow/campaigns
```

レスポンス:
```json
{
  "status": "success",
  "data": {
    "campaigns": [
      {
        "id": "uuid",
        "name": "XRPステーキングキャンペーン",
        "description": "100 XRPを30日間ロックすると限定NFTがもらえる！",
        "min_amount_xrp": 100,
        "lock_days": 30,
        "nft_reward": {
          "name": "Airzone Staker NFT",
          "description": "...",
          "image_url": "..."
        },
        "start_date": "2024-01-01T00:00:00",
        "end_date": "2024-03-31T23:59:59",
        "max_participants": 1000,
        "current_participants": 234
      }
    ]
  }
}
```

### ステーク作成

```bash
POST /api/v1/escrow/stake
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "campaign_id": "uuid",
  "amount_xrp": 100
}
```

レスポンス:
```json
{
  "status": "success",
  "data": {
    "escrow_id": "uuid",
    "transaction_hash": "...",
    "finish_after": 1234567890,
    "amount_xrp": 100,
    "lock_days": 30
  }
}
```

### 自分のステーク一覧

```bash
GET /api/v1/escrow/my-stakes
Authorization: Bearer <access_token>
```

レスポンス:
```json
{
  "status": "success",
  "data": {
    "stakes": [
      {
        "id": "uuid",
        "campaign_name": "XRPステーキングキャンペーン",
        "amount_xrp": 100,
        "lock_days": 30,
        "finish_after": "2024-02-01T00:00:00",
        "status": "active",
        "nft_reward": "Airzone Staker NFT",
        "transaction_hash": "..."
      }
    ]
  }
}
```

## フロントエンド実装

### キャンペーン表示

```tsx
import { useState, useEffect } from 'react';

export default function EscrowCampaigns() {
  const [campaigns, setCampaigns] = useState([]);

  useEffect(() => {
    fetch('/api/v1/escrow/campaigns')
      .then(res => res.json())
      .then(data => setCampaigns(data.data.campaigns));
  }, []);

  return (
    <div>
      {campaigns.map(campaign => (
        <div key={campaign.id} className="campaign-card">
          <h3>{campaign.name}</h3>
          <p>{campaign.description}</p>
          <p>最小: {campaign.min_amount_xrp} XRP</p>
          <p>期間: {campaign.lock_days}日</p>
          <button onClick={() => joinCampaign(campaign.id)}>
            参加する
          </button>
        </div>
      ))}
    </div>
  );
}
```

### ステーク作成

```tsx
const joinCampaign = async (campaignId: string, amount: number) => {
  const response = await fetch('/api/v1/escrow/stake', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
    },
    body: JSON.stringify({
      campaign_id: campaignId,
      amount_xrp: amount,
    }),
  });

  if (response.ok) {
    alert('ステーキング完了！期間終了後にNFTを受け取れます。');
  }
};
```

## セキュリティ

### Escrowの安全性

1. **ブロックチェーン保証**: XRPLのEscrow機能で保護
2. **自動実行**: 期間終了後は誰でも完了可能
3. **取り消し不可**: 一度作成したら取り消せない

### 不正防止

1. **最小金額チェック**: キャンペーン条件を満たすか確認
2. **期間チェック**: キャンペーン期間内のみ参加可能
3. **参加上限**: 最大参加者数を設定可能

## 管理画面

### キャンペーン管理

管理画面で以下を管理:
- キャンペーン一覧
- 参加者数
- ロック中のXRP総額
- NFT発行状況

### ステーク一覧

各ユーザーのステーク状況:
- ロック中のXRP
- 解放予定日時
- NFT発行ステータス

## 注意事項

### ユーザー向け

1. **ロック期間**: 指定期間はXRPを引き出せません
2. **最小金額**: キャンペーンごとに最小金額が設定されています
3. **NFT発行**: 期間終了後、自動的にNFTが発行されます
4. **XRP返却**: 期間終了後、XRPは自動的に返却されます

### 管理者向け

1. **定期チェック**: 完了可能なEscrowを定期的にチェック
2. **NFT在庫**: NFT発行に必要なスポンサーウォレット残高を確保
3. **キャンペーン期間**: 適切な期間設定

## トラブルシューティング

### Q: Escrowが作成できない

**原因:**
- ウォレット残高不足
- 最小金額未満
- キャンペーン期間外

**解決策:**
1. ウォレット残高を確認
2. キャンペーン条件を確認
3. エラーメッセージを確認

### Q: 期間終了後もXRPが返ってこない

**原因:**
- Escrow完了トランザクションが未実行
- システムの定期チェックが停止

**解決策:**
1. 管理者に問い合わせ
2. 手動でEscrow完了を実行

## 今後の拡張

- [ ] 複数キャンペーン同時参加
- [ ] ロック量に応じたNFTレアリティ
- [ ] 早期解約機能（ペナルティあり）
- [ ] ステーキング報酬（XRP利息）
- [ ] NFT以外の報酬（コイン、限定商品など）

## 関連ドキュメント

- [XRPL統合ガイド](xrpl-integration.md)
- [NFTシステム](xrpl-integration.md#nft発行)
- [管理パネルガイド](../admin/README.md)

## 参考リンク

- [XRPL Escrow](https://xrpl.org/escrow.html)
- [Escrow Tutorials](https://xrpl.org/use-escrows.html)
