# ステーキングページ表示修正

## 問題

https://airz.one/staking でエスクローキャンペーンがDBに登録されているのに表示されない。

## 原因

バックエンドAPIのレスポンス構造とフロントエンドの期待する構造が一致していませんでした。

### 修正前のAPIレスポンス

```json
{
  "status": "success",
  "data": {
    "campaigns": [...]
  }
}
```

### 修正後のAPIレスポンス

```json
{
  "status": "success",
  "campaigns": [
    {
      "id": "uuid",
      "name": "キャンペーン名",
      "description": "説明",
      "min_amount_drops": 100000000,
      "lock_days": 30,
      "nft_reward_name": "NFT名",
      "nft_reward_description": "NFT説明",
      "nft_reward_image_url": "https://...",
      "start_date": "2024-01-01T00:00:00",
      "end_date": "2024-12-31T23:59:59",
      "max_participants": 1000,
      "current_participants": 0,
      "status": "active"
    }
  ]
}
```

## 修正内容

### 1. バックエンドAPI修正

**ファイル**: `backend/routes/escrow.py`

- `/api/v1/escrow/campaigns` エンドポイントのレスポンス構造を変更
- `data.campaigns` → `campaigns` に変更
- `min_amount_xrp` → `min_amount_drops` に変更（フロントエンドで変換）
- `nft_reward` オブジェクト → フラットな構造に変更
- `status` フィールドを追加

**ファイル**: `backend/services/escrow_campaign_service.py`

- `get_user_escrows()` メソッドのレスポンスに以下を追加：
  - `campaign_id`
  - `amount_drops`（`amount_xrp`から変更）
  - `escrow_sequence`
  - `created_at`

### 2. マイステークAPIのレスポンス修正

**修正前**:
```json
{
  "status": "success",
  "data": {
    "stakes": [...]
  }
}
```

**修正後**:
```json
{
  "status": "success",
  "stakes": [
    {
      "id": "uuid",
      "campaign_id": "uuid",
      "campaign_name": "キャンペーン名",
      "amount_drops": 100000000,
      "lock_days": 30,
      "finish_after": "2024-02-01T00:00:00",
      "status": "active",
      "escrow_sequence": 12345,
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

## 適用手順

### 1. バックエンドの再起動

```bash
# バックエンドディレクトリに移動
cd backend

# Flaskアプリケーションを再起動
# 開発環境の場合
python app.py

# または本番環境の場合
# systemctl restart airzone-backend
# または
# supervisorctl restart airzone-backend
```

### 2. 動作確認

#### APIエンドポイントのテスト

```bash
# キャンペーン一覧を取得
curl -X GET http://localhost:5000/api/v1/escrow/campaigns \
  -H "Authorization: Bearer YOUR_TOKEN"

# マイステーク一覧を取得
curl -X GET http://localhost:5000/api/v1/escrow/my-stakes \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### フロントエンドでの確認

1. https://airz.one/staking にアクセス
2. ログイン済みの場合、キャンペーン一覧が表示されることを確認
3. 「キャンペーン一覧」タブにキャンペーンが表示されることを確認
4. 「マイステーク」タブで自分のステーク履歴が表示されることを確認

## データベース確認

キャンペーンが登録されているか確認：

```sql
-- キャンペーン一覧を確認
SELECT id, name, is_active, start_date, end_date, current_participants, max_participants 
FROM escrow_campaigns;

-- アクティブなキャンペーンを確認
SELECT * FROM escrow_campaigns 
WHERE is_active = TRUE 
AND start_date <= NOW() 
AND end_date >= NOW();
```

## トラブルシューティング

### キャンペーンが表示されない場合

1. **データベースにキャンペーンが存在するか確認**
   ```sql
   SELECT COUNT(*) FROM escrow_campaigns WHERE is_active = TRUE;
   ```

2. **キャンペーンの期間を確認**
   - `start_date` が現在より前
   - `end_date` が現在より後
   - `is_active` が TRUE

3. **バックエンドのログを確認**
   ```bash
   # ログファイルを確認
   tail -f backend/logs/app.log
   
   # またはコンソール出力を確認
   ```

4. **ブラウザのコンソールを確認**
   - F12キーを押して開発者ツールを開く
   - Consoleタブでエラーメッセージを確認
   - Networkタブで `/api/v1/escrow/campaigns` のレスポンスを確認

### APIエラーが発生する場合

```bash
# バックエンドが起動しているか確認
curl http://localhost:5000/health

# データベース接続を確認
mysql -u airzone_user -p airzone -e "SELECT 1"
```

## 完了

バックエンドを再起動すると、ステーキングページにキャンペーンが正しく表示されるようになります。
