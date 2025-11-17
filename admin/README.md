# Airzone 管理パネル

## 概要

Airzone管理パネルは、Laravel 10で構築された管理インターフェースです。ユーザー、商品、注文、NFTの管理、および効果測定ダッシュボードを提供します。

## 主な機能

### 1. ダッシュボード

効果測定指標をリアルタイムで表示：

- **DAU (Daily Active Users)**: 本日のアクティブユーザー数
- **MAU (Monthly Active Users)**: 今月のアクティブユーザー数
- **ダウンロード数**: 本日/総ダウンロード数
- **エンゲージメント率**: DAU/MAU比率
- **トレンドグラフ**: 過去7日間のDAU/ダウンロード推移

### 2. ユーザー管理

- ユーザー一覧表示
- ユーザー詳細情報
- ウォレット情報
- NFT保有状況
- 注文履歴

### 3. 商品管理

- 商品の作成・編集・削除
- 在庫管理
- 価格設定
- NFT要件設定
- 画像URL管理

### 4. 注文管理

- 注文一覧表示
- 注文詳細情報
- ステータス更新
- 決済情報確認

### 5. NFT管理

- NFT発行履歴
- 発行ステータス確認
- トランザクション情報
- ユーザー別NFT一覧

## 技術スタック

- **フレームワーク**: Laravel 10
- **データベース**: MySQL 8.0
- **フロントエンド**: Blade テンプレート + Tailwind CSS
- **認証**: Laravel標準認証

## セットアップ

詳細なインストール手順は [INSTALL.md](INSTALL.md) を参照してください。

### クイックスタート

```bash
cd admin

# 依存関係のインストール
composer install

# 環境変数の設定
cp .env.example .env
php artisan key:generate

# データベースマイグレーション
php artisan migrate

# 管理者アカウント作成
php artisan tinker
```

## ディレクトリ構造

```
admin/
├── app/
│   ├── Http/
│   │   └── Controllers/
│   │       └── Admin/          # 管理画面コントローラー
│   │           ├── AuthController.php
│   │           ├── DashboardController.php
│   │           ├── UserController.php
│   │           ├── ProductController.php
│   │           ├── OrderController.php
│   │           └── NFTController.php
│   └── Models/                 # モデル
│       ├── Admin.php
│       ├── User.php
│       ├── Product.php
│       ├── Order.php
│       └── NFTMint.php
├── resources/
│   └── views/
│       └── admin/              # 管理画面ビュー
│           ├── layout.blade.php
│           ├── dashboard.blade.php
│           ├── users/
│           ├── products/
│           ├── orders/
│           └── nfts/
├── routes/
│   └── web.php                 # ルート定義
└── database/
    └── migrations/             # マイグレーション
```

## 効果測定機能

### データ収集

バックエンドAPIが以下のアクティビティを自動記録：

1. **ログイン**: ユーザーがGoogle OAuthでログイン
2. **ダウンロード**: 商品をダウンロード
3. **購入**: 商品を購入

### 指標の計算

- **DAU**: 本日ログインしたユニークユーザー数
- **MAU**: 今月ログインしたユニークユーザー数
- **エンゲージメント率**: (DAU / MAU) × 100

### データベーステーブル

```sql
CREATE TABLE user_activities (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    activity_type VARCHAR(255) NOT NULL,
    ip_address VARCHAR(255) NULL,
    user_agent VARCHAR(255) NULL,
    metadata JSON NULL,
    created_at TIMESTAMP NOT NULL,
    INDEX idx_user_created (user_id, created_at),
    INDEX idx_activity_created (activity_type, created_at)
);
```

## API連携

管理パネルは以下のデータベーステーブルを直接参照：

- `users` - ユーザー情報
- `wallets` - XRPLウォレット情報
- `products` - 商品情報
- `orders` - 注文情報
- `nft_mints` - NFT発行履歴
- `user_activities` - ユーザーアクティビティ

## セキュリティ

### 認証

- Laravel標準認証を使用
- セッションベースの認証
- CSRF保護

### アクセス制御

- 管理者専用ミドルウェア (`auth:admin`)
- ルートレベルでの認証チェック

### データ保護

- パスワードのハッシュ化 (bcrypt)
- SQLインジェクション対策 (Eloquent ORM)
- XSS対策 (Blade自動エスケープ)

## 開発

### ローカル開発サーバー

```bash
php artisan serve
```

http://localhost:8000/admin でアクセス

### キャッシュクリア

```bash
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear
```

### 本番環境最適化

```bash
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

## トラブルシューティング

### 500エラー

```bash
# ログを確認
tail -f storage/logs/laravel.log

# キャッシュをクリア
php artisan cache:clear
php artisan config:clear
```

### パーミッションエラー

```bash
sudo chown -R www-data:www-data storage bootstrap/cache
sudo chmod -R 775 storage bootstrap/cache
```

### データベース接続エラー

`.env`ファイルのデータベース設定を確認：

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=airzone
DB_USERNAME=airzone_user
DB_PASSWORD=your_password
```

## ウォレット管理

### ウォレットタイプ

ユーザーは2種類のウォレットを使用できます：

1. **自動生成ウォレット**: ユーザー登録時に自動作成
2. **Xaman Wallet**: ユーザーが自分のXaman Walletを接続

管理パネルでは両方のウォレットタイプを確認できます。

## 関連ドキュメント

### セットアップ
- [インストールガイド](INSTALL.md)
- [完全セットアップガイド](../docs/SETUP_GUIDE_JP.md)

### 機能
- [効果測定ダッシュボード](../docs/analytics-dashboard.md)
- [ウォレット管理](../docs/xaman-wallet-integration.md)

### ブロックチェーン
- [XRPL統合](../docs/xrpl-integration.md)
- [Xaman Wallet統合](../docs/xaman-wallet-integration.md)

### 参考
- [Laravel 10 ドキュメント](https://laravel.com/docs/10.x)
