# Admin画面404エラーの修正手順

## 問題
`https://airz.one/admin` にアクセスすると404エラーが表示される

## 原因
Apache設定で`/admin`エイリアスが正しく設定されていないか、mod_rewriteが有効になっていない

## 修正手順

### 1. Apache設定ファイルの確認

```bash
sudo nano /etc/apache2/sites-available/airz-one.conf
```

以下の設定が含まれているか確認：

```apache
<VirtualHost *:443>
    ServerName airz.one
    
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/airz.one/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/airz.one/privkey.pem
    
    # Laravel Admin - この部分が重要！
    Alias /admin /var/www/airzone/admin/public
    
    <Directory /var/www/airzone/admin/public>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
        
        <IfModule mod_rewrite.c>
            RewriteEngine On
            
            # Handle Authorization Header
            RewriteCond %{HTTP:Authorization} .
            RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
            
            # Redirect Trailing Slashes If Not A Folder
            RewriteCond %{REQUEST_FILENAME} !-d
            RewriteCond %{REQUEST_URI} (.+)/$
            RewriteRule ^ %1 [L,R=301]
            
            # Send Requests To Front Controller
            RewriteCond %{REQUEST_FILENAME} !-d
            RewriteCond %{REQUEST_FILENAME} !-f
            RewriteRule ^ index.php [L]
        </IfModule>
    </Directory>
    
    # Next.js Frontend - adminとapiを除外
    ProxyPass /admin !
    ProxyPass /api !
    ProxyPass / http://127.0.0.1:3000/
    ProxyPassReverse / http://127.0.0.1:3000/
</VirtualHost>
```

### 2. mod_rewriteが有効か確認

```bash
sudo a2enmod rewrite
```

### 3. Apache設定をテスト

```bash
sudo apache2ctl configtest
```

エラーがなければ「Syntax OK」と表示されます。

### 4. Apacheを再起動

```bash
sudo systemctl restart apache2
```

### 5. パーミッションの確認

```bash
sudo chown -R www-data:www-data /var/www/airzone/admin
sudo chmod -R 775 /var/www/airzone/admin/storage
sudo chmod -R 775 /var/www/airzone/admin/bootstrap/cache
```

### 6. Laravelキャッシュのクリア

```bash
cd /var/www/airzone/admin
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear
```

### 7. 動作確認

#### テスト1: 直接publicディレクトリにアクセス
```bash
curl -I https://airz.one/admin/
```

200 OKが返ってくるはずです。

#### テスト2: ログインページにアクセス
ブラウザで以下にアクセス：
```
https://airz.one/admin/login
```

### 8. ログの確認

エラーが続く場合は、ログを確認：

```bash
# Apacheエラーログ
sudo tail -f /var/log/apache2/error.log

# Laravelログ
tail -f /var/www/airzone/admin/storage/logs/laravel.log
```

## 代替案: サブドメインを使用

`/admin`エイリアスがうまく動作しない場合、サブドメインを使用する方が簡単です：

### 1. DNS設定
`admin.airz.one` のAレコードを追加

### 2. Apache設定

```apache
<VirtualHost *:443>
    ServerName admin.airz.one
    
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/airz.one/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/airz.one/privkey.pem
    
    DocumentRoot /var/www/airzone/admin/public
    
    <Directory /var/www/airzone/admin/public>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    ErrorLog ${APACHE_LOG_DIR}/admin-error.log
    CustomLog ${APACHE_LOG_DIR}/admin-access.log combined
</VirtualHost>
```

### 3. SSL証明書の更新

```bash
sudo certbot --apache -d admin.airz.one
```

### 4. Apacheを再起動

```bash
sudo systemctl restart apache2
```

これで `https://admin.airz.one` でアクセスできます。

## トラブルシューティング

### 問題: 500エラーが出る

```bash
cd /var/www/airzone/admin
php artisan cache:clear
sudo chown -R www-data:www-data storage bootstrap/cache
```

### 問題: "No input file specified"エラー

`.htaccess`が読み込まれていません。Apache設定で`AllowOverride All`を確認してください。

### 問題: CSSやJSが読み込まれない

```bash
cd /var/www/airzone/admin
php artisan storage:link
```

## 確認コマンド一覧

```bash
# Apache設定の確認
sudo apache2ctl -S

# mod_rewriteの確認
apache2ctl -M | grep rewrite

# パーミッションの確認
ls -la /var/www/airzone/admin/storage
ls -la /var/www/airzone/admin/bootstrap/cache

# Laravelルートの確認
cd /var/www/airzone/admin
php artisan route:list
```

## 成功の確認

以下のURLにアクセスして確認：

1. `https://airz.one/admin/login` - ログインページが表示される
2. ログイン後、ダッシュボードが表示される

問題が解決しない場合は、ログファイルの内容を確認してください。
