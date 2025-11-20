# データベースセットアップ（簡単版）

rootユーザー不要で、SQLだけでセットアップできます。

## クイックスタート

### 1. パスワードを設定

`backend/setup_database.sql`を開いて、パスワードを変更：

```sql
CREATE USER IF NOT EXISTS 'airzone_user'@'localhost' IDENTIFIED BY 'your_secure_password';
```

### 2. SQLを実行

```bash
mysql -u your_admin_user -p < backend/setup_database.sql
```

### 3. .envファイルを作成

```bash
cp backend/.env.example backend/.env
```

`backend/.env`を編集：

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=airzone
DB_USER=airzone_user
DB_PASSWORD=your_secure_password
```

**重要**: `DB_ADMIN_USER`と`DB_ADMIN_PASSWORD`は不要です！

### 4. マイグレーションを実行

```bash
cd backend
pip install -r requirements.txt
python setup_db_simple.py
```

完了！

## 各ステップの詳細

### SQLスクリプトの内容

`backend/setup_database.sql`は以下を実行します：

- データベース`airzone`を作成
- ユーザー`airzone_user`を作成
- 必要な権限を付与

### マイグレーションスクリプト

`backend/setup_db_simple.py`は以下を実行します：

- データベース接続を確認
- Alembicマイグレーションでテーブルを作成
- 初期データを投入（オプション）

## トラブルシューティング

### MySQLにログインできない

管理者権限を持つユーザーでログインしてください：

```bash
mysql -u your_admin_user -p
```

### データベースが既に存在する

問題ありません。SQLスクリプトは`IF NOT EXISTS`を使用しているので、既存のデータベースには影響しません。

### ユーザーが既に存在する

問題ありません。SQLスクリプトは`IF NOT EXISTS`を使用しています。

### マイグレーションエラー

手動で実行してみてください：

```bash
cd backend
alembic upgrade head
```

## 確認

セットアップが成功したか確認：

```bash
python backend/verify_database.py
```

## 次のステップ

1. バックエンドを起動: `cd backend && python app.py`
2. フロントエンドを起動: `cd frontend && npm run dev`
3. http://localhost:3000 にアクセス

## 詳細なドキュメント

より詳しい情報は以下を参照：

- `backend/DATABASE_SETUP_NO_ROOT.md` - Root不要のセットアップ方法
- `backend/DATABASE_SETUP.md` - 完全なセットアップガイド
- `backend/DATABASE_QUICK_START.md` - クイックスタートガイド
