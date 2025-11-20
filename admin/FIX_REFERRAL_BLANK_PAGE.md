# 紹介ページ真っ白問題の修正

## 問題

https://airz.one/referral にアクセスすると真っ白なページが表示される。

## 原因

1. バックエンドAPIがエラーを返している
2. `users`テーブルに`referral_code`、`referred_by`、`coins`カラムが存在しない
3. エラーハンドリングのコードでレスポンスを2回読み込もうとしていた

## 修正内容

### 1. フロントエンドの修正

- エラーハンドリングを簡素化
- エラーが発生してもデフォルト値を設定してページを表示
- デバッグログを追加

### 2. データベースマイグレーション（必須）

以下のSQLを実行してください：

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

### 3. バックエンドの再起動

```bash
cd backend
python app.py
```

## 動作確認

### 1. データベースの確認

```sql
-- usersテーブルの構造を確認
DESCRIBE users;

-- 以下のカラムが存在することを確認
-- - referral_code VARCHAR(20)
-- - referred_by CHAR(36)
-- - coins INT
```

### 2. APIの確認

```bash
# ログイン後、トークンを取得
TOKEN="YOUR_ACCESS_TOKEN"

# 紹介統計を取得
curl -X GET http://localhost:5000/api/v1/referral/stats \
  -H "Authorization: Bearer $TOKEN"

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

### 3. フロントエンドの確認

1. https://airz.one/referral にアクセス
2. ページが表示されることを確認
3. F12キーを押して開発者ツールを開く
4. Consoleタブで以下を確認：
   - `Stats API response:` のログ
   - エラーメッセージがないこと

## エラーが表示される場合

エラーメッセージが表示されても、ページは表示されるようになりました：

- 赤いバナーにエラーメッセージが表示されます
- 紹介カードと使い方セクションは表示されます
- 統計は0として表示されます

これにより、データベースマイグレーションを実行する前でもページが使用可能です。

## 完了

マイグレーション実行後：
1. ページが正常に表示される
2. 紹介コードが自動生成される
3. 統計情報が正しく表示される
4. 紹介履歴が表示される

## 注意事項

**必ずデータベースマイグレーションを実行してください。**

マイグレーションを実行しないと：
- 紹介コードが生成できない
- コイン残高が表示されない
- 紹介機能が正常に動作しない

詳細は `admin/FIX_REFERRAL_JSON_ERROR.md` を参照してください。
