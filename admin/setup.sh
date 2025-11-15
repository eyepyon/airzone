#!/bin/bash
# Airzone Admin Setup Script

set -e

echo "=========================================="
echo "Airzone Admin Setup"
echo "=========================================="
echo ""

# 環境設定
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    php artisan key:generate
fi

# 依存関係のインストール
echo "Installing dependencies..."
composer install --no-dev --optimize-autoloader

# マイグレーション実行
echo "Running migrations..."
php artisan migrate --force

# 管理者アカウント作成
echo ""
echo "Creating admin account..."
php artisan admin:create

# パーミッション設定
echo "Setting permissions..."
chmod -R 775 storage bootstrap/cache

# キャッシュクリア
echo "Clearing cache..."
php artisan config:clear
php artisan cache:clear
php artisan view:clear

# 本番環境最適化
echo "Optimizing for production..."
php artisan config:cache
php artisan route:cache
php artisan view:cache

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Access: https://airz.one/admin"
echo ""
