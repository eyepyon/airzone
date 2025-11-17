# Airzone セットアップガイド

## 必要な環境

- **Python 3.11+** - [ダウンロード](https://www.python.org/downloads/)
- **Node.js 18+** - [ダウンロード](https://nodejs.org/)
- **MySQL 8.0+** - [ダウンロード](https://dev.mysql.com/downloads/)

## ステップバイステップセットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd airzone
```

### 2. データベースのセットアップ

```bash
# MySQLにログイン
mysql -u root -p

# データベースとユーザーを作成
CREATE DATABASE airzone CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'airzone_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON airzone.* TO 'airzone_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# テーブルを作成
mysql -u airzone_user -p airzone < backend/setup_database.sql
```

### 3. バックエンドのセットアップ

```bash
cd backend

# 仮想環境を作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt

# 環境変数を設定
cp .env.example .env
```

`.env`ファイルを編集:

```env
# データベース
DB_HOST=localhost
DB_PORT=3306
DB_NAME=airzone
DB_USER=airzone_user
DB_PASSWORD=your_password

# JWT
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Stripe
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
STRIPE_WEBHOOK_SECRET=your-webhook-secret

# XRPL Blockchain
XRPL_NETWORK=testnet
XRPL_SPONSOR_SEED=your-sponsor-seed

# セキュリティ
ENCRYPTION_KEY=your-encryption-key

# CORS
CORS_ORIGINS=http://localhost:3000
```

### 4. XRPLスポンサーウォレットの生成

```bash
python ../scripts/generate_sponsor_wallet.py
```

1. ネットワークを選択（開発環境では`1. Testnet`を推奨）
2. 生成されたアドレスとシードをメモ
3. `.env`ファイルに`XRPL_SPONSOR_SEED`を設定

### 5. テストネットから資金を取得

1. https://xrpl.org/xrp-testnet-faucet.html にアクセス
2. 生成したウォレットアドレスを入力
3. テストXRPを取得

### 6. XRPL接続を確認

```bash
python verify_xrpl_client.py
```

### 7. バックエンドサーバーを起動

```bash
python app.py
```

サーバーは http://localhost:5000 で起動します。

### 8. フロントエンドのセットアップ

新しいターミナルを開いて:

```bash
cd frontend

# 依存関係をインストール
npm install

# 環境変数を設定
cp .env.local.example .env.local
```

`.env.local`ファイルを編集:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000/api/v1
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
```

### 9. フロントエンドサーバーを起動

```bash
npm run dev
```

フロントエンドは http://localhost:3000 で起動します。

### 10. 管理パネルのセットアップ

新しいターミナルを開いて:

```bash
cd admin

# Composerで依存関係をインストール
composer install

# 環境変数を設定
cp .env.example .env
```

`.env`ファイルを編集:

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=airzone
DB_USERNAME=airzone_user
DB_PASSWORD=your_password
```

### 11. 管理パネルのマイグレーション

```bash
php artisan migrate
```

### 12. 管理パネルにアクセス

http://localhost/admin （Apacheを使用している場合）

## 動作確認

### バックエンドAPI

```bash
curl http://localhost:5000/api/v1/health
```

### フロントエンド

ブラウザで http://localhost:3000 を開く

### 管理パネル

ブラウザで http://localhost/admin を開く

## トラブルシューティング

### データベース接続エラー

```bash
# MySQLが起動しているか確認
sudo systemctl status mysql  # Linux
brew services list  # macOS

# 接続をテスト
mysql -u airzone_user -p airzone
```

### XRPLスポンサーウォレットの残高不足

```bash
python backend/verify_xrpl_client.py
```

残高が不足している場合は、テストネットフォーセットから追加で取得してください。

### ポートが使用中

```bash
# ポート5000を使用しているプロセスを確認
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# プロセスを終了
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

## 次のステップ

1. **Google OAuth設定**: [Google Cloud Console](https://console.cloud.google.com/)でOAuthクライアントを作成
2. **Stripe設定**: [Stripe Dashboard](https://dashboard.stripe.com/)でAPIキーを取得
3. **本番環境デプロイ**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)を参照

## 参考資料

- [XRPL統合ガイド](docs/xrpl-integration.md)
- [効果測定ダッシュボード](docs/analytics-dashboard.md)
- [管理パネルインストール](admin/INSTALL.md)
- [API リファレンス](backend/API_REFERENCE.md)
