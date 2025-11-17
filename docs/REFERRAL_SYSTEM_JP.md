# 紹介リンクシステム

## 概要

Airzoneの紹介リンクシステムは、ユーザーが友達を招待してコインを獲得できる機能です。紹介された友達は限定商品にアクセスできるようになります。

## 主な機能

### 1. 紹介者の特典
- **コイン獲得**: 友達が登録すると100コインを獲得
- **紹介履歴**: 誰を紹介したか確認可能
- **統計情報**: 紹介数、獲得コイン数を表示

### 2. 被紹介者の特典
- **限定商品アクセス**: 紹介経由で登録すると限定商品が購入可能
- **特別な体験**: 紹介者とのつながり

### 3. SNSシェア
- **Twitter**: ワンクリックでツイート
- **LINE**: LINEで友達に送信
- **Facebook**: Facebookでシェア

## 使い方

### 紹介者側

#### 1. 紹介コードを取得

```
ダッシュボード
  ↓
「友達を招待」カード
  ↓
紹介コードが表示される
```

#### 2. 紹介リンクをシェア

**方法1: リンクをコピー**
```
1. 「コピー」ボタンをクリック
2. SNSやメッセージアプリに貼り付け
3. 友達に送信
```

**方法2: SNSボタンを使用**
```
1. Twitter/LINE/Facebookボタンをクリック
2. 自動的にシェア画面が開く
3. そのまま投稿
```

#### 3. コインを獲得

```
友達が紹介リンクから登録
  ↓
自動的に100コイン獲得
  ↓
コイン残高に反映
```

### 被紹介者側

#### 1. 紹介リンクからアクセス

```
https://airz.one?ref=ABC12345
```

#### 2. 登録

```
Google OAuth でログイン
  ↓
自動的に紹介関係が記録される
  ↓
限定商品が購入可能に
```

#### 3. 紹介コードを手動入力（オプション）

```
ダッシュボード
  ↓
「紹介コードを入力」
  ↓
コードを入力して適用
```

## API エンドポイント

### 紹介コード取得

```bash
GET /api/v1/referral/code
Authorization: Bearer <access_token>
```

レスポンス:
```json
{
  "status": "success",
  "data": {
    "referral_code": "ABC12345",
    "referral_link": "https://airz.one?ref=ABC12345",
    "share_links": {
      "twitter": "https://twitter.com/intent/tweet?...",
      "facebook": "https://www.facebook.com/sharer/...",
      "line": "https://line.me/R/msg/text/?..."
    }
  }
}
```

### 紹介コード適用

```bash
POST /api/v1/referral/apply
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "referral_code": "ABC12345"
}
```

レスポンス:
```json
{
  "status": "success",
  "data": {
    "referrer_name": "John Doe",
    "message": "紹介コードが適用されました！限定商品が購入可能になりました。"
  }
}
```

### 紹介統計取得

```bash
GET /api/v1/referral/stats
Authorization: Bearer <access_token>
```

レスポンス:
```json
{
  "status": "success",
  "data": {
    "total_referrals": 10,
    "completed_referrals": 8,
    "pending_referrals": 2,
    "total_coins_earned": 800,
    "current_coins": 500
  }
}
```

### コイン残高取得

```bash
GET /api/v1/referral/coins
Authorization: Bearer <access_token>
```

レスポンス:
```json
{
  "status": "success",
  "data": {
    "coins": 500
  }
}
```

## データベーススキーマ

### usersテーブル拡張

```sql
ALTER TABLE users 
ADD COLUMN referral_code VARCHAR(20) UNIQUE,
ADD COLUMN coins INT DEFAULT 0,
ADD COLUMN referred_by CHAR(36) NULL;
```

### referralsテーブル

```sql
CREATE TABLE referrals (
    id CHAR(36) PRIMARY KEY,
    referrer_id CHAR(36) NOT NULL,
    referred_id CHAR(36) NOT NULL,
    status ENUM('pending', 'completed', 'cancelled'),
    coins_awarded INT DEFAULT 0,
    created_at TIMESTAMP,
    completed_at TIMESTAMP NULL
);
```

### coin_transactionsテーブル

```sql
CREATE TABLE coin_transactions (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    amount INT NOT NULL,
    transaction_type ENUM('referral_bonus', 'purchase', 'admin_adjustment'),
    description TEXT,
    balance_after INT NOT NULL,
    related_id CHAR(36) NULL,
    created_at TIMESTAMP
);
```

### productsテーブル拡張

```sql
ALTER TABLE products
ADD COLUMN is_referral_only BOOLEAN DEFAULT FALSE;
```

## 設定

### コイン報酬

`backend/services/referral_service.py`:
```python
REFERRAL_BONUS_COINS = 100  # 紹介成功時のコイン
```

### 紹介コード長

```python
REFERRAL_CODE_LENGTH = 8  # 8文字の英数字
```

## フロントエンド実装

### 紹介カードコンポーネント

```tsx
import ReferralCard from '@/components/referral/ReferralCard';

export default function Dashboard() {
  return (
    <div>
      <h1>ダッシュボード</h1>
      <ReferralCard />
    </div>
  );
}
```

### 紹介コード入力

```tsx
const applyReferralCode = async (code: string) => {
  const response = await fetch('/api/v1/referral/apply', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
    },
    body: JSON.stringify({ referral_code: code }),
  });
  
  if (response.ok) {
    alert('紹介コードが適用されました！');
  }
};
```

## 管理パネル

### 紹介統計

管理パネルで以下の情報を確認可能:
- 総紹介数
- アクティブな紹介者
- 付与されたコイン総数
- 紹介経由の登録率

### 紹介履歴

各ユーザーの紹介履歴を確認:
- 紹介した人数
- 獲得コイン
- 紹介ステータス

## セキュリティ

### 不正防止

1. **自己紹介防止**: 自分の紹介コードは使用不可
2. **重複防止**: 1ユーザー1回のみ紹介コード適用可能
3. **コード検証**: 存在する紹介コードのみ有効

### レート制限

- 紹介コード生成: 1ユーザー1回のみ
- 紹介コード適用: 1ユーザー1回のみ

## トラブルシューティング

### Q: 紹介コードが適用できない

**原因:**
- 既に別の紹介コードを適用済み
- 無効な紹介コード
- 自分の紹介コード

**解決策:**
1. 紹介コードを確認
2. 別のコードを試す
3. サポートに問い合わせ

### Q: コインが付与されない

**原因:**
- 紹介がまだ完了していない（pending状態）
- システムエラー

**解決策:**
1. 紹介履歴を確認
2. ステータスがcompletedか確認
3. 管理者に問い合わせ

### Q: 限定商品が表示されない

**原因:**
- 紹介コードが未適用
- 商品が紹介限定に設定されていない

**解決策:**
1. 紹介コードを適用
2. ページをリロード
3. 商品設定を確認

## 今後の拡張

- [ ] コインで商品購入
- [ ] コイン交換機能
- [ ] 紹介ランキング
- [ ] 特別ボーナスキャンペーン
- [ ] 紹介レベル（2段階紹介）

## 関連ドキュメント

- [API リファレンス](../backend/API_REFERENCE.md)
- [管理パネルガイド](../admin/README.md)
- [セットアップガイド](SETUP_GUIDE_JP.md)
