# エスクローキャンペーン表示問題のデバッグ

## 問題

https://airz.one/staking でキャンペーンがデータベースに存在するのに「現在開催中のキャンペーンはありません」と表示される。

## 原因の可能性

1. `is_active`が`FALSE`または`0`
2. `start_date`が未来の日付
3. `end_date`が過去の日付
4. データベースのデータ型の問題

## デバッグ手順

### 1. データベースのキャンペーンを確認

```sql
-- すべてのキャンペーンを確認
SELECT 
    id,
    name,
    is_active,
    start_date,
    end_date,
    NOW() as current_time,
    CASE 
        WHEN is_active = FALSE THEN 'is_active is FALSE'
        WHEN start_date > NOW() THEN 'start_date is in future'
        WHEN end_date < NOW() THEN 'end_date is in past'
        ELSE 'Should be visible'
    END as visibility_status
FROM escrow_campaigns
ORDER BY created_at DESC;
```

### 2. APIが返すキャンペーンを確認

```sql
-- APIが返すべきキャンペーン（バックエンドと同じ条件）
SELECT * FROM escrow_campaigns 
WHERE is_active = TRUE 
AND start_date <= NOW() 
AND end_date >= NOW()
ORDER BY created_at DESC;
```

### 3. データ型を確認

```sql
-- テーブル構造を確認
DESCRIBE escrow_campaigns;

-- is_activeのデータ型を確認（BOOLEAN, TINYINT, INTなど）
-- start_date, end_dateのデータ型を確認（TIMESTAMP, DATETIMEなど）
```

## 修正方法

### ケース1: is_activeが0の場合

```sql
-- すべてのキャンペーンを有効化
UPDATE escrow_campaigns SET is_active = 1;

-- または特定のキャンペーンを有効化
UPDATE escrow_campaigns SET is_active = 1 WHERE id = 'YOUR_CAMPAIGN_ID';
```

### ケース2: 日付が不適切な場合

```sql
-- 現在の日付を確認
SELECT NOW();

-- キャンペーンの日付を更新
UPDATE escrow_campaigns 
SET 
    start_date = NOW(),
    end_date = DATE_ADD(NOW(), INTERVAL 90 DAY)
WHERE id = 'YOUR_CAMPAIGN_ID';
```

### ケース3: データ型の問題

MySQLの`BOOLEAN`型は実際には`TINYINT(1)`として保存されます：
- `TRUE` = `1`
- `FALSE` = `0`

```sql
-- is_activeを明示的に1に設定
UPDATE escrow_campaigns SET is_active = 1;

-- 確認
SELECT id, name, is_active, is_active = 1 as is_truly_active 
FROM escrow_campaigns;
```

## バックエンドのデバッグ

### ログを追加

`backend/routes/escrow.py`の`get_campaigns`関数にログを追加：

```python
campaigns = g.db.execute(
    """
    SELECT * FROM escrow_campaigns 
    WHERE is_active = TRUE 
    AND start_date <= NOW() 
    AND end_date >= NOW()
    ORDER BY created_at DESC
    """
).fetchall()

logger.info(f"Found {len(campaigns)} active campaigns")
for c in campaigns:
    logger.info(f"Campaign: {c['name']}, active={c['is_active']}, start={c['start_date']}, end={c['end_date']}")
```

### APIレスポンスを直接確認

```bash
# ログイン後、トークンを取得
TOKEN="YOUR_ACCESS_TOKEN"

# キャンペーン一覧を取得
curl -X GET http://localhost:5000/api/v1/escrow/campaigns \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

## フロントエンドのデバッグ

ブラウザのコンソール（F12）で以下を確認：

1. **Network タブ**
   - `/api/v1/escrow/campaigns` のリクエストを確認
   - レスポンスの内容を確認
   - ステータスコードを確認（200 OKか）

2. **Console タブ**
   - `Campaigns API response:` のログを確認
   - `campaigns` 配列の長さを確認
   - エラーメッセージを確認

## 推奨される修正SQL

以下のSQLを実行して、キャンペーンを確実に表示されるようにします：

```sql
-- 1. すべてのキャンペーンの状態を確認
SELECT 
    id,
    name,
    is_active,
    start_date,
    end_date,
    NOW() as now
FROM escrow_campaigns;

-- 2. キャンペーンを有効化し、日付を適切に設定
UPDATE escrow_campaigns 
SET 
    is_active = 1,
    start_date = CASE 
        WHEN start_date > NOW() THEN NOW()
        ELSE start_date
    END,
    end_date = CASE 
        WHEN end_date < NOW() THEN DATE_ADD(NOW(), INTERVAL 90 DAY)
        ELSE end_date
    END;

-- 3. 確認
SELECT * FROM escrow_campaigns 
WHERE is_active = 1 
AND start_date <= NOW() 
AND end_date >= NOW();
```

## 完了確認

修正後、以下を確認：

1. **データベース**
   ```sql
   SELECT COUNT(*) FROM escrow_campaigns 
   WHERE is_active = TRUE 
   AND start_date <= NOW() 
   AND end_date >= NOW();
   ```
   → 1以上の値が返ること

2. **API**
   - `/api/v1/escrow/campaigns` が空でない配列を返すこと

3. **フロントエンド**
   - https://airz.one/staking でキャンペーンが表示されること

## トラブルシューティング

### それでもキャンペーンが表示されない場合

1. **バックエンドを再起動**
   ```bash
   cd backend
   python app.py
   ```

2. **ブラウザのキャッシュをクリア**
   - Ctrl + Shift + Delete
   - キャッシュをクリア

3. **フロントエンドを再ビルド**
   ```bash
   cd frontend
   npm run build
   ```

4. **データベース接続を確認**
   ```bash
   mysql -u airzone_user -p airzone -e "SELECT 1"
   ```
