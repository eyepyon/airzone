# Airzone Admin インストール手順

## サーバー上でのセットアップ

### 1. Composerのインストール（まだの場合）

```bash
cd ~
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
composer --version
```

### 2. Laravelプロジェクトの作成

```bash
cd /var/www/airzone
composer create-project laravel/laravel:^10.0 admin
cd admin
```

### 3. 環境設定

```bash
cp .env.example .env
php artisan key:generate
```

`.env`を編集：

```bash
nano .env
```

以下を設定：

```env
APP_NAME="Airzone Admin"
APP_ENV=production
APP_DEBUG=false
APP_URL=https://airz.one/admin

DB_CONNECTION=mysql
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=airdb
DB_USERNAME=kanri
DB_PASSWORD=Kane90904!

SESSION_DRIVER=database
```

### 4. データベースマイグレーション

```bash
php artisan migrate
```

### 5. 管理者テーブルの作成

```bash
php artisan make:migration create_admins_table
```

マイグレーションファイルを編集後：

```bash
php artisan migrate
```

### 6. パーミッション設定

```bash
sudo chown -R www-data:www-data /var/www/airzone/admin
sudo chmod -R 775 /var/www/airzone/admin/storage
sudo chmod -R 775 /var/www/airzone/admin/bootstrap/cache
```

### 7. Apache設定

```bash
sudo nano /etc/apache2/sites-available/airz-one.conf
```

以下を追加：

```apache
<VirtualHost *:443>
    ServerName airz.one
    
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/airz.one/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/airz.one/privkey.pem
    
    # Laravel Admin
    Alias /admin /var/www/airzone/admin/public
    
    <Directory /var/www/airzone/admin/public>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
        
        <IfModule mod_rewrite.c>
            RewriteEngine On
            RewriteCond %{REQUEST_FILENAME} !-f
            RewriteCond %{REQUEST_FILENAME} !-d
            RewriteRule ^ index.php [L]
        </IfModule>
    </Directory>
    
    # Next.js Frontend
    ProxyPass /admin !
    ProxyPass /api !
    ProxyPass / http://127.0.0.1:3000/
    ProxyPassReverse / http://127.0.0.1:3000/
</VirtualHost>
```

### 8. Apache再起動

```bash
sudo systemctl restart apache2
```

### 9. 最適化

```bash
cd /var/www/airzone/admin
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

### 10. 管理者アカウント作成

```bash
php artisan tinker
```

Tinkerで実行：

```php
$admin = new App\Models\Admin();
$admin->name = 'Admin';
$admin->email = 'admin@airz.one';
$admin->password = bcrypt('your_secure_password');
$admin->save();
```

## アクセス

https://airz.one/admin にアクセスしてログイン

## トラブルシューティング

### 500エラーが出る場合

```bash
cd /var/www/airzone/admin
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear
```

### パーミッションエラー

```bash
sudo chown -R www-data:www-data /var/www/airzone/admin
sudo chmod -R 775 /var/www/airzone/admin/storage
sudo chmod -R 775 /var/www/airzone/admin/bootstrap/cache
```

### ログの確認

```bash
tail -f /var/www/airzone/admin/storage/logs/laravel.log
```
