# Airzone セットアップガイド（完全版）

## 目次

1. [システム要件](#システム要件)
2. [データベースセットアップ](#データベースセットアップ)
3. [バックエンドセットアップ](#バックエンドセットアップ)
4. [XRPLブロックチェーン設定](#xrplブロックチェーン設定)
5. [フロントエンドセットアップ](#フロントエンドセットアップ)
6. [管理パネルセットアップ](#管理パネルセットアップ)
7. [外部サービス設定](#外部サービス設定)
8. [動作確認](#動作確認)

## システム要件

### 必須ソフトウェア

- **Python 3.11以上**
- **Node.js 18以上**
- **MySQL 8.0以上**
- **PHP 8.1以上** (管理パネル用)
- **Composer** (管理パネル用)

### 推奨環境

- **OS**: Ubuntu 22.04 LTS / macOS / Windows 10+
- **メモリ**: 4GB以上
- **ストレージ**: 10GB以上の空き容量

## データベースセットアップ

### 1. MySQLのインストール

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

#### macOS (Homebrew)
```bash
brew install mysql
brew services start mysql
```

#### Windows
[MySQL公式サイト](https://dev.mysql.com/downloads/)からインストーラーをダウンロード

### 2. データベースとユーザーの作成

```bash
mysql -u root -p
```

```sql
CREATE DATABASE airzone CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'airzone_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON airzone.* TO 'airzone_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. テーブルの作成

```bash
mysql -u airzone_user -p airzone < backend/setup_database.sql
```

## バックエンドセットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd airzone
```

### 2. Python仮想環境の作成

```bash
cd backend
python -m venv venv

# アクティベート
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

```bash
cp .env.example .env
```

`.env`ファイルを編集：

```env
# Flask
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production

# Database
DB_HOST=localhost
DB_PORT=3306
DB_NAME=airzone
DB_USER=airzone_user
DB_PASSWORD=your_secure_password

# JWT
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000

# CORS
CORS_ORIGINS=http://localhost:3000

# Security
ENCRYPTION_KEY=your-32-byte-encryption-key
```

### 5. 暗号化キーの生成

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

生成されたキーを`.env`の`ENCRYPTION_KEY`に設定

## XRPLブロックチェーン設定

### 1. スポンサーウォレットの生成

```bash
python ../scripts/generate_sponsor_wallet.py
```

1. ネットワークを選択（開発環境では`1. Testnet`）
2. 生成されたアドレスとシードをメモ
3. `.env`に追加：

```env
XRPL_NETWORK=testnet
XRPL_SPONSOR_SEED=sXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### 2. テストネットから資金を取得

1. https://xrpl.org/xrp-testnet-faucet.html にアクセス
2. 生成したウォレットアドレスを入力
3. テストXRPを取得（通常1000 XRP）

### 3. XRPL接続の確認

```bash
python verify_xrpl_client.py
```

成功すると以下のような出力が表示されます：

```
✓ Configuration valid
✓ XRPL client initialized
✓ Sponsor wallet configured
✓ Wallet generation working
✅ All checks passed! XRPL client is ready for use.
```

## フロントエンドセットアップ

### 1. 依存関係のインストール

```bash
cd ../frontend
npm install
```

### 2. 環境変数の設定

```bash
cp .env.local.example .env.local
```

`.env.local`ファイルを編集：

```env
NEXT_PUBLIC_API_URL=http://localhost:5000/api/v1
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
```

### 3. 開発サーバーの起動

```bash
npm run dev
```

フロントエンドは http://localhost:3000 で起動します。

## 管理パネルセットアップ

### 1. Composerのインストール

#### Linux/macOS
```bash
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
```

#### Windows
[Composer公式サイト](https://getcomposer.org/)からインストーラーをダウンロード

### 2. 依存関係のインストール

```bash
cd ../admin
composer install
```

### 3. 環境変数の設定

```bash
cp .env.example .env
php artisan key:generate
```

`.env`ファイルを編集：

```env
APP_NAME="Airzone Admin"
APP_ENV=local
APP_DEBUG=true
APP_URL=http://localhost:8000

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=airzone
DB_USERNAME=airzone_user
DB_PASSWORD=your_secure_password
```

### 4. データベースマイグレーション

```bash
php artisan migrate
```

### 5. 管理者アカウントの作成

```bash
php artisan tinker
```

Tinkerで実行：

```php
$admin = new App\Models\Admin();
$admin->name = 'Admin';
$admin->email = 'admin@example.com';
$admin->password = bcrypt('your_admin_password');
$admin->save();
exit
```

### 6. 開発サーバーの起動

```bash
php artisan serve
```

管理パネルは http://localhost:8000 で起動します。

## 外部サービス設定

### Google OAuth

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. 新しいプロジェクトを作成
3. 「APIとサービス」→「認証情報」
4. 「OAuth 2.0 クライアント ID」を作成
5. 承認済みのリダイレクトURIを追加：
   - `http://localhost:3000`
   - `http://localhost:3000/auth/callback`
6. クライアントIDとシークレットを取得
7. `.env`に追加：

```env
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### Stripe

1. [Stripe Dashboard](https://dashboard.stripe.com/)にアクセス
2. 「開発者」→「APIキー」
3. テストモードのキーを取得
4. `.env`に追加：

```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
```

5. Webhookの設定：
   - 「開発者」→「Webhook」
   - エンドポイントURL: `http://localhost:5000/api/v1/payments/webhook`
   - イベント選択: `payment_intent.succeeded`, `payment_intent.payment_failed`
   - Webhook署名シークレットを取得
   - `.env`に追加：

```env
STRIPE_WEBHOOK_SECRET=whsec_...
```

## 動作確認

### 1. バックエンドAPI

```bash
cd backend
python app.py
```

別のターミナルで：

```bash
curl http://localhost:5000/api/v1/health
```

期待される出力：
```json
{"status": "ok"}
```

### 2. フロントエンド

ブラウザで http://localhost:3000 を開く

### 3. 管理パネル

ブラウザで http://localhost:8000 を開く

### 4. NFT発行テスト

```bash
cd backend
python -c "
from clients.xrpl_client import XRPLClient
from config import Config

client = XRPLClient(Config.XRPL_NETWORK, Config.XRPL_SPONSOR_SEED)
result = client.mint_nft(
    recipient_address=client.sponsor_wallet.classic_address,
    nft_uri='https://example.com/nft/metadata.json'
)
print('NFT Token ID:', result['nft_token_id'])
print('Transaction Hash:', result['transaction_hash'])
"
```

## トラブルシューティング

### データベース接続エラー

```bash
# MySQLが起動しているか確認
sudo systemctl status mysql  # Linux
brew services list           # macOS

# 接続テスト
mysql -u airzone_user -p airzone
```

### XRPLスポンサーウォレットの残高不足

```bash
python backend/verify_xrpl_client.py
```

残高が不足している場合は、テストネットフォーセットから追加で取得

### ポートが使用中

```bash
# ポート使用状況を確認
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# プロセスを終了
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Python仮想環境のアクティベート失敗

```bash
# 仮想環境を再作成
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 次のステップ

1. **本番環境デプロイ**: [DEPLOYMENT_CHECKLIST.md](../DEPLOYMENT_CHECKLIST.md)を参照
2. **XRPL統合**: [xrpl-integration.md](xrpl-integration.md)を参照
3. **効果測定**: [analytics-dashboard.md](analytics-dashboard.md)を参照
4. **API リファレンス**: [backend/API_REFERENCE.md](../backend/API_REFERENCE.md)を参照

## サポート

問題が発生した場合は、以下を確認してください：

- ログファイル: `backend/logs/app.log`
- Laravelログ: `admin/storage/logs/laravel.log`
- ブラウザのコンソール（フロントエンド）

## 参考資料

- [XRPL公式ドキュメント](https://xrpl.org/)
- [Flask公式ドキュメント](https://flask.palletsprojects.com/)
- [Next.js公式ドキュメント](https://nextjs.org/docs)
- [Laravel公式ドキュメント](https://laravel.com/docs/10.x)
