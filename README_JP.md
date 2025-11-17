# Airzone

WiFiトリガー型NFT配布とECショッププラットフォーム（XRPL ブロックチェーン搭載）

## 概要

Airzoneは、WiFi接続をトリガーとしてNFTを自動配布し、NFT保有者限定の商品販売を行うプラットフォームです。XRPL (XRP Ledger) ブロックチェーンを使用して、高速・低コストでNFTを発行します。

## 主な機能

- **WiFiトリガーNFT配布**: 特定のWiFiに接続すると自動的にNFTを発行
- **Google OAuth認証**: 簡単なユーザー登録・ログイン
- **自動ウォレット生成**: ユーザー登録時にXRPLウォレットを自動作成
- **NFT保有者限定商品**: NFT保有者のみが購入できる商品設定
- **Stripe決済**: クレジットカード決済に対応
- **管理パネル**: ユーザー、商品、注文、NFTの管理
- **効果測定**: DAU、MAU、ダウンロード数などの指標を可視化

## プロジェクト構成

```
airzone/
├── backend/          # Flask API サーバー
├── frontend/         # Next.js Webアプリケーション
├── admin/            # Laravel 管理パネル
├── scripts/          # デプロイ・ユーティリティスクリプト
└── docs/             # ドキュメント
```

## 技術スタック

- **バックエンド**: Flask 3.0 + Python 3.11+ + SQLAlchemy
- **フロントエンド**: Next.js 14 + TypeScript + Tailwind CSS
- **ブロックチェーン**: XRPL (XRP Ledger)
- **データベース**: MySQL 8.0
- **決済**: Stripe
- **管理パネル**: Laravel 10 + PHP 8.1

## クイックスタート

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd airzone
```

### 2. データベースのセットアップ

```bash
mysql -u root -p
```

```sql
CREATE DATABASE airzone CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'airzone_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON airzone.* TO 'airzone_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

```bash
mysql -u airzone_user -p airzone < backend/setup_database.sql
```

### 3. バックエンドのセットアップ

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

`.env`を編集して必要な設定を追加

### 4. XRPLスポンサーウォレットの生成

```bash
python ../scripts/generate_sponsor_wallet.py
```

生成されたシードを`.env`に追加：

```env
XRPL_NETWORK=testnet
XRPL_SPONSOR_SEED=sXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### 5. テストネットから資金を取得

https://xrpl.org/xrp-testnet-faucet.html

### 6. バックエンドサーバーの起動

```bash
python app.py
```

### 7. フロントエンドのセットアップ

```bash
cd ../frontend
npm install
cp .env.local.example .env.local
npm run dev
```

### 8. 管理パネルのセットアップ

```bash
cd ../admin
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate
php artisan serve
```

## アクセスURL

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:5000
- **管理パネル**: http://localhost:8000

## ドキュメント

- [完全セットアップガイド](docs/SETUP_GUIDE_JP.md)
- [XRPL統合ガイド](docs/xrpl-integration.md)
- [効果測定ダッシュボード](docs/analytics-dashboard.md)
- [管理パネルガイド](admin/README.md)
- [管理パネルインストール](admin/INSTALL.md)
- [ブロックチェーン移行](BLOCKCHAIN_MIGRATION.md)
- [API リファレンス](backend/API_REFERENCE.md)

## システム要件

- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- PHP 8.1+ (管理パネル用)
- Composer (管理パネル用)

## 外部サービス

以下のサービスのアカウントとAPIキーが必要です：

- **Google OAuth**: ユーザー認証用
- **Stripe**: 決済処理用
- **XRPL Testnet**: NFT発行用（本番環境ではMainnet）

## 開発状況

- ✅ バックエンドAPI (Flask)
- ✅ フロントエンドUI (Next.js)
- ✅ XRPL統合
- ✅ データベース設計・マイグレーション
- ✅ 管理パネル
- ✅ 効果測定ダッシュボード
- ✅ デプロイインフラ

## ライセンス

[ライセンス情報を記載]

## サポート

問題が発生した場合は、以下を確認してください：

- [トラブルシューティング](docs/SETUP_GUIDE_JP.md#トラブルシューティング)
- ログファイル: `backend/logs/app.log`
- Laravelログ: `admin/storage/logs/laravel.log`

## 参考リンク

- [XRPL公式ドキュメント](https://xrpl.org/)
- [Flask公式ドキュメント](https://flask.palletsprojects.com/)
- [Next.js公式ドキュメント](https://nextjs.org/docs)
- [Laravel公式ドキュメント](https://laravel.com/docs/10.x)
