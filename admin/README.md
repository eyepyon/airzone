# Airzone Admin Panel

Laravel 10ベースの管理者用ダッシュボード

## 機能

- ユーザー管理
- 注文管理
- 商品管理
- NFT管理
- WiFiセッション管理
- 統計ダッシュボード

## セットアップ

### 1. 依存関係のインストール

```bash
cd admin
composer install
npm install
```

### 2. 環境設定

```bash
cp .env.example .env
php artisan key:generate
```

`.env`ファイルを編集してデータベース接続情報を設定：

```env
DB_CONNECTION=mysql
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=airdb
DB_USERNAME=kanri
DB_PASSWORD=your_password
```

### 3. アセットのビルド

```bash
npm run build
```

### 4. 管理者アカウントの作成

```bash
php artisan admin:create
```

## 開発

```bash
# 開発サーバー起動
php artisan serve

# アセットの監視
npm run dev
```

## 本番環境デプロイ

### Apache設定

```apache
<VirtualHost *:443>
    ServerName airz.one
    
    # Laravel Admin
    Alias /admin /var/www/airzone/admin/public
    
    <Directory /var/www/airzone/admin/public>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
        
        RewriteEngine On
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule ^ index.php [L]
    </Directory>
    
    # Next.js Frontend (その他のパス)
    ProxyPass /admin !
    ProxyPass / http://127.0.0.1:3000/
    ProxyPassReverse / http://127.0.0.1:3000/
</VirtualHost>
```

### パーミッション設定

```bash
cd /var/www/airzone/admin
chmod -R 775 storage bootstrap/cache
chown -R www-data:www-data storage bootstrap/cache
```

### 最適化

```bash
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

## アクセス

- URL: https://airz.one/admin
- デフォルト管理者: admin@airz.one

## セキュリティ

- 管理画面は認証必須
- CSRF保護有効
- セッションベース認証
- IPホワイトリスト設定可能
