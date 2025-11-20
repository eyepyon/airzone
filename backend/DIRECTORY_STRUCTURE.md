# Backend Directory Structure

## ディレクトリ構成

```
backend/
├── app.py                      # メインアプリケーション
├── config.py                   # 設定ファイル
├── requirements.txt            # Python依存関係
│
├── clients/                    # 外部サービスクライアント
│   ├── stripe_client.py       # Stripe決済クライアント
│   └── xrpl_client.py         # XRPLブロックチェーンクライアント
│
├── database/                   # データベース関連
│   ├── migrations/            # SQLマイグレーションファイル
│   └── schema.sql             # データベーススキーマ
│
├── middleware/                 # ミドルウェア
│   └── auth.py                # 認証ミドルウェア
│
├── models/                     # データモデル
│   ├── nft.py                 # NFTモデル
│   ├── order.py               # 注文モデル
│   ├── product.py             # 商品モデル
│   ├── referral.py            # 紹介モデル
│   ├── user.py                # ユーザーモデル
│   └── wallet.py              # ウォレットモデル
│
├── repositories/               # データアクセス層
│   ├── base.py                # ベースリポジトリ
│   ├── nft_repository.py      # NFTリポジトリ
│   ├── order_repository.py    # 注文リポジトリ
│   ├── product_repository.py  # 商品リポジトリ
│   ├── user_repository.py     # ユーザーリポジトリ
│   └── wallet_repository.py   # ウォレットリポジトリ
│
├── routes/                     # APIルート
│   ├── auth.py                # 認証エンドポイント
│   ├── escrow.py              # エスクローエンドポイント
│   ├── nft.py                 # NFTエンドポイント
│   ├── order.py               # 注文エンドポイント
│   ├── payment.py             # 決済エンドポイント
│   ├── product.py             # 商品エンドポイント
│   ├── referral.py            # 紹介エンドポイント
│   └── wallet.py              # ウォレットエンドポイント
│
├── scripts/                    # セットアップ・メンテナンススクリプト
│   ├── README.md              # スクリプトのドキュメント
│   ├── init_db.py             # データベース初期化
│   ├── run_migration.py       # マイグレーション実行
│   ├── setup_db_simple.py     # シンプルなDB設定
│   └── fund_sponsor_wallet.py # ウォレット資金供給
│
├── services/                   # ビジネスロジック
│   ├── auth_service.py        # 認証サービス
│   ├── batch_transfer_service.py # バッチ転送サービス
│   ├── escrow_campaign_service.py # エスクローキャンペーンサービス
│   ├── nft_service.py         # NFTサービス
│   ├── order_service.py       # 注文サービス
│   ├── payment_service.py     # 決済サービス
│   ├── referral_service.py    # 紹介サービス
│   └── wallet_service.py      # ウォレットサービス
│
└── tests/                      # テストスクリプト
    ├── README.md              # テストのドキュメント
    ├── run_all_tests.py       # 全テスト実行
    ├── test_*.py              # 単体テスト
    └── verify_*.py            # 検証スクリプト
```

## 主要コンポーネント

### 1. アプリケーション層 (app.py)

- Flaskアプリケーションの初期化
- ルートの登録
- ミドルウェアの設定
- エラーハンドリング

### 2. ルート層 (routes/)

- HTTPリクエストの受付
- リクエストバリデーション
- レスポンスの返却
- エラーハンドリング

### 3. サービス層 (services/)

- ビジネスロジックの実装
- トランザクション管理
- 外部サービスとの連携
- データの加工・変換

### 4. リポジトリ層 (repositories/)

- データベースアクセス
- CRUDオペレーション
- クエリの構築
- データマッピング

### 5. モデル層 (models/)

- データ構造の定義
- バリデーションルール
- リレーションシップ
- ビジネスルール

### 6. クライアント層 (clients/)

- 外部APIとの通信
- Stripe決済処理
- XRPLブロックチェーン操作
- エラーハンドリング

### 7. ミドルウェア層 (middleware/)

- 認証・認可
- リクエストログ
- エラーハンドリング
- CORS設定

## データフロー

```
HTTP Request
    ↓
Routes (リクエスト受付)
    ↓
Middleware (認証・バリデーション)
    ↓
Services (ビジネスロジック)
    ↓
Repositories (データアクセス)
    ↓
Models (データ構造)
    ↓
Database / External APIs
    ↓
Response
```

## 開発ガイドライン

### 新機能の追加

1. **モデルの定義** (`models/`)
   - データ構造を定義
   - バリデーションルールを追加

2. **リポジトリの作成** (`repositories/`)
   - データアクセスメソッドを実装
   - BaseRepositoryを継承

3. **サービスの実装** (`services/`)
   - ビジネスロジックを実装
   - トランザクション管理

4. **ルートの追加** (`routes/`)
   - エンドポイントを定義
   - リクエスト/レスポンスを処理

5. **テストの作成** (`tests/`)
   - 単体テストを作成
   - 統合テストを作成

### コーディング規約

- **命名規則**: snake_case
- **ドキュメント**: docstringを必ず記述
- **エラーハンドリング**: try-exceptで適切に処理
- **ログ**: 重要な処理はログに記録
- **型ヒント**: 可能な限り型ヒントを使用

### セキュリティ

- **SQLインジェクション対策**: パラメータバインディングを使用
- **認証**: JWTトークンで認証
- **パスワード**: bcryptでハッシュ化
- **環境変数**: 機密情報は環境変数で管理

## 関連ドキュメント

- [API仕様書](../README.md)
- [データベース設計](./database/README.md)
- [テストガイド](./tests/README.md)
- [スクリプトガイド](./scripts/README.md)
- [デプロイメントガイド](../DEPLOYMENT_INDEX.md)
