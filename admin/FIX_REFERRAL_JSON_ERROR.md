# 紹介機能JSONパースエラー修正

## 問題

https://airz.one/referral にアクセスすると以下のエラーが発生：
```
JSON.parse: unexpected character at line 1 column 1 of the JSON data
```

## 原因

1. `users`テーブルに`referral_code`、`referred_by`、`coins`カラムが存在しない
2. バックエンドAPIがエラーを返しているが、HTMLエラーページとして返されている

## 解決方法

### 1. データベースマイグレーション実行

以下のSQLを実行して必要なカラムを追加します：

```sql
USE airzone;

-- referral_codeカラムを追加
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS referral_code VARCHAR(20) UNIQUE;

-- referred_byカラムを追加
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS referred_by CHAR(36);

-- coinsカラムを追加
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS coins INT DEFAULT 0;

-- インデックスを追加
CREATE INDEX IF NOT EXISTS idx_users_referral_code ON users(referral_code);
CREATE INDEX IF NOT EXISTS idx_users_referred_by ON users(referred_by);

-- 既存データのデフォルト値を設定
UPDATE users SET coins = 0 WHERE coins IS NULL;
```

または、マイグレーションファイルを実行：

```bash
mysql -u airzone_user -p airzone < backend/database/migrations/add_user_referral_coins.sql
```

### 2. テーブル構造の確認

```sql
-- usersテーブルの構造を確認
DESCRIBE users;

-- 以下のカラムが存在することを確認
-- - referral_code VARCHAR(20)
-- - referred_by CHAR(36)
-- - coins INT
```

### 3. フロントエンドの改善

フロントエンドのエラーハンドリングを改善しました：
- JSONレスポンスでない場合の適切なエラーメッセージ
- コンソールに詳細なエラー情報を出力

### 4. バックエンドの再起動

マイグレーション実行後、バックエンドを再起動：

```bash
cd backend
python app.py
```

または本番環境：
```bash
systemctl restart airzone-backend
```

## 動作確認

### 1. APIエンドポイントのテスト

```bash
# 紹介統計を取得
curl -X GET http://localhost:5000/api/v1/referral/stats \
  -H "Authorization: Bearer YOUR_TOKEN"

# 期待されるレスポンス
{
  "status": "success",
  "data": {
    "total_referrals": 0,
    "completed_referrals": 0,
    "pending_referrals": 0,
    "total_coins_earned": 0,
    "current_coins": 0
  }
}
```

### 2. フロントエンドでの確認

1. https://airz.one/referral にアクセス
2. ログイン済みの場合、紹介ページが正常に表示されることを確認
3. 紹介コードが表示されることを確認
4. 統計情報（総紹介数、完了数、コイン残高など）が表示されることを確認

## トラブルシューティング

### エラー: "Column 'coins' not found"

→ マイグレーションが実行されていません。上記のSQLを実行してください。

### エラー: "Duplicate column name 'coins'"

→ カラムは既に存在しています。`IF NOT EXISTS`を使用しているため、通常このエラーは発生しません。

### JSONパースエラーが続く場合

1. **ブラウザのコンソールを確認**
   - F12キーを押して開発者ツールを開く
   - Consoleタブでエラーメッセージを確認
   - Networkタブで`/api/v1/referral/stats`のレスポンスを確認

2. **バックエンドのログを確認**
   ```bash
   # ログファイルを確認
   tail -f backend/logs/app.log
   
   # またはコンソール出力を確認
   ```

3. **データベース接続を確認**
   ```bash
   mysql -u airzone_user -p airzone -e "SELECT COUNT(*) FROM users"
   ```

### レスポンスがHTMLの場合

バックエンドでエラーが発生しています：
1. バックエンドのログを確認
2. データベース接続を確認
3. 必要なテーブルとカラムが存在するか確認

## 紹介機能の使い方

マイグレーション実行後、以下の機能が利用可能になります：

### 紹介コードの取得

1. 紹介ページにアクセス
2. 自動的に紹介コードが生成されます
3. 紹介リンクをコピーしてシェア

### 紹介コードの適用

新規ユーザーが登録時に紹介コードを入力すると：
- 紹介者に100コイン付与
- 被紹介者は限定商品が購入可能に

### コインの確認

- 紹介ページで現在のコイン残高を確認
- 紹介履歴とコイン獲得履歴を表示

## 完了

マイグレーション実行後、紹介機能が正常に動作するようになります。
