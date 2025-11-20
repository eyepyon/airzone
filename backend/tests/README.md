# Backend Tests

このディレクトリには、バックエンドのテストスクリプトが含まれています。

## テストの種類

### 検証スクリプト (verify_*.py)

各コンポーネントの動作を検証するスクリプト：

- `verify_auth_endpoints.py` - 認証エンドポイントの検証
- `verify_auth_endpoints_static.py` - 認証エンドポイントの静的検証
- `verify_auth_middleware.py` - 認証ミドルウェアの検証
- `verify_auth_middleware_static.py` - 認証ミドルウェアの静的検証
- `verify_blueprints.py` - Blueprintの検証
- `verify_database.py` - データベース接続の検証
- `verify_endpoints.py` - 全エンドポイントの検証
- `verify_nft_blueprint.py` - NFT Blueprintの検証
- `verify_nft_blueprint_static.py` - NFT Blueprintの静的検証
- `verify_order_routes.py` - 注文ルートの検証
- `verify_payment_routes.py` - 決済ルートの検証
- `verify_product_blueprint.py` - 商品Blueprintの検証
- `verify_stripe_client.py` - Stripeクライアントの検証
- `verify_wallet_service.py` - ウォレットサービスの検証
- `verify_xrpl_client.py` - XRPLクライアントの検証

### 単体テスト (test_*.py)

特定の機能をテストするスクリプト：

- `test_auth_wallet.py` - 認証サービスのウォレット作成テスト
- `test_escrow_campaigns.py` - エスクローキャンペーンテーブルのテスト
- `test_wallet_generation.py` - ウォレット生成テスト
- `test_xrpl_functions.py` - XRPL機能のテスト

### 統合テスト

- `run_all_tests.py` - すべてのテストを実行

## 使用方法

### 個別のテストを実行

```bash
cd backend
python tests/verify_database.py
```

### すべてのテストを実行

```bash
cd backend
python tests/run_all_tests.py
```

### 特定のコンポーネントをテスト

```bash
# データベース接続をテスト
python tests/verify_database.py

# 認証エンドポイントをテスト
python tests/verify_auth_endpoints.py

# XRPLクライアントをテスト
python tests/verify_xrpl_client.py
```

## テストの追加

新しいテストを追加する場合：

1. `tests/` ディレクトリに新しいファイルを作成
2. ファイル名は `test_*.py` または `verify_*.py` の形式
3. 実行可能にする：`chmod +x tests/your_test.py`
4. このREADMEを更新

## 注意事項

- テストは開発環境で実行してください
- 本番データベースに対してテストを実行しないでください
- テストの実行前に `.env` ファイルが正しく設定されていることを確認してください

## 環境変数

テストの実行には以下の環境変数が必要です：

```bash
# データベース
DATABASE_URL=mysql+pymysql://user:password@localhost/airzone

# XRPL
XRPL_NETWORK=testnet
XRPL_SPONSOR_SEED=sXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Stripe
STRIPE_SECRET_KEY=sk_test_XXXXXXXXXXXXXXXXXXXXXXXX
```

## トラブルシューティング

### データベース接続エラー

```bash
python tests/verify_database.py
```

### XRPL接続エラー

```bash
python tests/verify_xrpl_client.py
```

### 認証エラー

```bash
python tests/verify_auth_endpoints.py
```
