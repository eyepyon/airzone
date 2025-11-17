# Airzone

WiFiトリガー型NFT配布とECショッププラットフォーム（XRPL ブロックチェーン搭載）

PV  
https://youtu.be/atGWUDFrQtA  

Pitch資料  
https://www.canva.com/design/DAG4wX75q2Q/8x4YbLt6gLt0rS4JGVMSMA/view?utm_content=DAG4wX75q2Q&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h44c606fe9d

Website  
https://airz.one/  

対象Prize
XRPL Main Track
XRPL Deep Track

## 概要

Airzoneは、WiFi接続をトリガーとしてNFTを自動配布し、NFT保有者限定の商品販売を行う次世代プラットフォームです。XRPL (XRP Ledger) ブロックチェーンを使用して、高速・低コストでNFTを発行し、革新的なユーザー体験を提供します。

## 🚀 主な機能

### 🎯 コア機能
- **WiFiトリガーNFT配布**: 特定のWiFiに接続すると自動的にNFTを発行
- **Google OAuth認証**: 簡単なユーザー登録・ログイン
- **自動ウォレット生成**: ユーザー登録時にXRPLウォレットを自動作成
- **Xaman Wallet対応**: ユーザーが自分のXaman Walletを接続可能
- **NFT保有者限定商品**: NFT保有者のみが購入できる商品設定
- **Stripe決済**: クレジットカード決済に対応

### 🎁 紹介・リワードシステム
- **紹介リンク機能**: 友達を招待してコインを獲得
- **SNSシェア**: Twitter、LINE、Facebookでワンクリックシェア
- **限定商品アクセス**: 紹介経由ユーザーは限定商品を購入可能
- **コイン報酬**: 紹介成功で100コイン獲得

### 💎 ステーキング機能
- **XRP Escrowステーキング**: XRPを一定期間ロックして限定NFTを獲得
- **自動解放**: 期間終了後にXRPとNFTを自動受け取り
- **キャンペーン管理**: 複数のステーキングキャンペーンを同時開催

### 👑 ユーザー重要度システム
- **スコア算出**: 購入数、紹介数、ログイン数などから重要度を自動計算
- **5段階レベル**: Bronze、Silver、Gold、Platinum、Diamond
- **VIP特典**: 高レベルユーザーに特別な特典を提供

### 📊 管理・分析機能
- **管理パネル**: ユーザー、商品、注文、NFTの包括的管理
- **効果測定ダッシュボード**: DAU、MAU、ダウンロード数などの指標を可視化
- **紹介管理**: 紹介統計、ランキング、詳細履歴の確認
- **重要ユーザー管理**: ユーザー重要度ランキングと詳細分析

## 🏗️ プロジェクト構成

```
airzone/
├── backend/          # Flask API サーバー
│   ├── clients/      # XRPL、Stripe、Google OAuth クライアント
│   ├── services/     # ビジネスロジック（NFT、紹介、ステーキング等）
│   ├── routes/       # API エンドポイント
│   └── models/       # データモデル
├── frontend/         # Next.js Webアプリケーション
│   ├── components/   # React コンポーネント
│   ├── lib/          # ユーティリティ（Xaman Wallet等）
│   └── stores/       # 状態管理
├── admin/            # Laravel 管理パネル
│   ├── app/Http/Controllers/Admin/  # 管理画面コントローラー
│   └── resources/views/admin/       # 管理画面ビュー
├── scripts/          # デプロイ・ユーティリティスクリプト
└── docs/             # ドキュメント
```

## 💻 技術スタック

### バックエンド
- **フレームワーク**: Flask 3.0 + Python 3.11+
- **ORM**: SQLAlchemy 2.0
- **認証**: JWT + Google OAuth 2.0
- **ブロックチェーン**: XRPL (xrpl-py)
- **決済**: Stripe Python SDK
- **タスク管理**: カスタムタスクマネージャー

### フロントエンド
- **フレームワーク**: Next.js 14 (App Router)
- **言語**: TypeScript
- **スタイリング**: Tailwind CSS
- **状態管理**: Zustand
- **ウォレット**: Xaman Wallet SDK

### ブロックチェーン
- **メインチェーン**: XRPL (XRP Ledger)
- **機能**: ネイティブNFT、Escrow、高速トランザクション
- **コスト**: 約0.00001 XRP/トランザクション
- **確定時間**: 3-5秒

### データベース・インフラ
- **データベース**: MySQL 8.0
- **管理パネル**: Laravel 10 + PHP 8.1
- **Webサーバー**: Apache 2.4
- **SSL/TLS**: Let's Encrypt

## 🔥 新機能ハイライト

### 🎁 紹介リンクシステム

友達を招待してコインを獲得し、被紹介者は限定商品にアクセス可能：

- **紹介コード生成**: 8文字のユニークコード
- **SNSシェア**: Twitter、LINE、Facebookでワンクリック投稿
- **コイン報酬**: 紹介成功で100コイン獲得
- **限定商品**: 紹介経由ユーザー専用商品
- **クリック追跡**: リファラルリンクのクリック数を記録

詳細: [紹介システムガイド](docs/REFERRAL_SYSTEM_JP.md)

### 💎 XRP Escrowステーキング

XRPLのEscrow機能を使った革新的なステーキングシステム：

- **真のロック**: XRPが実際にブロックチェーン上でロック
- **自動解放**: 期間終了後にXRPとNFTを自動受け取り
- **限定NFT**: ステーキング参加者限定のNFTを発行
- **透明性**: 全てブロックチェーン上で検証可能
- **安全性**: XRPLのネイティブ機能で最高レベルのセキュリティ

詳細: [Escrowステーキングガイド](docs/ESCROW_STAKING_JP.md)

### 👑 ユーザー重要度スコア

包括的なユーザー評価システム：

- **多角的評価**: 購入、紹介、ログイン、NFT発行など複数指標
- **自動計算**: リアルタイムでスコアを更新
- **5段階レベル**: 🥉Bronze → 🥈Silver → 🥇Gold → 💎Platinum → 👑Diamond
- **VIP特典**: レベルに応じた特別な特典とサービス
- **ランキング**: トップユーザーの可視化

詳細: [ユーザー重要度システムガイド](docs/USER_IMPORTANCE_SYSTEM_JP.md)

### 📊 高度な分析機能

- **効果測定**: DAU、MAU、エンゲージメント率の自動計測
- **紹介分析**: 紹介数、クリック数、コンバージョン率
- **ユーザー分析**: 重要度別の行動パターン分析
- **リアルタイム**: 全指標をリアルタイムで更新

## 🔗 ウォレット統合

### 自動ウォレット vs Xaman Wallet

| 機能 | 自動ウォレット | Xaman Wallet |
|------|----------------|---------------|
| 生成 | 自動 | ユーザーが接続 |
| 秘密鍵管理 | バックエンド | ユーザー |
| セキュリティ | 標準 | 最高 |
| 初心者使い易さ | ★★★★★ | ★★★★☆ |
| 推奨用途 | 初心者 | セキュリティ重視 |

### ドキュメント

- **ユーザー向け**: [ウォレット管理ガイド](docs/WALLET_GUIDE_JP.md)
- **開発者向け**: [Xaman Wallet統合ガイド](docs/xaman-wallet-integration.md)

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

## 📚 ドキュメント

### 🚀 セットアップ
- [完全セットアップガイド](docs/SETUP_GUIDE_JP.md) - 詳細なインストール手順
- [クイックスタート](GETTING_STARTED_JP.md) - 素早く始める
- [ドキュメント索引](docs/INDEX_JP.md) - 全ドキュメント一覧

### 🏗️ アーキテクチャ
- [システムアーキテクチャ](ARCHITECTURE_JP.md) - 全体設計と技術スタック

### 🔗 ブロックチェーン
- [XRPL統合ガイド](docs/xrpl-integration.md) - XRPL基礎と統合方法
- [Xaman Wallet統合](docs/xaman-wallet-integration.md) - 開発者向け詳細
- [ウォレット管理ガイド](docs/WALLET_GUIDE_JP.md) - ユーザー向け使い方
- [Escrowステーキング](docs/ESCROW_STAKING_JP.md) - XRPステーキング機能
- [ブロックチェーン移行](BLOCKCHAIN_MIGRATION.md) - 移行の詳細

### 🎁 機能ガイド
- [紹介システム](docs/REFERRAL_SYSTEM_JP.md) - 紹介リンク機能の詳細
- [ユーザー重要度システム](docs/USER_IMPORTANCE_SYSTEM_JP.md) - スコア算出システム
- [効果測定ダッシュボード](docs/analytics-dashboard.md) - DAU/MAU分析

### 🛠️ 管理
- [管理パネルガイド](admin/README.md) - 管理画面の使い方
- [管理パネルインストール](admin/INSTALL.md) - セットアップ手順

### 📡 API
- [API リファレンス](backend/API_REFERENCE.md) - エンドポイント詳細

### 🔗 その他
- [クイックリンク集](docs/QUICK_LINKS.md) - よく使うリンク
- [ドキュメント一覧](docs/README.md) - 英語版索引

## 💡 ユースケース

### 🏪 店舗・施設向け
- **カフェ・レストラン**: WiFi接続でNFTクーポン配布
- **ホテル・旅館**: 宿泊記念NFTとリピーター特典
- **イベント会場**: 参加証明NFTと限定グッズ販売
- **商業施設**: 来店ポイントNFTとVIP会員制度

### 🎯 マーケティング活用
- **ブランド認知**: NFTを通じたブランド体験
- **顧客ロイヤリティ**: 段階的な特典とVIPプログラム
- **バイラルマーケティング**: 紹介システムによる拡散
- **データ分析**: 詳細な顧客行動分析

### 💰 収益モデル
- **NFT限定商品**: 高付加価値商品の販売
- **ステーキング手数料**: Escrowキャンペーンの運営費
- **VIP会員制度**: プレミアムサービスの提供
- **データ活用**: 匿名化された行動データの分析

## 🔧 システム要件

### 必須環境
- **Python**: 3.11以上
- **Node.js**: 18以上
- **MySQL**: 8.0以上
- **PHP**: 8.1以上 (管理パネル用)
- **Composer**: 最新版 (管理パネル用)

### 推奨スペック
- **CPU**: 2コア以上
- **メモリ**: 4GB以上
- **ストレージ**: 20GB以上
- **ネットワーク**: 安定したインターネット接続

## 🌐 外部サービス

以下のサービスのアカウントとAPIキーが必要です：

### 必須サービス
- **Google OAuth**: ユーザー認証用
- **Stripe**: 決済処理用
- **XRPL**: NFT発行・ステーキング用（Testnet/Mainnet）

### オプションサービス
- **Xaman Wallet**: 高度なウォレット機能
- **IPFS**: NFTメタデータ保存（推奨）
- **CDN**: 画像・静的ファイル配信

## ✅ 開発状況

### コア機能
- ✅ **バックエンドAPI** (Flask) - 完全実装
- ✅ **フロントエンドUI** (Next.js) - 完全実装
- ✅ **XRPL統合** - NFT発行・ウォレット管理
- ✅ **データベース設計** - 完全なスキーマとマイグレーション
- ✅ **認証システム** - Google OAuth + JWT
- ✅ **決済システム** - Stripe統合

### 高度な機能
- ✅ **紹介システム** - コイン報酬・限定商品アクセス
- ✅ **Escrowステーキング** - XRPロック・NFT報酬
- ✅ **ユーザー重要度** - スコア算出・レベル管理
- ✅ **効果測定** - DAU/MAU/エンゲージメント分析

### 管理機能
- ✅ **管理パネル** - Laravel製フル機能管理画面
- ✅ **ダッシュボード** - リアルタイム統計表示
- ✅ **紹介管理** - ランキング・詳細履歴
- ✅ **ユーザー管理** - 重要度スコア・VIP管理

### インフラ
- ✅ **デプロイ構成** - 本番環境対応
- ✅ **セキュリティ** - JWT認証・CORS設定
- ✅ **ログ管理** - 包括的なロギングシステム
- ✅ **エラーハンドリング** - 統一されたエラー処理

## ライセンス

[ライセンス情報を記載]

## 🎯 主要APIエンドポイント

### 認証
- `POST /api/v1/auth/google` - Google OAuth認証
- `POST /api/v1/auth/refresh` - トークンリフレッシュ

### NFT
- `GET /api/v1/nfts` - NFT一覧取得
- `POST /api/v1/nfts/mint` - NFT発行

### 紹介システム
- `GET /api/v1/referral/code` - 紹介コード取得
- `POST /api/v1/referral/register` - 紹介経由登録
- `GET /api/v1/referral/stats` - 紹介統計取得

### Escrowステーキング
- `GET /api/v1/escrow/campaigns` - キャンペーン一覧
- `POST /api/v1/escrow/stake` - ステーク作成
- `GET /api/v1/escrow/my-stakes` - 自分のステーク一覧

### ユーザー重要度
- `GET /api/v1/users/importance` - 重要度スコア取得
- `GET /api/v1/users/importance/ranking` - ランキング取得

詳細: [API リファレンス](backend/API_REFERENCE.md)

## 🛡️ セキュリティ

### 実装済みセキュリティ機能
- **JWT認証**: アクセストークン + リフレッシュトークン
- **CORS設定**: クロスオリジンリクエスト制御
- **レート制限**: API呼び出し制限
- **入力検証**: 全エンドポイントで入力バリデーション
- **SQLインジェクション対策**: SQLAlchemy ORM使用
- **XSS対策**: 出力エスケープ処理
- **秘密鍵管理**: 環境変数による管理

### ブロックチェーンセキュリティ
- **Escrow機能**: XRPLネイティブの安全なロック機能
- **トランザクション署名**: 秘密鍵による署名検証
- **ウォレット分離**: ユーザーごとに独立したウォレット

## 🔧 トラブルシューティング

### よくある問題

#### データベース接続エラー
```bash
# MySQL接続確認
mysql -u airzone_user -p airzone

# マイグレーション実行
mysql -u airzone_user -p airzone < backend/setup_database.sql
```

#### XRPL接続エラー
```bash
# スポンサーウォレット確認
python scripts/generate_sponsor_wallet.py

# テストネット資金取得
# https://xrpl.org/xrp-testnet-faucet.html
```

#### 紹介システムが動作しない
```bash
# マイグレーション実行
mysql -u airzone_user -p airzone < backend/database/migrations/add_referral_system.sql
```

#### Escrowステーキングが動作しない
```bash
# マイグレーション実行
mysql -u airzone_user -p airzone < backend/database/migrations/add_escrow_campaigns.sql
```

### ログ確認
- **バックエンド**: `backend/logs/app.log`
- **Laravel**: `admin/storage/logs/laravel.log`
- **フロントエンド**: ブラウザコンソール

詳細: [セットアップガイド - トラブルシューティング](docs/SETUP_GUIDE_JP.md#トラブルシューティング)

## 参考リンク

- [XRPL公式ドキュメント](https://xrpl.org/)
- [Flask公式ドキュメント](https://flask.palletsprojects.com/)
- [Next.js公式ドキュメント](https://nextjs.org/docs)
- [Laravel公式ドキュメント](https://laravel.com/docs/10.x)
- [Xaman Wallet](https://xaman.app/)
