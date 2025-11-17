# ユーザー重要度スコアシステム

## 概要

ユーザーの活動を総合的に評価し、重要度をスコア化するシステムです。購入数、紹介数、ログイン数などから自動的にスコアを計算し、5段階のレベルで分類します。

## 重要度レベル

| レベル | バッジ | スコア範囲 | 説明 |
|--------|--------|-----------|------|
| Bronze | 🥉 | 0-499 | 一般ユーザー |
| Silver | 🥈 | 500-1,499 | アクティブユーザー |
| Gold | 🥇 | 1,500-2,999 | 優良ユーザー |
| Platinum | 💎 | 3,000-4,999 | VIPユーザー |
| Diamond | 👑 | 5,000+ | 最重要ユーザー |

## スコア配点

### 基本配点

| 項目 | 配点 | 説明 |
|------|------|------|
| 購入 | 100pt | 1回の購入につき |
| 紹介成功 | 50pt | 1件の紹介完了につき |
| NFT発行 | 30pt | 1回のNFT発行につき |
| リファラルクリック | 5pt | 紹介リンククリック1回につき |
| ログイン | 2pt | 1日のログインにつき（過去90日） |
| 購入金額 | 0.1pt | 購入金額1円につき |

### 計算例

**ユーザーA:**
- 購入: 5回 → 500pt
- 紹介成功: 3件 → 150pt
- NFT発行: 2回 → 60pt
- リファラルクリック: 20回 → 100pt
- ログイン: 30日 → 60pt
- 購入金額: 50,000円 → 5,000pt

**合計: 5,870pt → Diamond レベル 👑**

## データベーススキーマ

### usersテーブル拡張

```sql
ALTER TABLE users 
ADD COLUMN importance_score INT DEFAULT 0,
ADD COLUMN importance_level ENUM('bronze', 'silver', 'gold', 'platinum', 'diamond') DEFAULT 'bronze',
ADD COLUMN last_score_updated TIMESTAMP NULL;
```

### referral_clicksテーブル

```sql
CREATE TABLE referral_clicks (
    id CHAR(36) PRIMARY KEY,
    referral_code VARCHAR(20) NOT NULL,
    referrer_id CHAR(36) NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    clicked_at TIMESTAMP,
    converted BOOLEAN DEFAULT FALSE,
    converted_user_id CHAR(36) NULL
);
```

### user_score_historyテーブル

```sql
CREATE TABLE user_score_history (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    score_before INT NOT NULL,
    score_after INT NOT NULL,
    score_change INT NOT NULL,
    reason VARCHAR(255) NOT NULL,
    details JSON,
    created_at TIMESTAMP
);
```

## スコア更新

### 自動更新

以下のイベント発生時に自動更新:
- 購入完了時
- 紹介完了時
- NFT発行完了時
- ログイン時

### 手動更新

管理画面から手動でスコアを再計算可能:
```
管理画面 → 重要ユーザー → ユーザー詳細 → スコア更新
```

### バッチ更新

全ユーザーのスコアを一括更新:
```bash
# バックエンドAPIを呼び出し
curl -X POST http://localhost:5000/api/v1/admin/users/update-all-scores \
  -H "Authorization: Bearer <admin_token>"
```

## 管理画面

### 重要ユーザー一覧

`/admin/users/importance`

表示内容:
- ランキング順位
- ユーザー情報
- 重要度レベル（バッジ）
- スコア
- 購入数
- 紹介数
- ログイン数

### 紹介一覧での表示

紹介一覧にも重要度バッジを表示:
- 紹介コードの横にバッジ表示
- リファラルクリック数も表示

## リファラルクリック追跡

### フロントエンド実装

```typescript
// 紹介リンクからアクセス時
const urlParams = new URLSearchParams(window.location.search);
const refCode = urlParams.get('ref');

if (refCode) {
  // クリックを追跡
  await fetch('/api/v1/referral/track-click', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      referral_code: refCode,
    }),
  });
  
  // ローカルストレージに保存（登録時に使用）
  localStorage.setItem('referral_code', refCode);
}
```

### バックエンドAPI

```python
@referral_blueprint.route('/track-click', methods=['POST'])
def track_click():
    data = request.get_json()
    referral_code = data.get('referral_code')
    
    importance_service = UserImportanceService(g.db)
    importance_service.track_referral_click(
        referral_code=referral_code,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    
    return jsonify({'status': 'success'})
```

## 活用方法

### マーケティング

1. **VIP特典**: Platinum以上のユーザーに特別割引
2. **限定商品**: Diamond限定の商品を用意
3. **優先サポート**: 高レベルユーザーを優先対応

### 分析

1. **ユーザーセグメント**: レベル別の行動分析
2. **リテンション**: レベル別の継続率
3. **LTV予測**: スコアとLTVの相関分析

### エンゲージメント

1. **レベルアップ通知**: レベルが上がったら通知
2. **目標設定**: 次のレベルまでの必要スコアを表示
3. **ランキング**: トップユーザーを公開

## API エンドポイント

### スコア計算

```bash
POST /api/v1/admin/users/{user_id}/calculate-score
Authorization: Bearer <admin_token>
```

### スコア更新

```bash
POST /api/v1/admin/users/{user_id}/update-score
Authorization: Bearer <admin_token>
```

### トップユーザー取得

```bash
GET /api/v1/admin/users/top?limit=100
Authorization: Bearer <admin_token>
```

## 設定のカスタマイズ

`backend/services/user_importance_service.py`:

```python
# スコア配点を変更
SCORE_WEIGHTS = {
    'purchase': 100,
    'referral_completed': 50,
    'referral_click': 5,
    'login': 2,
    'nft_mint': 30,
    'order_amount': 0.1,
}

# レベル閾値を変更
IMPORTANCE_LEVELS = {
    'bronze': 0,
    'silver': 500,
    'gold': 1500,
    'platinum': 3000,
    'diamond': 5000,
}
```

## トラブルシューティング

### Q: スコアが更新されない

**解決策:**
1. マイグレーションを実行
2. 手動でスコア更新を実行
3. ログを確認

### Q: クリック数がカウントされない

**解決策:**
1. フロントエンドの実装を確認
2. APIエンドポイントが正しいか確認
3. ネットワークタブでリクエストを確認

## 今後の拡張

- [ ] スコア減衰（長期間ログインなしでスコア減少）
- [ ] ボーナスイベント（期間限定で配点2倍）
- [ ] バッジシステム（特定の条件達成で獲得）
- [ ] レベル特典の自動適用
- [ ] スコア予測（将来のスコアを予測）

## 関連ドキュメント

- [紹介システム](REFERRAL_SYSTEM_JP.md)
- [効果測定ダッシュボード](analytics-dashboard.md)
- [管理パネルガイド](../admin/README.md)
