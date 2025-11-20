# データベースセットアップ（Root不要）

rootユーザーを使わずにデータベースをセットアップする方法です。

## 方法1: SQLファイルを使用（推奨）

### 1. パスワードを設定

`backend/setup_database.sql`を開いて、`your_secure_password`を実際のパスワードに変更してください：

```sql
CREATE USER IF NOT EXISTS 'airzone_user'@'localhost' IDENTIFIED BY 'your_secure_password';
```

### 2. SQLスクリプトを実行

データベース作成権限を持つユーザーで実行：

```bash
mysql -u your_admin_user -p < backend/setup_database.sql
```

または、MySQLクライアント内で：

```bash
mysql -u your_admin_user -p
```

```sql
SOURCE backend/setup_database.sql;
```

### 3. .envファイルを設定

`backend/.env`を作成・編集：

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=airzone
DB_USER=airzone_user
DB_PASSWORD=your_secure_password

# Root credentials are NOT needed!
# DB_ROOT_USER=root
# DB_ROOT_PASSWORD=
```

### 4. マイグレーションを実行

```bash
cd backend
alembic upgrade head
```

### 5. 初期データを投入（オプション）

```bash
python ../scripts/seed_data.py
```

## 方法2: 手動でMySQLコマンドを実行

MySQLにログイン：

```bash
mysql -u your_admin_user -p
```

以下のコマンドを実行：

```sql
-- データベース作成
CREATE DATABASE IF NOT EXISTS airzone CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ユーザー作成
CREATE USER IF NOT EXISTS 'airzone_user'@'localhost' IDENTIFIED BY 'your_password';
CREATE USER IF NOT EXISTS 'airzone_user'@'%' IDENTIFIED BY 'your_password';

-- 権限付与
GRANT ALL PRIVILEGES ON airzone.* TO 'airzone_user'@'localhost';
GRANT ALL PRIVILEGES ON airzone.* TO 'airzone_user'@'%';
FLUSH PRIVILEGES;

-- 確認
SHOW DATABASES;
SELECT User, Host FROM mysql.user WHERE User = 'airzone_user';
```

その後、方法1の手順3〜5を実行してください。

## 方法3: 既存のデータベースを使用

既にデータベースとユーザーが作成されている場合：

### 1. .envファイルのみ設定

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=airzone
DB_USER=airzone_user
DB_PASSWORD=your_existing_password
```

### 2. マイグレーションを実行

```bash
cd backend
alembic upgrade head
```

### 3. 初期データを投入（オプション）

```bash
python ../scripts/seed_data.py
```

## トラブルシューティング

### エラー: Access denied for user

ユーザーに適切な権限があるか確認：

```sql
SHOW GRANTS FOR 'airzone_user'@'localhost';
```

必要な権限：
- SELECT, INSERT, UPDATE, DELETE
- CREATE, ALTER, DROP (マイグレーション用)
- INDEX, REFERENCES

### エラー: Unknown database 'airzone'

データベースが作成されているか確認：

```sql
SHOW DATABASES LIKE 'airzone';
```

### マイグレーションエラー

Alembicの状態を確認：

```bash
cd backend
alembic current
alembic history
```

## 確認

セットアップが正しく完了したか確認：

```bash
python backend/verify_database.py
```

成功すると以下が表示されます：
```
✓ Database connection successful
✓ All tables exist
✓ Migrations have been applied
```

## 次のステップ

1. バックエンドを起動: `cd backend && python app.py`
2. フロントエンドを起動: `cd frontend && npm run dev`
3. ブラウザで http://localhost:3000 にアクセス
